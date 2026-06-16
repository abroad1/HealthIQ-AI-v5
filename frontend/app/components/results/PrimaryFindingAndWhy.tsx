'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicianEvidenceItem, ClinicianReportV1 } from '@/types/analysis';
import { buildSection3LeadStatement, buildWhatThisMeansBlock, firstSentence } from '@/lib/primaryFindingShaping';
import { formatBiomarkerDisplayName } from '@/lib/resultsPageLayout';
import { neutraliseHypothesisTitleForDisplay } from '@/lib/hypothesisDisplayCopy';
import { scrubConsumerRetailNarrative } from '@/lib/retailNarrativeSanitize';

function formatMarkerRef(id: string): string {
  return formatBiomarkerDisplayName(id);
}

function evidenceLine(ev: ClinicianEvidenceItem): string {
  const item = scrubConsumerRetailNarrative(ev.item || '');
  const refs = ev.marker_refs?.length
    ? ` (related markers: ${ev.marker_refs.map(formatMarkerRef).join(', ')})`
    : '';
  return `${item}${refs}`;
}

export interface PrimaryFindingAndWhyProps {
  report: ClinicianReportV1 | null | undefined;
  /** When true, hides the lead + “what this means” blocks (hero already surfaced them). */
  omitIntroDuplicate?: boolean;
  /** FE-R3 — omit confirmatory test bullets when the next-steps section surfaces them. */
  omitConfirmatoryInClarify?: boolean;
  /** FE-R6A — hero lead pattern label when hypothesis title differs. */
  leadPatternLabel?: string | null;
  /** LC-S7 — evidence chains / raw ranking rationale only when user enables technical detail. */
  showTechnicalDetail?: boolean;
}

/**
 * FE-R2 Section 3 — Primary finding and why (deterministic clinician_report fields only).
 */
