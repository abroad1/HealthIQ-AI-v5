"""
Dev smoke to prove Upload -> Parse endpoint remains green.

No network server required; uses FastAPI TestClient against the app object.

"""
import importlib

import json

from fastapi.testclient import TestClient

def load_app():
    # Try fully-qualified first (preferred when running from repo root)
    for mod in ("backend.app.main", "app.main"):
        try:
            return getattr(importlib.import_module(mod), "app")
        except Exception:
            continue
    raise SystemExit("FastAPI app not found (tried backend.app.main, app.main)")

def post_parse(client, text: str):
    r = client.post("/api/upload/parse", data={"text_content": text})
    try:
        body = r.json()
    except Exception:
        body = {"_non_json": r.text}
    keys = list(body.keys()) if isinstance(body, dict) else []
    count = (len(body.get("parsed_data", {}).get("biomarkers", []))
             if isinstance(body, dict) else None)
    return {"status": r.status_code, "keys": keys, "count": count, "body": body}

def main():
    app = load_app()
    c = TestClient(app)
    cases = {
        "empty": "",
        "two_lines": "ALT,42,U/L\nHDL,1.0,mmol/L"
    }
    results = {name: post_parse(c, txt) for name, txt in cases.items()}
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

