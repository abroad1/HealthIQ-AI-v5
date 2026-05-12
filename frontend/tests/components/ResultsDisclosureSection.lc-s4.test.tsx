import { render, screen } from '@testing-library/react';
import { ResultsDisclosureSection } from '@/components/results/ResultsDisclosureSection';

describe('ResultsDisclosureSection LC-S4', () => {
  it('defaults open when defaultOpen is true', () => {
    render(
      <ResultsDisclosureSection title="What this means" defaultOpen>
        <p>Inner governed copy</p>
      </ResultsDisclosureSection>,
    );
    expect(screen.getByText('Inner governed copy')).toBeInTheDocument();
  });
});
