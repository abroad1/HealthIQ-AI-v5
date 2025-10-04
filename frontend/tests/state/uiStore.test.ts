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
    // Clear localStorage mock
    localStorageMock.getItem.mockReturnValue(null);
    localStorageMock.setItem.mockClear();
    localStorageMock.removeItem.mockClear();
    localStorageMock.clear.mockClear();
    
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
        width: 1024, // Default when window is undefined
        height: 768,
        isMobile: false,
        isTablet: false,
        isDesktop: true,
      });
      expect(state.preferences).toEqual({
        theme: 'system',
        language: 'en',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        dateFormat: 'MM/DD/YYYY',
        timeFormat: '12h',
        notifications: {
          email: true,
          push: true,
          analysis: true,
          alerts: true,
        },
        accessibility: {
          highContrast: false,
          reducedMotion: false,
          fontSize: 'medium',
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
      
      // Check initial state
      const initialSidebarOpen = store.sidebarOpen;
      
      store.toggleSidebar();
      expect(store.sidebarOpen).toBe(!initialSidebarOpen);
      expect(store.layout.sidebarOpen).toBe(!initialSidebarOpen);
      
      store.toggleSidebar();
      expect(store.sidebarOpen).toBe(initialSidebarOpen);
      expect(store.layout.sidebarOpen).toBe(initialSidebarOpen);
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
      
      // Check initial state
      const initialTheme = store.theme;
      
      store.toggleTheme();
      expect(store.theme).toBe(initialTheme === 'dark' ? 'light' : 'dark');
      
      store.toggleTheme();
      expect(store.theme).toBe(initialTheme);
    });

    it('should set theme', () => {
      useUIStore.getState().setTheme('light');
      expect(useUIStore.getState().theme).toBe('light');

      useUIStore.getState().setTheme('dark');
      expect(useUIStore.getState().theme).toBe('dark');
    });

    it('should persist theme to localStorage', () => {
      useUIStore.getState().setTheme('light');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('ui-store', expect.stringContaining('"theme":"light"'));
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
        dateFormat: 'MM/DD/YYYY' as const,
        timeFormat: '12h' as const,
        notifications: {
          email: false,
          push: true,
          analysis: true,
          alerts: true,
        },
        accessibility: {
          highContrast: false,
          reducedMotion: false,
          fontSize: 'medium' as const,
        },
      };

      useUIStore.getState().setPreferences(preferences);
      expect(useUIStore.getState().preferences).toEqual(preferences);
    });

    it('should persist preferences to localStorage', () => {
      const preferences = {
        language: 'fr',
        timezone: 'Europe/Paris',
        dateFormat: 'DD/MM/YYYY' as const,
        timeFormat: '24h' as const,
        notifications: {
          email: true,
          push: false,
          analysis: true,
          alerts: true,
        },
        accessibility: {
          highContrast: false,
          reducedMotion: false,
          fontSize: 'medium' as const,
        },
      };

      useUIStore.getState().setPreferences(preferences);
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'ui-store',
        expect.stringContaining('"preferences"')
      );
    });
  });

  describe('Notification Actions', () => {
    it('should add notification', () => {
      const notification = {
        type: 'success' as const,
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
      };

      useUIStore.getState().addNotification(notification);
      const notifications = useUIStore.getState().notifications;
      expect(notifications).toHaveLength(1);
      expect(notifications[0]).toMatchObject({
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        read: false,
        id: expect.any(String),
        created_at: expect.any(String),
      });
    });

    it('should remove notification', () => {
      const notification = {
        type: 'success' as const,
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
      };

      useUIStore.getState().addNotification(notification);
      const notifications = useUIStore.getState().notifications;
      expect(notifications).toHaveLength(1);

      useUIStore.getState().removeNotification(notifications[0].id);
      expect(useUIStore.getState().notifications).toHaveLength(0);
    });

    it('should clear all notifications', () => {
      useUIStore.getState().addNotification({
        type: 'success' as const,
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
      });
      useUIStore.getState().addNotification({
        type: 'error' as const,
        title: 'Error',
        message: 'Operation failed',
        duration: 5000,
      });

      expect(useUIStore.getState().notifications).toHaveLength(2);

      useUIStore.getState().clearNotifications();
      expect(useUIStore.getState().notifications).toHaveLength(0);
    });
  });

  describe('Modal Actions', () => {
    it('should open modal', () => {
      const modal = {
        type: 'confirmation' as const,
        title: 'Confirm Action',
        content: 'Are you sure?',
        size: 'md' as const,
        closable: true,
      };

      const modalId = useUIStore.getState().openModal(modal);
      const modals = useUIStore.getState().modals;
      expect(modals).toHaveLength(1);
      expect(modals[0]).toMatchObject({
        id: modalId,
        type: 'confirmation',
        title: 'Confirm Action',
        content: 'Are you sure?',
        size: 'md',
        closable: true,
      });
    });

    it('should close modal', () => {
      const modal = {
        type: 'confirmation' as const,
        title: 'Confirm Action',
        content: 'Are you sure?',
        size: 'md' as const,
        closable: true,
      };

      const modalId = useUIStore.getState().openModal(modal);
      expect(useUIStore.getState().modals).toHaveLength(1);

      useUIStore.getState().closeModal(modalId);
      expect(useUIStore.getState().modals).toHaveLength(0);
    });

    it('should close all modals', () => {
      useUIStore.getState().openModal({
        type: 'confirmation' as const,
        title: 'Modal 1',
        content: 'Content 1',
        size: 'md' as const,
        closable: true,
      });
      useUIStore.getState().openModal({
        type: 'info' as const,
        title: 'Modal 2',
        content: 'Content 2',
        size: 'md' as const,
        closable: true,
      });

      expect(useUIStore.getState().modals).toHaveLength(2);

      useUIStore.getState().closeAllModals();
      expect(useUIStore.getState().modals).toHaveLength(0);
    });
  });

  describe('Toast Actions', () => {
    it('should show toast', () => {
      const toast = {
        type: 'success' as const,
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        position: 'top-right' as const,
      };

      const toastId = useUIStore.getState().showToast(toast);
      const toasts = useUIStore.getState().toasts;
      expect(toasts).toHaveLength(1);
      expect(toasts[0]).toMatchObject({
        id: toastId,
        type: 'success',
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        position: 'top-right',
      });
    });

    it('should hide toast', () => {
      const toast = {
        type: 'success' as const,
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        position: 'top-right' as const,
      };

      const toastId = useUIStore.getState().showToast(toast);
      expect(useUIStore.getState().toasts).toHaveLength(1);

      useUIStore.getState().hideToast(toastId);
      expect(useUIStore.getState().toasts).toHaveLength(0);
    });

    it('should clear all toasts', () => {
      useUIStore.getState().showToast({
        type: 'success' as const,
        title: 'Success',
        message: 'Operation completed',
        duration: 5000,
        position: 'top-right' as const,
      });
      useUIStore.getState().showToast({
        type: 'error' as const,
        title: 'Error',
        message: 'Operation failed',
        duration: 5000,
        position: 'top-right' as const,
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
      expect(useUIStore.getState().loading.analysis).toBe(false);
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
      expect(useUIStore.getState().errors.analysis).toBeNull();
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
      expect(useUIStore.getState().errors.analysis).toBeNull();
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
      expect(useUIStore.getState().getError('clusters')).toBeNull();
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
