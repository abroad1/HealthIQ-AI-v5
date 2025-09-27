# 📦 STACK_FRONTEND.md

> ⚠️ NOTE: This file is the authoritative source of truth for frontend implementation.  
> References in `UX_UI_GUIDE.md` are visual/design guidelines only and should not override these architectural decisions.

This document defines the complete frontend stack architecture for HealthIQ-AI v5. It reflects the design system, UX components, state and data flow, tooling, and implementation phases agreed with Loveable.dev.

### Frontend Ownership

**Lovable.dev** is the primary UX builder and leads implementation of the frontend UI based on the defined UX system.  
**Cursor agents** may contribute to components, state logic, or integrations as long as they follow the conventions defined in `UX_UI_GUIDE.md` and the documented component architecture.

**Note**: The UX guidelines in `UX_UI_GUIDE.md` by Lovable.dev serve as the canonical UX reference.

---

## ✅ Frontend Tech Stack Overview

| Category                | Tool / Library                    | Rationale                                      |
|------------------------|-----------------------------------|------------------------------------------------|
| Framework              | **Next.js**                       | Production-grade React framework              |
| Language               | **TypeScript**                    | Type safety across all UI layers              |
| Styling                | **Tailwind CSS**                  | Utility-first, themeable design                |
| UI Kit                 | **shadcn/ui**                     | Accessible, composable components             |
| Animations             | **Framer Motion**                 | Smooth transitions, scroll animations         |
| Data Fetching          | **TanStack Query**                | Server state management and caching           |
| State Management       | **Zustand**                       | Simple yet powerful local state (clusters)    |
| Charts & Visuals       | **Recharts + D3 + Visx**          | Data viz, biomarker dials, cluster networks   |
| Linting & Types        | **ESLint + Zod + zod-to-json-schema** | DX & schema safety                        |
| Storybook              | **@storybook/nextjs**             | UI documentation and design system preview    |
| Real-Time Data         | **WebSockets + react-use-websocket** | Live updates (future stage)               |
| Virtual Scrolling      | **@tanstack/react-virtual**       | Performance with large datasets               |

### Routing

HealthIQ AI uses **Next.js 14+ with App Router**, which provides file-system-based routing.  
**Routing is handled by the Next.js App Router — no use of `react-router-dom`.**

The App Router provides:
- File-system-based routing with `app/` directory
- Server and Client Components
- Built-in layouts, loading states, and error handling
- Automatic code splitting and optimization

---

## 🎨 Design System

- Design language inspired by **Function Health**, implemented with Tailwind tokens.
- Includes scroll-based animations (`ScrollReveal`, `ParallaxSection`).
- Holographic UI with `HolographicGauge`, `BiomarkerGrid`, `ClusterDials`.
- Medical-grade aesthetic using the **"Natural Sophistication"** colour palette:
  - `#FFF5D0` (Barley), `#FAD564` (Naples), `#B4BD62` (Light Olive),
    `#8EBD9D` (Neptune), `#1B475D` (Rhino)
- Dark mode is implemented via the `data-theme` attribute system (`light` / `dark`), as described in `UX_UI_GUIDE.md`. Cursor agents may assume this system is active in all theme-aware components.

---

## 📁 Component Architecture

```
components/
├── clusters/ # NEW: Cluster visualisation suite
│   ├── ClusterRadarChart.tsx
│   ├── ClusterConnectionMap.tsx
│   └── ClusterInsightPanel.tsx
├── biomarkers/ # Existing: Enhancements only
│   ├── HolographicGauge.tsx
│   ├── BiomarkerGrid.tsx
│   └── BiomarkerTrendPanel.tsx
├── insights/ # NEW: Insight delivery system
│   ├── InsightCard.tsx
│   ├── ActionableRecommendation.tsx
│   └── ProgressTracker.tsx
├── pipeline/ # NEW: User upload-to-results pipeline
│   └── AnalysisPipeline.tsx
└── ui/ # Shared ShadCN UI components
```

---

## 🧠 Data & State Management Architecture

### State Management Strategy

HealthIQ AI v5 uses a **dual-state architecture** combining Zustand for client-side state and TanStack Query for server-side data:

| State Type | Tool | Purpose | Examples |
|------------|------|---------|----------|
| **Client State** | **Zustand** | UI interactions, selections, filters | Cluster selection, panel visibility, theme |
| **Server State** | **TanStack Query** | API data, caching, synchronization | Analysis results, biomarker data, user profiles |

### Store Architecture

#### `analysisStore.ts` - Analysis Context
```ts
interface AnalysisState {
  currentAnalysisId: string | null;
  analysisMetadata: AnalysisMetadata | null;
  isAnalysisActive: boolean;
  analysisProgress: 'idle' | 'uploading' | 'processing' | 'complete';
}
```
**Purpose**: Manages the current analysis session, progress tracking, and analysis-level metadata.

