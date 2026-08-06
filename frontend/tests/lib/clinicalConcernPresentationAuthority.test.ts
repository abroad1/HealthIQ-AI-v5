import {
  broaderContextLineFromLegacyLabel,
  narrativeConflictsWithConcernLead,
  resolveAuthoritativeBodyOverview,
  resolveAuthoritativeHeroSummary,
  resolveAuthoritativeLeadNarrative,
  resolveClinicalPresentationAuthority,
} from '../../app/lib/clinicalConcernPresentationAuthority';
import type {
  AnalysisResult,
  ClinicalFindingV1,
  ConsolidatedConcernSetV1,
} from '../../app/types/analysis';

function hepaticLeadFinding(overrides: Partial<ClinicalFindingV1> = {}): ClinicalFindingV1 {
  return {
    finding_id: 'hepatic:HEP-F1:consolidated',
    domain: 'hepatic',
    finding_type: 'HEP-F1',
    label: 'consolidated_hepatocellular_enzyme_elevation',
    constituent_activation_keys: ['signal_alt_high::activation'],
    constituent_biomarker_ids: ['alt'],
    urgency_time_band: 'within_days',
    severity_band: 'marked',
    concern_tier: 1,
    role: 'principal_concern',
    nested_constituent_labels: ['mcv_mild_macrocytosis'],
    ...overrides,
  };
}

function altUatConcernSet(
  overrides: Partial<ConsolidatedConcernSetV1> = {}
): ConsolidatedConcernSetV1 {
  const hepatic = hepaticLeadFinding();
  return {
    contract_version: 'clinical_concern_set_v1',
    findings: [
      hepatic,
      {
        finding_id: 'cbc:mcv_mild:1',
        domain: 'cbc',
        finding_type: 'MCV-mild',
        label: 'mcv_mild_macrocytosis',
        constituent_activation_keys: ['signal_mcv_high::activation'],
        constituent_biomarker_ids: ['mcv'],
        urgency_time_band: 'within_weeks',
        severity_band: 'mild',
        concern_tier: 3,
        role: 'contextual',
      },
    ],
    lead_finding_ids: [hepatic.finding_id],
    co_lead_finding_ids: [],
    presentation_mode: 'principal',
    no_forced_lead: false,
    ...overrides,
  };
}

/** Legacy conflicting ranking payload — not typed on AnalysisResult; stored for documentation in tests. */
const CONFLICTING_TOP_FINDINGS = [
  {
    signal_id: 'signal_mcv_high',
    title: 'MCV elevated',
    confidence: 0.9,
    supporting_marker_count: 3,
  },
  {
    signal_id: 'signal_alt_high',
    title: 'ALT elevated',
    confidence: 0.8,
    supporting_marker_count: 1,
  },
];

function analysisWithConcern(
  concernSet: ConsolidatedConcernSetV1 | null,
  extras: Partial<AnalysisResult> = {}
): AnalysisResult {
  return {
    analysis_id: '1ce310e1-0467-4482-a2f6-56c412329c2e',
    status: 'completed',
    created_at: '2026-01-01T00:00:00Z',
    completed_at: '2026-01-01T00:00:00Z',
    biomarkers: [],
    clusters: [],
    insights: [],
    overall_score: null,
    meta: concernSet
      ? {
          insight_graph: {
            clinical_concern_set: concernSet,
          },
          // Document conflicting legacy ranking — presentation authority must ignore it
          report_v1_top_findings_fixture: CONFLICTING_TOP_FINDINGS,
        }
      : {
          report_v1_top_findings_fixture: CONFLICTING_TOP_FINDINGS,
        },
    narrative_report_v1: {
      retail_summary:
        'Your results centre on a high MCV reading as the main pattern to discuss first.',
      body_overview:
        'Your results highlight mcv high as the main pattern to discuss first. Mild enzyme changes are also present.',
      lead_narrative: 'MCV high is the main pattern to discuss first on this panel.',
      secondary_narratives: '',
      longitudinal_narrative: '',
      secondary_systems: '',
      next_steps_narrative: '',
      clinician_synthesis: '',
    },
    ...extras,
  };
}

