# HealthIQ AI v5 - Frontend

This is the Next.js 14+ App Router frontend for HealthIQ AI v5, a precision biomarker intelligence platform.

## Architecture Overview

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with semantic design tokens
- **Component Library**: shadcn/ui (built on Radix UI)
- **Animation**: Framer Motion
- **Icons**: lucide-react
- **State Management**: 
  - **Zustand** for client state
  - **TanStack Query** for server state
- **Testing**: Jest + React Testing Library + Storybook + Playwright

## Project Structure

```
frontend/
├── app/                  # Next.js App Router (file-system routing)
├── components/           # Shared + feature-specific components
├── styles/               # Tailwind config and design tokens
├── state/                # Zustand stores
├── queries/              # TanStack Query hooks
├── lib/                  # Frontend utilities
├── types/                # TypeScript type definitions
├── public/               # Static assets
├── tests/                # Jest + RTL tests
└── .storybook/           # Storybook configuration
```

## Key Features

### 🧠 Intelligence Lifecycle Integration
- **Stage 1**: User Interface for data upload
- **Stage 8**: Lifestyle recommendations display
- **Stage 9**: Visualization & insight rendering
- **Stage 10**: Monitoring & feedback

### 🎨 Design System
- Medical-grade aesthetic with "Natural Sophistication" palette
- Holographic UI elements (gauges, grids, dials)
- Dark/light mode support via `data-theme` attribute
- Scroll-based animations and transitions

### 📊 Data Visualization
- Interactive cluster graphs (D3 + Recharts)
- Biomarker visualization with holographic gauges
- Real-time progress tracking
- Actionable recommendation flows

### 🔄 State Management
- **Client State**: Zustand stores for UI interactions
- **Server State**: TanStack Query for API data
- **Real-time Updates**: WebSocket integration (future)

## API types (OpenAPI)

Contract types for the FastAPI surface are generated from a committed OpenAPI snapshot (Sprint 2 — integration stabilisation).

1. **Regenerate** after backend API schema changes (or refresh the snapshot — see `scripts/openapi-snapshot.json` header):

   ```bash
   npm run generate-types
   ```

2. This writes `app/types/generated/openapi.ts`. Domain types in `app/types/analysis.ts` re-export selected schemas (for example `ApiAnalysisStartRequest`, `ApiAnalysisStartResponse`) and keep presentation-specific shapes where the OpenAPI schema is intentionally loose.

3. **CI**: no automated gate in this sprint; run `npm run type-check` locally before PRs touching API clients.

## Development Guidelines

### Component Development
1. Use TypeScript for all components
2. Follow shadcn/ui patterns
3. Implement proper error boundaries
4. Use Tailwind CSS design tokens
5. Write comprehensive tests
6. Document with Storybook

### State Management
- **UI toggles** → `uiStore.ts`
- **User selections** → `uiStore.ts`
- **API data** → TanStack Query
- **Analysis workflow** → `analysisStore.ts`
- **Cluster interactions** → `clusterStore.ts`

### Testing Strategy
- **Unit Tests**: Jest + React Testing Library
- **Visual Tests**: Storybook Snapshots
- **E2E Tests**: Playwright (planned)
- **Coverage Target**: 90%+

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm run test

# Run Storybook
npm run storybook

# Build for production
npm run build
```

## Team Responsibilities

- **Lovable.dev**: Primary UX builder and component implementation
- **Cursor Agents**: Component scaffolding, state logic, and integrations

## Integration Points

- **Backend API**: FastAPI endpoints for data processing
- **Authentication**: Supabase Auth integration
- **Real-time Data**: WebSocket connections for live updates
- **File Upload**: Biomarker data processing pipeline

---

**Note**: This frontend architecture replaces the previous Vite + React Router setup and represents our canonical structure for Sprint 1 and beyond.