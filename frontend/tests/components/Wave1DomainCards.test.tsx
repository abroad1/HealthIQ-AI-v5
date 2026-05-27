import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import fs from 'fs';
import path from 'path';
import { Wave1DomainCards } from '../../app/components/results/Wave1DomainCards';
import type { ConsumerDomainScoreV1 } from '../../app/types/analysis';

function minimalLiverDomain(overrides: Partial<ConsumerDomainScoreV1> = {}): ConsumerDomainScoreV1 {
  return {
    domain_id: 'wave1_liver',
    consumer_label: 'Liver health',
    clinical_label: 'Hepatic',
    score: 0.8,
    band_label: 'stable',
    confidence_tier: 'medium',
    active_signal_ids: [],
    primary_idl_record_id: null,
    missing_marker_ids: ['total_bilirubin', 'ast', 'ggt'],
    source_track: 'test',
    caveat_flags: [],
    contributing_system_keys: ['liver'],
    raw_evidence_refs: {},
    headline_sentence: 'Your liver health looks broadly stable based on your current enzyme markers.',
    contributor_sentence: 'Your liver enzyme markers are within their reference ranges.',
    confidence_sentence: 'Medium confidence',
    consequence_sentence: 'Neutral.',
    next_step_sentence: 'Discuss with a clinician.',
    plain_english_descriptor: 'Liver strain and processing load',
    evidence_completeness_numerator: 2,
    evidence_completeness_denominator: 5,
    subsystems: null,
    ...overrides,
  };
}