describe('clinicalConcernPresentationAuthority', () => {
  it('uses concern-set hepatic lead over conflicting report_v1.top_findings (ALT 250 / mild MCV)', () => {
    const analysis = analysisWithConcern(altUatConcernSet());
    const authority = resolveClinicalPresentationAuthority(analysis);

    expect(authority.source).toBe('clinical_concern_set');
    expect(authority.primaryTitle).toBe('Consolidated hepatocellular enzyme elevation');
    expect(authority.urgencyPhrase).toBe('within days');
    expect(authority.discussFirstSentence).toMatch(/consolidated hepatocellular enzyme elevation/i);
    expect(authority.discussFirstSentence).toMatch(/within days/i);
    expect(authority.discussFirstSentence).not.toMatch(/\bmcv\b/i);

    const top = (
      analysis.meta as { report_v1_top_findings_fixture?: { title: string; confidence: number }[] }
    )?.report_v1_top_findings_fixture?.[0];
    expect(top?.title).toMatch(/MCV/i);
    expect(top?.confidence).toBeGreaterThan(0.8);
    expect(authority.primaryTitle).not.toMatch(/MCV/i);
  });

  it('overrides conflicting narrative main-pattern / discuss-first language', () => {
    const analysis = analysisWithConcern(altUatConcernSet());
    const authority = resolveClinicalPresentationAuthority(analysis);
    const conflicting =
      'Your results highlight mcv high as the main pattern to discuss first. Mild enzyme changes are also present.';

    expect(narrativeConflictsWithConcernLead(conflicting, authority)).toBe(true);

    const body = resolveAuthoritativeBodyOverview(
      authority,
      conflicting,
      'legacy clinician primary'
    );
    expect(body).toMatch(/consolidated hepatocellular enzyme elevation/i);
    expect(body.toLowerCase()).not.toContain('mcv high as the main pattern');

    const hero = resolveAuthoritativeHeroSummary(authority, 'IDL vascular inflammation summary');
    expect(hero).toMatch(/consolidated hepatocellular enzyme elevation/i);
    expect(hero).not.toMatch(/vascular inflammation/i);

    const lead = resolveAuthoritativeLeadNarrative(
      authority,
      'MCV high is the main pattern to discuss first on this panel.'
    );
    expect(lead).toMatch(/consolidated hepatocellular enzyme elevation/i);
    expect(lead).not.toMatch(/MCV high is the main pattern/i);
  });

  it('keeps IDL / cluster-driver framing subordinate to hepatic lead', () => {
    const analysis = analysisWithConcern(altUatConcernSet());
    const authority = resolveClinicalPresentationAuthority(analysis);
    const line = broaderContextLineFromLegacyLabel(authority, 'Vascular Inflammation Risk');

    expect(line).toBe('Broader pattern context: Vascular Inflammation Risk');
    expect(authority.primaryTitle).not.toMatch(/Vascular/i);
    expect(authority.discussFirstSentence).not.toMatch(/discuss.*Vascular/i);
  });

  it('retains MCV as contextual nested detail without promoting it to lead', () => {
    const set = altUatConcernSet();
    const analysis = analysisWithConcern(set);
    const authority = resolveClinicalPresentationAuthority(analysis);

    expect(authority.leadFindings[0]?.label).toBe(
      'consolidated_hepatocellular_enzyme_elevation'
    );
    const nested = authority.leadFindings[0]?.nested_constituent_labels || [];
    expect(nested.some((l) => /mcv/i.test(l))).toBe(true);
    expect(authority.primaryTitle).not.toMatch(/mcv/i);
  });

  it('falls back to legacy when concern set is absent', () => {
    const analysis = analysisWithConcern(null);
    const authority = resolveClinicalPresentationAuthority(analysis);
    expect(authority.source).toBe('legacy');
    expect(authority.primaryTitle).toBeNull();

    const hero = resolveAuthoritativeHeroSummary(authority, 'Legacy MCV retail summary');
    expect(hero).toBe('Legacy MCV retail summary');

    const body = resolveAuthoritativeBodyOverview(
      authority,
      'Compiled MCV body overview',
      'Clinician primary'
    );
    expect(body).toBe('Compiled MCV body overview');
  });

  it('falls back to legacy when concern set is empty (no authority)', () => {
    const malformed: ConsolidatedConcernSetV1 = {
      findings: [],
      lead_finding_ids: ['missing'],
      co_lead_finding_ids: [],
      presentation_mode: 'principal',
      no_forced_lead: false,
    };
    const analysis = analysisWithConcern(malformed);
    const authority = resolveClinicalPresentationAuthority(analysis);
    expect(authority.source).toBe('legacy');
  });

  it('preserves co-lead presentation without manufacturing a solo lead', () => {
    const set = altUatConcernSet({
      lead_finding_ids: [],
      co_lead_finding_ids: ['hepatic:HEP-F1:consolidated', 'cbc:mcv_mild:1'],
      presentation_mode: 'co_lead',
      no_forced_lead: false,
    });
    const authority = resolveClinicalPresentationAuthority(analysisWithConcern(set));
    expect(authority.source).toBe('clinical_concern_set');
    expect(authority.presentationMode).toBe('co_lead');
    expect(authority.primaryTitle).toMatch(/Consolidated hepatocellular/i);
    expect(authority.primaryTitle).toMatch(/mcv mild macrocytosis/i);
    expect(authority.discussFirstSentence).toMatch(/More than one finding shares lead priority/i);
  });

  it('preserves no-forced-lead without inventing a lead', () => {
    const set = altUatConcernSet({
      presentation_mode: 'no_forced_lead',
      no_forced_lead: true,
      lead_finding_ids: ['hepatic:HEP-F1:consolidated'],
      co_lead_finding_ids: ['cbc:mcv_mild:1'],
    });
    const authority = resolveClinicalPresentationAuthority(analysisWithConcern(set));
    expect(authority.noForcedLead).toBe(true);
    expect(authority.discussFirstSentence).toMatch(/no single lead is forced/i);
  });

  it('does not derive priority from confidence or supporting-marker count', () => {
    const source = resolveClinicalPresentationAuthority.toString();
    expect(source).not.toMatch(/confidence/);
    expect(source).not.toMatch(/supporting_marker/);
    expect(source).not.toMatch(/top_findings/);

    const analysis = analysisWithConcern(altUatConcernSet());
    const authority = resolveClinicalPresentationAuthority(analysis);
    expect(authority.primaryTitle).toBe('Consolidated hepatocellular enzyme elevation');
  });
});
