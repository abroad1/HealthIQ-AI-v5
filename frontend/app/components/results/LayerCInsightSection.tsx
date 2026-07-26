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
import {
  FATIGUE_NO_DRIVERS_EXPLANATION,
  FATIGUE_NO_DRIVERS_VALUE_LINE,
  LAYER_C_INSIGHT_COPY,
  LAYER_C_INSIGHT_DISPLAY_ORDER,
  type LayerCInsightKind,
} from '@/lib/layerCInsightCopy';

type LayerCKind = LayerCInsightKind;

interface QualifiedRow {
  kind: LayerCKind;
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

/**
 * Presence gate only: a feature qualifies when Layer B gave it confidence above zero.
 * ARCH-CONV-CORRECT-1 — the surviving rows keep the fixed display order; Layer C does not
 * re-rank them by confidence.
 */
function collectQualified(bundle: LayerCFeatureBundleV1): QualifiedRow[] {
  const confidenceFor = (kind: LayerCKind): number => {
    switch (kind) {
      case 'metabolic_age':
        return bundle.metabolic_age?.confidence ?? 0;
      case 'heart_insight':
        return bundle.heart_insight?.confidence ?? 0;
      case 'inflammation':
        return bundle.inflammation?.confidence ?? 0;
      case 'fatigue_root_cause':
        return bundle.fatigue_root_cause?.confidence ?? 0;
      case 'detox_filtration':
        return bundle.detox_filtration?.confidence ?? 0;
      default:
        return 0;
    }
  };

  return LAYER_C_INSIGHT_DISPLAY_ORDER.map((kind, tieIdx) => ({ kind, tieIdx }))
    .filter((row) => confidenceFor(row.kind) > 0)
    .slice(0, 3);
}

function MetabolicCard({ m }: { m: MetabolicAgeFeatureV1 }) {
  const age = Math.round(m.metabolic_age);
  const delta = m.age_delta_years;
  const deltaStr =
    typeof delta === 'number' && !Number.isNaN(delta) && delta !== 0
      ? ` (${delta > 0 ? '+' : ''}${delta.toFixed(1)} yrs vs expectation)`
      : '';
  const valueLine = `~${age} years${deltaStr}`;
  const copy = LAYER_C_INSIGHT_COPY.metabolic_age;
  const homa = m.homa_ir > 0 ? ` HOMA-IR ${m.homa_ir.toFixed(2)} is included in this read.` : '';
  return (
    <InsightCardShell
      title={copy.title}
      valueLine={valueLine}
      explanation={`${copy.explanation}${homa}`}
      whyItMatters={copy.whyItMatters}
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
  const copy = LAYER_C_INSIGHT_COPY.heart_insight;
  return (
    <InsightCardShell
      title={copy.title}
      valueLine={`Score ${score}${ratio ? ` ·${ratio}` : ''}`}
      explanation={copy.explanation}
      whyItMatters={copy.whyItMatters}
      severity={h.severity}
    />
  );
}

function InflammationCard({ f }: { f: InflammationFeatureV1 }) {
  const score = f.inflammation_burden_score.toFixed(1);
  const nlr = f.nlr != null ? ` · NLR ${f.nlr.toFixed(2)}` : '';
  const copy = LAYER_C_INSIGHT_COPY.inflammation;
  return (
    <InsightCardShell
      title={copy.title}
      valueLine={`Score ${score}${nlr}`}
      explanation={copy.explanation}
      whyItMatters={copy.whyItMatters}
      severity={f.severity}
    />
  );
}

function FatigueCard({ f }: { f: FatigueFeatureV1 }) {
  const causes = (f.root_causes || []).slice(0, 4).map(humanizeToken).filter(Boolean);
  const valueLine = causes.length > 0 ? causes.slice(0, 2).join(' · ') : FATIGUE_NO_DRIVERS_VALUE_LINE;
  const copy = LAYER_C_INSIGHT_COPY.fatigue_root_cause;
  return (
    <InsightCardShell
      title={copy.title}
      valueLine={valueLine}
      explanation={causes.length > 0 ? copy.explanation : FATIGUE_NO_DRIVERS_EXPLANATION}
      whyItMatters={copy.whyItMatters}
      severity={f.severity}
    />
  );
}

function DetoxCard({ d }: { d: DetoxFeatureV1 }) {
  const main = d.detox_filtration_score.toFixed(0);
  const liver = d.liver_score.toFixed(0);
  const kidney = d.kidney_score.toFixed(0);
  const egfr = d.egfr != null ? ` · eGFR ${d.egfr.toFixed(0)}` : '';
  const copy = LAYER_C_INSIGHT_COPY.detox_filtration;
  return (
    <InsightCardShell
      title={copy.title}
      valueLine={`Overall ${main} · liver ${liver} · kidney ${kidney}${egfr}`}
      explanation={copy.explanation}
      whyItMatters={copy.whyItMatters}
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
