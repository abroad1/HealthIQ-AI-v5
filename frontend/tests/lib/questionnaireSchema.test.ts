import {
  assertQuestionnaireSchemaCompatible,
  parseQuestionnaireSchemaPayload,
  fetchQuestionnaireSchema,
} from '@/lib/questionnaireSchema';
import type { QuestionnaireQuestion } from '@/lib/questionnaireSchema';

describe('questionnaireSchema', () => {
  const bloodPressureReading: QuestionnaireQuestion = {
    id: 'blood_pressure_reading',
    section: 'medical_history',
    question: 'Blood Pressure Reading (if available)',
    type: 'group',
    fields: [
      { label: 'Systolic (mmHg)', type: 'number', min: 70, max: 250 },
      { label: 'Diastolic (mmHg)', type: 'number', min: 40, max: 150 },
    ],
    required: false,
  };

  it('parseQuestionnaireSchemaPayload accepts API wrapper with schema array', () => {
    const data = {
      schema: [bloodPressureReading],
      total_questions: 1,
      version: '1.0',
    };
    const out = parseQuestionnaireSchemaPayload(data);
    expect(out).toHaveLength(1);
    expect(out[0].id).toBe('blood_pressure_reading');
    expect(out[0].type).toBe('group');
  });

  it('assertQuestionnaireSchemaCompatible allows blood_pressure_reading group', () => {
    expect(() => assertQuestionnaireSchemaCompatible([bloodPressureReading])).not.toThrow();
  });

  it('assertQuestionnaireSchemaCompatible rejects unsupported types', () => {
    expect(() =>
      assertQuestionnaireSchemaCompatible([
        {
          id: 'bad',
          section: 'x',
          question: 'q',
          type: 'radio',
          required: true,
        } as QuestionnaireQuestion,
      ])
    ).toThrow(/Unsupported questionnaire question type/);
  });

  it('parseQuestionnaireSchemaPayload throws when schema is missing', () => {
    expect(() => parseQuestionnaireSchemaPayload({})).toThrow(/expected \{ schema/);
  });

  it('fetchQuestionnaireSchema calls /api/questionnaire/schema and returns questions', async () => {
    const mockFetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        schema: [bloodPressureReading],
        total_questions: 1,
      }),
    });
    global.fetch = mockFetch as unknown as typeof fetch;

    const result = await fetchQuestionnaireSchema();

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/api\/questionnaire\/schema$/),
      expect.objectContaining({ credentials: 'omit', cache: 'no-store' })
    );
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('blood_pressure_reading');
  });
});