describe('Wave1DomainCards', () => {
  it('renders user-safe labels for missing markers (D-7)', async () => {
    const domains: ConsumerDomainScoreV1[] = [
      minimalLiverDomain({
        subsystems: [
          {
            subsystem_id: 'wave1_liver_processing',
            subsystem_label: 'Liver processing context',
            included_marker_ids: ['total_bilirubin'],
            missing_marker_ids: ['ast', 'ggt'],
            included_markers: [{ id: 'total_bilirubin', display_label: 'Total bilirubin' }],
            missing_markers: [
              { id: 'ast', display_label: 'AST (aspartate aminotransferase)' },
              { id: 'ggt', display_label: 'GGT (gamma-glutamyl transferase)' },
            ],
            status_label: null,
            evidence_role: null,
            source_trace: 'Wave 1 governed subsystem map',
          },
        ],
      }),
    ];
    const user = userEvent.setup();
    render(<Wave1DomainCards domains={domains} embedInJourney />);

    await user.click(screen.getByRole('button', { name: /more detail/i }));

    expect(await screen.findByText('Total bilirubin')).toBeInTheDocument();
    expect(screen.getByText(/AST \(aspartate aminotransferase\)/i)).toBeInTheDocument();
    expect(screen.getByText(/GGT \(gamma-glutamyl transferase\)/i)).toBeInTheDocument();
    expect(screen.queryByText('total_bilirubin')).not.toBeInTheDocument();
    expect(screen.queryByText(/^ast$/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/^ggt$/i)).not.toBeInTheDocument();
  });

  it('shows DOMAIN-UX1A consumer fields without clinical label (DOMAIN-UX1A)', () => {
    render(<Wave1DomainCards domains={[minimalLiverDomain()]} embedInJourney />);
    expect(screen.getByTestId('fe-domain-ux1a-health-systems-cards')).toBeInTheDocument();
    expect(screen.getByTestId('wave1-plain-english-descriptor')).toHaveTextContent(
      'Liver strain and processing load'
    );
    expect(screen.getByText('Score reliability')).toBeInTheDocument();
    expect(screen.getByTestId('wave1-score-reliability')).toHaveTextContent('Moderate reliability');
    expect(screen.getByTestId('wave1-score-visual')).toBeInTheDocument();
    expect(screen.getByTestId('wave1-band-label')).toHaveTextContent('Stable');
    expect(screen.getByText('Evidence completeness')).toBeInTheDocument();
    expect(screen.getByTestId('wave1-evidence-completeness')).toHaveTextContent(
      '2 of 5 expected markers included'
    );
    expect(screen.queryByText('Hepatic')).not.toBeInTheDocument();
  });

  it('shows insufficient-data state for zero-evidence cards (DOMAIN-UX1A-PATCH)', () => {
    render(
      <Wave1DomainCards
        domains={[
          minimalLiverDomain({
            score: 0,
            band_label: 'review',
            evidence_completeness_numerator: 0,
            evidence_completeness_denominator: 3,
            confidence_tier: 'low',
          }),
        ]}
        embedInJourney
      />
    );

    expect(screen.getByTestId('wave1-insufficient-data-state')).toHaveTextContent('Not enough data');
    expect(screen.queryByText('/ 100')).not.toBeInTheDocument();
    expect(screen.queryByText('Needs attention')).not.toBeInTheDocument();
    expect(screen.getByTestId('wave1-score-reliability')).toHaveTextContent('Limited reliability');
    expect(screen.getByTestId('wave1-evidence-completeness')).toHaveTextContent(
      '0 of 3 expected markers included'
    );
    expect(screen.queryByTestId('wave1-score-visual')).not.toBeInTheDocument();
  });

  it('shows premium score visual for scored cards (DOMAIN-UX1B)', () => {
    render(<Wave1DomainCards domains={[minimalLiverDomain()]} embedInJourney />);
    expect(screen.getByTestId('wave1-score-visual')).toBeInTheDocument();
    expect(screen.getByText('80')).toBeInTheDocument();
  });

  it('shows partial-evidence limited coverage hint (DOMAIN-UX1B)', () => {
    render(
      <Wave1DomainCards
        domains={[
          minimalLiverDomain({
            domain_id: 'wave1_cardiovascular',
            consumer_label: 'Cardiovascular health',
            evidence_completeness_numerator: 1,
            evidence_completeness_denominator: 5,
            confidence_tier: 'low',
            score: 1,
            band_label: 'strong',
          }),
        ]}
        embedInJourney
      />
    );
    expect(screen.getByTestId('wave1-limited-coverage-hint')).toHaveTextContent(
      'Limited marker coverage on this panel'
    );
    expect(screen.getByTestId('wave1-coverage-panel')).toBeInTheDocument();
  });

  it('keeps legacy missing-marker pill list out of parent card body (DOMAIN-UX1D)', async () => {
    const user = userEvent.setup();
    render(<Wave1DomainCards domains={[minimalLiverDomain()]} embedInJourney />);
    await user.click(screen.getByRole('button', { name: /more detail/i }));
    expect(screen.queryByTestId('wave1-missing-markers')).not.toBeInTheDocument();
  });

  it('renders subsystem evidence section from backend DTO when expanded (DOMAIN-UX1D)', async () => {
    const user = userEvent.setup();
    render(
      <Wave1DomainCards
        domains={[
          minimalLiverDomain({
            subsystems: [
              {
                subsystem_id: 'wave1_liver_processing',
                subsystem_label: 'Liver processing context',
                included_marker_ids: ['alt', 'alp'],
                missing_marker_ids: ['ggt'],
                included_markers: [
                  { id: 'alt', display_label: 'ALT (alanine aminotransferase)' },
                  { id: 'alp', display_label: 'ALP (alkaline phosphatase)' },
                ],
                missing_markers: [{ id: 'ggt', display_label: 'GGT (gamma-glutamyl transferase)' }],
                status_label: null,
                evidence_role: null,
                source_trace: 'Wave 1 governed subsystem map',
              },
            ],
          }),
        ]}
        embedInJourney
      />
    );

    await user.click(screen.getByRole('button', { name: /more detail/i }));

    expect(screen.getByTestId('wave1-subsystems-section')).toBeInTheDocument();
    expect(screen.getByText('Liver processing context')).toBeInTheDocument();
    expect(screen.getByText(/ALT \(alanine aminotransferase\)/i)).toBeInTheDocument();
    expect(screen.getByText(/ALP \(alkaline phosphatase\)/i)).toBeInTheDocument();
    expect(screen.getByText(/GGT \(gamma-glutamyl transferase\)/i)).toBeInTheDocument();
    expect(screen.getByText('Not uploaded')).toBeInTheDocument();
    expect(screen.queryByTestId('wave1-subsystem-status')).not.toBeInTheDocument();
    expect(screen.queryByText(/mg\/dl/i)).not.toBeInTheDocument();
    expect(screen.queryByText('Ldl Cholesterol')).not.toBeInTheDocument();
    expect(screen.queryByText('Hdl Cholesterol')).not.toBeInTheDocument();
    expect(screen.queryByText('Tc Hdl Ratio')).not.toBeInTheDocument();
  });

  it('keeps subsystem rendering isolated from Wave1DomainCards implementation (DOMAIN-UX1D)', () => {
    const cardsPath = path.join(process.cwd(), 'app/components/results/Wave1DomainCards.tsx');
    const src = fs.readFileSync(cardsPath, 'utf8');

    expect(src).toContain('Wave1SubsystemEvidenceSection');
    expect(src).not.toContain('included_marker_ids');
    expect(src).not.toContain('missing_marker_ids');
    expect(src).not.toContain('wave1_cv_lipid_transport');
    expect(src).not.toContain('Lipid transport');
  });

  it('does not expand wave1ConfidenceMarkerLabels as primary subsystem label fix (DOMAIN-LABEL1)', () => {
    const labelsPath = path.join(process.cwd(), 'app/lib/wave1ConfidenceMarkerLabels.ts');
    const src = fs.readFileSync(labelsPath, 'utf8');
    expect(src).not.toContain("hba1c:");
    expect(src).not.toContain("crp:");
    expect(src).not.toContain("tc_hdl_ratio:");
    expect(src).not.toContain("ldl_cholesterol:");
    expect(src).not.toContain("hdl_cholesterol:");
  });
});
