import { API_BASE } from '@/lib/api';

/**
 * Question shape from GET /api/questionnaire/schema → `schema` array (SSOT-aligned).
 * Used by QuestionnaireForm rendering; must stay compatible with backend/ssot/questionnaire.json.
 */
export type QuestionImportanceV1 = 'mandatory' | 'recommended' | 'optional' | 'advanced';

export interface QuestionnaireQuestion {
  id: string;
  section: string;
  question: string;
  type: string;
  required: boolean;
  /** WP3 tier from SSOT; when absent, UI falls back to `required` for copy only. */
  importance?: QuestionImportanceV1;
  options?: string[];
  fields?: Array<{
    label: string;
    type: string;
    min?: number;
    max?: number;
  }>;
  alternativeUnit?: {
    label: string;
    type: string;
    min?: number;
    max?: number;
  };
  label?: string;
  min?: number;
  max?: number;
  helpText?: string;
  allowOther?: boolean;
  labels?: Record<string, string>;
  conditionalDisplay?: {
    dependsOn: string;
    showWhen: string[];
  };
}

/** Types handled explicitly by QuestionnaireForm (not the default Textarea fallback). */
const RENDERER_EXPLICIT_TYPES = new Set([
  'text',
  'email',
  'phone',
  'date',
  'number',
  'dropdown',
  'slider',
  'checkbox',
  'group',
]);

/**
 * Ensures every question uses a type the form renderer supports.
 * @throws Error if an unknown type is present (prevents silent UX drift).
 */
export function assertQuestionnaireSchemaCompatible(questions: QuestionnaireQuestion[]): void {
  for (const q of questions) {
    if (!q?.type || !RENDERER_EXPLICIT_TYPES.has(q.type)) {
      throw new Error(
        `Unsupported questionnaire question type: "${q?.type}" (id: ${q?.id ?? 'unknown'}). Update QuestionnaireForm or SSOT.`
      );
    }
  }
}

/**
 * Validates GET /api/questionnaire/schema JSON body and returns the schema array.
 */
export function parseQuestionnaireSchemaPayload(data: unknown): QuestionnaireQuestion[] {
  if (!data || typeof data !== 'object') {
    throw new Error('Invalid questionnaire schema response: expected an object');
  }
  const schema = (data as { schema?: unknown }).schema;
  if (!Array.isArray(schema)) {
    throw new Error('Invalid questionnaire schema response: expected { schema: Question[] }');
  }
  assertQuestionnaireSchemaCompatible(schema as QuestionnaireQuestion[]);
  return schema as QuestionnaireQuestion[];
}

/**
 * Fetches governed questionnaire schema from the backend (SSOT via API). No mock fallback.
 */
export async function fetchQuestionnaireSchema(): Promise<QuestionnaireQuestion[]> {
  const res = await fetch(`${API_BASE}/api/questionnaire/schema`, {
    credentials: 'omit',
    cache: 'no-store',
  });
  if (!res.ok) {
    throw new Error(`Questionnaire schema request failed (${res.status})`);
  }
  const data: unknown = await res.json();
  return parseQuestionnaireSchemaPayload(data);
}
