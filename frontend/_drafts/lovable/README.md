# Lovable Mock-up Drafts

This directory contains static HTML snapshots of Lovable frontend mock-ups that serve as design references for Cursor conversion.

## Workflow

1. **Lovable Output**: Lovable produces Vite/React previews that cannot be integrated directly with Next.js
2. **Manual Capture**: Static HTML snapshots are manually captured and placed here
3. **Cursor Conversion**: Cursor converts these drafts into production-ready Next.js 14 App Router components
4. **Build Exclusion**: These files are excluded from all build processes

## File Naming Convention

- `[feature].html` - Static HTML snapshots of specific features
- Examples: `dashboard.html`, `analysis-form.html`, `results-view.html`

## Integration Process

1. Capture Lovable mock-up as static HTML
2. Place file in this directory with descriptive name
3. Cursor analyzes design patterns and component structure
4. Convert to Next.js 14 App Router pages/components
5. Adapt Tailwind classes to Natural Sophistication theme
6. Apply medical shadow styling conventions
7. Integrate with existing Zustand stores and API services
8. Update documentation and create test placeholders

## Theme Requirements

- **Natural Sophistication**: Clean, medical-grade aesthetic
- **Medical Shadows**: Consistent shadow patterns for depth and professionalism
- **Accessibility**: WCAG compliance for medical applications
- **Responsive Design**: Mobile-first approach with cross-device compatibility

## Documentation Updates

After each conversion, Cursor must update:
- `docs/context/IMPLEMENTATION_PLAN.md` - Sprint progress and workflow
- `docs/context/PROJECT_STRUCTURE.md` - Component structure changes
- `TEST_LEDGER.md` - Test coverage placeholders for new components

## Status

- **Current**: Directory established for Sprint 9-10 Lovable integration
- **Next Steps**: Begin capturing Lovable mock-ups as they become available
- **Target**: All mock-ups converted to production Next.js components by Sprint 10 completion
