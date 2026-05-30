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
  });
});
