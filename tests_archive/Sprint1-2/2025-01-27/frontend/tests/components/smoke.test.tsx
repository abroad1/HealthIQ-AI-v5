/**
 * ARCHIVED: 2025-01-27 - Sprint 1-2 Prerequisites Implementation
 * Basic smoke test component for testing infrastructure verification.
 */

import { render, screen } from '@testing-library/react'

/**
 * Basic smoke test component for testing infrastructure verification.
 */
function Hello() {
  return <div>hello</div>
}

/**
 * Smoke test to verify Jest + React Testing Library setup.
 */
test('renders hello', () => {
  render(<Hello />)
  expect(screen.getByText(/hello/i)).toBeInTheDocument()
})

/**
 * Test basic React component functionality.
 */
test('component renders without crashing', () => {
  const { container } = render(<Hello />)
  expect(container.firstChild).toBeInTheDocument()
})

/**
 * Test that testing library matchers are working.
 */
test('testing library matchers work', () => {
  render(<Hello />)
  expect(screen.getByText('hello')).toBeVisible()
  expect(screen.queryByText('goodbye')).not.toBeInTheDocument()
})
