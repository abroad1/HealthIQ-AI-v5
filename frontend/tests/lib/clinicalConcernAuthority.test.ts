import {
  isCloseCallMode,
  shouldRenderWhyThisLeadWonSection,
} from '../../app/lib/leadUncertaintySection';
import type { ClinicianReportV1 } from '../../app/types/analysis';
import { getClinicalConcernSet, hasClinicalConcernAuthority } from '../../app/lib/clinicalConcernSet';
import type { AnalysisResult, ConsolidatedConcernSetV1 } from '../../app/types/analysis';

function baseReport(mode: ClinicianReportV1['sections']['page1']['primary_concern_mode']): ClinicianReportV1 {
  return {
    header: {
      report_version: 'v1',
      disclaimer_top: 'd',
      footer_line: 'f',
    },
    data_quality: {
      panel_completeness_present: 1,
      panel_completeness_expected: 1,
      lab_range_quality_by_primary_metric: [],
      confidence_caveat: '',
      data_quality_passed: true,
    },
    sections: {
      page1: {
        primary_concern: 'Lead',
        key_findings: ['kf'],
        chains: [],
        top_hypothesis_line: '',
        confidence_and_missing_data: '',
        primary_concern_mode: mode,
        runner_up_topic_line: 'Runner topic',
        runner_up_why_not_lead_line: 'Why not',
        co_primary_signal_ids: ['signal_a'],
      },
      root_cause: null,
      confirmatory_tests: [],
    },
    suppressed_confirmatory_tests: [],
  };
}

describe('clinical concern single-authority demotion', () => {
  it('treats technical_tiebreak_lead as close-call without concern authority', () => {
    expect(isCloseCallMode('technical_tiebreak_lead')).toBe(true);
  });

  it('demotes technical_tiebreak_lead when clinical concern authority is present', () => {
    expect(
      isCloseCallMode('technical_tiebreak_lead', { clinicalConcernAuthority: true })
    ).toBe(false);
  });

  it('suppresses why-lead-won tiebreak framing when concern set owns priority', () => {
    const report = baseReport('technical_tiebreak_lead');
    expect(shouldRenderWhyThisLeadWonSection(report)).toBe(true);
    // Without confidence/caveat, demoted authority yields no section
    expect(
      shouldRenderWhyThisLeadWonSection(report, { clinicalConcernAuthority: true })
    ).toBe(false);
    report.sections.page1.confidence_and_missing_data = 'Limited markers';
    expect(
      shouldRenderWhyThisLeadWonSection(report, { clinicalConcernAuthority: true })
    ).toBe(true);
  });

  it('reads clinical_concern_set from insight_graph meta', () => {
    const set: ConsolidatedConcernSetV1 = {
      findings: [
        {
          finding_id: 'hepatic:HEP-F1:abc',
          domain: 'hepatic',
          finding_type: 'HEP-F1',
          label: 'enzyme_elevation',
          constituent_activation_keys: ['signal_alt_high::activation'],
          urgency_time_band: 'within_days',
          concern_tier: 1,
          role: 'principal_concern',
        },
      ],
      lead_finding_ids: ['hepatic:HEP-F1:abc'],
      co_lead_finding_ids: [],
      presentation_mode: 'principal',
      no_forced_lead: false,
    };
    const analysis = {
      analysis_id: 'x',
      status: 'completed',
      meta: { insight_graph: { clinical_concern_set: set } },
    } as unknown as AnalysisResult;
    expect(getClinicalConcernSet(analysis)?.presentation_mode).toBe('principal');
    expect(hasClinicalConcernAuthority(analysis)).toBe(true);
    expect(hasClinicalConcernAuthority({} as AnalysisResult)).toBe(false);
  });
});
