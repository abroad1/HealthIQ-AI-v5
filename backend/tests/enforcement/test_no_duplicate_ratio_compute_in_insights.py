"""
Sprint 5 - Enforcement: no duplicate canonical ratio computation in insight modules.

Deterministic, AST-based, read-only scanner.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


MODULES_DIR = Path(__file__).parent.parent.parent / "core" / "insights" / "modules"
PANEL_NAMES = {"panel", "biomarkers", "inputs"}

# Verified against ratio_registry.py ownership in this sprint.
RATIO_OPERAND_PAIRS = {
    ("total_cholesterol", "hdl_cholesterol"): "tc_hdl_ratio",
    ("triglycerides", "hdl_cholesterol"): "tg_hdl_ratio",
    ("ldl_cholesterol", "hdl_cholesterol"): "ldl_hdl_ratio",
    ("apob", "apoa1"): "apoB_apoA1_ratio",
    ("neutrophils", "lymphocytes"): "nlr",
    ("ast", "alt"): "ast_alt_ratio",
    ("urea", "creatinine"): "urea_creatinine_ratio",
    ("bun", "creatinine"): "bun_creatinine_ratio",
}

# Allow reversed ordering to keep detection robust to implementation variants.
REVERSED_RATIO_OPERAND_PAIRS = {
    (right, left): ratio_name for (left, right), ratio_name in RATIO_OPERAND_PAIRS.items()
}
ALL_RATIO_OPERAND_PAIRS = {**RATIO_OPERAND_PAIRS, **REVERSED_RATIO_OPERAND_PAIRS}


@dataclass(frozen=True)
class Violation:
    filepath: str
    lineno: int
    message: str


def _extract_target_names(target: ast.AST) -> set[str]:
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        out: set[str] = set()
        for elt in target.elts:
            out.update(_extract_target_names(elt))
        return out
    return set()


def _string_slice(node: ast.Subscript) -> str | None:
    slice_node = node.slice
    if isinstance(slice_node, ast.Constant) and isinstance(slice_node.value, str):
        return slice_node.value
    return None


class RatioComputeScanner(ast.NodeVisitor):
    def __init__(self, filepath: Path) -> None:
        self.filepath = str(filepath.as_posix())
        self.panel_aliases: set[str] = set(PANEL_NAMES)
        self.var_sources: dict[str, set[str]] = {}
        self.violations: list[Violation] = []

    def _lookup_sources(self, node: ast.AST) -> set[str]:
        if isinstance(node, ast.Name):
            return set(self.var_sources.get(node.id, set()))

        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
            key = _string_slice(node)
            if key is not None and node.value.id in self.panel_aliases:
                return {key}
            return self._lookup_sources(node.value)

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "get" and isinstance(node.func.value, ast.Name):
                if (
                    node.func.value.id in self.panel_aliases
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    return {node.args[0].value}
            return self._lookup_sources(node.func.value)

        if isinstance(node, ast.Attribute):
            return self._lookup_sources(node.value)

        if isinstance(node, ast.UnaryOp):
            return self._lookup_sources(node.operand)

        if isinstance(node, ast.BinOp):
            return self._lookup_sources(node.left) | self._lookup_sources(node.right)

        if isinstance(node, ast.IfExp):
            return (
                self._lookup_sources(node.test)
                | self._lookup_sources(node.body)
                | self._lookup_sources(node.orelse)
            )

        return set()

    def _record(self, lineno: int, message: str) -> None:
        self.violations.append(Violation(self.filepath, lineno, message))

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Name) and node.value.id in self.panel_aliases:
            for target in node.targets:
                self.panel_aliases.update(_extract_target_names(target))

        value_sources = self._lookup_sources(node.value)
        if value_sources:
            for target in node.targets:
                for name in _extract_target_names(target):
                    self.var_sources[name] = set(value_sources)

        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            return

        if isinstance(node.value, ast.Name) and node.value.id in self.panel_aliases:
            self.panel_aliases.update(_extract_target_names(node.target))

        value_sources = self._lookup_sources(node.value)
        if value_sources:
            for name in _extract_target_names(node.target):
                self.var_sources[name] = set(value_sources)

        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if isinstance(node.op, ast.Div):
            left_sources = sorted(self._lookup_sources(node.left))
            right_sources = sorted(self._lookup_sources(node.right))
            for left in left_sources:
                for right in right_sources:
                    ratio_name = ALL_RATIO_OPERAND_PAIRS.get((left, right))
                    if ratio_name is not None:
                        self._record(
                            node.lineno,
                            f"duplicate_ratio_compute: local computation of {ratio_name} from {left}/{right}",
                        )
                        break
                else:
                    continue
                break
        self.generic_visit(node)


def _scan_file(path: Path) -> list[Violation]:
    source = path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(source, filename=str(path))
    scanner = RatioComputeScanner(path)
    scanner.visit(tree)
    return scanner.violations


def test_no_duplicate_ratio_compute_in_insights_ast() -> None:
    files = sorted(
        [p for p in MODULES_DIR.glob("*.py") if p.name != "__init__.py"],
        key=lambda p: p.as_posix(),
    )
    violations: list[Violation] = []
    for path in files:
        violations.extend(_scan_file(path))

    violations.sort(key=lambda v: (v.filepath, v.lineno, v.message))
    if violations:
        report = "\n".join(
            f"{v.filepath}:{v.lineno}: {v.message}" for v in violations
        )
        raise AssertionError("DUPLICATE_RATIO_COMPUTE_VIOLATIONS:\n" + report)

    print("NO_DUPLICATE_RATIO_COMPUTE_VIOLATIONS: PASS")
