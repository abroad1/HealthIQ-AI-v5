import React from 'react';
import { render, screen } from '@testing-library/react';
import { StaleResultBanner } from '../../app/components/results/StaleResultBanner';

describe('StaleResultBanner', () => {
  it('renders nothing for current results', () => {
    const { container } = render(
      <StaleResultBanner
        versioning={{
          immutable_snapshot: true,
          result_status: 'current',
          stale_reasons: [],
        }}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it('shows warning for stale results', () => {
    render(
      <StaleResultBanner
        versioning={{
          immutable_snapshot: true,
          result_status: 'stale',
          stale_reasons: ['completeness_policy_missing'],
          user_message: 'Generated using an older engine.',
        }}
      />
    );
    const banner = screen.getByTestId('stale-result-banner');
    expect(banner).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /older engine/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /regenerat/i })).toBeNull();
  });

  it('shows warning for incompatible results', () => {
    render(
      <StaleResultBanner
        versioning={{
          immutable_snapshot: true,
          result_status: 'incompatible',
          stale_reasons: ['missing_required_keys'],
          user_message: 'This saved result cannot be displayed with the current results page contract.',
        }}
      />
    );
    expect(screen.getByTestId('stale-result-banner')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /older format/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /regenerat/i })).toBeNull();
  });
});
