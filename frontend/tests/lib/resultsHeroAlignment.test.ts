import {
  buildIdlLedHeroSummary,
  buildPrimaryHeroSummary,
  deriveSecondaryRankedSignalLine,
  normalizeHeroComparisonKey,
  resolveHeroPrimaryStory,
  selectGovernedPrimaryDriver,
} from '@/lib/resultsPageLayout';
import type {
  Cluster,
  ClinicianReportV1,
  InterpretationDisplayRecordV1,
  PrimaryDriverAuthorityV1,
} from '@/types/analysis';

function driverAuthority(partial: Partial<PrimaryDriverAuthorityV1>): PrimaryDriverAuthorityV1 {
  return {
    schema: 'primary_driver_authority_v1',
    authority_source: 'report_v1.top_findings',
    ranking_policy_version: 'v1',
    priority_rank: 1,
    signal_id: 'signal_mcv_high',
    activation_key: '',
    source_spec_id: '',
    primary_metric: 'mcv',
    system: 'haematological',
    cluster_id: '',
    cluster_name: '',
    cluster_resolved: false,
    biomarker_keys: [],
    ...partial,
  };
}

function idlRecord(partial: Partial<InterpretationDisplayRecordV1>): InterpretationDisplayRecordV1 {
  return {
    internal_id: 'x',
    scientific_class: 'phenotype',
    clinical_display_label: 'Clinical',
    retail_display_label: 'Retail pattern',
    subtitle: '',
    why_it_matters: '',
    severity_state: 'attention',
    supporting_biomarkers_summary: '',
    frontend_allowed_term: 'phenotype_allowed',
    display_order_priority: 0,
    enabled_for_frontend: true,
    ...partial,
  };
}

describe('results hero alignment', () => {
  it('normalizeHeroComparisonKey strips noise', () => {
    expect(normalizeHeroComparisonKey('Hello, World!')).toBe('hello world');
  });

  it('buildIdlLedHeroSummary composes from IDL fields', () => {
    const s = buildIdlLedHeroSummary(
      idlRecord({
        why_it_matters: 'This pattern matters for energy. More detail.',
        subtitle: 'A short subtitle.',
      })
    );
    expect(s).toContain('This pattern matters for energy');
    expect(s.length).toBeGreaterThan(10);
  });

  it('buildPrimaryHeroSummary prefers IDL body over narrative when IDL present', () => {
    const idl = idlRecord({
      why_it_matters: 'IDL explains the retail pattern clearly.',
    });
    const summary = buildPrimaryHeroSummary(
      'Narrative retail talks about something completely different and should not win.',
      null,
      idl
    );
    expect(summary).toContain('IDL explains');
    expect(summary).not.toContain('Narrative retail');
  });

  it('buildPrimaryHeroSummary uses narrative when no IDL', () => {
    const summary = buildPrimaryHeroSummary('Retail line one. Retail line two.', null, null);
    expect(summary).toContain('Retail line one');
  });

  it('deriveSecondaryRankedSignalLine adds line when concern differs from hero title', () => {
    const report: ClinicianReportV1 = {
      header: {
        report_version: 'v1',
        disclaimer_top: '',
        footer_line: '',
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
          primary_concern: 'LDL cholesterol is the dominant signal on this panel.',
          key_findings: [],
          chains: [],
          top_hypothesis_line: '',
          confidence_and_missing_data: '',
        },
        root_cause: null,
        confirmatory_tests: [],
      },
      suppressed_confirmatory_tests: [],
    };
    const idl = idlRecord({ retail_display_label: 'Metabolic stress pattern' });
    const line = deriveSecondaryRankedSignalLine(report, 'Metabolic stress pattern', idl);
    expect(line).toContain('Leading pattern described');
    expect(line).toContain('LDL');
  });

  it('resolveHeroPrimaryStory swaps hero title when ranked lead differs from IDL label', () => {
    const report: ClinicianReportV1 = {
      header: {
        report_version: 'v1',
        disclaimer_top: '',
        footer_line: '',
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
          primary_concern: 'LDL cholesterol is the dominant signal on this panel.',
          key_findings: [],
          chains: [],
          top_hypothesis_line: '',
          confidence_and_missing_data: '',
        },
        root_cause: null,
        confirmatory_tests: [],
      },
      suppressed_confirmatory_tests: [],
    };
    const idl = idlRecord({ retail_display_label: 'Metabolic stress pattern' });
    const pack = resolveHeroPrimaryStory(report, 'Metabolic stress pattern', idl);
    expect(pack.heroTitle).toContain('LDL');
    expect(pack.systemContextLine).toContain('Broader system context');
    expect(pack.bridgeExplanation).toBeNull();
  });

  // ARCH-CONV-CORRECT-1 — the primary driver is a Layer B ranking decision. Layer C resolves
  // the governed record to a cluster and otherwise renders nothing.
  const driverClusters: Cluster[] = [
    {
      cluster_id: 'weak',
      name: 'Zebra unrelated',
      severity: 'critical',
      biomarkers: ['z1'],
    },
    {
      cluster_id: 'governed',
      name: 'Macrocytic pattern',
      severity: 'moderate',
      biomarkers: ['mcv', 'homocysteine'],
    },
  ];

  it('selectGovernedPrimaryDriver renders the cluster named by Layer B', () => {
    const d = selectGovernedPrimaryDriver(
      driverClusters,
      driverAuthority({ cluster_id: 'governed', cluster_resolved: true, biomarker_keys: ['mcv'] })
    );
    expect(d?.id).toBe('governed');
    expect(d?.biomarkers).toEqual(['mcv']);
  });

  it('selectGovernedPrimaryDriver ignores severity and never substitutes a fallback', () => {
    expect(selectGovernedPrimaryDriver(driverClusters, driverAuthority({}))).toBeNull();
    expect(selectGovernedPrimaryDriver(driverClusters, null)).toBeNull();
    expect(
      selectGovernedPrimaryDriver(driverClusters, driverAuthority({ cluster_id: 'not-on-this-page' }))
    ).toBeNull();
  });
});
