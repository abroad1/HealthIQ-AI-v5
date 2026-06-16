import { neutraliseHypothesisTitleForDisplay } from '@/lib/hypothesisDisplayCopy';
import {
  formatConsumerDriverBandStatusLabel,
  resolveHeroPrimaryStory,
} from '@/lib/resultsPageLayout';
import { scrubConsumerRetailNarrative } from '@/lib/retailNarrativeSanitize';
import type { BiomarkerResult, ClinicianReportV1, InterpretationDisplayRecordV1 } from '@/types/analysis';
import fs from 'node:fs';
import path from 'node:path';

function idlRecord(partial: Partial<InterpretationDisplayRecordV1>): InterpretationDisplayRecordV1 {
  return {
    internal_id: 'x',
    scientific_class: 'phenotype',
    clinical_display_label: 'Clinical',
    retail_display_label: 'Vascular Inflammation Risk',
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

describe('IUAT results trust hardening', () => {
  it('IUAT-001 neutralises B12-associated title when B12 counter-evidence present', () => {
    const title = neutraliseHypothesisTitleForDisplay('B12-associated pattern', [
      {
        item: 'B12 appears clearly within range, which makes a B12-driven pattern less likely on this panel alone.',
      },
    ]);
    expect(title).toBe('Homocysteine-related pattern');
    expect(title).not.toMatch(/B12-associated/i);
  });

  it('IUAT-002 body overview copy does not claim unavailable when clusters exist', () => {
    const src = fs.readFileSync(
      path.join(process.cwd(), 'app/components/results/ResultsBodyOverview.tsx'),
      'utf8'
    );
    expect(src).toContain('Detailed pattern groups are hidden in this view');
    expect(src).toContain(') : hasBuckets ? (');
  });

  it('IUAT-003 distinguishes uploaded markers from key headline markers', () => {
    const pageSrc = fs.readFileSync(path.join(process.cwd(), 'app/(app)/results/page.tsx'), 'utf8');
    const pipelineSrc = fs.readFileSync(
      path.join(process.cwd(), 'app/components/pipeline/PipelineStatus.tsx'),
      'utf8'
    );
    expect(pageSrc).toContain('uploaded markers');
    expect(pipelineSrc).toContain('key markers available for this headline interpretation');
  });

  it('IUAT-004 scrubs markdown, internal system names, and analytical model phrasing', () => {
    const raw =
      'Your main finding sits in a **Cardiovascular 4 Biomarkers** context. ' +
      'This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel.';
    const out = scrubConsumerRetailNarrative(raw);
    expect(out).not.toContain('**');
    expect(out).not.toMatch(/Cardiovascular 4 Biomarkers/i);
    expect(out).not.toMatch(/analytical model/i);
    expect(out).toContain('cardiovascular markers on this panel');
  });

  it('IUAT-005 hero hierarchy separates lead finding from broader system context', () => {
    const report: ClinicianReportV1 = {
      header: { report_version: 'v1', disclaimer_top: '', footer_line: '' },
      data_quality: {
        panel_completeness_present: 9,
        panel_completeness_expected: 9,
        lab_range_quality_by_primary_metric: [],
        confidence_caveat: '',
        data_quality_passed: true,
      },
      sections: {
        page1: {
          primary_concern: 'Raised homocysteine pattern warrants attention on this panel.',
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
    const idl = idlRecord({ retail_display_label: 'Vascular Inflammation Risk' });
    const pack = resolveHeroPrimaryStory(report, 'Vascular Inflammation Risk', idl);
    expect(pack.heroTitle.toLowerCase()).toContain('homocysteine');
    expect(pack.systemContextLine).toMatch(/Broader system context:/i);
    expect(pack.systemContextLine).toContain('Vascular Inflammation Risk');
  });

  it('IUAT-006 driver band avoids Critical for below-range transferrin with backend interpretation', () => {
    const transferrin: BiomarkerResult = {
      biomarker_name: 'transferrin',
      value: 2.0,
      unit: 'g/L',
      score: 40,
      status: 'critical',
      interpretation: 'Transferrin is below the lab reference range on this panel.',
      reference_range: { min: 2.15, max: 3.65 },
    };
    expect(formatConsumerDriverBandStatusLabel(transferrin)).toBe('Below range');
    expect(formatConsumerDriverBandStatusLabel(transferrin)).not.toBe('Critical');
  });
});
