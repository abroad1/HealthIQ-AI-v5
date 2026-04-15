'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type {
  DetoxFeatureV1,
  FatigueFeatureV1,
  HeartFeatureV1,
  InflammationFeatureV1,
  LayerCFeatureBundleV1,
  MetabolicAgeFeatureV1,
} from '@/types/layerCFeatures';

type LayerCKind = 'metabolic_age' | 'heart_insight' | 'inflammation' | 'fatigue_root_cause' | 'detox_filtration';

interface QualifiedRow {
  kind: LayerCKind;
  confidence: number;
  tieIdx: number;
}

function humanizeToken(s: string): string {
  return s
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Plain-language hint for severity — not clinical labelling. */
function severityHint(sev: string): string {
  const x = sev.toLowerCase();
  if (x === 'normal' || x === 'low') return 'Lower concern on this panel';
  if (x === 'mild' || x === 'moderate') return 'Worth monitoring in context';
  if (x === 'high' || x === 'elevated' || x === 'critical') return 'Stronger signal on this panel';
  return 'Review in context below';
}

function collectQualified(bundle: LayerCFeatureBundleV1): QualifiedRow[] {
  const rows: QualifiedRow[] = [];
  const push = (kind: LayerCKind, tieIdx: number, confidence: number) => {
    if (confidence > 0) rows.push({ kind, confidence, tieIdx });
  };
  push('metabolic_age', 0, bundle.metabolic_age?.confidence ?? 0);
  push('heart_insight', 1, bundle.heart_insight?.confidence ?? 0);
  push('inflammation', 2, bundle.inflammation?.confidence ?? 0);
  push('fatigue_root_cause', 3, bundle.fatigue_root_cause?.confidence ?? 0);
  push('detox_filtration', 4, bundle.detox_filtration?.confidence ?? 0);

  rows.sort((a, b) => {
    if (b.confidence !== a.confidence) return b.confidence - a.confidence;
    return a.tieIdx - b.tieIdx;
  });
  return rows.slice(0, 3);
}

function MetabolicCard({ m }: { m: MetabolicAgeFeatureV1 }) {
  const age = Math.round(m.metabolic_age);
  const delta = m.age_delta_years;
  const deltaStr =
    typeof delta === 'number' && !Number.isNaN(delta) && delta !== 0
      ? ` (${delta > 0 ? '+' : ''}${delta.toFixed(1)} yrs vs expectation)`
      : '';
  const valueLine = `~${age} years${deltaStr}`;
  const homa = m.homa_ir > 0 ? ` HOMA-IR ${m.homa_ir.toFixed(2)} is included in this read.` : '';
  return (
    <InsightCardShell
      title="Metabolic age pattern"
      valueLine={valueLine}
      explanation={`This lines up insulin–glucose signals from your panel into an age-style summary.${homa}`}
      whyItMatters="It shows whether metabolic markers sit where they would broadly be expected for the story above—not a diagnosis on their own."
      severity={m.severity}
    />
  );
}

function HeartCard({ h }: { h: HeartFeatureV1 }) {
  const score = Math.round(h.heart_resilience_score);
  const ratio =
    h.ldl_hdl_ratio != null
      ? ` LDL/HDL ${h.ldl_hdl_ratio.toFixed(2)}`
      : h.tc_hdl_ratio != null
        ? ` TC/HDL ${h.tc_hdl_ratio.toFixed(2)}`
        : h.tg_hdl_ratio != null
          ? ` TG/HDL ${h.tg_hdl_ratio.toFixed(2)}`
          : '';
  return (
    <InsightCardShell
      title="Heart resilience"
      valueLine={`Score ${score}${ratio ? ` ·${ratio}` : ''}`}
      explanation="One combined read of lipid balance signals we use for cardiovascular resilience on this snapshot."
      whyItMatters="It tells you whether heart-related markers are broadly aligned or pulling in the same direction—useful context next to your main finding."
      severity={h.severity}
    />
  );
}

function InflammationCard({ f }: { f: InflammationFeatureV1 }) {
  const score = f.inflammation_burden_score.toFixed(1);
  const nlr = f.nlr != null ? ` · NLR ${f.nlr.toFixed(2)}` : '';
  return (
    <InsightCardShell
      title="Inflammation burden"
      valueLine={`Score ${score}${nlr}`}
      explanation="Summarises inflammatory markers on the panel into a single burden read."
      whyItMatters="Inflammation can amplify other patterns; this keeps that signal explicit without drifting into lifestyle advice."
      severity={f.severity}
    />
  );
}

function FatigueCard({ f }: { f: FatigueFeatureV1 }) {
  const causes = (f.root_causes || []).slice(0, 4).map(humanizeToken).filter(Boolean);
  const valueLine =
    causes.length > 0 ? causes.slice(0, 2).join(' · ') : 'Cross-check across iron, thyroid, vitamins, inflammation, and cortisol signals';
  return (
    <InsightCardShell
      title="Fatigue drivers"
      valueLine={valueLine}
      explanation={
        causes.length > 0
          ? 'These are the main driver lines we could separate deterministically from your markers.'
          : 'We reviewed the fatigue-related status lines below against your results.'
      }
      whyItMatters="Fatigue is often multi-factor; this keeps the deterministic drivers visible without claiming a single cause."
      severity={f.severity}
    />
  );
}

function DetoxCard({ d }: { d: DetoxFeatureV1 }) {
  const main = d.detox_filtration_score.toFixed(0);
  const liver = d.liver_score.toFixed(0);
  const kidney = d.kidney_score.toFixed(0);
  const egfr = d.egfr != null ? ` · eGFR ${d.egfr.toFixed(0)}` : '';
  return (
    <InsightCardShell
      title="Detox and filtration"
      valueLine={`Overall ${main} · liver ${liver} · kidney ${kidney}${egfr}`}
      explanation="Combines liver and kidney-facing signals we can read from this panel into one filtration view."
      whyItMatters="It helps you see whether clearance-related markers look broadly supported or under strain alongside everything else."
      severity={d.severity}
    />
  );
}

function InsightCardShell({
  title,
  valueLine,
  explanation,
  whyItMatters,
  severity,
}: {
  title: string;
  valueLine: string;
  explanation: string;
  whyItMatters: string;
  severity: string;
}) {
  return (
    <Card className="border-slate-200 bg-white shadow-sm h-full">
      <CardHeader className="pb-2 space-y-2">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <CardTitle className="text-base font-semibold text-gray-900 leading-snug">{title}</CardTitle>
          <Badge variant="outline" className="font-normal text-xs shrink-0">
            {severityHint(severity)}
          </Badge>
        </div>
        <p className="text-lg font-semibold text-gray-900 tabular-nums">{valueLine}</p>
      </CardHeader>
      <CardContent className="space-y-3 text-sm text-gray-700 leading-relaxed pt-0">
        <p>{explanation}</p>
        <p className="text-gray-600 border-t border-gray-100 pt-3">
          <span className="font-medium text-gray-800">Why it matters: </span>
          {whyItMatters}
        </p>
      </CardContent>
    </Card>
  );
}

export interface LayerCInsightSectionProps {
  /** From `meta.insight_graph.layer_c_features`; null when absent. */
  bundle: LayerCFeatureBundleV1 | null | undefined;
}

/**
 * FE-R6 — Section 7: deterministic Layer C features only (confidence > 0), max 3 cards.
 */
export function LayerCInsightSection({ bundle }: LayerCInsightSectionProps) {
  if (!bundle) return null;

  const qualified = collectQualified(bundle);
  if (qualified.length === 0) return null;

  return (
    <section className="space-y-4" aria-labelledby="layer-c-insights-heading" data-testid="layer-c-insight-section">
      <h2 id="layer-c-insights-heading" className="text-xl font-semibold text-gray-900">
        Key body-level insights
      </h2>
      <p className="text-sm text-gray-600 max-w-prose">
        A small set of higher-order reads computed from your results—not a full list of every signal. Shown only when the
        model had enough confidence to surface them.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {qualified.map((row) => {
          const key = `${row.kind}-${row.tieIdx}`;
          switch (row.kind) {
            case 'metabolic_age':
              return <MetabolicCard key={key} m={bundle.metabolic_age} />;
            case 'heart_insight':
              return <HeartCard key={key} h={bundle.heart_insight} />;
            case 'inflammation':
              return <InflammationCard key={key} f={bundle.inflammation} />;
            case 'fatigue_root_cause':
              return <FatigueCard key={key} f={bundle.fatigue_root_cause} />;
            case 'detox_filtration':
              return <DetoxCard key={key} d={bundle.detox_filtration} />;
            default:
              return null;
          }
        })}
      </div>
    </section>
  );
}