export function PrimaryFindingAndWhy({
  report,
  omitIntroDuplicate = false,
  omitConfirmatoryInClarify = false,
  leadPatternLabel = null,
  showTechnicalDetail = false,
}: PrimaryFindingAndWhyProps) {
  if (!report) {
    return (
      <section aria-labelledby="primary-finding-why-heading" data-testid="primary-finding-and-why">
        <Card className="border-indigo-100 bg-white shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle id="primary-finding-why-heading" className="text-xl font-semibold text-gray-900">
              Primary finding and why
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-600">
              A structured clinician interpretation is not available for this result yet. Use system groups and biomarkers
              below, or Advanced analysis when present.
            </p>
          </CardContent>
        </Card>
      </section>
    );
  }

  const page1 = report?.sections?.page1;
  const rc = report?.sections?.root_cause;
  const hyp0 = rc?.hypotheses?.[0];
  const confirmatory = report?.sections?.confirmatory_tests ?? [];

  const lead = scrubConsumerRetailNarrative(buildSection3LeadStatement(page1) || '');
  let bodyB = scrubConsumerRetailNarrative(buildWhatThisMeansBlock(page1) || '');
  const hypSummary = scrubConsumerRetailNarrative((hyp0?.summary || '').trim());
  const hypRanking = scrubConsumerRetailNarrative((hyp0?.ranking_rationale || '').trim());

  const chains = (page1?.chains ?? []).map((c) => scrubConsumerRetailNarrative(c.trim())).filter(Boolean).slice(0, 2);

  const supports = (hyp0?.evidence_for ?? []).slice(0, 3);
  const against = (hyp0?.evidence_against ?? []).slice(0, 3);
  const gaps = (hyp0?.missing_data ?? []).slice(0, 2);
  const hypConfirmatory = (hyp0?.confirmatory_tests ?? []).slice(0, 2);
  const confirmatoryShort = confirmatory.slice(0, 2);
  const clarifyTestsRaw = confirmatoryShort.length > 0 ? confirmatoryShort : hypConfirmatory;
  const clarifyTests = omitConfirmatoryInClarify ? [] : clarifyTestsRaw;

  const hasRootNarrative = Boolean(hyp0);
  const showSupportsComplicates = hasRootNarrative && (supports.length > 0 || against.length > 0);

  if (!bodyB && hypSummary) {
    bodyB = hypSummary;
  }
  if (!bodyB && page1) {
    const kfOnly = (page1.key_findings?.[0] || '').trim();
    const noTopHyp = !(page1.top_hypothesis_line || '').trim();
    if (noTopHyp && kfOnly) {
      bodyB = scrubConsumerRetailNarrative(firstSentence(kfOnly));
    }
  }

  return (
    <section aria-labelledby="primary-finding-why-heading" data-testid="primary-finding-and-why">
      <Card className="border-indigo-100 bg-white shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle id="primary-finding-why-heading" className="text-xl font-semibold text-gray-900">
            Primary finding and why
          </CardTitle>
          {hyp0?.title ? (
            <p className="text-sm font-medium text-indigo-950 pt-1">
              {scrubConsumerRetailNarrative(
                neutraliseHypothesisTitleForDisplay(hyp0.title, hyp0.evidence_against)
              )}
            </p>
          ) : null}
          {leadPatternLabel && hyp0?.title && leadPatternLabel.trim().toLowerCase() !== hyp0.title.trim().toLowerCase() ? (
            <p className="text-sm text-slate-600 pt-1" data-testid="primary-finding-lead-pattern-bridge">
              Lead pattern on this panel:{' '}
              <span className="font-medium text-slate-800">{scrubConsumerRetailNarrative(leadPatternLabel)}</span>
              . The hypothesis below explains how that pattern is being interpreted from your markers.
            </p>
          ) : null}
        </CardHeader>
        <CardContent className="space-y-6 text-sm text-gray-800">
          {!omitIntroDuplicate ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">Lead finding</p>
              <p className="text-base text-gray-900 leading-relaxed">{lead}</p>
            </div>
          ) : null}

          {!omitIntroDuplicate && bodyB ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">What this means</p>
              <p className="leading-relaxed">{bodyB}</p>
            </div>
          ) : null}

          {(hypRanking && hasRootNarrative) || chains.length > 0 ? (
            showTechnicalDetail ? (
              <details className="rounded-md border border-slate-200 bg-slate-50/60 px-3 py-2">
                <summary className="text-sm font-medium text-slate-800 cursor-pointer select-none">
                  Technical ranking and evidence chains (optional detail)
                </summary>
                <div className="mt-4 space-y-4">
                  {hypRanking && hasRootNarrative ? (
                    <div className="rounded-md border border-indigo-100 bg-indigo-50/40 px-3 py-2">
                      <p className="text-xs font-semibold uppercase tracking-wide text-indigo-900 mb-1">
                        How this ranks on this panel
                      </p>
                      <p className="text-indigo-950 leading-relaxed">{hypRanking}</p>
                    </div>
                  ) : null}
                  {chains.length > 0 ? (
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">
                        How the evidence connects
                      </p>
                      <ul className="list-disc pl-5 space-y-2">
                        {chains.map((line, i) => (
                          <li key={i} className="leading-relaxed">
                            {line}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                </div>
              </details>
            ) : (
              <p className="text-sm text-slate-600 border border-dashed border-slate-200 rounded-md px-3 py-2 bg-slate-50/50">
                Technical ranking references and evidence-chain wording are hidden by default. Turn on{' '}
                <strong>Show technical detail</strong> above to review them when you need them.
              </p>
            )
          ) : null}

          {showSupportsComplicates && supports.length > 0 ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-green-900 mb-2">Supports this interpretation</p>
              <ul className="list-disc pl-5 space-y-1">
                {supports.map((ev, i) => (
                  <li key={`s-${i}`}>{evidenceLine(ev)}</li>
                ))}
              </ul>
            </div>
          ) : null}

          {showSupportsComplicates && against.length > 0 ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-amber-900 mb-2">
                Pulls against or complicates it
              </p>
              <ul className="list-disc pl-5 space-y-1">
                {against.map((ev, i) => (
                  <li key={`a-${i}`}>{evidenceLine(ev)}</li>
                ))}
              </ul>
            </div>
          ) : null}

          {gaps.length > 0 || clarifyTests.length > 0 ? (
            <div className="rounded-md border border-slate-200 bg-slate-50/80 px-3 py-3 space-y-2">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-600">What would clarify the picture</p>
              {gaps.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1">
                  {gaps.map((m, i) => (
                    <li key={`g-${i}`}>
                      <span className="font-medium">{formatMarkerRef(m.marker_id)}:</span> {m.reason}
                    </li>
                  ))}
                </ul>
              ) : null}
              {clarifyTests.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1">
                  {clarifyTests.map((t) => (
                    <li key={t.test_id}>
                      <span className="font-medium">{t.display_name}:</span> {t.rationale}
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
          ) : null}

          {!hasRootNarrative && !chains.length && !bodyB && page1 ? (
            <p className="text-sm text-slate-600 border border-dashed border-slate-200 rounded-md px-3 py-2">
              Deeper hypothesis detail is limited on this result — use the clinical interpretation notes and system
              groups below for the next level of context.
            </p>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}
