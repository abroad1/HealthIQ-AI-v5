/**
 * @jest-environment node
 *
 * Guard: dashboard Recent Analyses must use ordinary history, not trend-eligible.
 */

import fs from 'fs';
import path from 'path';

describe('dashboard Recent Analyses history authority', () => {
  it('uses useHistory (GET /api/analysis/history) for Recent analyses, not trend-eligible', () => {
    const dashboardPath = path.join(
      __dirname,
      '../../app/(app)/dashboard/page.tsx'
    );
    const src = fs.readFileSync(dashboardPath, 'utf8');

    expect(src).toMatch(/useHistory\(/);
    expect(src).toMatch(/Recent analyses/);
    // Trends glance may use useTrendData; Recent analyses must not replace history with it.
    const recentBlock = src.slice(src.indexOf('Recent analyses'));
    expect(recentBlock).not.toMatch(/useTrendData|getTrendEligibleHistory|trend-eligible/);
    expect(src).toMatch(/hooks\/useHistory/);
  });
});
