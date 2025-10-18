from sqlalchemy import create_engine, text

TEST_DB_URL = "postgresql://postgres:test@localhost:5433/healthiq_test"
engine = create_engine(TEST_DB_URL)

with engine.begin() as conn:
    # Check if profile already exists
    result = conn.execute(text("SELECT COUNT(*) FROM profiles WHERE id = '00000000-0000-0000-0000-000000000001'")).scalar()
    
    if result == 0:
        # Base profile
        conn.execute(text("""
            INSERT INTO profiles (id, user_id, email, demographics, consent_given, consent_version, created_at, updated_at)
            VALUES ('00000000-0000-0000-0000-000000000001',
                    '00000000-0000-0000-0000-000000000001',
                    'seed-test@example.com',
                    '{"age": 30, "sex": "M"}',
                    true,
                    '1.0',
                    now(), now())
        """))
        print("✅ Test profile created")
    else:
        print("✅ Test profile already exists")

    # Check if analysis already exists
    result = conn.execute(text("SELECT COUNT(*) FROM analyses WHERE id = '00000000-0000-0000-0000-000000000002'")).scalar()
    
    if result == 0:
        # Linked analysis
        conn.execute(text("""
            INSERT INTO analyses (id, user_id, status, raw_biomarkers, questionnaire_data, analysis_version, pipeline_version, created_at, updated_at)
            VALUES ('00000000-0000-0000-0000-000000000002',
                    '00000000-0000-0000-0000-000000000001',
                    'completed', '{}', '{}', '1.0.0', '1.0.0', now(), now())
        """))
        print("✅ Test analysis created")
    else:
        print("✅ Test analysis already exists")

print("✅ Database seeding completed successfully")
