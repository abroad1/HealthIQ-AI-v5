import React from 'react';
import { render, screen } from '@testing-library/react';
import { ClinicalConcernPrioritySection } from '../../app/components/results/ClinicalConcernPrioritySection';
import type { ConsolidatedConcernSetV1 } from '../../app/types/analysis';
import ClinicianReportRenderer from '../../app/components/results/ClinicianReportRenderer';
import type { ClinicianReportV1 } from '../../app/types/analysis';

const concernSet: ConsolidatedConcernSetV1 = {
  findings: [
    {
      finding_id: 'renal:RE-F3:aaa',
      domain: 'renal_electrolyte',
      finding_type: 'RE-F3',
      label: 'hyperkalaemia',
      constituent_activation_keys: ['signal_potassium_high::activation'],
      urgency_time_band: 'same_day',
      concern_tier: 0,
      role: 'co_lead',
    },
    {
      finding_id: 'hepatic:HEP-F1:bbb',
      domain: 'hepatic',
      finding_type: 'HEP-F1',
      label: 'enzyme_elevation',
      constituent_activation_keys: ['signal_alt_high::activation'],
      urgency_time_band: 'same_day',
      concern_tier: 0,
      role: 'co_lead',
    },
  ],
  lead_finding_ids: [],
  co_lead_finding_ids: ['renal:RE-F3:aaa', 'hepatic:HEP-F1:bbb'],
  presentation_mode: 'co_lead',
  no_forced_lead: false,
};

describe('ClinicalConcernPrioritySection', () => {
  it('renders same-day co-equal group without manufacturing a solo lead', () => {
    render(<ClinicalConcernPrioritySection concernSet={concernSet} />);
    expect(screen.getByTestId('clinical-concern-priority-section')).toBeInTheDocument();
    expect(screen.getByTestId('clinical-concern-co-leads')).toBeInTheDocument();
    expect(screen.queryByTestId('clinical-concern-leads')).not.toBeInTheDocument();
    expect(screen.getByText(/Same-day co-equal group|Co-leads/i)).toBeInTheDocument();
  });
});

describe('ClinicianReportRenderer technical_tiebreak demotion', () => {
  const report: ClinicianReportV1 = {
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
        primary_concern: 'Homocysteine elevated',
        key_findings: ['kf'],
        chains: [],
        top_hypothesis_line: 'hyp',
        confidence_and_missing_data: 'conf',
        primary_concern_mode: 'technical_tiebreak_lead',
        runner_up_topic_line: 'Runner',
        runner_up_why_not_lead_line: 'Why',
        co_primary_signal_ids: ['signal_a'],
        ranking_policy_version: 'v-test',
      },
      root_cause: null,
      confirmatory_tests: [],
    },
    suppressed_confirmatory_tests: [],
  };

  it('hides competing ranked finding when clinical concern authority is present', () => {
    render(
      <ClinicianReportRenderer report={report} clinicalConcernAuthority showTechnicalDetail={false} />
    );
    expect(screen.queryByTestId('page1-runner-up-clinician')).not.toBeInTheDocument();
    // Technical note only when showTechnicalDetail under authority
    expect(screen.queryByTestId('primary-concern-mode-technical')).not.toBeInTheDocument();
  });
});
