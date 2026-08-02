#!/usr/bin/env python3
"""
ARCH-CONV-PKGC-1 — waist-unit MARK_STALE_NO_REWRITE remediation runner.

Default mode is dry-run. Write mode requires --write and a reachable DATABASE_URL.
Never rewrites historic waist values/units.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO = Path(__file__).resolve().parents[2]
BACKEND = REPO / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from core.dto.arch_conv_pkgc_1_waist_remediation_v1 import (  # noqa: E402
    APPROVED_ANALYSIS_IDS,
    apply_planned_remediation,
    plan_remediation,
)


def _load_env() -> None:
    """Load env files with backend/.env winning (matches alembic migrations/env.py).

    A stale shell DATABASE_URL (e.g. localhost:5433/healthiq_test) must not
    override the governed project DATABASE_URL in backend/.env.
    """
    for rel, override in ((".env", False), ("backend/.env", True)):
        path = REPO / rel
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if override or key not in os.environ:
                os.environ[key] = value


def _load_rows_from_db() -> List[Dict[str, Any]]:
    from sqlalchemy import create_engine, text

    url = os.environ.get("DATABASE_URL", "")
    if not url:
        raise RuntimeError("DATABASE_URL missing")
    eng = create_engine(url)
    rows: List[Dict[str, Any]] = []
    with eng.connect() as conn:
        for analysis_id in APPROVED_ANALYSIS_IDS:
            analysis = conn.execute(
                text(
                    "select id, questionnaire_data from analyses where id::text = :id"
                ),
                {"id": analysis_id},
            ).fetchone()
            if analysis is None:
                rows.append(
                    {
                        "analysis_id": analysis_id,
                        "exists": False,
                        "questionnaire_data": None,
                        "processing_metadata": None,
                        "already_superseded": False,
                    }
                )
                continue
            result = conn.execute(
                text(
                    "select processing_metadata from analysis_results "
                    "where analysis_id::text = :id "
                    "order by created_at desc nulls last limit 1"
                ),
                {"id": analysis_id},
            ).fetchone()
            pm = result[0] if result and isinstance(result[0], dict) else {}
            rows.append(
                {
                    "analysis_id": analysis_id,
                    "exists": True,
                    "questionnaire_data": analysis[1],
                    "processing_metadata": pm,
                    "already_superseded": False,
                }
            )
    return rows


def _persist_rows(rows_to_persist: List[Dict[str, Any]]) -> None:
    from sqlalchemy import create_engine, text

    url = os.environ.get("DATABASE_URL", "")
    eng = create_engine(url)
    with eng.begin() as conn:
        for item in rows_to_persist:
            aid = item["analysis_id"]
            pm = item["processing_metadata"]
            conn.execute(
                text(
                    "update analysis_results "
                    "set processing_metadata = CAST(:pm AS json) "
                    "where analysis_id = CAST(:id AS uuid) "
                    "and id = ("
                    "  select id from analysis_results "
                    "  where analysis_id = CAST(:id AS uuid) "
                    "  order by created_at desc nulls last limit 1"
                    ")"
                ),
                {"id": aid, "pm": json.dumps(pm)},
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="ARCH-CONV-PKGC-1 waist remediation")
    parser.add_argument("--write", action="store_true", help="Persist stamps (default dry-run)")
    parser.add_argument(
        "--fixture-json",
        type=str,
        default="",
        help="Optional path to synthetic row fixtures (skips DB)",
    )
    parser.add_argument("--output", type=str, default="", help="Write machine-readable report JSON")
    args = parser.parse_args()

    _load_env()

    try:
        if args.fixture_json:
            payload = json.loads(Path(args.fixture_json).read_text(encoding="utf-8"))
            rows = payload if isinstance(payload, list) else payload.get("rows") or []
        else:
            rows = _load_rows_from_db()
    except Exception as exc:
        report = {
            "work_id": "ARCH-CONV-PKGC-1",
            "mode": "aborted",
            "write_executed": False,
            "complete_success": False,
            "error": f"unable to load rows: {type(exc).__name__}: {exc}",
            "live_db_dependency_outstanding": True,
        }
        text = json.dumps(report, indent=2, sort_keys=True)
        print(text)
        if args.output:
            Path(args.output).write_text(text + "\n", encoding="utf-8")
        return 2

    plan = plan_remediation(rows)
    result = apply_planned_remediation(plan, write=bool(args.write))

    if args.write and result.get("write_executed"):
        try:
            _persist_rows(result.get("rows_to_persist") or [])
        except Exception as exc:
            result["write_executed"] = False
            result["complete_success"] = False
            result["error"] = f"persist failed: {type(exc).__name__}: {exc}"
            result["mode"] = "write_failed"

    # Never claim complete success for partial/idempotent-only unless all 12 stamped.
    if result.get("write_executed"):
        stamped = sum(
            1
            for r in result.get("results") or []
            if r.get("precondition") in {"PASS", "ALREADY_REMEDIATED"}
        )
        result["complete_success"] = stamped == len(APPROVED_ANALYSIS_IDS) and not result.get(
            "fail_closed"
        )

    text = json.dumps(result, indent=2, sort_keys=True, default=str)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")

    if result.get("fail_closed") or result.get("mode") in {"aborted", "write_failed", "write_refused"}:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
