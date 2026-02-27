"""
Sprint 19 Layer 2 — Deterministic Lifestyle Modifier Engine.

Bounded additive modifiers to system burden. UK metric canonical only.
No fuzzy logic. No file I/O. Accepts pre-loaded registry dict.
"""

from __future__ import annotations

import ast
from typing import Any, Dict, List, Optional


def _r4(v: float) -> float:
    """Round to 4 decimal places for deterministic output."""
    return round(float(v), 4)


class LifestyleModifierEngine:
    """Deterministic lifestyle modifier engine. Phase 1: bounded additive modifiers."""

    def __init__(self, registry: dict) -> None:
        self._registry = registry
        self._sit_stand = registry.get("sit_stand", {})
        self._derived_spec = registry.get("derived", {})
        self._inputs_spec = registry.get("inputs", {})
        self._system_caps = registry.get("system_caps", {})
        self._system_modifiers = registry.get("system_modifiers", {})
        self._confidence_rules = registry.get("confidence_rules", {})
        self._missing_penalty = self._confidence_rules.get("missing_input_confidence_penalty", {})
        self._core_inputs = self._confidence_rules.get("core_inputs_by_system", {})

    def compute_derived(self, lifestyle_inputs: dict) -> Dict[str, float]:
        """Compute derived values (waist_to_height_ratio, bmi)."""
        out: Dict[str, float] = {}
        for name, spec in self._derived_spec.items():
            dt = spec.get("type")
            if dt == "ratio":
                num_key = spec.get("numerator")
                den_key = spec.get("denominator")
                mult = float(spec.get("multiplier", 1.0))
                num = _to_float(lifestyle_inputs.get(num_key))
                den = _to_float(lifestyle_inputs.get(den_key))
                if num is not None and den is not None and den != 0:
                    out[name] = _r4(num / den * mult)
            elif dt == "formula":
                formula = spec.get("formula", "")
                inputs_list = spec.get("inputs", [])
                locals_map: Dict[str, float] = {}
                ok = True
                for k in inputs_list:
                    v = _to_float(lifestyle_inputs.get(k))
                    if v is None:
                        ok = False
                        break
                    locals_map[k] = v
                if ok:
                    try:
                        tree = ast.parse(formula, mode="eval")
                        val = _eval_ast(tree.body, locals_map)
                        if val is not None:
                            out[name] = _r4(val)
                    except Exception:
                        pass
        return out

    def validate_inputs(self, lifestyle_inputs: dict) -> List[str]:
        """Return list of validation errors. Does not raise by default."""
        errors: List[str] = []
        derived = self.compute_derived(lifestyle_inputs)
        merged = {**lifestyle_inputs, **derived}
        for name, spec in self._inputs_spec.items():
            val = merged.get(name)
            inp_type = spec.get("type", "numeric")
            if inp_type == "numeric":
                f = _to_float(val)
                if val is not None and f is None:
                    errors.append(f"{name}: expected numeric, got {type(val).__name__}")
                elif f is not None:
                    mn = spec.get("min")
                    mx = spec.get("max")
                    if mn is not None and f < mn:
                        errors.append(f"{name}: below min {mn}")
                    if mx is not None and f > mx:
                        errors.append(f"{name}: above max {mx}")
            elif inp_type == "categorical":
                if val is not None:
                    allowed = spec.get("values", [])
                    if allowed and val not in allowed:
                        errors.append(f"{name}: invalid category '{val}', expected one of {allowed}")
        return errors

    def apply(
        self,
        base_system_burdens: Dict[str, float],
        lifestyle_inputs: dict,
    ) -> dict:
        """Apply lifestyle modifiers to base burdens. Returns full result contract."""
        derived = self.compute_derived(lifestyle_inputs)
        validated = {**lifestyle_inputs, **derived}
        input_errors = self.validate_inputs(lifestyle_inputs)
        system_modifiers_out: Dict[str, dict] = {}
        all_systems = sorted(set(self._system_modifiers.keys()) | set(self._system_caps.keys()))
        for system in all_systems:
            mod_data = self._compute_system_modifiers(system, validated, input_errors)
            system_modifiers_out[system] = mod_data
        adjusted = self._compute_adjusted_burdens(
            base_system_burdens, system_modifiers_out, all_systems
        )
        return {
            "derived_inputs": {k: v for k, v in sorted(derived.items())},
            "validated_inputs": {k: _to_json_safe(v) for k, v in sorted(validated.items())},
            "input_errors": input_errors,
            "system_modifiers": system_modifiers_out,
            "adjusted_system_burdens": adjusted,
        }

    def _compute_system_modifiers(
        self,
        system: str,
        validated: dict,
        input_errors: List[str],
    ) -> dict:
        mod_spec = self._system_modifiers.get(system, {})
        system_cap = _to_float(self._system_caps.get(system)) or 0.0
        contributions: List[dict] = []
        total = 0.0
        input_rules = sorted((k, v) for k, v in mod_spec.items())
        for input_name, rule_spec in input_rules:
            rule_type = rule_spec.get("type")
            if rule_type == "passthrough":
                continue
            mod_val = self._eval_rule(rule_type, input_name, rule_spec, validated)
            if mod_val is None:
                continue
            cap = _to_float(rule_spec.get("cap")) or 1.0
            capped = min(mod_val, cap)
            total += capped
            raw_val = validated.get(input_name)
            contributions.append({
                "input": input_name,
                "rule": rule_type,
                "value": _to_json_safe(raw_val),
                "modifier": _r4(mod_val),
                "capped_modifier": _r4(capped),
                "details": {},
            })
        contributions.sort(key=lambda c: c["input"])
        capped_total = min(total, system_cap)
        missing_core = []
        core_list = self._core_inputs.get(system, [])
        errored_inputs = set()
        for err in input_errors:
            if ": " in err:
                errored_inputs.add(err.split(": ", 1)[0])
        for inp in core_list:
            val = validated.get(inp)
            missing = val is None or (isinstance(val, str) and not val.strip())
            invalid = inp in errored_inputs
            if missing or invalid:
                missing_core.append(inp)
        penalty = _to_float(self._missing_penalty.get(system)) or 0.0
        if not missing_core:
            penalty = 0.0
        return {
            "total_modifier": _r4(total),
            "capped_total_modifier": _r4(capped_total),
            "cap": _r4(system_cap),
            "contributions": contributions,
            "missing_core_inputs": sorted(missing_core),
            "confidence_penalty": _r4(penalty),
        }

    def _eval_rule(
        self,
        rule_type: str,
        input_name: str,
        rule_spec: dict,
        validated: dict,
    ) -> Optional[float]:
        val = validated.get(input_name)
        if rule_type == "thresholds_above":
            f = _to_float(val)
            if f is None:
                return None
            thresholds = rule_spec.get("thresholds", [])
            best: Optional[float] = None
            for t in thresholds:
                above = _to_float(t.get("above"))
                if above is not None and f > above:
                    m = _to_float(t.get("modifier")) or 0.0
                    if best is None or m > best:
                        best = m
            return best if best is not None else 0.0
        if rule_type == "thresholds_below":
            f = _to_float(val)
            if f is None:
                return None
            thresholds = rule_spec.get("thresholds", [])
            best = None
            for t in thresholds:
                below = _to_float(t.get("below"))
                if below is not None and f < below:
                    m = _to_float(t.get("modifier")) or 0.0
                    if best is None or m > best:
                        best = m
            return best if best is not None else 0.0
        if rule_type == "categorical_values":
            values = rule_spec.get("values", {})
            key = str(val).strip() if val is not None else ""
            return _to_float(values.get(key, 0.0))
        if rule_type == "sit_stand_phase1":
            test_type = validated.get("sit_stand_test_type")
            v = _to_float(val)
            if v is None:
                return 0.0
            cfg = self._sit_stand.get(str(test_type or ""), {})
            thresh = _to_float(cfg.get("threshold"))
            mod = _to_float(cfg.get("modifier")) or 0.0
            direction = str(cfg.get("direction", "")).strip().lower()
            if thresh is None:
                return 0.0
            if direction == "below" and v < thresh:
                return mod
            if direction == "above" and v > thresh:
                return mod
            return 0.0
        return None

    def _compute_adjusted_burdens(
        self,
        base_system_burdens: Dict[str, float],
        system_modifiers_out: Dict[str, dict],
        all_systems: List[str],
    ) -> dict:
        out: Dict[str, dict] = {}
        for system in all_systems:
            base = _to_float(base_system_burdens.get(system)) or 0.0
            mod_data = system_modifiers_out.get(system, {})
            modifier = mod_data.get("capped_total_modifier", 0.0)
            adj = max(0.0, min(1.0, base + modifier))
            penalty = mod_data.get("confidence_penalty", 0.0)
            out[system] = {
                "base_burden": _r4(base),
                "modifier": _r4(modifier),
                "adjusted_burden": _r4(adj),
                "confidence_penalty": _r4(penalty),
            }
        return out


def _to_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def _to_json_safe(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return _r4(v) if isinstance(v, float) else v
    if isinstance(v, str):
        return v
    return v


def _eval_ast(node: ast.AST, locals_map: Dict[str, float]) -> Optional[float]:
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left, locals_map)
        right = _eval_ast(node.right, locals_map)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.Div):
            return left / right if right != 0 else None
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Pow):
            return left ** right
        return None
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        child = _eval_ast(node.operand, locals_map)
        return -child if child is not None else None
    if isinstance(node, ast.Name):
        return locals_map.get(node.id)
    if isinstance(node, ast.Constant):
        val = node.value
        return float(val) if isinstance(val, (int, float)) else None
    return None
