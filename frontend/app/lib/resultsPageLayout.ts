import type {
  BiomarkerResult,
  Cluster,
  ClinicianReportV1,
  InterpretationDisplayLayerBundleV1,
  InterpretationDisplayRecordV1,
} from '@/types/analysis';
import { buildBodyOverviewPrimarySentence, extractFirstSentence } from '@/lib/bodyOverviewPrimarySentence';
import { buildSection3LeadStatement, buildWhatThisMeansBlock, firstSentence } from '@/lib/primaryFindingShaping';

export function takeUpToNSentences(text: string, maxSentences: number): string {
  const t = text.trim();
  if (!t) return '';
  const out: string[] = [];
  let rest = t;
  for (let i = 0; i < maxSentences && rest; i += 1) {
    const m = rest.match(/^(.+?[.!?])(\s+|$)/);
    if (m) {
      out.push(m[1].trim());
      rest = rest.slice(m[0].length).trim();
    } else {
      out.push(rest.trim());
      break;
    }
  }
  return out.join(' ');
}

function formatImlSeverity(sev: InterpretationDisplayRecordV1['severity_state']): string {
  return sev
    .split('_')
    .map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w))
    .join(' ');
}

function clusterSeverityLabel(sev: string | null | undefined): string {
  const x = (sev || 'moderate').toLowerCase();
  if (x === 'critical') return 'Critical attention';
  if (x === 'high') return 'High priority';
  if (x === 'moderate' || x === 'medium') return 'Moderate signal';
  if (x === 'mild' || x === 'low' || x === 'normal') return 'Lower concern';
  return 'Review in context';
}

export function resolvePrimaryFindingSeverity(
  firstIdl: InterpretationDisplayRecordV1 | null | undefined,
  primaryCluster: Cluster | null | undefined
): { label: string; tone: 'rose' | 'amber' | 'slate' | 'emerald' } {
  if (firstIdl) {
    const s = firstIdl.severity_state;
    const label = formatImlSeverity(s);
    if (s === 'strong_signal') return { label, tone: 'rose' };
    if (s === 'attention') return { label, tone: 'amber' };
    if (s === 'watch') return { label, tone: 'slate' };
    return { label, tone: 'emerald' };
  }
  if (primaryCluster) {
    return { label: clusterSeverityLabel(primaryCluster.severity), tone: 'amber' };
  }
  return { label: 'Summary', tone: 'slate' };
}

export function pickPhenotypeLabel(
  clinicianReport: ClinicianReportV1 | null | undefined,
  firstIdl: InterpretationDisplayRecordV1 | null | undefined,
  primaryDriver: { name: string } | null
): string {
  const p1 = clinicianReport?.sections?.page1;
  const idl = firstIdl?.retail_display_label?.trim();
  if (idl) return idl;
  const hypTitle = clinicianReport?.sections?.root_cause?.hypotheses?.[0]?.title?.trim();
  if (hypTitle) return hypTitle;
  if (primaryDriver?.name?.trim()) return primaryDriver.name.trim();
  const concern = p1?.primary_concern?.trim();
  if (concern) return extractFirstSentence(concern);
  const kf0 = p1?.key_findings?.[0]?.trim();
  if (kf0) return extractFirstSentence(kf0);
  return 'Your analysis summary';
}

export function buildPrimaryHeroSummary(
  narrativeRetail: string | null | undefined,
  clinicianReport: ClinicianReportV1 | null | undefined
): string {
  const retail = (narrativeRetail ?? '').trim();
  if (retail) {
    return takeUpToNSentences(retail, 3);
  }
  if (!clinicianReport) {
    return "We've organised the clearest interpretation available from your report fields below.";
  }
  const page1 = clinicianReport.sections?.page1;
  const wtm = buildWhatThisMeansBlock(page1);
  const lead = buildSection3LeadStatement(page1);
  if (wtm && lead) {
    const combined = firstSentence(lead) === firstSentence(wtm) ? wtm : `${wtm} ${firstSentence(lead)}`;
    return takeUpToNSentences(combined, 3);
  }
  if (wtm) return takeUpToNSentences(wtm, 3);
  if (lead) return takeUpToNSentences(lead, 3);
  return buildBodyOverviewPrimarySentence(page1);
}

