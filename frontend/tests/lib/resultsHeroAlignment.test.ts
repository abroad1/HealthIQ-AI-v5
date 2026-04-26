import {
  buildIdlLedHeroSummary,
  buildPrimaryHeroSummary,
  deriveSecondaryRankedSignalLine,
  normalizeHeroComparisonKey,
  pickHeroAlignedPrimaryDriver,
  pickSeverityPrimaryDriverCluster,
} from '@/lib/resultsPageLayout';
import type { Cluster, ClinicianReportV1, InterpretationDisplayRecordV1 } from '@/types/analysis';

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
    expect(line).toContain('Top ranked signal');
    expect(line).toContain('LDL');
  });

  it('pickHeroAlignedPrimaryDriver falls back to severity when no IDL alignment', () => {
    const clusters: Cluster[] = [
      {
        cluster_id: 'a',
        name: 'Unrelated name xyz',
        severity: 'high',
        biomarkers: ['m1'],
      },
      {
        cluster_id: 'b',
        name: 'Other',
        severity: 'moderate',
        biomarkers: ['m2', 'm3'],
      },
    ];
    const idl = idlRecord({ retail_display_label: 'Metabolic pattern alpha' });
    const d = pickHeroAlignedPrimaryDriver(clusters, idl);
    const sev = pickSeverityPrimaryDriverCluster(clusters);
    expect(d?.id).toBe(sev?.id);
  });

  it('pickHeroAlignedPrimaryDriver picks name-aligned cluster when score high enough', () => {
    const clusters: Cluster[] = [
      {
        cluster_id: 'weak',
        name: 'Zebra unrelated',
        severity: 'critical',
        biomarkers: ['z1'],
      },
      {
        cluster_id: 'aligned',
        name: 'Metabolic stress pattern detail',
        severity: 'moderate',
        biomarkers: ['glucose', 'insulin'],
      },
    ];
    const idl = idlRecord({ retail_display_label: 'Metabolic stress pattern' });
    const d = pickHeroAlignedPrimaryDriver(clusters, idl);
    expect(d?.id).toBe('aligned');
    expect(d?.biomarkers).toContain('glucose');
  });
});
