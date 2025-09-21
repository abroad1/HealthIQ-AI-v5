# Components Directory

This directory contains all reusable UI components for HealthIQ AI v5.

## Structure

- `ui/` - Base UI components (shadcn/ui)
- `clusters/` - Cluster visualization suite
- `biomarkers/` - Biomarker visualization components
- `insights/` - Insight delivery system
- `pipeline/` - User upload-to-results pipeline
- `forms/` - Form components
- `layout/` - Layout components

## Component Guidelines

1. **Use TypeScript** - All components must be fully typed
2. **Follow shadcn/ui patterns** - Use existing UI components as base
3. **Implement proper error boundaries** - Handle edge cases gracefully
4. **Use Tailwind CSS** - Follow design system tokens
5. **Write tests** - Include unit tests for all components
6. **Document with Storybook** - Create stories for component documentation

## Development Notes

- Components should be client components by default unless server-side rendering is needed
- Use proper prop interfaces and default values
- Follow the established naming conventions
- Include proper accessibility attributes
