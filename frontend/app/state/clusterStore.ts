import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

// Cluster-related types
export interface BiomarkerCluster {
  id: string;
  name: string;
  description: string;
  biomarkers: string[];
  score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  insights: string[];
  recommendations: string[];
  created_at: string;
}

export interface ClusterInsight {
  id: string;
  cluster_id: string;
  type: 'pattern' | 'anomaly' | 'trend' | 'correlation';
  title: string;
  description: string;
  confidence: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  biomarkers_involved: string[];
  recommendations: string[];
  created_at: string;
}

export interface ClusterFilter {
  risk_level?: string[];
  category?: string[];
  score_range?: [number, number];
  biomarkers?: string[];
}

export interface ClusterSort {
  field: 'score' | 'risk_level' | 'created_at' | 'name';
  direction: 'asc' | 'desc';
}

interface ClusterState {
  // Cluster data
  clusters: BiomarkerCluster[];
  selectedCluster: BiomarkerCluster | null;
  clusterInsights: ClusterInsight[];
  
  // UI state
  isLoading: boolean;
  error: string | null;
  
  // Filtering and sorting
  filters: ClusterFilter;
  sort: ClusterSort;
  searchQuery: string;
  
  // Pagination
  currentPage: number;
  itemsPerPage: number;
  totalItems: number;
  