#### `clusterStore.ts` - Cluster Interactions
```ts
interface ClusterState {
  selectedCluster: string | null;
  clusterFilters: ClusterFilter[];
  clusterViewMode: 'radar' | 'network' | 'list';
  isClusterExpanded: boolean;
}
```
**Purpose**: Handles cluster selection, filtering, view modes, and cluster-specific UI state.

#### `uiStore.ts` - UI State
```ts
interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  activePanel: 'overview' | 'clusters' | 'biomarkers' | 'recommendations';
  selectedBiomarker: string | null;
}
```
**Purpose**: Manages UI toggles, panel visibility, theme settings, and general interface state.

### Server Data Management

#### TanStack Query Integration
```ts
// API data fetching and caching
const { data: analysisResult, isLoading } = useQuery({
  queryKey: ['analysis', analysisId],
  queryFn: () => fetchAnalysis(analysisId),
  enabled: !!analysisId
});
```

### State Decision Guide

| What to Store | Where to Put It | Why |
|---------------|-----------------|-----|
| **UI toggles** (sidebar, panels) | `uiStore.ts` | Client-side UI state |
| **Selected biomarker** | `uiStore.ts` | User selection state |
| **Loaded API data** | TanStack Query | Server state with caching |
| **Progress phases** | `analysisStore.ts` | Analysis workflow state |
| **Cluster selections** | `clusterStore.ts` | Domain-specific interactions |
| **Theme settings** | `uiStore.ts` | Global UI preferences |
| **Analysis results** | TanStack Query | Server data with refetching |

### WebSockets (Future Enhancement)
- Real-time cluster updates and progress streaming
- Managed via react-use-websocket or socket.io-client
- Will integrate with existing Zustand stores for real-time updates

---

## 🔄 Suggested Implementation Phases

### Phase 1: Foundation Enhancement (Weeks 1–2)
- Implement Zustand stores (`analysisStore.ts`, `clusterStore.ts`, `uiStore.ts`)
- Set up TanStack Query for API data fetching
- Create placeholder cluster components
- Wire up stores to AnalysisResult structure

### Phase 2: Data Visualisation (Weeks 3–4)
- Implement interactive cluster graphs (D3 + Recharts)
- Enhance BiomarkerGrid with clustering
- Build ActionableRecommendation flow

### Phase 3: Real-Time Enhancements (Weeks 5–6)
- Add WebSocket-based live cluster updates
- Progressive analysis UI pipeline

### Phase 4: Polish & Optimise (Weeks 7–8)
- Finalise transitions and animations
- Improve performance via virtualisation
- Final DX cleanup and Storybook publishing

---

## 🧪 Dev Tools & Tooling

- **Storybook**: `npm run storybook`
- **Zod**: Schema to UI type generation
- **ESLint + TypeScript** strict mode
- Component snapshots for UX regression detection

### Frontend Testing Strategy (Value-First)

#### **Test Pyramid Distribution**
- **Unit Tests (70%)**: Business logic, state management, critical components
- **Integration Tests (25%)**: API integration, service boundaries
- **E2E Tests (5%)**: Critical user journeys only

#### **Testing Framework**
- **Jest + React Testing Library**: Unit and integration testing
- **Playwright**: E2E testing for critical user workflows
- **Storybook**: Visual regression testing (optional)

#### **Value-First Testing Principles**
- **Business Value**: Test user workflows and business-critical functionality
- **Component Focus**: Test high-value components that impact user experience
- **State Management**: Test Zustand stores for data consistency
- **API Integration**: Test service layer for reliable data flow

#### **Test Structure**
```
frontend/tests/
├── state/                    # Store tests (business logic)
│   ├── analysisStore.test.ts
│   ├── clusterStore.test.ts
│   └── uiStore.test.ts
├── services/                 # API integration tests
│   └── analysis.test.ts
├── components/               # High-value component tests only
└── e2e/                     # Critical user journeys
    └── analysis-flow.spec.ts
```

#### **Test Quality Checklist**
- Does this test **prevent user pain**?
- Does this test **catch real bugs**?
- Is this test **maintainable**?
- Would I **delete this test** if it broke?

**Cursor agents should create tests only for business-critical functionality, not for testing's sake.**

---

## 📝 TODO

- [ ] Actual implementation by Loveable.dev team
- [ ] Add links to design prototypes or Figma references
- [ ] Integrate narrative AI explanations with insight cards

---

## 🧠 Role in the Intelligence Lifecycle

This frontend stack is responsible for **Stages 1 (User Interface only)** and **Stages 8 through 10** of the 10-stage Intelligence Lifecycle described in `INTELLIGENCE_LIFECYCLE.md`.

| Stage | Responsibility |
|-------|----------------|
| 1. Upload Input UI | File upload, blood test form, lifestyle questionnaire |
| 8. Lifestyle Recommendations | Display detailed, AI-personalised advice |
| 9. Visualisation & Insight Rendering | Dials, clusters, graphs, narratives |
| 10. Monitoring & Feedback | Progress tracking, history, user behaviour logging |

Stages 2–7 (parsing, scoring, engine execution, AI synthesis) are handled by the backend.