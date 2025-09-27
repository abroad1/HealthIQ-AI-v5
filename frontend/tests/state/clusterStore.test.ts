/**
 * Cluster Store Tests
 * Tests for frontend/app/state/clusterStore.ts
 */

import { useClusterStore } from '../../app/state/clusterStore';

describe('ClusterStore', () => {
  beforeEach(() => {
    // Reset store state
    useClusterStore.getState().clearClusters();
    jest.clearAllMocks();
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = useClusterStore.getState();

      expect(state.clusters).toEqual([]);
      expect(state.selectedCluster).toBeNull();
      expect(state.clusterInsights).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.filters).toEqual({});
      expect(state.sort).toEqual({
        field: 'score',
        direction: 'desc',
      });
      expect(state.currentPage).toBe(1);
      expect(state.itemsPerPage).toBe(10);
      expect(state.totalItems).toBe(0);
    });
  });

  describe('Basic Setters', () => {
    it('should set clusters', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic Health',
          category: 'metabolic',
          biomarkers: ['glucose', 'insulin'],
          status: 'normal',
          score: 85,
          description: 'Metabolic health cluster',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
      expect(useClusterStore.getState().clusters).toEqual(clusters);
    });

    it('should set selected cluster', () => {
      const clusterId = 'cluster-1';
      useClusterStore.getState().setSelectedCluster(clusterId);
      expect(useClusterStore.getState().selectedCluster).toBe(clusterId);
    });

    it('should set clusterInsights', () => {
      const clusterInsights = [
        {
          id: 'insight-1',
          cluster_id: 'cluster-1',
          type: 'recommendation',
          title: 'Improve glucose control',
          description: 'Focus on diet and exercise',
          priority: 'high',
          actionable: true,
        },
      ];

      useClusterStore.getState().setClusterInsights(clusterInsights);
      expect(useClusterStore.getState().clusterInsights).toEqual(clusterInsights);
    });

    it('should set loading state', () => {
      useClusterStore.getState().setLoading(true);
      expect(useClusterStore.getState().isLoading).toBe(true);

      useClusterStore.getState().setLoading(false);
      expect(useClusterStore.getState().isLoading).toBe(false);
    });

    it('should set error', () => {
      const error = 'Test error';
      useClusterStore.getState().setError(error);
      expect(useClusterStore.getState().error).toBe(error);
    });
  });

  describe('Filtering', () => {
    beforeEach(() => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic Health',
          category: 'metabolic',
          biomarkers: ['glucose', 'insulin'],
          status: 'normal',
          score: 85,
          description: 'Metabolic health cluster',
        },
        {
          id: 'cluster-2',
          name: 'Cardiovascular',
          category: 'cardiovascular',
          biomarkers: ['cholesterol', 'ldl'],
          status: 'warning',
          score: 65,
          description: 'Cardiovascular health cluster',
        },
        {
          id: 'cluster-3',
          name: 'Inflammation',
          category: 'inflammation',
          biomarkers: ['crp', 'esr'],
          status: 'critical',
          score: 45,
          description: 'Inflammation cluster',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
    });

    it('should filter by category', () => {
      useClusterStore.getState().setFilters({ category: 'metabolic' });
      const filtered = useClusterStore.getState().getFilteredClusters();

      expect(filtered).toHaveLength(1);
      expect(filtered[0].category).toBe('metabolic');
    });

    it('should filter by status', () => {
      useClusterStore.getState().setFilters({ status: 'warning' });
      const filtered = useClusterStore.getState().getFilteredClusters();

      expect(filtered).toHaveLength(1);
      expect(filtered[0].status).toBe('warning');
    });

    it('should filter by search term', () => {
      useClusterStore.getState().setFilters({ search: 'cardio' });
      const filtered = useClusterStore.getState().getFilteredClusters();

      expect(filtered).toHaveLength(1);
      expect(filtered[0].name).toBe('Cardiovascular');
    });

    it('should combine multiple filters', () => {
      useClusterStore.getState().setFilters({
        category: 'metabolic',
        status: 'normal',
        search: 'health',
      });
      const filtered = useClusterStore.getState().getFilteredClusters();

      expect(filtered).toHaveLength(1);
      expect(filtered[0].name).toBe('Metabolic Health');
    });

    it('should return all clusters when no filters', () => {
      useClusterStore.getState().setFilters({
        category: 'all',
        status: 'all',
        search: '',
      });
      const filtered = useClusterStore.getState().getFilteredClusters();

      expect(filtered).toHaveLength(3);
    });
  });

  describe('Sorting', () => {
    beforeEach(() => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Zebra Cluster',
          category: 'metabolic',
          biomarkers: ['glucose'],
          status: 'normal',
          score: 85,
          description: 'Z cluster',
        },
        {
          id: 'cluster-2',
          name: 'Alpha Cluster',
          category: 'cardiovascular',
          biomarkers: ['cholesterol'],
          status: 'warning',
          score: 65,
          description: 'A cluster',
        },
        {
          id: 'cluster-3',
          name: 'Beta Cluster',
          category: 'inflammation',
          biomarkers: ['crp'],
          status: 'critical',
          score: 45,
          description: 'B cluster',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
    });

    it('should sort by name ascending', () => {
      useClusterStore.getState().setSort({ field: 'name', direction: 'asc' });
      const sorted = useClusterStore.getState().getSortedClusters();

      expect(sorted[0].name).toBe('Alpha Cluster');
      expect(sorted[1].name).toBe('Beta Cluster');
      expect(sorted[2].name).toBe('Zebra Cluster');
    });

    it('should sort by name descending', () => {
      useClusterStore.getState().setSort({ field: 'name', direction: 'desc' });
      const sorted = useClusterStore.getState().getSortedClusters();

      expect(sorted[0].name).toBe('Zebra Cluster');
      expect(sorted[1].name).toBe('Beta Cluster');
      expect(sorted[2].name).toBe('Alpha Cluster');
    });

    it('should sort by score ascending', () => {
      useClusterStore.getState().setSort({ field: 'score', direction: 'asc' });
      const sorted = useClusterStore.getState().getSortedClusters();

      expect(sorted[0].score).toBe(45);
      expect(sorted[1].score).toBe(65);
      expect(sorted[2].score).toBe(85);
    });

    it('should sort by score descending', () => {
      useClusterStore.getState().setSort({ field: 'score', direction: 'desc' });
      const sorted = useClusterStore.getState().getSortedClusters();

      expect(sorted[0].score).toBe(85);
      expect(sorted[1].score).toBe(65);
      expect(sorted[2].score).toBe(45);
    });
  });

  describe('Pagination', () => {
    beforeEach(() => {
      const clusters = Array.from({ length: 25 }, (_, i) => ({
        id: `cluster-${i}`,
        name: `Cluster ${i}`,
        category: 'metabolic',
        biomarkers: ['glucose'],
        status: 'normal',
        score: 80,
        description: `Cluster ${i} description`,
      }));

      useClusterStore.getState().setClusters(clusters);
    });

    it('should paginate clusters correctly', () => {
      useClusterStore.getState().setPagination({ page: 1, perPage: 10, total: 25 });
      const paginated = useClusterStore.getState().getPaginatedClusters();

      expect(paginated).toHaveLength(10);
      expect(paginated[0].name).toBe('Cluster 0');
      expect(paginated[9].name).toBe('Cluster 9');
    });

    it('should handle second page', () => {
      useClusterStore.getState().setPagination({ page: 2, perPage: 10, total: 25 });
      const paginated = useClusterStore.getState().getPaginatedClusters();

      expect(paginated).toHaveLength(10);
      expect(paginated[0].name).toBe('Cluster 10');
      expect(paginated[9].name).toBe('Cluster 19');
    });

    it('should handle last page with fewer items', () => {
      useClusterStore.getState().setPagination({ page: 3, perPage: 10, total: 25 });
      const paginated = useClusterStore.getState().getPaginatedClusters();

      expect(paginated).toHaveLength(5);
      expect(paginated[0].name).toBe('Cluster 20');
      expect(paginated[4].name).toBe('Cluster 24');
    });
  });

  describe('Complex Actions', () => {
    it('should load clusters with pagination', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic Health',
          category: 'metabolic',
          biomarkers: ['glucose', 'insulin'],
          status: 'normal',
          score: 85,
          description: 'Metabolic health cluster',
        },
      ];

      useClusterStore.getState().loadClusters(clusters, 1, 10, 1);

      const state = useClusterStore.getState();
      expect(state.clusters).toEqual(clusters);
      expect(state.pagination).toEqual({
        page: 1,
        perPage: 10,
        total: 1,
      });
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });

    it('should select cluster and load clusterInsights', () => {
      const clusterId = 'cluster-1';
      const clusterInsights = [
        {
          id: 'insight-1',
          cluster_id: clusterId,
          type: 'recommendation',
          title: 'Improve glucose control',
          description: 'Focus on diet and exercise',
          priority: 'high',
          actionable: true,
        },
      ];

      useClusterStore.getState().selectCluster(clusterId, clusterInsights);

      const state = useClusterStore.getState();
      expect(state.selectedCluster).toBe(clusterId);
      expect(state.clusterInsights).toEqual(clusterInsights);
    });

    it('should clear clusters', () => {
      // Set some data first
      useClusterStore.getState().setClusters([
        {
          id: 'cluster-1',
          name: 'Test Cluster',
          category: 'metabolic',
          biomarkers: ['glucose'],
          status: 'normal',
          score: 85,
          description: 'Test cluster',
        },
      ]);
      useClusterStore.getState().setSelectedCluster('cluster-1');
      useClusterStore.getState().setClusterInsights([]);

      useClusterStore.getState().clearClusters();

      const state = useClusterStore.getState();
      expect(state.clusters).toEqual([]);
      expect(state.selectedCluster).toBeNull();
      expect(state.clusterInsights).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });
  });

  describe('Utility Functions', () => {
    beforeEach(() => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic Health',
          category: 'metabolic',
          biomarkers: ['glucose', 'insulin'],
          status: 'normal',
          score: 85,
          description: 'Metabolic health cluster',
        },
        {
          id: 'cluster-2',
          name: 'Cardiovascular',
          category: 'cardiovascular',
          biomarkers: ['cholesterol', 'ldl'],
          status: 'warning',
          score: 65,
          description: 'Cardiovascular health cluster',
        },
        {
          id: 'cluster-3',
          name: 'Inflammation',
          category: 'inflammation',
          biomarkers: ['crp', 'esr'],
          status: 'critical',
          score: 45,
          description: 'Inflammation cluster',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
    });

    it('should get cluster categories', () => {
      const categories = useClusterStore.getState().getClusterCategories();

      expect(categories).toEqual(['metabolic', 'cardiovascular', 'inflammation']);
    });

    it('should get cluster summary', () => {
      const summary = useClusterStore.getState().getClusterSummary();

      expect(summary).toEqual({
        total: 3,
        byCategory: {
          metabolic: 1,
          cardiovascular: 1,
          inflammation: 1,
        },
        byStatus: {
          normal: 1,
          warning: 1,
          critical: 1,
        },
        averageScore: 65,
      });
    });

    it('should get clusterInsights for cluster', () => {
      const clusterInsights = [
        {
          id: 'insight-1',
          cluster_id: 'cluster-1',
          type: 'recommendation',
          title: 'Improve glucose control',
          description: 'Focus on diet and exercise',
          priority: 'high',
          actionable: true,
        },
        {
          id: 'insight-2',
          cluster_id: 'cluster-2',
          type: 'warning',
          title: 'Cholesterol warning',
          description: 'Monitor cholesterol levels',
          priority: 'medium',
          actionable: true,
        },
      ];

      useClusterStore.getState().setClusterInsights(clusterInsights);

      const insightsForCluster = useClusterStore.getState().getInsightsForCluster('cluster-1');
      expect(insightsForCluster).toHaveLength(1);
      expect(insightsForCluster[0].cluster_id).toBe('cluster-1');
    });

    it('should get actionable clusterInsights', () => {
      const clusterInsights = [
        {
          id: 'insight-1',
          cluster_id: 'cluster-1',
          type: 'recommendation',
          title: 'Improve glucose control',
          description: 'Focus on diet and exercise',
          priority: 'high',
          actionable: true,
        },
        {
          id: 'insight-2',
          cluster_id: 'cluster-2',
          type: 'warning',
          title: 'Cholesterol warning',
          description: 'Monitor cholesterol levels',
          priority: 'medium',
          actionable: false,
        },
      ];

      useClusterStore.getState().setClusterInsights(clusterInsights);

      const actionableInsights = useClusterStore.getState().getActionableInsights();
      expect(actionableInsights).toHaveLength(1);
      expect(actionableInsights[0].actionable).toBe(true);
    });
  });
});