  // Actions
  setClusters: (clusters: BiomarkerCluster[]) => void;
  setSelectedCluster: (cluster: BiomarkerCluster | null) => void;
  setClusterInsights: (insights: ClusterInsight[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Filtering and sorting
  setFilters: (filters: Partial<ClusterFilter>) => void;
  clearFilters: () => void;
  setSort: (sort: ClusterSort) => void;
  setSearchQuery: (query: string) => void;
  
  // Pagination
  setCurrentPage: (page: number) => void;
  setItemsPerPage: (items: number) => void;
  setPagination: (pagination: { page: number; perPage: number; total: number }) => void;
  
  // Complex actions
  loadClusters: (analysisId: string) => Promise<void>;
  selectClusterById: (clusterId: string) => void;
  selectCluster: (clusterId: string, clusterInsights: ClusterInsight[]) => void;
  getClusterInsights: (clusterId: string) => ClusterInsight[];
  getFilteredClusters: () => BiomarkerCluster[];
  getPaginatedClusters: () => BiomarkerCluster[];
  getSortedClusters: () => BiomarkerCluster[];
  
  // Utility actions
  getClusterById: (clusterId: string) => BiomarkerCluster | undefined;
  getClustersByRiskLevel: (riskLevel: string) => BiomarkerCluster[];
  getClustersByCategory: (category: string) => BiomarkerCluster[];
  getHighRiskClusters: () => BiomarkerCluster[];
  getClusterSummary: () => {
    totalClusters: number;
    highRiskClusters: number;
    averageScore: number;
    categories: string[];
  };
  getClusterCategories: () => string[];
  getInsightsForCluster: (clusterId: string) => ClusterInsight[];
  getActionableInsights: () => ClusterInsight[];
  
  // Analysis integration
  updateClustersFromAnalysis: (analysisResults: any) => void;
  clearClusters: () => void;
}

export const useClusterStore = create<ClusterState>()(
  devtools(
    (set, get) => ({
      // Initial state
      clusters: [],
      selectedCluster: null,
      clusterInsights: [],
      isLoading: false,
      error: null,
      filters: {},
      sort: { field: 'score', direction: 'desc' },
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,

      // Basic setters
      setClusters: (clusters) => set({ 
        clusters, 
        totalItems: clusters.length 
      }),
      
      setSelectedCluster: (cluster) => set({ selectedCluster: cluster }),
      
      setClusterInsights: (insights) => set({ clusterInsights: insights }),
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (error) => set({ error }),
      
      // Filtering and sorting
      setFilters: (newFilters) => set((state) => ({
        filters: { ...state.filters, ...newFilters },
        currentPage: 1, // Reset to first page when filters change
      })),
      
      clearFilters: () => set({ 
        filters: {}, 
        currentPage: 1 
      }),
      
      setSort: (sort) => set({ sort, currentPage: 1 }),
      
      setSearchQuery: (query) => set({ 
        searchQuery: query, 
        currentPage: 1 
      }),
      
      // Pagination
      setCurrentPage: (page) => set({ currentPage: page }),
      
      setItemsPerPage: (items) => set({ 
        itemsPerPage: items, 
        currentPage: 1 
      }),

      setPagination: (pagination) => set({
        currentPage: pagination.page,
        itemsPerPage: pagination.perPage,
        totalItems: pagination.total
      }),

      // Complex actions
      loadClusters: async (analysisId) => {
        set({ isLoading: true, error: null });
        try {
          // This would typically call an API service
          // For now, we'll simulate with mock data
          const mockClusters: BiomarkerCluster[] = [
            {
              id: 'cluster_1',
              name: 'Cardiovascular Risk',
              description: 'Biomarkers related to cardiovascular health',
              biomarkers: ['total_cholesterol', 'ldl_cholesterol', 'hdl_cholesterol'],
              score: 0.75,
              risk_level: 'medium',
              category: 'cardiovascular',
              insights: ['Elevated cholesterol levels detected'],
              recommendations: ['Consider lifestyle modifications', 'Regular exercise recommended'],
              created_at: new Date().toISOString(),
            },
            {
              id: 'cluster_2',
              name: 'Metabolic Health',
              description: 'Glucose and insulin-related biomarkers',
              biomarkers: ['glucose', 'hba1c', 'insulin'],
              score: 0.90,
              risk_level: 'low',
              category: 'metabolic',
              insights: ['Normal glucose metabolism'],
              recommendations: ['Maintain current lifestyle'],
              created_at: new Date().toISOString(),
            },
          ];
          
          set({ 
            clusters: mockClusters, 
            totalItems: mockClusters.length,
            isLoading: false 
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to load clusters',
            isLoading: false 
          });
        }
      },

      selectClusterById: (clusterId) => {
        const state = get();
        const cluster = state.clusters.find(c => c.id === clusterId);
        set({ selectedCluster: cluster || null });
      },

      selectCluster: (clusterId, clusterInsights) => {
        const state = get();
        const cluster = state.clusters.find(c => c.id === clusterId);
        set({ 
          selectedCluster: cluster || null,
          clusterInsights: clusterInsights
        });
      },

      getClusterInsights: (clusterId) => {
        const state = get();
        return state.clusterInsights.filter(insight => insight.cluster_id === clusterId);
      },

      getFilteredClusters: () => {
        const state = get();
        let filtered = [...state.clusters];

        // Apply search query
        if (state.searchQuery) {
          const query = state.searchQuery.toLowerCase();
          filtered = filtered.filter(cluster =>
            cluster.name.toLowerCase().includes(query) ||
            cluster.description.toLowerCase().includes(query) ||
            cluster.biomarkers.some(biomarker => biomarker.toLowerCase().includes(query))
          );
        }

        // Apply filters
        if (state.filters.risk_level?.length) {
          filtered = filtered.filter(cluster =>
            state.filters.risk_level!.includes(cluster.risk_level)
          );
        }

        if (state.filters.category?.length) {
          filtered = filtered.filter(cluster =>
            state.filters.category!.includes(cluster.category)
          );
        }

        if (state.filters.score_range) {
          const [min, max] = state.filters.score_range;
          filtered = filtered.filter(cluster =>
            cluster.score >= min && cluster.score <= max
          );
        }

        if (state.filters.biomarkers?.length) {
          filtered = filtered.filter(cluster =>
            state.filters.biomarkers!.some(biomarker =>
              cluster.biomarkers.includes(biomarker)
            )
          );
        }

        // Apply sorting
        filtered.sort((a, b) => {
          const { field, direction } = state.sort;
          let aValue: any = a[field];
          let bValue: any = b[field];

          if (field === 'risk_level') {
            const riskOrder = { critical: 4, high: 3, medium: 2, low: 1 };
            aValue = riskOrder[a.risk_level as keyof typeof riskOrder];
            bValue = riskOrder[b.risk_level as keyof typeof riskOrder];
          }

          if (typeof aValue === 'string') {
            aValue = aValue.toLowerCase();
            bValue = bValue.toLowerCase();
          }

          if (direction === 'asc') {
            return aValue > bValue ? 1 : -1;
          } else {
            return aValue < bValue ? 1 : -1;
          }
        });

        return filtered;
      },

      getPaginatedClusters: () => {
        const state = get();
        const filtered = get().getFilteredClusters();
        const start = (state.currentPage - 1) * state.itemsPerPage;
        const end = start + state.itemsPerPage;
        return filtered.slice(start, end);
      },

      getSortedClusters: () => {
        return get().getFilteredClusters();
      },

      // Utility functions
      getClusterById: (clusterId) => {
        const state = get();
        return state.clusters.find(cluster => cluster.id === clusterId);
      },

      getClustersByRiskLevel: (riskLevel) => {
        const state = get();
        return state.clusters.filter(cluster => cluster.risk_level === riskLevel);
      },

      getClustersByCategory: (category) => {
        const state = get();
        return state.clusters.filter(cluster => cluster.category === category);
      },

      getHighRiskClusters: () => {
        const state = get();
        return state.clusters.filter(cluster => 
          cluster.risk_level === 'high' || cluster.risk_level === 'critical'
        );
      },

      getClusterSummary: () => {
        const state = get();
        const clusters = state.clusters;
        const highRisk = clusters.filter(c => 
          c.risk_level === 'high' || c.risk_level === 'critical'
        );
        const scores = clusters.map(c => c.score).filter(score => typeof score === 'number');
        const categories = Array.from(new Set(clusters.map(c => c.category)));

        return {
          totalClusters: clusters.length,
          highRiskClusters: highRisk.length,
          averageScore: scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0,
          categories,
        };
      },

      getClusterCategories: () => {
        const state = get();
        return Array.from(new Set(state.clusters.map(c => c.category)));
      },

      getInsightsForCluster: (clusterId) => {
        const state = get();
        return state.clusterInsights.filter(insight => insight.cluster_id === clusterId);
      },

      getActionableInsights: () => {
        const state = get();
        return state.clusterInsights.filter(insight => insight.severity === 'high' || insight.severity === 'critical');
      },

      // Analysis integration
      updateClustersFromAnalysis: (analysisResults) => {
        if (analysisResults?.clusters) {
          set({ clusters: analysisResults.clusters });
        }
        if (analysisResults?.insights) {
          set({ clusterInsights: analysisResults.insights });
        }
      },

      clearClusters: () => set({
        clusters: [],
        selectedCluster: null,
        clusterInsights: [],
        error: null,
        currentPage: 1,
        totalItems: 0,
      }),
    }),
    {
      name: 'cluster-store',
    }
  )
);
