/**
 * @jest-environment jsdom
 *
 * ARCH-CONV-CORRECT-1 — Layer C medical boundary.
 *
 * Proves that the components on the live results path derive no medical meaning from raw
 * biomarker values: colour, ordering, confidence and interpretation must all come from the
 * backend, and absent backend fields must render as absent rather than being invented.
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import BiomarkerDials from '../../app/components/biomarkers/BiomarkerDials';
import ClusterSummary from '../../app/components/clusters/ClusterSummary';
import { LayerCInsightSection } from '../../app/components/results/LayerCInsightSection';

describe('Layer C medical boundary — no frontend inference from raw values', () => {
  it('does not interpret a marker whose backend status is missing', () => {
    const { container } = render(
      <BiomarkerDials
        biomarkers={{
          homocysteine: { value: 16.2, unit: 'umol/L', referenceRange: { min: 5, max: 15, unit: 'umol/L' } },
        }}
      />
    );

    // No clinical colour is chosen from the dial position; an unknown status renders neutral.
    expect(container.querySelector('.stroke-red-500')).toBeNull();
    expect(container.querySelector('.stroke-yellow-500')).toBeNull();
    expect(container.querySelector('.stroke-green-500')).toBeNull();
    expect(container.querySelector('.stroke-gray-400')).not.toBeNull();
  });

  it('colours a marker from the backend status, not the value', () => {
    const outOfRangeButNormal = render(
      <BiomarkerDials
        biomarkers={{
          homocysteine: {
            value: 16.2,
            unit: 'umol/L',
            status: 'normal',
            referenceRange: { min: 5, max: 15, unit: 'umol/L' },
          },
        }}
      />
    );
    expect(outOfRangeButNormal.container.querySelector('.stroke-green-500')).not.toBeNull();
    expect(outOfRangeButNormal.container.querySelector('.stroke-red-500')).toBeNull();
  });

  it('omits cluster confidence when the backend did not supply it', () => {
    render(
      <ClusterSummary
        clusters={[
          {
            id: 'c1',
            name: 'Macrocytic pattern',
            category: 'cbc',
            score: 42,
            biomarkers: ['mcv'],
            description: 'Backend description.',
            recommendations: [],
            severity: 'moderate',
          },
        ]}
      />
    );

    expect(screen.queryByText(/Confidence:/)).toBeNull();
    expect(screen.queryByText('85%')).toBeNull();
  });

  it('renders Layer C features in the fixed order rather than by confidence', () => {
    render(
      <LayerCInsightSection
        bundle={
          {
            metabolic_age: { metabolic_age: 44, age_delta_years: 2, homa_ir: 0, severity: 'mild', confidence: 0.2 },
            heart_insight: { heart_resilience_score: 70, severity: 'mild', confidence: 0.9 },
            inflammation: { inflammation_burden_score: 0, severity: 'normal', confidence: 0 },
            fatigue_root_cause: { root_causes: [], severity: 'normal', confidence: 0 },
            detox_filtration: { detox_filtration_score: 0, liver_score: 0, kidney_score: 0, severity: 'normal', confidence: 0 },
          } as never
        }
      />
    );

    const titles = screen.getAllByRole('heading', { level: 3 }).map((h) => h.textContent);
    const metabolicIdx = titles.findIndex((t) => t?.includes('Metabolic age'));
    const heartIdx = titles.findIndex((t) => t?.includes('Heart resilience'));
    expect(metabolicIdx).toBeGreaterThanOrEqual(0);
    expect(heartIdx).toBeGreaterThan(metabolicIdx);
  });
});
