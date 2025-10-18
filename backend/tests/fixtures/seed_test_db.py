from sqlalchemy import create_engine, text

TEST_DB_URL = "postgresql://postgres:test@localhost:5433/healthiq_test"
engine = create_engine(TEST_DB_URL)

with engine.begin() as conn:
    # --- Base user / profile ---
    conn.execute(text("""
        INSERT INTO profiles (id, user_id, email, demographics, consent_given,
                              consent_version, created_at, updated_at)
        VALUES ('00000000-0000-0000-0000-000000000001',
                '00000000-0000-0000-0000-000000000001',
                'test_user@example.com',
                '{"age": 30, "sex": "M"}', TRUE, '1.0', now(), now())
        ON CONFLICT (id) DO NOTHING;
    """))

    # --- Base analysis linked to profile ---
    conn.execute(text("""
        INSERT INTO analyses (id, user_id, analysis_version, pipeline_version,
                              status, raw_biomarkers, questionnaire_data,
                              created_at, updated_at)
        VALUES ('00000000-0000-0000-0000-000000000002',
                '00000000-0000-0000-0000-000000000001',
                '1.0.0', '1.0.0', 'completed', '{}', '{}', now(), now())
        ON CONFLICT (id) DO NOTHING;
    """))

    # --- Consents table with required fields ---
    conn.execute(text("""
        INSERT INTO consents (id, user_id, consent_type, granted, version,
                              created_at, updated_at)
        VALUES ('00000000-0000-0000-0000-000000000003',
                '00000000-0000-0000-0000-000000000001',
                'data_processing', TRUE, '1.0', now(), now())
        ON CONFLICT (id) DO NOTHING;
    """))

    # --- Audit log with required fields ---
    conn.execute(text("""
        INSERT INTO audit_logs (id, user_id, action, resource_type, created_at)
        VALUES ('00000000-0000-0000-0000-000000000004',
                '00000000-0000-0000-0000-000000000001',
                'seed_insert', 'profiles', now())
        ON CONFLICT (id) DO NOTHING;
    """))

print("Seed completed")