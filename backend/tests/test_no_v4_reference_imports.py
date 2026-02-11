from pathlib import Path


SKIP_DIRS = {
    ".git",
    "venv",
    ".venv",
    "site-packages",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
}


def _should_skip(path: Path) -> bool:
    if path.name == "test_no_v4_reference_imports.py":
        return True
    return any(part in SKIP_DIRS for part in path.parts)


def test_no_v4_reference_paths():
    backend_root = Path(__file__).resolve().parents[1]
    assert not (backend_root / "v4_reference").exists(), "backend/v4_reference must not exist"

    for path in backend_root.rglob("*"):
        if _should_skip(path):
            continue
        if "v4_reference" in path.parts:
            raise AssertionError(f"Unexpected v4_reference path found: {path}")


def test_no_get_close_matches_usage():
    repo_root = Path(__file__).resolve().parents[2]
    for path in repo_root.rglob("*"):
        if path.is_dir():
            continue
        if _should_skip(path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if "get_close_matches(" in content:
            raise AssertionError(f"get_close_matches usage found in: {path}")

