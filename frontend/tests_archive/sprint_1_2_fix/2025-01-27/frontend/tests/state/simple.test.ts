// ARCHIVED TEST
// Reason: Medium-value test (duplicate coverage of state stores)
// Archived: 2025-01-27
// Original Path: frontend/tests/state/simple.test.ts

/**
 * Simple State Store Tests
 * Basic tests for frontend state stores to achieve coverage
 */

import { useAnalysisStore } from '../../../../app/state/analysisStore';
import { useClusterStore } from '../../../../app/state/clusterStore';
import { useUIStore } from '../../../../app/state/uiStore';

describe('Frontend State Stores', () => {
  beforeEach(() => {
    // Reset all stores
    useAnalysisStore.getState().clearAnalysis();
    useClusterStore.getState().clearClusters();
    // UI store doesn't have a clear method, so we'll test individual setters
  });

  describe('AnalysisStore', () => {
    it('should have correct initial state', () => {
      const state = useAnalysisStore.getState();

      expect(state.currentAnalysis).toBeNull();
      expect(state.analysisHistory).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.currentPhase).toBe('idle');
      expect(state.progress).toBe(0);
    });

    it('should set current analysis', () => {
      const analysis = {
        analysis_id: 'test-123',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
      };

      useAnalysisStore.getState().setCurrentAnalysis(analysis);
      expect(useAnalysisStore.getState().currentAnalysis).toEqual(analysis);
    });

    it('should set loading state', () => {
      useAnalysisStore.getState().setLoading(true);
      expect(useAnalysisStore.getState().isLoading).toBe(true);

      useAnalysisStore.getState().setLoading(false);
      expect(useAnalysisStore.getState().isLoading).toBe(false);
    });

    it('should set error', () => {
      const error = {
        message: 'Test error',
        code: 'TEST_ERROR',
        details: null,
      };

      useAnalysisStore.getState().setError(error);
      expect(useAnalysisStore.getState().error).toEqual(error);
    });

    it('should set phase', () => {
      useAnalysisStore.getState().setPhase('processing');
      expect(useAnalysisStore.getState().currentPhase).toBe('processing');
    });

    it('should set progress', () => {
      useAnalysisStore.getState().setProgress(50);
      expect(useAnalysisStore.getState().progress).toBe(50);
    });

    it('should set raw biomarkers', () => {
      const biomarkers = {
        cholesterol: { value: 4.9, unit: 'mmol/L' },
        glucose: { value: 5.2, unit: 'mmol/L' },
      };

      useAnalysisStore.getState().setRawBiomarkers(biomarkers);
      expect(useAnalysisStore.getState().rawBiomarkers).toEqual(biomarkers);
    });

    it('should set normalized biomarkers', () => {
      const biomarkers = {
        cholesterol: { value: 4.9, unit: 'mmol/L' },
        glucose: { value: 5.2, unit: 'mmol/L' },
      };

      useAnalysisStore.getState().setNormalizedBiomarkers(biomarkers);
      expect(useAnalysisStore.getState().normalizedBiomarkers).toEqual(biomarkers);
    });

    it('should set user profile', () => {
      const profile = {
        age: 35,
        sex: 'male' as const,
        weight: 75,
        height: 180,
      };

      useAnalysisStore.getState().setUserProfile(profile);
      expect(useAnalysisStore.getState().userProfile).toEqual(profile);
    });

    it('should add to history', () => {
      const analysis = {
        analysis_id: 'test-123',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
        results: {
          clusters: [],
          insights: [],
          overall_score: 85,
          risk_assessment: {},
          recommendations: [],
        },
      };

      useAnalysisStore.getState().addToHistory(analysis);
      expect(useAnalysisStore.getState().analysisHistory).toHaveLength(1);
      expect(useAnalysisStore.getState().analysisHistory[0]).toEqual(analysis);
    });

    it('should get analysis by id', () => {
      const analysis = {
        analysis_id: 'test-123',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
      };

      useAnalysisStore.getState().addToHistory(analysis);
      const found = useAnalysisStore.getState().getAnalysisById('test-123');
      expect(found).toEqual(analysis);
    });

    it('should get recent analyses', () => {
      const analysis1 = {
        analysis_id: 'test-1',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
      };
      const analysis2 = {
        analysis_id: 'test-2',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
      };

      useAnalysisStore.getState().addToHistory(analysis1);
      useAnalysisStore.getState().addToHistory(analysis2);

      const recent = useAnalysisStore.getState().getRecentAnalyses(1);
      expect(recent).toHaveLength(1);
      expect(recent[0]).toEqual(analysis2);
    });

    it('should check if analysis is complete', () => {
      expect(useAnalysisStore.getState().isAnalysisComplete()).toBe(false);

      useAnalysisStore.getState().setCurrentAnalysis({
        analysis_id: 'test-123',
        status: 'completed',
        created_at: '2025-01-27T00:00:00Z',
      });

      expect(useAnalysisStore.getState().isAnalysisComplete()).toBe(true);
    });

    it('should get analysis summary', () => {
      const summary = useAnalysisStore.getState().getAnalysisSummary();
      expect(summary).toEqual({
        totalAnalyses: 0,
        completedAnalyses: 0,
        failedAnalyses: 0,
        averageScore: 0,
      });
    });

    it('should clear analysis', () => {
      useAnalysisStore.getState().setCurrentAnalysis({
        analysis_id: 'test',
        status: 'processing',
        created_at: '2025-01-27T00:00:00Z',
      });
      useAnalysisStore.getState().setLoading(true);
      useAnalysisStore.getState().setError({
        message: 'test error',
        code: 'TEST_ERROR',
        details: null,
      });

      useAnalysisStore.getState().clearAnalysis();

      const state = useAnalysisStore.getState();
      expect(state.currentAnalysis).toBeNull();
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.currentPhase).toBe('idle');
      expect(state.progress).toBe(0);
    });
  });

  describe('ClusterStore', () => {
    it('should have correct initial state', () => {
      const state = useClusterStore.getState();

      expect(state.clusters).toEqual([]);
      expect(state.selectedCluster).toBeNull();
      expect(state.clusterInsights).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });

    it('should set clusters', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic Health',
          description: 'Metabolic health cluster',
          biomarkers: ['glucose', 'insulin'],
          score: 0.85,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal glucose metabolism'],
          recommendations: ['Maintain current lifestyle'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
      expect(useClusterStore.getState().clusters).toEqual(clusters);
    });

    it('should set selected cluster', () => {
      const cluster = {
        id: 'cluster-1',
        name: 'Metabolic Health',
        description: 'Metabolic health cluster',
        biomarkers: ['glucose'],
        score: 0.85,
        risk_level: 'low' as const,
        category: 'metabolic',
        insights: ['Normal glucose metabolism'],
        recommendations: ['Maintain current lifestyle'],
        created_at: '2025-01-27T00:00:00Z',
      };

      useClusterStore.getState().setSelectedCluster(cluster);
      expect(useClusterStore.getState().selectedCluster).toEqual(cluster);
    });

    it('should set cluster insights', () => {
      const insights = [
        {
          id: 'insight-1',
          cluster_id: 'cluster-1',
          type: 'pattern' as const,
          title: 'Glucose Pattern',
          description: 'Normal glucose metabolism',
          confidence: 0.9,
          severity: 'low' as const,
          biomarkers_involved: ['glucose'],
          recommendations: ['Maintain current lifestyle'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ];

      useClusterStore.getState().setClusterInsights(insights);
      expect(useClusterStore.getState().clusterInsights).toEqual(insights);
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

    it('should set filters', () => {
      const filters = {
        risk_level: ['low', 'medium'],
        category: ['metabolic'],
      };

      useClusterStore.getState().setFilters(filters);
      expect(useClusterStore.getState().filters).toEqual(filters);
    });

    it('should clear filters', () => {
      useClusterStore.getState().setFilters({ risk_level: ['low'] });
      useClusterStore.getState().clearFilters();
      expect(useClusterStore.getState().filters).toEqual({});
    });

    it('should set sort', () => {
      const sort = { field: 'score' as const, direction: 'desc' as const };
      useClusterStore.getState().setSort(sort);
      expect(useClusterStore.getState().sort).toEqual(sort);
    });

    it('should set search query', () => {
      const query = 'metabolic';
      useClusterStore.getState().setSearchQuery(query);
      expect(useClusterStore.getState().searchQuery).toBe(query);
    });

    it('should set current page', () => {
      useClusterStore.getState().setCurrentPage(2);
      expect(useClusterStore.getState().currentPage).toBe(2);
    });

    it('should set items per page', () => {
      useClusterStore.getState().setItemsPerPage(20);
      expect(useClusterStore.getState().itemsPerPage).toBe(20);
    });

    it('should get cluster by id', () => {
      const cluster = {
        id: 'cluster-1',
        name: 'Metabolic Health',
        description: 'Metabolic health cluster',
        biomarkers: ['glucose'],
        score: 0.85,
        risk_level: 'low' as const,
        category: 'metabolic',
        insights: ['Normal glucose metabolism'],
        recommendations: ['Maintain current lifestyle'],
        created_at: '2025-01-27T00:00:00Z',
      };

      useClusterStore.getState().setClusters([cluster]);
      const found = useClusterStore.getState().getClusterById('cluster-1');
      expect(found).toEqual(cluster);
    });

    it('should get clusters by risk level', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Low Risk',
          description: 'Low risk cluster',
          biomarkers: ['glucose'],
          score: 0.9,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal'],
          recommendations: ['Maintain'],
          created_at: '2025-01-27T00:00:00Z',
        },
        {
          id: 'cluster-2',
          name: 'High Risk',
          description: 'High risk cluster',
          biomarkers: ['cholesterol'],
          score: 0.3,
          risk_level: 'high' as const,
          category: 'cardiovascular',
          insights: ['Elevated'],
          recommendations: ['Monitor'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
      const lowRisk = useClusterStore.getState().getClustersByRiskLevel('low');
      expect(lowRisk).toHaveLength(1);
      expect(lowRisk[0].risk_level).toBe('low');
    });

    it('should get clusters by category', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic',
          description: 'Metabolic cluster',
          biomarkers: ['glucose'],
          score: 0.9,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal'],
          recommendations: ['Maintain'],
          created_at: '2025-01-27T00:00:00Z',
        },
        {
          id: 'cluster-2',
          name: 'Cardiovascular',
          description: 'Cardiovascular cluster',
          biomarkers: ['cholesterol'],
          score: 0.3,
          risk_level: 'high' as const,
          category: 'cardiovascular',
          insights: ['Elevated'],
          recommendations: ['Monitor'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
      const metabolic = useClusterStore.getState().getClustersByCategory('metabolic');
      expect(metabolic).toHaveLength(1);
      expect(metabolic[0].category).toBe('metabolic');
    });

    it('should get high risk clusters', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Low Risk',
          description: 'Low risk cluster',
          biomarkers: ['glucose'],
          score: 0.9,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal'],
          recommendations: ['Maintain'],
          created_at: '2025-01-27T00:00:00Z',
        },
        {
          id: 'cluster-2',
          name: 'High Risk',
          description: 'High risk cluster',
          biomarkers: ['cholesterol'],
          score: 0.3,
          risk_level: 'high' as const,
          category: 'cardiovascular',
          insights: ['Elevated'],
          recommendations: ['Monitor'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
      const highRisk = useClusterStore.getState().getHighRiskClusters();
      expect(highRisk).toHaveLength(1);
      expect(highRisk[0].risk_level).toBe('high');
    });

    it('should get cluster summary', () => {
      const clusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic',
          description: 'Metabolic cluster',
          biomarkers: ['glucose'],
          score: 0.9,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal'],
          recommendations: ['Maintain'],
          created_at: '2025-01-27T00:00:00Z',
        },
        {
          id: 'cluster-2',
          name: 'Cardiovascular',
          description: 'Cardiovascular cluster',
          biomarkers: ['cholesterol'],
          score: 0.3,
          risk_level: 'high' as const,
          category: 'cardiovascular',
          insights: ['Elevated'],
          recommendations: ['Monitor'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ];

      useClusterStore.getState().setClusters(clusters);
      const summary = useClusterStore.getState().getClusterSummary();
      expect(summary.totalClusters).toBe(2);
      expect(summary.highRiskClusters).toBe(1);
      expect(summary.averageScore).toBe(0.6);
      expect(summary.categories).toContain('metabolic');
      expect(summary.categories).toContain('cardiovascular');
    });

    it('should clear clusters', () => {
      useClusterStore.getState().setClusters([
        {
          id: 'cluster-1',
          name: 'Test Cluster',
          description: 'Test cluster',
          biomarkers: ['glucose'],
          score: 0.9,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal'],
          recommendations: ['Maintain'],
          created_at: '2025-01-27T00:00:00Z',
        },
      ]);
      useClusterStore.getState().setSelectedCluster({
        id: 'cluster-1',
        name: 'Test Cluster',
        description: 'Test cluster',
        biomarkers: ['glucose'],
        score: 0.9,
        risk_level: 'low' as const,
        category: 'metabolic',
        insights: ['Normal'],
        recommendations: ['Maintain'],
        created_at: '2025-01-27T00:00:00Z',
      });

      useClusterStore.getState().clearClusters();

      const state = useClusterStore.getState();
      expect(state.clusters).toEqual([]);
      expect(state.selectedCluster).toBeNull();
      expect(state.clusterInsights).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });
  });

  describe('UIStore', () => {
    it('should have correct initial state', () => {
      const state = useUIStore.getState();

      expect(state.layout.sidebarOpen).toBe(false);
      expect(state.theme).toBe('dark');
      expect(state.viewport.width).toBe(0);
      expect(state.viewport.height).toBe(0);
      expect(state.preferences.language).toBe('en');
      expect(state.notifications).toEqual([]);
      expect(state.modals).toEqual([]);
      expect(state.toasts).toEqual([]);
      expect(state.loading).toEqual({});
      expect(state.errors).toEqual({});
    });

    it('should toggle sidebar', () => {
      const store = useUIStore.getState();
      
      expect(store.layout.sidebarOpen).toBe(false);
      
      store.toggleSidebar();
      expect(store.layout.sidebarOpen).toBe(true);
      
      store.toggleSidebar();
      expect(store.layout.sidebarOpen).toBe(false);
    });

    it('should set sidebar state', () => {
      useUIStore.getState().setSidebarOpen(true);
      expect(useUIStore.getState().layout.sidebarOpen).toBe(true);

      useUIStore.getState().setSidebarOpen(false);
      expect(useUIStore.getState().layout.sidebarOpen).toBe(false);
    });

    it('should toggle theme', () => {
      const store = useUIStore.getState();
      
      expect(store.theme).toBe('dark');
      
      store.toggleTheme();
      expect(store.theme).toBe('light');
      
      store.toggleTheme();
      expect(store.theme).toBe('dark');
    });

    it('should set theme', () => {
      useUIStore.getState().setTheme('light');
      expect(useUIStore.getState().theme).toBe('light');

      useUIStore.getState().setTheme('dark');
      expect(useUIStore.getState().theme).toBe('dark');
    });

    it('should update viewport', () => {
      const viewport = {
        width: 1920,
        height: 1080,
        isMobile: false,
        isTablet: false,
        isDesktop: true,
      };

      useUIStore.getState().updateViewport(viewport);
      expect(useUIStore.getState().viewport).toEqual(viewport);
    });

    it('should update preferences', () => {
      const preferences = {
        language: 'es',
        timezone: 'America/New_York',
        dateFormat: 'MM/DD/YYYY',
        numberFormat: 'es-ES',
        notifications: {
          email: false,
          push: true,
          sms: true,
        },
      };

      useUIStore.getState().updatePreferences(preferences);
      expect(useUIStore.getState().preferences).toEqual(preferences);
    });

    it('should add notification', () => {
      const notification = {
        id: 'notif-1',
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        timestamp: '2025-01-27T00:00:00Z',
      };

      useUIStore.getState().addNotification(notification);
      expect(useUIStore.getState().notifications).toHaveLength(1);
      expect(useUIStore.getState().notifications[0]).toEqual(notification);
    });

    it('should remove notification', () => {
      const notification = {
        id: 'notif-1',
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        timestamp: '2025-01-27T00:00:00Z',
      };

      useUIStore.getState().addNotification(notification);
      expect(useUIStore.getState().notifications).toHaveLength(1);

      useUIStore.getState().removeNotification('notif-1');
      expect(useUIStore.getState().notifications).toHaveLength(0);
    });

    it('should clear all notifications', () => {
      useUIStore.getState().addNotification({
        id: 'notif-1',
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        timestamp: '2025-01-27T00:00:00Z',
      });
      useUIStore.getState().addNotification({
        id: 'notif-2',
        type: 'error',
        title: 'Error',
        message: 'Operation failed',
        duration: 5000,
        timestamp: '2025-01-27T00:00:00Z',
      });

      expect(useUIStore.getState().notifications).toHaveLength(2);

      useUIStore.getState().clearNotifications();
      expect(useUIStore.getState().notifications).toHaveLength(0);
    });

    it('should open modal', () => {
      const modal = {
        id: 'modal-1',
        type: 'confirmation',
        title: 'Confirm Action',
        content: 'Are you sure?',
        actions: [
          { label: 'Cancel', action: 'cancel' },
          { label: 'Confirm', action: 'confirm' },
        ],
      };

      useUIStore.getState().openModal(modal);
      expect(useUIStore.getState().modals).toHaveLength(1);
      expect(useUIStore.getState().modals[0]).toEqual(modal);
    });

    it('should close modal', () => {
      const modal = {
        id: 'modal-1',
        type: 'confirmation',
        title: 'Confirm Action',
        content: 'Are you sure?',
        actions: [],
      };

      useUIStore.getState().openModal(modal);
      expect(useUIStore.getState().modals).toHaveLength(1);

      useUIStore.getState().closeModal('modal-1');
      expect(useUIStore.getState().modals).toHaveLength(0);
    });

    it('should show toast', () => {
      const toast = {
        id: 'toast-1',
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
      };

      useUIStore.getState().showToast(toast);
      expect(useUIStore.getState().toasts).toHaveLength(1);
      expect(useUIStore.getState().toasts[0]).toEqual(toast);
    });

    it('should hide toast', () => {
      const toast = {
        id: 'toast-1',
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
      };

      useUIStore.getState().showToast(toast);
      expect(useUIStore.getState().toasts).toHaveLength(1);

      useUIStore.getState().hideToast('toast-1');
      expect(useUIStore.getState().toasts).toHaveLength(0);
    });

    it('should set loading state', () => {
      useUIStore.getState().setLoading('analysis', true);
      expect(useUIStore.getState().loading.analysis).toBe(true);

      useUIStore.getState().setLoading('analysis', false);
      expect(useUIStore.getState().loading.analysis).toBe(false);
    });

    it('should set error state', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      expect(useUIStore.getState().errors.analysis).toBe('Analysis failed');

      useUIStore.getState().setError('analysis', null);
      expect(useUIStore.getState().errors.analysis).toBeUndefined();
    });

    it('should check if loading', () => {
      useUIStore.getState().setLoading('analysis', true);
      expect(useUIStore.getState().isLoading('analysis')).toBe(true);
      expect(useUIStore.getState().isLoading('clusters')).toBe(false);
    });

    it('should check if has error', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      expect(useUIStore.getState().hasError('analysis')).toBe(true);
      expect(useUIStore.getState().hasError('clusters')).toBe(false);
    });

    it('should get error message', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      expect(useUIStore.getState().getError('analysis')).toBe('Analysis failed');
      expect(useUIStore.getState().getError('clusters')).toBeUndefined();
    });
  });
});
