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
                '1.0.0', '1.0.0', 'completed', 
                '{"glucose": {"value": 5.1, "unit": "mmol/L", "normal_range": [3.9, 5.5], "status": "normal"}, "hdl": {"value": 1.4, "unit": "mmol/L", "normal_range": [1.0, 2.0], "status": "normal"}, "ldl": {"value": 2.3, "unit": "mmol/L", "normal_range": [1.5, 3.0], "status": "normal"}, "triglycerides": {"value": 1.1, "unit": "mmol/L", "normal_range": [0.4, 1.8], "status": "normal"}, "cholesterol_total": {"value": 4.8, "unit": "mmol/L", "normal_range": [3.0, 5.0], "status": "normal"}, "hba1c": {"value": 34, "unit": "mmol/mol", "normal_range": [20, 42], "status": "normal"}}', 
                '{"full_name": "Test User", "email_address": "test@example.com", "phone_number": "07123456789", "country": "United Kingdom", "state_province": "London", "date_of_birth": "1990-01-15", "biological_sex": "Male", "height": {"Feet": 6, "Inches": 0}, "weight": 180, "sleep_hours_nightly": "7-8 hours", "sleep_quality_rating": 7, "alcohol_drinks_weekly": "4-7 drinks", "tobacco_use": "Never used", "stress_level_rating": 5, "vigorous_exercise_days": "3 days", "current_medications": "None", "long_term_medications": ["None"], "chronic_conditions": ["None"], "medical_conditions": ["None"], "current_symptoms": ["None"], "regular_migraines": "No"}', 
                now(), now())
        ON CONFLICT (id) DO UPDATE SET 
            raw_biomarkers = EXCLUDED.raw_biomarkers,
            questionnaire_data = EXCLUDED.questionnaire_data,
            updated_at = now();
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