/**
 * ARCH-CONV-CORRECT-1 — governed static copy for the Layer C insight cards.
 *
 * Every string here is fixed product copy describing what a deterministic Layer C
 * feature is. None of it is derived from a user's biomarker values, and none of it
 * asserts a cause, diagnosis, risk level or recommendation about the reader. Numeric
 * values shown on a card come from the Layer C feature DTO only.
 *
 * Layer C must not author new medical prose: if a statement about a user is needed,
 * it has to arrive from Layer B as governed content.
 */

export type LayerCInsightKind =
  | 'metabolic_age'
  | 'heart_insight'
  | 'inflammation'
  | 'fatigue_root_cause'
  | 'detox_filtration';

export interface LayerCInsightCopy {
  title: string;
  explanation: string;
  whyItMatters: string;
}

export const LAYER_C_INSIGHT_COPY: Record<LayerCInsightKind, LayerCInsightCopy> = {
  metabolic_age: {
    title: 'Metabolic age pattern',
    explanation: 'This lines up insulin–glucose signals from your panel into an age-style summary.',
    whyItMatters:
      'It shows whether metabolic markers sit where they would broadly be expected for the story above—not a diagnosis on their own.',
  },
  heart_insight: {
    title: 'Heart resilience',
    explanation:
      'One combined read of lipid balance signals we use for cardiovascular resilience on this snapshot.',
    whyItMatters:
      'It tells you whether heart-related markers are broadly aligned or pulling in the same direction—useful context next to your main finding.',
  },
  inflammation: {
    title: 'Inflammation burden',
    explanation: 'Summarises inflammatory markers on the panel into a single burden read.',
    whyItMatters:
      'Inflammation can amplify other patterns; this keeps that signal explicit without drifting into lifestyle advice.',
  },
  fatigue_root_cause: {
    title: 'Fatigue drivers',
    explanation: 'These are the main driver lines we could separate deterministically from your markers.',
    whyItMatters:
      'Fatigue is often multi-factor; this keeps the deterministic drivers visible without claiming a single cause.',
  },
  detox_filtration: {
    title: 'Detox and filtration',
    explanation:
      'Combines liver and kidney-facing signals we can read from this panel into one filtration view.',
    whyItMatters:
      'It helps you see whether clearance-related markers look broadly supported or under strain alongside everything else.',
  },
};

/** Shown when no deterministic fatigue drivers were separated by Layer B. */
export const FATIGUE_NO_DRIVERS_EXPLANATION =
  'We reviewed the fatigue-related status lines below against your results.';

export const FATIGUE_NO_DRIVERS_VALUE_LINE =
  'Cross-check across iron, thyroid, vitamins, inflammation, and cortisol signals';

/**
 * Fixed presentation order for the Layer C cards. Layer C renders in this order and
 * never re-ranks by confidence or severity — ranking is a Layer B decision.
 */
export const LAYER_C_INSIGHT_DISPLAY_ORDER: readonly LayerCInsightKind[] = [
  'metabolic_age',
  'heart_insight',
  'inflammation',
  'fatigue_root_cause',
  'detox_filtration',
];
