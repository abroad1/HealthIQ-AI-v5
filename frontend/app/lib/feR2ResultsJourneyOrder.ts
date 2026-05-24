/**
 * FE-R2 / FE-R5A — canonical retail journey section order (v6 Phase 1 + patterns bridge).
 * Used by page layout and regression guards.
 */
export const FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS = [
  'fe-r2-journey-body-overview',
  'fe-r2-journey-working-well',
  'fe-r2-journey-primary-finding',
  'fe-r2-journey-uncertainty',
  'fe-r5a-journey-patterns-across-body',
  'fe-r2-journey-marker-evidence',
  'fe-r2-journey-next-steps',
  'fe-r2-journey-clinician-summary',
] as const;

export type FeR2JourneySectionTestId = (typeof FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS)[number];
