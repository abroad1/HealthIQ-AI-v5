import type {
  BiomarkerResult,
  Cluster,
  ClinicianReportV1,
  Insight,
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

/** Normalized comparison for “same lead” heuristics (hero alignment). */
export function normalizeHeroComparisonKey(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * When the visible IDL record sets the hero title, the hero body must come from the same IDL authority —
 * not `narrative_report_v1.retail_summary` or clinician page1 alone (avoids AB/VR split-brain).
 */
export function buildIdlLedHeroSummary(idl: InterpretationDisplayRecordV1): string {
  const chunks: string[] = [];
  for (const raw of [
    idl.why_it_matters,
    idl.subtitle,
    idl.user_safe_description,
    idl.supporting_biomarkers_summary,
    idl.supporting_systems_summary,
  ]) {
    const s = (raw || '').trim();
    if (!s) continue;
    const sent = firstSentence(s);
    const k = normalizeHeroComparisonKey(sent);
    if (!k) continue;
    if (chunks.some((c) => normalizeHeroComparisonKey(c) === k)) continue;
    chunks.push(sent);
  }
  const combined = chunks.join(' ');
  if (combined.trim()) return takeUpToNSentences(combined, 3);
  return '';
}

/**
 * If the clinician-ranked lead (page1) differs from the pattern-led hero title, surface it only as secondary copy.
 */
export function deriveSecondaryRankedSignalLine(
  clinicianReport: ClinicianReportV1 | null | undefined,
  heroTitle: string,
  firstIdl: InterpretationDisplayRecordV1 | null | undefined
): string | null {
  if (!firstIdl || !clinicianReport?.sections?.page1) return null;
  const concern = (clinicianReport.sections.page1.primary_concern || '').trim();
  if (!concern) return null;
  const concernLead = extractFirstSentence(concern);
  const a = normalizeHeroComparisonKey(heroTitle);
  const b = normalizeHeroComparisonKey(concernLead);
  if (!a || !b) return null;
  if (a === b) return null;
  if (a.includes(b) || b.includes(a)) return null;
  const aTokens = new Set(a.split(' ').filter((t) => t.length > 3));
  const bTokens = b.split(' ').filter((t) => t.length > 3);
  if (bTokens.length > 0) {
    const overlap = bTokens.filter((t) => aTokens.has(t)).length;
    if (overlap >= Math.min(2, bTokens.length)) return null;
  }
  return `Top ranked signal on this panel: ${concernLead}`;
}

const _sevRank: Record<string, number> = { critical: 4, high: 3, moderate: 2, low: 1 };

function _clusterToDriver(
  cluster: Cluster,
  idx: number
): { id: string; name: string; biomarkers: string[] } {
  const id = String(cluster.cluster_id || cluster.id || `cluster-${idx}`);
  const name = cluster.name?.trim() ? cluster.name : 'Health pattern';
  const biomarkers = cluster.biomarkers || cluster.biomarkers_involved || [];
  return { id, name, biomarkers };
}

/** Severity/score winner — same rule as legacy results page `pickPrimaryDriverCluster`. */
export function pickSeverityPrimaryDriverCluster(clusters: Cluster[]): {
  id: string;
  name: string;
  biomarkers: string[];
} | null {
  let best: { id: string; name: string; biomarkers: string[]; rank: number; score: number } | null = null;
  clusters.forEach((cluster, idx) => {
    const id = String(cluster.cluster_id || cluster.id || `cluster-${idx}`);
    const sev = String(cluster.severity || 'moderate').toLowerCase();
    const rank = _sevRank[sev] ?? 2;
    const score = typeof cluster.score === 'number' ? cluster.score : (cluster.confidence ?? 0) * 100;
    const name = cluster.name?.trim() ? cluster.name : 'Health pattern';
    const biomarkers = cluster.biomarkers || cluster.biomarkers_involved || [];
    if (!best || rank > best.rank || (rank === best.rank && score > best.score)) {
      best = { id, name, biomarkers, rank, score };
    }
  });
  if (!best) return null;
  return { id: best.id, name: best.name, biomarkers: best.biomarkers };
}

function _scoreClusterAlignmentToIdl(c: Cluster, idl: InterpretationDisplayRecordV1): number {
  const name = (c.name || '').toLowerCase().trim();
  if (!name) return 0;
  const retail = (idl.retail_display_label || '').toLowerCase();
  const subtitle = (idl.subtitle || '').toLowerCase();
  const sys = (idl.supporting_systems_summary || '').toLowerCase();
  const blob = `${retail} ${subtitle} ${sys}`.trim();
  let score = 0;
  const nameWords = name.split(/\s+/).filter((w) => w.length > 3);
  for (const w of nameWords) {
    if (blob.includes(w)) score += 1;
  }
  if (retail && (name.includes(retail.slice(0, Math.min(18, retail.length))) || retail.includes(name.slice(0, Math.min(14, name.length)))))
    score += 3;
  if (subtitle && (name.includes(subtitle.slice(0, 14)) || subtitle.includes(name.slice(0, 12)))) score += 2;
  return score;
}

/**
 * Prefer a cluster aligned with the displayed IDL lead; otherwise fall back to severity primary driver.
 */
export function pickHeroAlignedPrimaryDriver(
  clusters: Cluster[],
  firstIdl: InterpretationDisplayRecordV1 | null | undefined
): { id: string; name: string; biomarkers: string[] } | null {
  if (!clusters.length) return null;
  const fallback = pickSeverityPrimaryDriverCluster(clusters);
  if (!firstIdl) return fallback;

  const ALIGN_THRESHOLD = 2;
  let best: { cluster: Cluster; idx: number; align: number; rank: number; score: number } | null = null;

  clusters.forEach((cluster, idx) => {
    const align = _scoreClusterAlignmentToIdl(cluster, firstIdl);
    if (align < ALIGN_THRESHOLD) return;
    const sev = String(cluster.severity || 'moderate').toLowerCase();
    const rank = _sevRank[sev] ?? 2;
    const score = typeof cluster.score === 'number' ? cluster.score : (cluster.confidence ?? 0) * 100;
    if (!best || align > best.align || (align === best.align && rank > best.rank) || (align === best.align && rank === best.rank && score > best.score)) {
      best = { cluster, idx, align, rank, score };
    }
  });

  if (best) return _clusterToDriver(best.cluster, best.idx);
  return fallback;
}

/**
 * Hero summary precedence:
 * 1) If a visible IDL record exists → IDL-only body (`buildIdlLedHeroSummary`), then clinician/narrative fallbacks that avoid retail_summary until IDL is exhausted.
 * 2) Else → `narrative_report_v1.retail_summary` if present, else clinician page1 shaping (legacy).
 */
export function buildPrimaryHeroSummary(
  narrativeRetail: string | null | undefined,
  clinicianReport: ClinicianReportV1 | null | undefined,
  firstIdl?: InterpretationDisplayRecordV1 | null
): string {
  if (firstIdl) {
    const idlBody = buildIdlLedHeroSummary(firstIdl);
    if (idlBody.trim()) return idlBody;
  }

  const retail = (narrativeRetail ?? '').trim();
  if (retail && !firstIdl) {
    return takeUpToNSentences(retail, 3);
  }

  if (!clinicianReport) {
    if (retail && !firstIdl) return takeUpToNSentences(retail, 3);
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
  if (retail && !firstIdl) return takeUpToNSentences(retail, 3);
  return buildBodyOverviewPrimarySentence(page1);
}

/**
 * D-6: When backend emits meta.wave1_aligned_drivers.biomarker_keys, prefer that for
 * "What's driving this" so the strip matches Wave 1 card authority (not cluster arbitration alone).
 */
export function pickBiomarkersByWave1Keys(
  biomarkers: BiomarkerResult[],
  canonicalKeys: string[] | null | undefined
): BiomarkerResult[] {
  if (!canonicalKeys?.length) return [];
  const byName = new Map(biomarkers.map((b) => [b.biomarker_name.toLowerCase(), b]));
  const out: BiomarkerResult[] = [];
  for (const k of canonicalKeys) {
    const b = byName.get(k.toLowerCase());
    if (b) out.push(b);
    if (out.length >= 8) break;
  }
  return out;
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
  if (raw.includes('diet')) return 'Diet';
  if (raw.includes('lifestyle')) return 'Lifestyle';
  if (raw.includes('supp')) return 'Supplement';
  if (raw.includes('medical') || raw.includes('referral')) return 'Medical referral';
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

function categoryFromInsight(ins: Insight): string {
  const raw = (ins.category || '').toLowerCase();
  if (raw.includes('diet') || raw.includes('nutrition')) return 'Diet';
  if (raw.includes('lifestyle') || raw.includes('exercise') || raw.includes('activity')) return 'Lifestyle';
  if (raw.includes('supp')) return 'Supplement';
  if (raw.includes('medical') || raw.includes('refer') || raw.includes('clinical')) return 'Medical referral';
  return 'Lifestyle';
}

function evidenceFromInsight(ins: Insight): string {
  if (typeof ins.confidence === 'number' && ins.confidence > 0) {
    if (ins.confidence >= 0.8) return 'Higher model confidence (contextual)';
    if (ins.confidence >= 0.5) return 'Moderate model confidence (contextual)';
  }
  const s = (ins.severity || '').toLowerCase();
  if (s === 'high' || s === 'critical') return 'Stronger emphasis in narrative block';
  return 'Supporting note (narrative insight)';
}

export interface BuildActionCardOptions {
  maxItems?: number;
  /** When cluster/panel recs are thin, use insight.recommendation lines (already in DTO). */
  insights?: Insight[] | null;
}

/** Flattens cluster recommendations, panel-level recs, then optional insight recs. Deterministic only. */
export function buildActionCardModels(
  clusters: Cluster[],
  topLevelRecs: string[] | null | undefined,
  options?: BuildActionCardOptions
): ResultActionCardModel[] {
  const maxItems = options?.maxItems ?? 8;
  const insights = options?.insights;
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
      if (out.length >= maxItems) return out;
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
    if (out.length >= maxItems) return out;
  }
  for (const ins of insights || []) {
    for (const r of ins.recommendations || []) {
      const paragraph = (r || '').trim();
      if (!paragraph) continue;
      const head = firstSentence(paragraph);
      out.push({
        heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
        paragraph,
        sourceLabel: (ins.summary || ins.category || ins.id || 'Narrative insight').slice(0, 120),
        categoryLabel: categoryFromInsight(ins),
        evidenceLevelLabel: evidenceFromInsight(ins),
      });
      if (out.length >= maxItems) return out;
    }
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
