"""
Summary PDF (Sprint 4) — retail summary only; no engine internals or full clinician text.

Builds a presentable A4 summary from the same analysis DTO as GET /api/analysis/result.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from fpdf import FPDF

DISCLAIMER = (
    "This report is for informational use only and is not a medical diagnosis. "
    "Please discuss findings with a qualified clinician."
)

SEV_RANK = {"critical": 4, "high": 3, "moderate": 2, "low": 1}


def _safe_text(s: Any, max_len: int = 4000) -> str:
    """Bounded plain text; core fonts (Helvetica) are latin-1 only in fpdf2."""
    if s is None:
        return ""
    t = str(s).replace("\r", " ").replace("\u2014", "-").replace("\u2013", "-").strip()
    if len(t) > max_len:
        t = t[: max_len - 3] + "..."
    return t.encode("latin-1", errors="replace").decode("latin-1")


def _first_sentence(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    m = re.match(r"^(.+?[.!?])(\s|$)", t)
    if m:
        return m.group(1).strip()
    if len(t) <= 220:
        return t
    return t[:217].rstrip() + "…"


def _take_sentences(text: str, max_sentences: int) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    out: List[str] = []
    rest = t
    for _ in range(max_sentences):
        if not rest:
            break
        m = re.match(r"^(.+?[.!?])(\s+|$)", rest)
        if m:
            out.append(m.group(1).strip())
            rest = rest[m.end() :].strip()
        else:
            out.append(rest.strip())
            break
    return " ".join(out).strip()


def _pick_primary_driver(clusters: List[dict]) -> Optional[Tuple[str, str, List[str]]]:
    best = None
    for idx, c in enumerate(clusters or []):
        if not isinstance(c, dict):
            continue
        cid = str(c.get("cluster_id") or c.get("id") or f"cluster-{idx}")
        sev = str(c.get("severity") or "moderate").lower()
        rank = SEV_RANK.get(sev, 2)
        score = c.get("score")
        if not isinstance(score, (int, float)):
            sc = c.get("confidence")
            score = (float(sc) * 100) if isinstance(sc, (int, float)) else 0.0
        name = (c.get("name") or "").strip() or "Health pattern"
        biomarkers = list(c.get("biomarkers") or c.get("biomarkers_involved") or [])
        if best is None or rank > best[0] or (rank == best[0] and score > best[1]):
            best = (rank, float(score), cid, name, biomarkers)
    if best is None:
        return None
    return best[2], best[3], [str(x) for x in best[4]]


def _idl_first_record(dto: dict) -> Optional[dict]:
    idl = dto.get("interpretation_display_layer_v1")
    if not isinstance(idl, dict):
        return None
    recs = idl.get("records")
    if not isinstance(recs, list) or not recs:
        return None
    visible = [r for r in recs if isinstance(r, dict) and r.get("enabled_for_frontend") is True]
    visible.sort(key=lambda r: int(r.get("display_order_priority") or 0))
    return visible[0] if visible else None


def _phenotype_label(dto: dict, driver: Optional[Tuple[str, str, List[str]]]) -> str:
    idl0 = _idl_first_record(dto)
    if idl0:
        label = (idl0.get("retail_display_label") or "").strip()
        if label:
            return label
    cr = dto.get("clinician_report_v1")
    if isinstance(cr, dict):
        rc = cr.get("sections", {}).get("root_cause")
        if isinstance(rc, dict):
            hyps = rc.get("hypotheses")
            if isinstance(hyps, list) and hyps and isinstance(hyps[0], dict):
                t = (hyps[0].get("title") or "").strip()
                if t:
                    return t
        p1 = cr.get("sections", {}).get("page1")
        if isinstance(p1, dict):
            pc = (p1.get("primary_concern") or "").strip()
            if pc:
                return _first_sentence(pc)
            k0 = p1.get("key_findings")
            if isinstance(k0, list) and k0 and k0[0]:
                return _first_sentence(str(k0[0]))
    if driver is not None:
        return _safe_text(driver[1], 200)
    return "Your analysis summary"


def _build_primary_summary(dto: dict) -> str:
    nr = dto.get("narrative_report_v1")
    if isinstance(nr, dict):
        rs = (nr.get("retail_summary") or "").strip()
        if rs:
            return _take_sentences(rs, 2)
    cr = dto.get("clinician_report_v1")
    if not isinstance(cr, dict):
        return "Summary text was not available for this export."
    p1 = cr.get("sections", {}).get("page1")
    if not isinstance(p1, dict):
        return "Summary text was not available for this export."
    th = (p1.get("top_hypothesis_line") or "").strip()
    k0 = p1.get("key_findings")
    k0s = (k0[0] or "").strip() if isinstance(k0, list) and k0 else ""
    if th and k0s and th != k0s:
        return _take_sentences(f"{_first_sentence(th)} {k0s}", 2)
    if th:
        return _take_sentences(th, 2)
    if k0s:
        return _take_sentences(k0s, 2)
    return "See your detailed sections in the app for the full interpretation."


def _marker_status(m: dict) -> str:
    s = m.get("status")
    if s is None:
        return "—"
    t = str(s).replace("_", " ")
    return " ".join(w.capitalize() for w in t.split())


def _top_markers(biomarkers: List[dict], driver: Optional[Tuple[str, str, List[str]]]) -> List[dict]:
    rows = [b for b in biomarkers if isinstance(b, dict) and b.get("value") is not None]
    by_name = {b.get("biomarker_name"): b for b in rows if b.get("biomarker_name")}

    out: List[dict] = []
    if driver is not None:
        for name in driver[2]:
            b = by_name.get(name)
            if b and name:
                out.append(b)
            if len(out) >= 3:
                return out

    def rank(b: dict) -> int:
        s = (str(b.get("status") or "")).lower()
        if any(x in s for x in ("high", "low", "critical", "abnormal")):
            return 4
        if "border" in s or "watch" in s:
            return 3
        if "optimal" in s or "normal" in s:
            return 0
        return 1

    rest = [b for b in rows if b not in out]
    rest.sort(key=rank, reverse=True)
    for b in rest:
        out.append(b)
        if len(out) >= 3:
            break
    return out[:3]


def _balanced_lines(dto: dict) -> List[str]:
    b = dto.get("balanced_systems_v1")
    if not isinstance(b, dict):
        return []
    items = b.get("items")
    if not isinstance(items, list):
        return []
    lines: List[str] = []
    for it in items[:6]:
        if not isinstance(it, dict):
            continue
        topic = (it.get("system_topic") or "").strip()
        line = (it.get("evidence_line") or "").strip()
        if topic and line:
            lines.append(f"{topic}: {line}")
        elif line:
            lines.append(line)
    return lines


def _top_action_lines(dto: dict, max_n: int) -> List[str]:
    out: List[str] = []
    for c in dto.get("clusters") or []:
        if not isinstance(c, dict):
            continue
        for r in c.get("recommendations") or []:
            s = (r or "").strip()
            if s:
                out.append(s)
            if len(out) >= max_n:
                return out
    for r in dto.get("recommendations") or []:
        s = (r or "").strip() if r is not None else ""
        if s:
            out.append(s)
        if len(out) >= max_n:
            return out
    return out[:max_n]


def _panel_name(dto: dict) -> str:
    meta = dto.get("meta")
    if not isinstance(meta, dict):
        return "Blood test panel"
    lo = meta.get("lab_origin")
    if isinstance(lo, dict):
        name = lo.get("lab_provider_name")
        if name and str(name).strip():
            return str(name).strip()
    return "Blood test panel"


def build_summary_pdf_bytes(dto: dict, user_display: str) -> bytes:
    """Return PDF bytes; dto must be the public analysis result shape (e.g. build_analysis_result_dto)."""
    title = "HealthIQ - Results summary"
    user_display = _safe_text(user_display, 120) or "User"
    date_str = _safe_text(dto.get("completed_at") or dto.get("created_at"), 40)[:19].replace("T", " ")

    clusters = [c for c in (dto.get("clusters") or []) if isinstance(c, dict)]
    driver = _pick_primary_driver(clusters)
    biomarkers = [b for b in (dto.get("biomarkers") or []) if isinstance(b, dict)]
    panel = _panel_name(dto)
    phenotype = _phenotype_label(dto, driver)
    summary = _build_primary_summary(dto)
    markers = _top_markers(biomarkers, driver)
    sys_lines = _balanced_lines(dto)
    actions = _top_action_lines(dto, 3)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)
    epw = float(pdf.epw)
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, title, ln=1)
    pdf.ln(2)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, f"Name: {user_display}", ln=1)
    pdf.cell(0, 6, f"Test panel: {panel}", ln=1)
    pdf.cell(0, 6, f"Analysis date: {date_str}", ln=1)
    pdf.ln(4)

    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 8, "Primary finding", ln=1)
    pdf.set_font("Helvetica", size=10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(epw, 5, f"{_safe_text(phenotype, 500)}\n\n{_safe_text(summary, 1200)}")
    pdf.ln(2)

    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 8, "Top driving signals", ln=1)
    pdf.set_font("Helvetica", size=10)
    if not markers:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(epw, 5, "No marker rows were available for the summary table.")
    else:
        for m in markers:
            name = _safe_text(m.get("biomarker_name"), 80)
            val = m.get("value")
            unit = _safe_text(m.get("unit"), 20)
            st = _marker_status(m)
            pdf.set_x(pdf.l_margin)
            line = f"- {name}: {val} {unit} ({st})"
            pdf.multi_cell(epw, 5, _safe_text(line, 500))
    pdf.ln(2)

    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 8, "System health overview", ln=1)
    pdf.set_font("Helvetica", size=10)
    if not sys_lines:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(epw, 5, "No balanced-systems summary was included for this result.")
    else:
        for line in sys_lines:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(epw, 5, f"- {_safe_text(line, 500)}")
    pdf.ln(2)

    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 8, "Recommended actions", ln=1)
    pdf.set_font("Helvetica", size=10)
    if not actions:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(epw, 5, "No separate action list was provided with this result.")
    else:
        for a in actions:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(epw, 5, f"- {_safe_text(a, 800)}")
    pdf.ln(6)

    pdf.set_font("Helvetica", style="I", size=8)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(epw, 4, _safe_text(DISCLAIMER, 500))

    pdf_output = pdf.output()
    if isinstance(pdf_output, (bytes, bytearray)):
        return bytes(pdf_output)
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1", errors="replace")
    return bytes(pdf_output)