export function pickTopDriverBiomarkers(
  biomarkers: BiomarkerResult[],
  primaryDriver: { biomarkers: string[] } | null
): BiomarkerResult[] {
  const withValues = biomarkers.filter((b) => b.biomarker_name && b.value != null && typeof b.value === 'number');
  const byName = new Map(withValues.map((b) => [b.biomarker_name, b]));
  const out: BiomarkerResult[] = [];
  for (const name of primaryDriver?.biomarkers ?? []) {
    const b = byName.get(name);
    if (b) out.push(b);
    if (out.length >= 3) return out;
  }
  const rank = (b: BiomarkerResult) => {
    const s = (b.status || '').toLowerCase();
    if (s.includes('high') || s.includes('low') || s.includes('critical') || s.includes('abnormal')) return 4;
    if (s.includes('border') || s.includes('watch')) return 3;
    if (s.includes('optimal') || s.includes('normal')) return 0;
    return 1;
  };
  const rest = withValues
    .filter((b) => !out.find((o) => o.biomarker_name === b.biomarker_name))
    .sort((a, b) => rank(b) - rank(a));
  for (const b of rest) {
    out.push(b);
    if (out.length >= 3) break;
  }
  return out.slice(0, 3);
}

function humanizeStatus(status: string | null | undefined): string {
  if (!status) return '—';
  return status
    .split(/[_\s]+/)
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(' ');
}

export function oneLineMarkerInterpretation(b: BiomarkerResult): string {
  const direct = b.interpretation?.trim();
  if (direct) return firstSentence(direct);
  const ex = b.biomarker_educational_explainer?.body?.trim();
  if (ex) return firstSentence(ex);
  return `Value sits in the ${humanizeStatus(b.status)} range for this marker on your panel.`;
}

export { humanizeStatus };

export interface ResultActionCardModel {
  heading: string;
  paragraph: string;
  sourceLabel: string;
  categoryLabel: string;
  /** Plain label derived from cluster severity — not a new clinical claim. */
  evidenceLevelLabel: string;
}

function categoryFromCluster(c: Cluster | undefined): string {
  const raw = (c?.category || '').toLowerCase();
  if (raw.includes('lifestyle') || raw.includes('diet')) return 'Lifestyle';
  if (raw.includes('supp')) return 'Supplement';
  if (raw.includes('medical') || raw.includes('referral')) return 'Medical follow-up';
  if (raw.includes('lab') || raw.includes('test')) return 'Testing';
  if (c?.name) return 'System pattern';
  return 'Follow-up';
}

function evidenceLevelFromCluster(c: Cluster | undefined): string {
  const x = (c?.severity || 'moderate').toLowerCase();
  if (x === 'critical' || x === 'high') return 'Stronger pattern on this panel';
  if (x === 'mild' || x === 'low' || x === 'normal') return 'Supporting / lower-priority note';
  return 'Moderate attention on this panel';
}

/** Flattens cluster recommendations and top-level result recommendations; deterministic ordering only. */
export function buildActionCardModels(
  clusters: Cluster[],
  topLevelRecs: string[] | null | undefined
): ResultActionCardModel[] {
  const out: ResultActionCardModel[] = [];
  for (const c of clusters) {
    const name = c.name?.trim() || 'System group';
    for (const r of c.recommendations || []) {
      const paragraph = (r || '').trim();
      if (!paragraph) continue;
      const head = firstSentence(paragraph);
      out.push({
        heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
        paragraph,
        sourceLabel: name,
        categoryLabel: categoryFromCluster(c),
        evidenceLevelLabel: evidenceLevelFromCluster(c),
      });
      if (out.length >= 5) return out;
    }
  }
  for (const r of topLevelRecs || []) {
    const paragraph = (r || '').trim();
    if (!paragraph) continue;
    const head = firstSentence(paragraph);
    out.push({
      heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
      paragraph,
      sourceLabel: 'Panel summary',
      categoryLabel: 'Follow-up',
      evidenceLevelLabel: 'Panel-level note',
    });
    if (out.length >= 5) return out;
  }
  return out;
}

function selectVisibleIdlRecordsLocal(
  bundle: InterpretationDisplayLayerBundleV1 | null | undefined
): InterpretationDisplayRecordV1[] {
  if (!bundle?.records?.length) return [];
  return [...bundle.records]
    .filter((r) => r.enabled_for_frontend === true)
    .sort((a, b) => a.display_order_priority - b.display_order_priority);
}

export function getFirstIdlRecord(
  bundle: InterpretationDisplayLayerBundleV1 | null | undefined
): InterpretationDisplayRecordV1 | null {
  const rows = selectVisibleIdlRecordsLocal(bundle);
  return rows[0] ?? null;
}
