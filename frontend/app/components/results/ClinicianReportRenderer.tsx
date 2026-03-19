'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicianReportV1 } from '@/types/analysis';

interface ClinicianReportRendererProps {
  report: ClinicianReportV1 | null | undefined;
}

export default function ClinicianReportRenderer({ report }: ClinicianReportRendererProps) {
  if (!report) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Clinician Summary Report</CardTitle>
          <CardDescription>This analysis does not include a clinician report payload.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const page1 = report.sections.page1;
  const rootCause = report.sections.root_cause;
  const confirmatoryTests = report.sections.confirmatory_tests || [];
  const suppressedTests = report.suppressed_confirmatory_tests || [];
  const quality = report.data_quality;
  const completeness = `${quality.panel_completeness_present}/${quality.panel_completeness_expected}`;

  return (
    <div className="space-y-6" data-testid="clinician-report-renderer">
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
          <p><strong>Primary concern:</strong> {page1.primary_concern}</p>
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
              {rootCause.signal_id} ({rootCause.signal_state}) - confidence {rootCause.signal_confidence}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {rootCause.hypotheses.map((hypothesis) => (
              <div key={hypothesis.hypothesis_id} className="rounded border p-3 space-y-2">
                <p className="font-semibold">{hypothesis.title}</p>
                <p className="text-sm">{hypothesis.summary}</p>
                <p className="text-sm"><strong>Confidence:</strong> {hypothesis.hypothesis_confidence}</p>
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
