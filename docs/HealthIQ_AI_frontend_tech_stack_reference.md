# HealthIQ AI — Frontend Tech Stack Reference (Short Paper)

## Purpose

This note sets out the recommended frontend stack for HealthIQ AI as the product moves into more serious frontend build work.

The goal is not just to make the app look modern. The goal is to support a premium, smooth, trustworthy health experience with:
- dynamic page composition
- high-quality scroll behaviour
- animated biomarker visuals
- strong type safety
- maintainable long-term growth

## Recommended stack

### Core application framework
- Next.js (App Router)
- React
- TypeScript

### Styling
- Tailwind CSS

### Accessible component primitives
- Radix UI

### Motion and interaction
- Motion for React as the default animation layer

### Data visuals
- Custom SVG biomarker dials and gauges

### Server-state and async UX
- TanStack Query

### Client/UI state
- Zustand

### Premium animation layer
- GSAP only where needed for standout hero moments

## Why this stack

### 1. Next.js + React + TypeScript
This gives HealthIQ AI a strong modern application base with:
- component-driven page building
- clean routing
- good long-term maintainability
- strong typing for contracts between backend and frontend

This is the right foundation for a product that will keep expanding.

### 2. Tailwind CSS
Tailwind is the fastest way to build and refine a premium UI system without creating heavy CSS sprawl.
It is especially useful while the product is still evolving quickly.

### 3. Radix UI
Radix should be treated as the headless component foundation for accessible interface primitives such as:
- dropdowns
- modals
- accordions
- tooltips
- popovers

It gives the frontend a reliable accessibility layer without forcing a heavy visual design system.

### 4. Motion for React
Motion should be the default animation layer because it is excellent for:
- smooth section reveals
- card transitions
- accordion expansion
- layout animation
- number and state transitions
- scroll-based progressive storytelling

It is the best default choice for a buttery smooth product UX without overcomplicating the stack.

### 5. Custom SVG dials
HealthIQ AI should not depend on generic gauge components as the long-term solution.
Custom SVG dials give much tighter control over:
- biomarker ranges
- normal zones
- age/sex-aware positioning
- marker needles
- animation quality
- premium visual polish

This matters because the biomarker dial experience is central to the product.

### 6. TanStack Query
Smooth UX is not only about animation. It is also about data loading and state behaviour.
TanStack Query should be used for server state, including:
- caching
- loading behaviour
- refetch control
- server-state consistency

It should not be treated as the main client/UI state tool.

### 7. Zustand
Zustand should be used for lightweight client-side state and UI state, for example:
- local dashboard/view state
- temporary interaction state
- user-interface toggles
- small cross-component client state

It should remain distinct from TanStack Query:
- TanStack Query = server state
- Zustand = client/UI state

### 8. GSAP only where justified
GSAP is powerful, but it should be used selectively.
It is best reserved for a few premium, choreographed moments rather than as the default animation layer across the whole app.

## Product recommendation

For HealthIQ AI, the recommended practical combination is:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Radix UI
- Motion for React
- Custom SVG dials
- TanStack Query
- Zustand

With:
- GSAP added only for a small number of premium interactions if needed later

## UX direction this stack supports

This stack is suitable for:
- dynamic results-page build
- section-by-section scroll reveal
- animated biomarker dials
- premium dashboard interactions
- progressive disclosure of complex health information
- a calm, high-trust, modern health-product feel

## Final recommendation

HealthIQ AI should use a frontend stack built around:
**Next.js + TypeScript + Tailwind + Radix UI + Motion + Custom SVG dials + TanStack Query + Zustand**

This is the best balance of:
- polish
- control
- speed of delivery
- maintainability
- premium user experience

## Repository inventory

Concrete installed versions and extra frontend libraries live in **`frontend/package.json`**. Cursor agents also mirror this reference plus a dependency cross-check in **`.cursor/rules/healthiq-frontend-tech-stack.mdc`** so implementation stays aligned with the stack described above.
