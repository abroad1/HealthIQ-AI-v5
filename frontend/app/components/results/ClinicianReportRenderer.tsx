'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicianReportV1, PrimaryConcernModeV1 } from '@/types/analysis';
import { scrubConsumerRetailNarrative } from '@/lib/retailNarrativeSanitize';

interface ClinicianReportRendererProps {
  report: ClinicianReportV1 | null | undefined;
  /** BE-W2-RQ3 — same deterministic balanced-system copy as main results (optional) */
  balancedSystems?: {
    intro_line: string;
    items: Array<{ system_topic: string; evidence_line: string; capacity_note?: string }>;
    context_line: string;
  } | null;
  /** F-1 — `narrative_report_v1.clinician_synthesis` (advanced / clinician tab only) */
  deterministicClinicianSynthesis?: string | null;
  /** LC-S7 — when false, ranking policy version string stays out of default visual scan. */
  showTechnicalDetail?: boolean;
}

function formatSignalIdForDisplay(signalId: string): string {
  const stripped = signalId.replace(/^signal_/, '').replace(/_/g, ' ');
  return stripped.replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatConfidence(value: number | undefined): string {
  if (value === undefined || Number.isNaN(value)) return '—';
  return (Math.round(value * 100) / 100).toFixed(2);
}

function normalizeConcernMode(mode: PrimaryConcernModeV1 | undefined): PrimaryConcernModeV1 {
  return mode ?? 'distinct_lead';
}

function Page1RankingContext({
  page1,
  showTechnicalDetail,
}: {
  page1: ClinicianReportV1['sections']['page1'];
  showTechnicalDetail: boolean;
}) {
  const mode = normalizeConcernMode(page1.primary_concern_mode);
  const coIds = page1.co_primary_signal_ids ?? [];
  const policyVersion = (page1.ranking_policy_version ?? '').trim();
  const runnerTopic = (page1.runner_up_topic_line ?? '').trim();
  const runnerWhy = (page1.runner_up_why_not_lead_line ?? '').trim();
  const showRunnerUp =
    Boolean(runnerTopic) && (mode === 'technical_tiebreak_lead' || mode === 'near_tie_ambiguity');

  const showPolicyStamp = policyVersion.length > 0;

  return (
    <div className="space-y-2" data-testid="page1-ranking-context">
      {showRunnerUp && (
        <div
          className="rounded-md border border-blue-200/80 bg-blue-50/60 px-3 py-2 text-sm text-blue-950"
          data-testid="page1-runner-up-clinician"
        >
          <p className="font-medium">Competing ranked finding</p>
          <p className="mt-1 text-foreground/90">{runnerTopic}</p>
          {runnerWhy ? <p className="mt-1 text-foreground/90">{runnerWhy}</p> : null}
        </div>
      )}

      {mode === 'technical_tiebreak_lead' && (
        <div
          className="rounded-md border border-amber-200/80 bg-amber-50/60 px-3 py-2 text-sm text-amber-950"
          data-testid="primary-concern-mode-technical"
        >
          <p className="font-medium">Ordering note</p>
          <p className="mt-1 text-foreground/90">
            The lead concern follows the report&rsquo;s structured ranking policy. Where evidence-aligned
            steps did not fully separate similar items, a technical tie-break may have determined order. This
            is not by itself a statement of clinical priority among close alternatives.
          </p>
          {coIds.length > 0 && (
            <p className="mt-2">
              <span className="font-medium">Co-ranked patterns:</span>{' '}
              {coIds.map((id) => formatSignalIdForDisplay(id)).join(' · ')}
            </p>
          )}
        </div>
      )}

      {mode === 'near_tie_ambiguity' && (
        <div
          className="rounded-md border border-sky-200/80 bg-sky-50/60 px-3 py-2 text-sm text-sky-950"
          data-testid="primary-concern-mode-ambiguity"
        >
          <p className="font-medium">Ambiguity</p>
          <p className="mt-1 text-foreground/90">
            Multiple concerns are similarly supported on this panel. Ordering is policy-guided; interpret
            co-ranked items together with your clinician rather than as a single definitive lead diagnosis.
          </p>
          {coIds.length > 0 && (
            <p className="mt-2">
              <span className="font-medium">Co-ranked patterns:</span>{' '}
              {coIds.map((id) => formatSignalIdForDisplay(id)).join(' · ')}
            </p>
          )}
        </div>
      )}

      {mode === 'distinct_lead' && (
        <p className="sr-only" data-testid="primary-concern-mode-distinct">
          Primary concern mode: distinct lead.
        </p>
      )}

      {showPolicyStamp ? (
        <>
          <p className="text-xs text-muted-foreground">
            Ordering follows a structured ranking policy for this panel.
          </p>
          {showTechnicalDetail ? (
            <p className="text-xs text-gray-500 mt-1" data-testid="ranking-policy-version">
              Policy reference: {policyVersion}
            </p>
          ) : (
            <span className="sr-only" data-testid="ranking-policy-version-sr">
                Policy reference: {policyVersion}
              </span>
          )}
        </>
      ) : null}
    </div>
  );
}

export default function ClinicianReportRenderer({
  report,
  balancedSystems,
  deterministicClinicianSynthesis,
  showTechnicalDetail = false,
}: ClinicianReportRendererProps) {
  if (!report) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Clinician Summary Report</CardTitle>
          <CardDescription>This analysis does not include a clinician summary for this run.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const synthesis = scrubConsumerRetailNarrative((deterministicClinicianSynthesis ?? '').trim());

  const page1 = report.sections.page1;
  const rootCause = report.sections.root_cause;
  const confirmatoryTests = report.sections.confirmatory_tests || [];
  const suppressedTests = report.suppressed_confirmatory_tests || [];
  const quality = report.data_quality;
  const completeness = `${quality.panel_completeness_present}/${quality.panel_completeness_expected}`;

  return (
    <div className="space-y-6" data-testid="clinician-report-renderer">
      {synthesis ? (
        <Card className="border-violet-200 bg-violet-50/40">
          <CardHeader className="pb-2">
            <CardTitle className="text-base">Clinician synthesis (structured rules)</CardTitle>
            <CardDescription>
              Compiled from narrative assets attached to this report — not a live model output.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-violet-950 whitespace-pre-line leading-relaxed">{synthesis}</CardContent>
        </Card>
      ) : null}
      {balancedSystems && balancedSystems.items?.length ? (
        <Card className="border-emerald-100 bg-emerald-50/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-base">Balanced panel context (structured)</CardTitle>
            <CardDescription>{balancedSystems.intro_line}</CardDescription>
          </CardHeader>
          <CardContent className="text-sm space-y-2 text-emerald-950">
            <ul className="list-disc pl-5 space-y-1">
              {balancedSystems.items.map((it, i) => (
                <li key={i}>
                  <span className="font-medium">{it.system_topic}:</span> {it.evidence_line}
                  {it.capacity_note ? <span className="block text-xs text-muted-foreground mt-0.5">{it.capacity_note}</span> : null}
                </li>
              ))}
            </ul>
            {balancedSystems.context_line ? <p className="pt-1">{balancedSystems.context_line}</p> : null}
          </CardContent>
        </Card>
      ) : null}

      <Card>
        <CardHeader>
          <CardTitle>Clinician Summary Report</CardTitle>
          <CardDescription>{report.header.disclaimer_top}</CardDescription>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Data Quality</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p><strong>Panel completeness:</strong> {completeness}</p>
          <p><strong>Confidence caveat:</strong> {quality.confidence_caveat}</p>
          <p><strong>Quality status:</strong> {quality.data_quality_passed ? 'Passed' : 'Needs review'}</p>
          {quality.lab_range_quality_by_primary_metric.length > 0 && (
            <ul className="list-disc list-inside space-y-1">
              {quality.lab_range_quality_by_primary_metric.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Page 1 Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <Page1RankingContext page1={page1} showTechnicalDetail={showTechnicalDetail} />
          <p>
            <strong>Primary concern:</strong> {page1.primary_concern}
          </p>
          <div>
            <p className="font-semibold">Key findings</p>
            <ul className="list-disc list-inside space-y-1">
              {page1.key_findings.map((finding) => (
                <li key={finding}>{finding}</li>
              ))}
            </ul>
          </div>
          {page1.chains.length > 0 && (
            <div>
              <p className="font-semibold">Chains</p>
              <ul className="list-disc list-inside space-y-1">
                {page1.chains.map((chain) => (
                  <li key={chain}>{chain}</li>
                ))}
              </ul>
            </div>
          )}
          <p><strong>Top hypothesis:</strong> {page1.top_hypothesis_line}</p>
          <p><strong>Confidence and missing data:</strong> {page1.confidence_and_missing_data}</p>
        </CardContent>
      </Card>

      {rootCause && (
        <Card>
          <CardHeader>
            <CardTitle>Root Cause</CardTitle>
            <CardDescription>
              {formatSignalIdForDisplay(rootCause.signal_id)} ({rootCause.signal_state}) — confidence{' '}
              {formatConfidence(rootCause.signal_confidence)}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {rootCause.hypotheses.map((hypothesis) => (
              <div key={hypothesis.hypothesis_id} className="rounded border p-3 space-y-2">
                <p className="font-semibold">{hypothesis.title}</p>
                <p className="text-sm">{hypothesis.summary}</p>
                <p className="text-sm">
                  <strong>Confidence:</strong> {formatConfidence(hypothesis.hypothesis_confidence)}
                </p>
                <p className="text-sm"><strong>Rationale:</strong> {hypothesis.ranking_rationale}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Confirmatory Tests</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          {confirmatoryTests.length > 0 ? (
            <ul className="list-disc list-inside space-y-1">
              {confirmatoryTests.map((test) => (
                <li key={test.test_id}>
                  <span className="font-medium">{test.display_name}:</span> {test.rationale}
                </li>
              ))}
            </ul>
          ) : (
            <p>No confirmatory tests were provided for this report.</p>
          )}
          {suppressedTests.length > 0 && (
            <p className="text-xs text-gray-600">
              Suppressed confirmatory test IDs: {suppressedTests.join(', ')}
            </p>
          )}
        </CardContent>
      </Card>

      <p className="text-xs text-gray-500">{report.header.footer_line}</p>
    </div>
  );
}
