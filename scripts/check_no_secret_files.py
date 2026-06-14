#!/usr/bin/env python3
"""
Guardrail: fail if any secret-bearing env files are tracked by git.

Safe example/test files (placeholder values only) are explicitly whitelisted.
Run this as a pre-commit check or CI step.
"""
import subprocess
import sys

BLOCKED_PATTERNS = [
    ".env",
    "old.env",
]

# Files that are allowed to be tracked (placeholders only)
ALLOWLIST = {
    ".env.example",
    ".env.local.example",
    ".env.test",
    "backend/.env.example",
    "backend/.env.test",
    "frontend/.env.local.example",
}

def get_tracked_files():
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.splitlines()

def is_blocked(filepath):
    import os
    filename = os.path.basename(filepath)
    # Exact allowlist check first
    if filepath in ALLOWLIST or filename in {a.split("/")[-1] for a in ALLOWLIST}:
        # Only allow if it's actually in the allowlist set
        if filepath in ALLOWLIST:
            return False
    # Block if filename matches any blocked pattern
    for pattern in BLOCKED_PATTERNS:
        if filename == pattern or filename.startswith("old.env"):
            return True
        if pattern == ".env" and filename == ".env":
            return True
    return False

def main():
    tracked = get_tracked_files()
    violations = [f for f in tracked if is_blocked(f)]

    if violations:
        print("GUARDRAIL FAILURE: secret-bearing env files are tracked by git:")
        for v in violations:
            print(f"  - {v}")
        print()
        print("Run: git rm --cached <file>  to untrack.")
        print("Ensure .gitignore covers these patterns:")
        print("  .env  *.env  *.env.*  old.env*")
        sys.exit(1)

    print("OK: no secret env files are git-tracked.")
    sys.exit(0)

if __name__ == "__main__":
    main()
