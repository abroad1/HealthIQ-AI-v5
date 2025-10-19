import os

def init_database():
    if os.getenv("ENV") == "prod":
        print("[INIT] Production mode – external DB expected")
    else:
        print("[INIT] Running HealthIQ-AI in fixture-only mode (no database required)")