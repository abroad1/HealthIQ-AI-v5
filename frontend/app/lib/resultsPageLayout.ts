import { sanitizeBiomarkerInterpretationForRetail } from '@/lib/feR6aRetailCopy';
import type {
  BiomarkerResult,
  Cluster,
  ClinicianReportV1,
  Insight,
  InterpretationDisplayLayerBundleV1,
  InterpretationDisplayRecordV1,
  PrimaryDriverAuthorityV1,
} from '@/types/analysis';
import { buildBodyOverviewPrimarySentence, extractFirstSentence } from '@/lib/bodyOverviewPrimarySentence';
import { buildSection3LeadStatement, buildWhatThisMeansBlock, firstSentence } from '@/lib/primaryFindingShaping';
import { sanitizePrimaryConcernForDisplay } from '@/lib/clinicianPage1Placeholders';
import { scrubConsumerRetailNarrative } from '@/lib/retailNarrativeSanitize';

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
  if (sev === 'strong_signal') return 'Needs attention';
  return sev
    .split('_')
    .map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w))
    .join(' ');
}

/** Shared consumer-safe severity labels for hero and IDL pattern surfaces. */
export function formatConsumerSeverityLabel(sev: InterpretationDisplayRecordV1['severity_state']): string {
  return formatImlSeverity(sev);
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
  const concern = sanitizePrimaryConcernForDisplay(p1?.primary_concern);
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

const LC_S7_BIOMARKER_LABELS: Record<string, string> = {
  tc_hdl_ratio: 'TC:HDL ratio',
  tg_hdl_ratio: 'TG:HDL ratio',
  ldl_hdl_ratio: 'LDL:HDL ratio',
  non_hdl_cholesterol: 'Non-HDL cholesterol',
  active_b12: 'Active B12',
  apoa1: 'ApoA1',
  apob: 'ApoB',
  egfr: 'eGFR',
  mcv: 'MCV',
  mch: 'MCH',
  mchc: 'MCHC',
  fsh: 'FSH',
  lh: 'LH',
  haemoglobin: 'Haemoglobin',
  hemoglobin: 'Haemoglobin',
};

export function formatBiomarkerDisplayName(raw: string): string {
  const s = (raw || '').trim();
  if (!s) return raw;
  const mapped = LC_S7_BIOMARKER_LABELS[s.toLowerCase()];
  if (mapped) return mapped;
  if (!s.includes('_')) {
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
  }
  return s
    .split('_')
    .filter(Boolean)
    .map((w) => {
      const lower = w.toLowerCase();
      if (lower === 'b12' || lower === 'mma' || lower === 'dna' || lower === 'alt' || lower === 'ast')
        return lower.toUpperCase();
      if (lower.length <= 2) return lower.toUpperCase();
      return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
    })
    .join(' ');
}

export function extractPage1ConcernLeadSentence(
  clinicianReport: ClinicianReportV1 | null | undefined
): string | null {
  const concern = sanitizePrimaryConcernForDisplay(clinicianReport?.sections?.page1?.primary_concern);
  if (!concern) return null;
  return extractFirstSentence(concern);
}

/**
 * LC-S6 — one primary story: lead pattern as headline when it differs from the IDL retail label,
 * with explicit system-context line instead of engineering “ranked signal” wording.
 */
export function resolveHeroPrimaryStory(
  clinicianReport: ClinicianReportV1 | null | undefined,
  phenotypeLabel: string,
  firstIdl: InterpretationDisplayRecordV1 | null | undefined
): { heroTitle: string; systemContextLine: string | null; bridgeExplanation: string | null } {
  const secondary = deriveSecondaryRankedSignalLine(clinicianReport, phenotypeLabel, firstIdl);
  const concernLead = extractPage1ConcernLeadSentence(clinicianReport);
  if (!secondary || !concernLead) {
    return { heroTitle: phenotypeLabel, systemContextLine: null, bridgeExplanation: secondary };
  }
  const systemLabel = scrubConsumerRetailNarrative(phenotypeLabel);
  return {
    heroTitle: concernLead,
    systemContextLine: `Broader system context: ${systemLabel}`,
    bridgeExplanation: null,
  };
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
  const concern = sanitizePrimaryConcernForDisplay(clinicianReport.sections.page1.primary_concern);
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
  return `Leading pattern described in this report: ${concernLead}`;
}

function _clusterToDriver(
  cluster: Cluster,
  idx: number
): { id: string; name: string; biomarkers: string[] } {
  const id = String(cluster.cluster_id || cluster.id || `cluster-${idx}`);
  const name = cluster.name?.trim() ? cluster.name : 'Health pattern';
  const biomarkers = cluster.biomarkers || cluster.biomarkers_involved || [];
  return { id, name, biomarkers };
}

/**
 * ARCH-CONV-CORRECT-1 — the primary driver is the Layer B ranked lead.
 *
 * Layer C resolves the governed `primary_driver_v1` record to the cluster it names and
 * renders it. It does not rank severity, score alignment or substitute a fallback: when
 * Layer B supplies no resolved lead the caller must suppress the driver surface.
 */
export function selectGovernedPrimaryDriver(
  clusters: Cluster[],
  authority: PrimaryDriverAuthorityV1 | null | undefined
): { id: string; name: string; biomarkers: string[] } | null {
  const clusterId = authority?.cluster_id?.trim();
  if (!clusterId) return null;
  const idx = clusters.findIndex(
    (cluster, i) => String(cluster.cluster_id || cluster.id || `cluster-${i}`) === clusterId
  );
  if (idx < 0) return null;
  const driver = _clusterToDriver(clusters[idx], idx);
  const governedMarkers = (authority?.biomarker_keys ?? []).map((k) => String(k).trim()).filter(Boolean);
  if (governedMarkers.length > 0) {
    return { ...driver, biomarkers: governedMarkers };
  }
  return driver;
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

/**
 * ARCH-CONV-CORRECT-1 — driver markers follow the governed order supplied by Layer B.
 *
 * Layer C no longer ranks markers by lab abnormality when the governed list is short;
 * an incomplete governed list yields a shorter strip rather than a frontend-chosen one.
 */
export function pickTopDriverBiomarkers(
  biomarkers: BiomarkerResult[],
  primaryDriver: { biomarkers: string[] } | null
): BiomarkerResult[] {
  const withValues = biomarkers.filter((b) => b.biomarker_name && b.value != null && typeof b.value === 'number');
  const byName = new Map(withValues.map((b) => [b.biomarker_name, b]));
  const out: BiomarkerResult[] = [];
  for (const name of primaryDriver?.biomarkers ?? []) {
    const b = byName.get(name);
    if (b && !out.find((o) => o.biomarker_name === b.biomarker_name)) out.push(b);
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

/**
 * IUAT-006 — consumer-safe status in the driving-signals band only.
 * Uses backend interpretation text when present; does not compute lab abnormality.
 */
export function formatConsumerDriverBandStatusLabel(b: BiomarkerResult): string {
  const status = (b.status || '').trim().toLowerCase();
  const interp = sanitizeBiomarkerInterpretationForRetail(b.interpretation);
  if (interp) {
    const snippet = firstSentence(interp).toLowerCase();
    if (/\b(below|low)\b/.test(snippet) && !/\babove\b/.test(snippet)) return 'Below range';
    if (/\b(above|elevated|high)\b/.test(snippet)) return 'Above range';
    if (/\b(in range|within range|optimal|normal)\b/.test(snippet)) return 'In range';
  }
  if (status === 'critical') return 'Needs review';
  if (status === 'elevated' || status === 'high') return 'Above range';
  if (status === 'low') return 'Below range';
  return humanizeStatus(b.status);
}

export function oneLineMarkerInterpretation(b: BiomarkerResult): string {
  const direct = sanitizeBiomarkerInterpretationForRetail(b.interpretation);
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
  /**
   * ARCH-CONV-CORRECT-1 — provenance of the line only. Layer C no longer bins backend
   * severity or confidence into an evidence-strength claim.
   */
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

const ACTION_SOURCE_CLUSTER_LABEL = 'From your system pattern group';
const ACTION_SOURCE_INSIGHT_LABEL = 'From a narrative insight block';
const ACTION_SOURCE_PANEL_LABEL = 'Panel-level note';
const ACTION_SOURCE_REPORT_LABEL = 'From your structured report';

function categoryFromInsight(ins: Insight): string {
  const raw = (ins.category || '').toLowerCase();
  if (raw.includes('diet') || raw.includes('nutrition')) return 'Diet';
  if (raw.includes('lifestyle') || raw.includes('exercise') || raw.includes('activity')) return 'Lifestyle';
  if (raw.includes('supp')) return 'Supplement';
  if (raw.includes('medical') || raw.includes('refer') || raw.includes('clinical')) return 'Medical referral';
  return 'Lifestyle';
}


export interface BuildActionCardOptions {
  maxItems?: number;
  /** When cluster/panel recs are thin, use insight.recommendation lines (already in DTO). */
  insights?: Insight[] | null;
  /** LC-S6 — governed `narrative_report_v1.next_steps_narrative` when structured rec lines are absent. */
  narrativeNextStepsNarrative?: string | null;
  /** LC-S7 — when true, skip narrative-derived action cards (next steps already shown in Direction). */
  omitNarrativeNextStepsFromCards?: boolean;
}

export function parseNarrativeNextStepParagraphs(text: string): string[] {
  const t = text.trim();
  if (!t) return [];
  const lines: string[] = [];
  for (const chunk of t.split(/\n+/)) {
    const line = chunk
      .replace(/^\s*[-•*]\s+/, '')
      .replace(/^\s*\d+[).]\s+/, '')
      .trim();
    if (!line.length) continue;
    if (/safe\s+next-?step\s+framing/i.test(line)) continue;
    if (line.length >= 12) lines.push(line);
  }
  if (lines.length === 0 && t.length >= 12) return [t];
  return lines;
}

function normalizeActionDedupeKey(s: string): string {
  return s
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[^a-z0-9\s]/g, '')
    .trim()
    .slice(0, 200);
}

/** Flattens cluster recommendations, panel-level recs, then optional insight recs. Deterministic only. */
export function buildActionCardModels(
  clusters: Cluster[],
  topLevelRecs: string[] | null | undefined,
  options?: BuildActionCardOptions
): ResultActionCardModel[] {
  const maxItems = options?.maxItems ?? 8;
  const insights = options?.insights;
  const omitNarrative = options?.omitNarrativeNextStepsFromCards === true;
  const out: ResultActionCardModel[] = [];
  const seen = new Set<string>();
  const pushDeduped = (m: ResultActionCardModel) => {
    const k = normalizeActionDedupeKey(m.paragraph);
    if (!k.length) return;
    if (seen.has(k)) return;
    seen.add(k);
    out.push(m);
  };
  for (const c of clusters) {
    const name = c.name?.trim() || 'System group';
    for (const r of c.recommendations || []) {
      const paragraph = (r || '').trim();
      if (!paragraph) continue;
      const head = firstSentence(paragraph);
      pushDeduped({
        heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
        paragraph,
        sourceLabel: name,
        categoryLabel: categoryFromCluster(c),
        evidenceLevelLabel: ACTION_SOURCE_CLUSTER_LABEL,
      });
      if (out.length >= maxItems) return out;
    }
  }
  for (const r of topLevelRecs || []) {
    const paragraph = (r || '').trim();
    if (!paragraph) continue;
    const head = firstSentence(paragraph);
    pushDeduped({
      heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
      paragraph,
      sourceLabel: 'Panel summary',
      categoryLabel: 'Follow-up',
      evidenceLevelLabel: ACTION_SOURCE_PANEL_LABEL,
    });
    if (out.length >= maxItems) return out;
  }
  for (const ins of insights || []) {
    for (const r of ins.recommendations || []) {
      const paragraph = (r || '').trim();
      if (!paragraph) continue;
      const head = firstSentence(paragraph);
      pushDeduped({
        heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
        paragraph,
        sourceLabel: (ins.summary || ins.category || ins.id || 'Narrative insight').slice(0, 120),
        categoryLabel: categoryFromInsight(ins),
        evidenceLevelLabel: ACTION_SOURCE_INSIGHT_LABEL,
      });
      if (out.length >= maxItems) return out;
    }
  }
  const nextNarr = options?.narrativeNextStepsNarrative?.trim();
  if (!omitNarrative && out.length === 0 && nextNarr) {
    for (const paragraph of parseNarrativeNextStepParagraphs(nextNarr)) {
      const cleaned = scrubConsumerRetailNarrative(paragraph);
      if (!cleaned.trim()) continue;
      const head = firstSentence(cleaned);
      pushDeduped({
        heading: head.length > 100 ? `${head.slice(0, 97).trim()}…` : head,
        paragraph: cleaned,
        sourceLabel: 'Report next steps',
        categoryLabel: 'Follow-up',
        evidenceLevelLabel: ACTION_SOURCE_REPORT_LABEL,
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
