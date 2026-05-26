import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
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
    const domains: ConsumerDomainScoreV1[] = [minimalLiverDomain()];
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
  });
});
