"""
Sprint 14 - Enforcement: deterministic failure envelope in orchestrator exception return.
"""

from pathlib import Path


def test_orchestrator_exception_return_has_no_nondeterministic_calls():
    path = Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    text = path.read_text(encoding="utf-8", errors="ignore")

    except_idx = text.find("except Exception as e:")
    assert except_idx != -1, "Expected orchestrator exception block"

    ret_idx = text.find("return AnalysisDTO(", except_idx)
    assert ret_idx != -1, "Expected AnalysisDTO return in orchestrator exception block"

    # Scope enforcement to the exception return block window only.
    return_block_window = text[ret_idx: ret_idx + 700]
    assert "uuid.uuid4()" not in return_block_window
    assert "datetime.now(" not in return_block_window
