"""
Sprint 4 - Enforcement: prohibit local derived biomarker logic in insight modules.

AST-based, deterministic, read-only scanner.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pytest


MODULES_DIR = Path(__file__).parent.parent.parent / "core" / "insights" / "modules"
PANEL_NAMES = {"panel", "biomarkers", "inputs"}


@dataclass(frozen=True)
class Violation:
    filepath: str
    lineno: int
    message: str


def _is_numeric_constant(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, (int, float))


def _subscript_key(node: ast.Subscript) -> str | None:
    slice_node = node.slice
    if isinstance(slice_node, ast.Constant) and isinstance(slice_node.value, str):
        return slice_node.value
    return None


def _extract_target_names(target: ast.AST) -> set[str]:
    names: set[str] = set()
    if isinstance(target, ast.Name):
        names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            names.update(_extract_target_names(elt))
    return names


class FunctionScanner(ast.NodeVisitor):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.derived_names: set[str] = set()
        self.panel_aliases: set[str] = set(PANEL_NAMES)
        self.violations: list[Violation] = []

    def _is_panel_lookup(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if (
                node.func.attr == "get"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in self.panel_aliases
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                return True
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
            if node.value.id in self.panel_aliases and _subscript_key(node) is not None:
                return True
        return False

    def _expr_is_derived(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id in self.derived_names
        if self._is_panel_lookup(node):
            return True
        if isinstance(node, ast.Attribute):
            return self._expr_is_derived(node.value)
        if isinstance(node, ast.Subscript):
            return self._expr_is_derived(node.value)
        if isinstance(node, ast.UnaryOp):
            return self._expr_is_derived(node.operand)
        if isinstance(node, ast.BinOp):
            return self._expr_is_derived(node.left) or self._expr_is_derived(node.right)
        if isinstance(node, ast.BoolOp):
            return any(self._expr_is_derived(v) for v in node.values)
        if isinstance(node, ast.Compare):
            return self._expr_is_derived(node.left) or any(
                self._expr_is_derived(c) for c in node.comparators
            )
        if isinstance(node, ast.Call):
            if self._expr_is_derived(node.func):
                return True
            return any(self._expr_is_derived(arg) for arg in node.args)
        return False

    def _record(self, lineno: int, message: str) -> None:
        self.violations.append(Violation(self.filepath, lineno, message))

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Name) and node.value.id in self.panel_aliases:
            for target in node.targets:
                self.panel_aliases.update(_extract_target_names(target))

        if self._is_panel_lookup(node.value) or self._expr_is_derived(node.value):
            for target in node.targets:
                self.derived_names.update(_extract_target_names(target))
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is not None:
            if isinstance(node.value, ast.Name) and node.value.id in self.panel_aliases:
                self.panel_aliases.update(_extract_target_names(node.target))
            if self._is_panel_lookup(node.value) or self._expr_is_derived(node.value):
                self.derived_names.update(_extract_target_names(node.target))
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if isinstance(node.op, ast.Div):
            if self._expr_is_derived(node.left) or self._expr_is_derived(node.right):
                self._record(
                    node.lineno,
                    "derived_logic_division: division uses biomarker-derived operand",
                )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        if self._expr_is_derived(node.left) and any(_is_numeric_constant(c) for c in node.comparators):
            self._record(
                node.lineno,
                "derived_logic_threshold: biomarker-derived value compared to numeric constant",
            )
        self.generic_visit(node)


def _scan_file(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(text, filename=str(path))
    scanner = FunctionScanner(filepath=str(path.as_posix()))
    scanner.visit(tree)
    return scanner.violations


def _iter_module_files() -> Iterable[Path]:
    for path in sorted(MODULES_DIR.glob("*.py"), key=lambda p: p.as_posix()):
        if path.name == "__init__.py":
            continue
        yield path


def test_no_derived_logic_in_insight_modules_ast_enforced() -> None:
    violations: list[Violation] = []
    for file_path in _iter_module_files():
        violations.extend(_scan_file(file_path))

    violations.sort(key=lambda v: (v.filepath, v.lineno, v.message))
    if violations:
        report = "\n".join(
            f"{v.filepath}:{v.lineno}: {v.message}" for v in violations
        )
        raise AssertionError("DERIVED_LOGIC_VIOLATIONS:\n" + report)

    print("NO_DERIVED_LOGIC_VIOLATIONS: PASS")
