# State Management

This directory contains Zustand stores for client-side state management in HealthIQ AI v5.

## Store Architecture

### `analysisStore.ts`
Manages the current analysis session, progress tracking, and analysis-level metadata.

**State:**
- `currentAnalysisId: string | null`
- `analysisMetadata: AnalysisMetadata | null`
- `isAnalysisActive: boolean`
- `analysisProgress: 'idle' | 'uploading' | 'processing' | 'complete'`

### `clusterStore.ts`
Handles cluster selection, filtering, view modes, and cluster-specific UI state.

**State:**
- `selectedCluster: string | null`
- `clusterFilters: ClusterFilter[]`
- `clusterViewMode: 'radar' | 'network' | 'list'`
- `isClusterExpanded: boolean`

### `uiStore.ts`
Manages UI toggles, panel visibility, theme settings, and general interface state.

**State:**
- `theme: 'light' | 'dark'`
- `sidebarOpen: boolean`
- `activePanel: 'overview' | 'clusters' | 'biomarkers' | 'recommendations'`
- `selectedBiomarker: string | null`

## Usage Guidelines

1. **Keep stores focused** - Each store should handle a specific domain
2. **Use TypeScript** - Define proper interfaces for all state
3. **Implement actions** - Provide clear methods for state updates
4. **Handle persistence** - Use localStorage for user preferences
5. **Test thoroughly** - Include unit tests for all store logic

## Integration with TanStack Query

- **Client state** → Zustand stores
- **Server state** → TanStack Query
- **Cache invalidation** → Coordinate between stores and queries
