/**
 * LC-S8D / FE-S8E — Layer C Mode A uploaded-panel fidelity (renderer-only).
 * Displays API-supplied upload_panel_observations; no unit conversion.
 */

import type { BiomarkerResult, DisplayUnitPolicyMeta, UploadPanelObservation } from '@/types/analysis';

export interface UploadedPanelFidelityRow {
  observationKey: string;
  linkedCanonicalId: string;
  displayLabel: string;
  value: number;
  unit: string;
  equivalenceNote: string | null;
  isEquivalentObservation: boolean;
}

const SKIP_UPLOAD_KEYS = new Set(['__unit_normalisation_meta__']);

const BIOMARKER_DISPLAY_NAMES: Record<string, string> = {
  hba1c: 'HbA1c',
  hba1c_pct: 'HbA1c (%)',
  hemoglobin: 'Haemoglobin',
  haemoglobin: 'Haemoglobin',
  hematocrit: 'Haematocrit',
  haematocrit: 'Haematocrit',
  platelets: 'Platelets',
  white_blood_cells: 'White Blood Cells',
  sodium: 'Sodium',
  potassium: 'Potassium',
  chloride: 'Chloride',
  glucose: 'Glucose',
};

export function normalizeUnitToken(unit: string | null | undefined): string {
  return (unit || '')
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/µ/g, 'u')
    .replace(/μ/g, 'u');
}

function displayNameFor(key: string): string {
  if (BIOMARKER_DISPLAY_NAMES[key]) return BIOMARKER_DISPLAY_NAMES[key];
  return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Optional policy map when API includes biomarker blocks; otherwise infer from keys. */
export function buildEquivalentCanonicalMap(
  policy: DisplayUnitPolicyMeta | null | undefined
): Map<string, string> {
  const map = new Map<string, string>();
  const biomarkers = policy?.biomarkers;
  if (!biomarkers || typeof biomarkers !== 'object') return map;

  for (const [canonicalId, entry] of Object.entries(biomarkers)) {
    const uploaded = entry?.uploaded_panel_fidelity;
    const ids = uploaded?.equivalent_canonical_ids;
    if (!Array.isArray(ids)) continue;
    for (const altId of ids) {
      if (typeof altId === 'string' && altId.trim()) {
        map.set(altId.trim(), canonicalId);
      }
    }
  }
  return map;
}

function resolveLinkedCanonicalId(
  observationKey: string,
  equivalentMap: Map<string, string>,
  canonicalByName: Map<string, BiomarkerResult>
): string | null {
  const fromPolicy = equivalentMap.get(observationKey);
  if (fromPolicy) return fromPolicy;

  if (canonicalByName.has(observationKey)) return observationKey;

  if (observationKey.endsWith('_pct')) {
    const base = observationKey.slice(0, -4);
    if (canonicalByName.has(base)) return base;
  }

  return null;
}

function parseObservation(raw: unknown): UploadPanelObservation | null {
  if (!raw || typeof raw !== 'object') return null;
  const row = raw as Record<string, unknown>;
  const value = row.value ?? row.measurement;
  if (typeof value !== 'number' || Number.isNaN(value)) return null;
  const unit = typeof row.unit === 'string' ? row.unit.trim() : '';
  if (!unit) return null;
  return { value, unit };
}

/**
 * Build rows for Mode A uploaded-panel fidelity UI.
 * Includes equivalent-only observations (e.g. hba1c_pct) and upload rows whose unit label
 * differs from the canonical analytical dial.
 */
export function buildUploadedPanelFidelityRows(
  uploadPanel: Record<string, unknown> | null | undefined,
  displayPolicy: DisplayUnitPolicyMeta | null | undefined,
  canonicalBiomarkers: BiomarkerResult[]
): UploadedPanelFidelityRow[] {
  if (!uploadPanel || typeof uploadPanel !== 'object') return [];

  const equivalentMap = buildEquivalentCanonicalMap(displayPolicy);
  const canonicalByName = new Map<string, BiomarkerResult>();
  for (const b of canonicalBiomarkers) {
    if (b.biomarker_name) canonicalByName.set(b.biomarker_name, b);
  }

  const rows: UploadedPanelFidelityRow[] = [];

  for (const [observationKey, raw] of Object.entries(uploadPanel)) {
    if (SKIP_UPLOAD_KEYS.has(observationKey) || observationKey.startsWith('unmapped_')) continue;

    const obs = parseObservation(raw);
    if (!obs) continue;

    const linkedCanonicalId = resolveLinkedCanonicalId(observationKey, equivalentMap, canonicalByName);
    if (!linkedCanonicalId) continue;

    const isEquivalentObservation = observationKey !== linkedCanonicalId;
    const canonical = canonicalByName.get(linkedCanonicalId);

    if (!isEquivalentObservation && canonical) {
      const uploadUnit = normalizeUnitToken(obs.unit);
      const canonicalUnit = normalizeUnitToken(canonical.unit);
      if (uploadUnit === canonicalUnit) continue;
    }

    const canonicalLabel = displayNameFor(linkedCanonicalId);
    let equivalenceNote: string | null = null;
    if (isEquivalentObservation) {
      equivalenceNote = `Uploaded representation of ${canonicalLabel} — not scored separately.`;
    } else if (canonical && normalizeUnitToken(obs.unit) !== normalizeUnitToken(canonical.unit)) {
      equivalenceNote = `Uploaded as reported on your panel; analytical review uses ${canonical.value} ${canonical.unit}.`;
    }

    rows.push({
      observationKey,
      linkedCanonicalId,
      displayLabel: displayNameFor(observationKey),
      value: obs.value,
      unit: obs.unit,
      equivalenceNote,
      isEquivalentObservation,
    });
  }

  rows.sort((a, b) => {
    const byCanonical = a.linkedCanonicalId.localeCompare(b.linkedCanonicalId);
    if (byCanonical !== 0) return byCanonical;
    if (a.isEquivalentObservation !== b.isEquivalentObservation) {
      return a.isEquivalentObservation ? 1 : -1;
    }
    return a.observationKey.localeCompare(b.observationKey);
  });

  return rows;
}
