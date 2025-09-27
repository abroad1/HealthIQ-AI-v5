/**
 * UI Store Tests
 * Tests for frontend/app/state/uiStore.ts
 */

import { useUIStore } from '../../app/state/uiStore';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('UIStore', () => {
  beforeEach(() => {
    // Reset store state
    useUIStore.getState().resetUI();
    jest.clearAllMocks();
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = useUIStore.getState();

      expect(state.layout).toEqual({
        sidebarOpen: false,
        headerHeight: 64,
        footerHeight: 48,
      });
      expect(state.theme).toBe('dark');
      expect(state.viewport).toEqual({
        width: 0,
        height: 0,
        isMobile: false,
        isTablet: false,
        isDesktop: false,
      });
      expect(state.preferences).toEqual({
        language: 'en',
        timezone: 'UTC',
        dateFormat: 'YYYY-MM-DD',
        numberFormat: 'en-US',
        notifications: {
          email: true,
          push: true,
          sms: false,
        },
      });
      expect(state.notifications).toEqual([]);
      expect(state.modals).toEqual([]);
      expect(state.toasts).toEqual([]);
      expect(state.loading).toEqual({});
      expect(state.errors).toEqual({});
    });
  });

  describe('Layout Actions', () => {
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

    it('should update layout', () => {
      const newLayout = {
        sidebarOpen: true,
        headerHeight: 80,
        footerHeight: 60,
      };

      useUIStore.getState().updateLayout(newLayout);
      expect(useUIStore.getState().layout).toEqual(newLayout);
    });
  });

  describe('Theme Actions', () => {
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

    it('should persist theme to localStorage', () => {
      useUIStore.getState().setTheme('light');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_theme', 'light');
    });
  });

  describe('Viewport Actions', () => {
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

    it('should detect mobile viewport', () => {
      const viewport = {
        width: 375,
        height: 667,
        isMobile: true,
        isTablet: false,
        isDesktop: false,
      };

      useUIStore.getState().updateViewport(viewport);
      expect(useUIStore.getState().viewport.isMobile).toBe(true);
    });

    it('should detect tablet viewport', () => {
      const viewport = {
        width: 768,
        height: 1024,
        isMobile: false,
        isTablet: true,
        isDesktop: false,
      };

      useUIStore.getState().updateViewport(viewport);
      expect(useUIStore.getState().viewport.isTablet).toBe(true);
    });
  });

  describe('Preferences Actions', () => {
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

    it('should persist preferences to localStorage', () => {
      const preferences = {
        language: 'fr',
        timezone: 'Europe/Paris',
        dateFormat: 'DD/MM/YYYY',
        numberFormat: 'fr-FR',
        notifications: {
          email: true,
          push: false,
          sms: false,
        },
      };

      useUIStore.getState().updatePreferences(preferences);
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'healthiq_preferences',
        JSON.stringify(preferences)
      );
    });
  });

  describe('Notification Actions', () => {
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
  });

  describe('Modal Actions', () => {
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

    it('should close all modals', () => {
      useUIStore.getState().openModal({
        id: 'modal-1',
        type: 'confirmation',
        title: 'Modal 1',
        content: 'Content 1',
        actions: [],
      });
      useUIStore.getState().openModal({
        id: 'modal-2',
        type: 'info',
        title: 'Modal 2',
        content: 'Content 2',
        actions: [],
      });

      expect(useUIStore.getState().modals).toHaveLength(2);

      useUIStore.getState().closeAllModals();
      expect(useUIStore.getState().modals).toHaveLength(0);
    });
  });

  describe('Toast Actions', () => {
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

    it('should clear all toasts', () => {
      useUIStore.getState().showToast({
        id: 'toast-1',
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
      });
      useUIStore.getState().showToast({
        id: 'toast-2',
        type: 'error',
        title: 'Error',
        message: 'Operation failed',
        duration: 5000,
      });

      expect(useUIStore.getState().toasts).toHaveLength(2);

      useUIStore.getState().clearToasts();
      expect(useUIStore.getState().toasts).toHaveLength(0);
    });
  });

  describe('Loading Actions', () => {
    it('should set loading state', () => {
      useUIStore.getState().setLoading('analysis', true);
      expect(useUIStore.getState().loading.analysis).toBe(true);

      useUIStore.getState().setLoading('analysis', false);
      expect(useUIStore.getState().loading.analysis).toBe(false);
    });

    it('should set multiple loading states', () => {
      useUIStore.getState().setLoading('analysis', true);
      useUIStore.getState().setLoading('clusters', true);
      useUIStore.getState().setLoading('reports', false);

      const state = useUIStore.getState();
      expect(state.loading.analysis).toBe(true);
      expect(state.loading.clusters).toBe(true);
      expect(state.loading.reports).toBe(false);
    });

    it('should clear loading state', () => {
      useUIStore.getState().setLoading('analysis', true);
      useUIStore.getState().setLoading('clusters', true);

      useUIStore.getState().clearLoading('analysis');
      expect(useUIStore.getState().loading.analysis).toBeUndefined();
      expect(useUIStore.getState().loading.clusters).toBe(true);
    });

    it('should clear all loading states', () => {
      useUIStore.getState().setLoading('analysis', true);
      useUIStore.getState().setLoading('clusters', true);

      useUIStore.getState().clearAllLoading();
      expect(useUIStore.getState().loading).toEqual({});
    });
  });

  describe('Error Actions', () => {
    it('should set error state', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      expect(useUIStore.getState().errors.analysis).toBe('Analysis failed');

      useUIStore.getState().setError('analysis', null);
      expect(useUIStore.getState().errors.analysis).toBeUndefined();
    });

    it('should set multiple error states', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      useUIStore.getState().setError('clusters', 'Clusters failed');

      const state = useUIStore.getState();
      expect(state.errors.analysis).toBe('Analysis failed');
      expect(state.errors.clusters).toBe('Clusters failed');
    });

    it('should clear error state', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      useUIStore.getState().setError('clusters', 'Clusters failed');

      useUIStore.getState().clearError('analysis');
      expect(useUIStore.getState().errors.analysis).toBeUndefined();
      expect(useUIStore.getState().errors.clusters).toBe('Clusters failed');
    });

    it('should clear all error states', () => {
      useUIStore.getState().setError('analysis', 'Analysis failed');
      useUIStore.getState().setError('clusters', 'Clusters failed');

      useUIStore.getState().clearAllErrors();
      expect(useUIStore.getState().errors).toEqual({});
    });
  });

  describe('Utility Functions', () => {
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

    it('should reset UI', () => {
      // Set some state
      useUIStore.getState().setSidebarOpen(true);
      useUIStore.getState().setTheme('light');
      useUIStore.getState().setLoading('analysis', true);
      useUIStore.getState().setError('analysis', 'Error');

      useUIStore.getState().resetUI();

      const state = useUIStore.getState();
      expect(state.layout.sidebarOpen).toBe(false);
      expect(state.theme).toBe('dark');
      expect(state.loading).toEqual({});
      expect(state.errors).toEqual({});
    });
  });
});
