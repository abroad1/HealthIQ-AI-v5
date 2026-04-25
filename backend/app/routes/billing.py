"""
Stripe billing — Checkout, Customer Portal, webhooks (Sprint 7).
"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional
from uuid import UUID

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from core.dependencies.auth import CurrentUser, get_current_user
from core.profile_bridge import ensure_profile_for_auth_user
from repositories import ProfileRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["billing"])


def _stripe_configured() -> bool:
    return bool((os.getenv("STRIPE_SECRET_KEY") or "").strip())


def _frontend_base() -> str:
    return (os.getenv("FRONTEND_BASE_URL") or "http://localhost:3000").rstrip("/")


def _stripe_price_id() -> str:
    pid = (os.getenv("STRIPE_PRICE_ID") or "").strip()
    if not pid:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe price is not configured (STRIPE_PRICE_ID).",
        )
    return pid


class CheckoutSessionResponse(BaseModel):
    url: str


class PortalSessionResponse(BaseModel):
    url: str


@router.post("/checkout-session", response_model=CheckoutSessionResponse)
def create_checkout_session(
    auth_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CheckoutSessionResponse:
    if not _stripe_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing is not configured (STRIPE_SECRET_KEY).",
        )
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    ensure_profile_for_auth_user(db, auth_user)
    price = _stripe_price_id()
    success_url = f"{_frontend_base()}/pricing?checkout=success"
    cancel_url = f"{_frontend_base()}/pricing?checkout=cancelled"

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            client_reference_id=auth_user.id,
            line_items=[{"price": price, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"user_id": auth_user.id},
            allow_promotion_codes=False,
        )
    except Exception as exc:
        logger.exception("Stripe checkout session failed")
        msg = getattr(exc, "user_message", None) or getattr(exc, "message", None) or str(exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(msg),
        ) from exc

    if not session.url:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe did not return a checkout URL",
        )
    return CheckoutSessionResponse(url=session.url)


@router.post("/portal-session", response_model=PortalSessionResponse)
def create_portal_session(
    auth_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PortalSessionResponse:
    if not _stripe_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing is not configured (STRIPE_SECRET_KEY).",
        )
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    user_uuid = ensure_profile_for_auth_user(db, auth_user)
    repo = ProfileRepository(db)
    profile = repo.get_by_user_id(user_uuid)
    cid = (profile.stripe_customer_id or "").strip() if profile else ""
    if not cid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Stripe customer on file. Subscribe from the pricing page first.",
        )
    return_url = f"{_frontend_base()}/settings"
    try:
        session = stripe.billing_portal.Session.create(
            customer=cid,
            return_url=return_url,
        )
    except Exception as exc:
        logger.exception("Stripe portal session failed")
        msg = getattr(exc, "user_message", None) or getattr(exc, "message", None) or str(exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(msg),
        ) from exc
    return PortalSessionResponse(url=session.url)


def _apply_subscription_state(
    db: Session,
    user_id: str,
    *,
    customer_id: Optional[str],
    subscription_id: Optional[str],
    subscription_status: str,
) -> None:
    ensure_profile_for_auth_user(
        db,
        CurrentUser(id=user_id, email=None),
    )
    user_uuid = UUID(user_id)
    repo = ProfileRepository(db)
    profile = repo.get_by_user_id(user_uuid)
    if not profile:
        logger.error("Profile missing after ensure for user %s", user_id)
        return
    updates: dict[str, Any] = {"subscription_status": subscription_status}
    if customer_id:
        updates["stripe_customer_id"] = customer_id
    if subscription_id:
        updates["stripe_subscription_id"] = subscription_id
    repo.update_by_user_id(user_uuid, **updates)


def _map_stripe_subscription_status(stripe_status: Optional[str]) -> str:
    s = (stripe_status or "").lower()
    if s in ("active", "trialing"):
        return "active"
    return "cancelled"


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    if not _stripe_configured():
        raise HTTPException(status_code=503, detail="Stripe not configured")
    wh_secret = (os.getenv("STRIPE_WEBHOOK_SECRET") or "").strip()
    if not wh_secret:
        raise HTTPException(status_code=503, detail="STRIPE_WEBHOOK_SECRET not set")

    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    payload = await request.body()
    sig = request.headers.get("stripe-signature") or ""

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig, secret=wh_secret)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid payload") from exc
    except Exception as exc:
        if exc.__class__.__name__ == "SignatureVerificationError":
            raise HTTPException(status_code=400, detail="Invalid Stripe signature") from exc
        raise

    etype = event["type"]
    data_object = event["data"]["object"]

    try:
        if etype == "checkout.session.completed":
            sess = data_object
            uid = (sess.get("client_reference_id") or sess.get("metadata", {}).get("user_id") or "").strip()
            if not uid:
                logger.warning("checkout.session.completed without user reference")
                return {"received": "true"}
            customer_id = sess.get("customer")
            sub_id = sess.get("subscription")
            if sess.get("mode") == "subscription":
                _apply_subscription_state(
                    db,
                    uid,
                    customer_id=str(customer_id) if customer_id else None,
                    subscription_id=str(sub_id) if sub_id else None,
                    subscription_status="active",
                )

        elif etype == "customer.subscription.updated":
            sub = data_object
            customer_id = sub.get("customer")
            sub_id = sub.get("id")
            stripe_status = sub.get("status")
            mapped = _map_stripe_subscription_status(stripe_status)
            if customer_id:
                repo = ProfileRepository(db)
                profile = repo.get_by_field("stripe_customer_id", str(customer_id))
                if profile:
                    repo.update_by_user_id(
                        profile.user_id,
                        subscription_status=mapped,
                        stripe_subscription_id=str(sub_id) if sub_id else profile.stripe_subscription_id,
                    )

        elif etype == "customer.subscription.deleted":
            sub = data_object
            customer_id = sub.get("customer")
            if customer_id:
                repo = ProfileRepository(db)
                profile = repo.get_by_field("stripe_customer_id", str(customer_id))
                if profile:
                    repo.update_by_user_id(
                        profile.user_id,
                        subscription_status="cancelled",
                    )
    except Exception:
        logger.exception("Webhook handler failed for event %s", etype)
        raise HTTPException(status_code=500, detail="Webhook processing failed") from None

    return {"received": "true"}
