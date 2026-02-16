"""
Sprint 10 - Enforcement: relationship logic must remain registry-driven.
"""

from pathlib import Path
import re


_RELATIONSHIP_IDS = (
    "tg_hdl_metabolic_pattern",
    "apob_ldl_discordance",
    "ferritin_crp_inflammation_modifier",
    "ast_alt_hepatic_pattern",
    "bun_creatinine_renal_pattern",
    "neutrophils_lymphocytes_inflammation_pattern",
)


def _runtime_py_files() -> list[Path]:
    root = Path(__file__).parent.parent.parent
    files = list((root / "core").rglob("*.py"))
    allowed_suffixes = {
        str(Path("core") / "analytics" / "relationship_registry.py"),
        str(Path("core") / "contracts" / "relationship_registry_v1.py"),
    }
    out: list[Path] = []
    for p in files:
        rel = str(p.relative_to(root))
        if rel in allowed_suffixes:
            continue
        out.append(p)
    return out


def test_no_hardcoded_relationship_ids_in_runtime_modules():
    """Relationship IDs must come from ssot/relationships.yaml, not runtime code constants."""
    offenders: list[str] = []
    for py_path in _runtime_py_files():
        text = py_path.read_text(encoding="utf-8", errors="ignore")
        for rid in _RELATIONSHIP_IDS:
            if rid in text:
                offenders.append(f"{py_path}: {rid}")
    assert not offenders, (
        "Sprint 10: hardcoded relationship IDs found outside registry modules:\n"
        + "\n".join(offenders)
    )


def test_no_inline_pairwise_relationship_conditions_in_insight_modules():
    """Insight modules should not encode pairwise relationship branching (registry owns it)."""
    root = Path(__file__).parent.parent.parent
    insights_dir = root / "core" / "insights" / "modules"
    patterns = [
        r"if\s+.*['\"]triglycerides['\"].*and.*['\"]hdl_cholesterol['\"]",
        r"if\s+.*['\"]apob['\"].*and.*['\"]ldl_cholesterol['\"]",
        r"if\s+.*['\"]ferritin['\"].*and.*['\"]crp['\"]",
        r"if\s+.*['\"]ast['\"].*and.*['\"]alt['\"]",
        r"if\s+.*['\"]bun['\"].*and.*['\"]creatinine['\"]",
        r"if\s+.*['\"]neutrophils['\"].*and.*['\"]lymphocytes['\"]",
    ]
    offenders: list[str] = []
    for py_path in insights_dir.rglob("*.py"):
        text = py_path.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in patterns:
            if re.search(pattern, text):
                offenders.append(f"{py_path}: {pattern}")
    assert not offenders, (
        "Sprint 10: inline pairwise relationship condition(s) found in insight modules:\n"
        + "\n".join(offenders)
    )
