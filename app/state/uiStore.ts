import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

// UI-related types
export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  duration?: number;
  actions?: Array<{
    label: string;
    action: () => void;
  }>;
  created_at: string;
  read: boolean;
}

export interface Modal {
  id: string;
  type: 'confirmation' | 'form' | 'info' | 'custom';
  title: string;
  content: React.ReactNode;
  size: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closable: boolean;
  onClose?: () => void;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
}

export interface Toast {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  duration: number;
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
}

export interface Viewport {
  width: number;
  height: number;
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  timezone: string;
  dateFormat: 'MM/DD/YYYY' | 'DD/MM/YYYY' | 'YYYY-MM-DD';
  timeFormat: '12h' | '24h';
  notifications: {
    email: boolean;
    push: boolean;
    analysis: boolean;
    alerts: boolean;
  };
  accessibility: {
    highContrast: boolean;
    reducedMotion: boolean;
    fontSize: 'small' | 'medium' | 'large';
  };
}

interface UIState {
  // Layout state
  layout: {
    sidebarOpen: boolean;
    headerHeight: number;
    footerHeight: number;
  };
  sidebarOpen: boolean;
  sidebarCollapsed: boolean;
  headerHeight: number;
  footerHeight: number;
  
  // Theme and appearance
  theme: 'light' | 'dark' | 'system';
  systemTheme: 'light' | 'dark';
  actualTheme: 'light' | 'dark';
  
  // Viewport information
  viewport: Viewport;
  
  // User preferences
  preferences: UserPreferences;
  
  // Notifications
  notifications: Notification[];
  unreadCount: number;
  
  // Modals
  modals: Modal[];
  
  // Toasts
  toasts: Toast[];
  
  // Loading states
  globalLoading: boolean;
  loadingStates: Record<string, boolean>;
  loading: Record<string, boolean>;
  
  // Error states
  globalError: string | null;
  errorStates: Record<string, string | null>;
  errors: Record<string, string | null>;
  
  // Questionnaire navigation
  currentStep: number;
  totalSteps: number;
  progress: number;
  
  // Actions - Layout
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setHeaderHeight: (height: number) => void;
  setFooterHeight: (height: number) => void;
  
  // Actions - Theme
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  toggleTheme: () => void;
  setSystemTheme: (theme: 'light' | 'dark') => void;
  
  // Actions - Viewport
  setViewport: (viewport: Viewport) => void;
  updateViewport: (updates: Partial<Viewport>) => void;
  
  // Actions - Preferences
  setPreferences: (preferences: Partial<UserPreferences>) => void;
  resetPreferences: () => void;
  
  // Actions - Notifications
  addNotification: (notification: Omit<Notification, 'id' | 'created_at' | 'read'>) => void;
  removeNotification: (id: string) => void;
  markNotificationRead: (id: string) => void;
  markAllNotificationsRead: () => void;
  clearNotifications: () => void;
  
  // Actions - Modals
  openModal: (modal: Omit<Modal, 'id'>) => string;
  closeModal: (id: string) => void;
  closeAllModals: () => void;
  
  // Actions - Toasts
  addToast: (toast: Omit<Toast, 'id'>) => string;
  removeToast: (id: string) => void;
  clearToasts: () => void;
  
  // Actions - Loading
  setGlobalLoading: (loading: boolean) => void;
  setLoading: (key: string, loading: boolean) => void;
  isLoading: (key?: string) => boolean;
  
  // Actions - Error
  setGlobalError: (error: string | null) => void;
  setError: (key: string, error: string | null) => void;
  clearError: (key?: string) => void;
  clearAllErrors: () => void;
  clearLoading: (key: string) => void;
  
  // Actions - Questionnaire Navigation
  setCurrentStep: (step: number) => void;
  setTotalSteps: (steps: number) => void;
  nextStep: () => void;
  prevStep: () => void;
  resetSteps: () => void;
  updateLayout: (layout: Partial<UIState['layout']>) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
  showToast: (toast: Omit<Toast, 'id'>) => string;
  hideToast: (id: string) => void;
  clearAllLoading: () => void;
  hasError: (key: string) => boolean;
  getError: (key: string) => string | null;
  
  // Utility actions
  isMobile: () => boolean;
  isTablet: () => boolean;
  isDesktop: () => boolean;
  getResponsiveValue: <T>(values: { mobile: T; tablet: T; desktop: T }) => T;
  resetUI: () => void;
}

const defaultPreferences: UserPreferences = {
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
};

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        layout: {
          sidebarOpen: false,
          headerHeight: 64,
          footerHeight: 48,
        },
        sidebarOpen: false,
        sidebarCollapsed: false,
        headerHeight: 64,
        footerHeight: 48,
        theme: 'dark',
        systemTheme: 'light',
        actualTheme: 'dark',
        viewport: {
          width: typeof window !== 'undefined' ? window.innerWidth : 1024,
          height: typeof window !== 'undefined' ? window.innerHeight : 768,
          isMobile: false,
          isTablet: false,
          isDesktop: true,
        },
        preferences: defaultPreferences,
        notifications: [],
        unreadCount: 0,
        modals: [],
        toasts: [],
        globalLoading: false,
        loadingStates: {},
        loading: {},
        globalError: null,
        errorStates: {},
        errors: {},
        currentStep: 1,
        totalSteps: 1,
        progress: 0,

        // Layout actions
        setSidebarOpen: (open) => set((state) => ({ 
          sidebarOpen: open,
          layout: { ...state.layout, sidebarOpen: open }
        })),
        
        toggleSidebar: () => set((state) => ({ 
          sidebarOpen: !state.sidebarOpen,
          layout: { ...state.layout, sidebarOpen: !state.sidebarOpen }
        })),
        
        setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
        
        setHeaderHeight: (height) => set({ headerHeight: height }),
        
        setFooterHeight: (height) => set({ footerHeight: height }),

        // Theme actions
        setTheme: (theme) => {
          const state = get();
          const actualTheme = theme === 'system' ? state.systemTheme : theme;
          set({ theme, actualTheme });
        },
        
        toggleTheme: () => {
          const state = get();
          const newTheme = state.actualTheme === 'light' ? 'dark' : 'light';
          set({ theme: newTheme, actualTheme: newTheme });
        },
        
        setSystemTheme: (theme) => {
          const state = get();
          const actualTheme = state.theme === 'system' ? theme : state.actualTheme;
          set({ systemTheme: theme, actualTheme });
        },

        // Viewport actions
        setViewport: (viewport) => set({ viewport }),
        
        updateViewport: (updates) => set((state) => ({
          viewport: { ...state.viewport, ...updates }
        })),

        // Preferences actions
        setPreferences: (updates) => set((state) => ({
          preferences: { ...state.preferences, ...updates }
        })),
        
        resetPreferences: () => set({ preferences: defaultPreferences }),

        // Notification actions
        addNotification: (notification) => {
          const id = `notification_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          const newNotification: Notification = {
            ...notification,
            id,
            created_at: new Date().toISOString(),
            read: false,
          };
          
          set((state) => ({
            notifications: [newNotification, ...state.notifications],
            unreadCount: state.unreadCount + 1,
          }));
        },
        
        removeNotification: (id) => set((state) => {
          const notification = state.notifications.find(n => n.id === id);
          const wasUnread = notification && !notification.read;
          return {
            notifications: state.notifications.filter(n => n.id !== id),
            unreadCount: wasUnread ? state.unreadCount - 1 : state.unreadCount,
          };
        }),
        
        markNotificationRead: (id) => set((state) => {
          const notification = state.notifications.find(n => n.id === id);
          if (notification && !notification.read) {
            return {
              notifications: state.notifications.map(n =>
                n.id === id ? { ...n, read: true } : n
              ),
              unreadCount: state.unreadCount - 1,
            };
          }
          return state;
        }),
        
        markAllNotificationsRead: () => set((state) => ({
          notifications: state.notifications.map(n => ({ ...n, read: true })),
          unreadCount: 0,
        })),
        
        clearNotifications: () => set({ notifications: [], unreadCount: 0 }),

        // Modal actions
        openModal: (modal) => {
          const id = `modal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          const newModal: Modal = { ...modal, id };
          
          set((state) => ({
            modals: [...state.modals, newModal]
          }));
          
          return id;
        },
        
        closeModal: (id) => set((state) => ({
          modals: state.modals.filter(m => m.id !== id)
        })),
        
        closeAllModals: () => set({ modals: [] }),

        // Toast actions
        addToast: (toast) => {
          const id = `toast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          const newToast: Toast = { ...toast, id };
          
          set((state) => ({
            toasts: [...state.toasts, newToast]
          }));
          
          // Auto-remove toast after duration
          if (toast.duration > 0) {
            setTimeout(() => {
              get().removeToast(id);
            }, toast.duration);
          }
          
          return id;
        },
        
        removeToast: (id) => set((state) => ({
          toasts: state.toasts.filter(t => t.id !== id)
        })),
        
        clearToasts: () => set({ toasts: [] }),

        // Loading actions
        setGlobalLoading: (loading) => set({ globalLoading: loading }),
        
        setLoading: (key, loading) => set((state) => ({
          loadingStates: { ...state.loadingStates, [key]: loading },
          loading: { ...state.loading, [key]: loading }
        })),
        
        isLoading: (key) => {
          const state = get();
          if (key) {
            return state.loadingStates[key] || false;
          }
          return state.globalLoading || Object.values(state.loadingStates).some(loading => loading);
        },

        // Error actions
        setGlobalError: (error) => set({ globalError: error }),
        
        setError: (key, error) => set((state) => ({
          errorStates: { ...state.errorStates, [key]: error },
          errors: { ...state.errors, [key]: error }
        })),
        
        clearError: (key) => {
          if (key) {
            set((state) => ({
              errorStates: { ...state.errorStates, [key]: null },
              errors: { ...state.errors, [key]: null }
            }));
          } else {
            set({ globalError: null, errorStates: {}, errors: {} });
          }
        },
        
        clearLoading: (key) => set((state) => ({
          loadingStates: { ...state.loadingStates, [key]: false },
          loading: { ...state.loading, [key]: false }
        })),
        
        clearAllErrors: () => set({ globalError: null, errorStates: {}, errors: {} }),
        
        // Questionnaire navigation actions
        setCurrentStep: (step) => {
          const state = get();
          const progress = state.totalSteps > 0 ? (step / state.totalSteps) * 100 : 0;
          set({ currentStep: step, progress });
        },
        
        setTotalSteps: (steps) => {
          const state = get();
          const progress = steps > 0 ? (state.currentStep / steps) * 100 : 0;
          set({ totalSteps: steps, progress });
        },
        
        nextStep: () => {
          const state = get();
          if (state.currentStep < state.totalSteps) {
            get().setCurrentStep(state.currentStep + 1);
          }
        },
        
        prevStep: () => {
          const state = get();
          if (state.currentStep > 1) {
            get().setCurrentStep(state.currentStep - 1);
          }
        },
        
        resetSteps: () => set({ currentStep: 1, totalSteps: 1, progress: 0 }),
        
        updateLayout: (layout) => set((state) => ({
          layout: { ...state.layout, ...layout }
        })),
        
        updatePreferences: (preferences) => set((state) => ({
          preferences: { ...state.preferences, ...preferences }
        })),
        
        showToast: (toast) => {
          return get().addToast(toast);
        },
        
        hideToast: (id) => {
          get().removeToast(id);
        },
        
        clearAllLoading: () => set({ globalLoading: false, loadingStates: {}, loading: {} }),
        
        hasError: (key) => {
          const state = get();
          return !!(state.errorStates[key] || state.globalError);
        },
        
        getError: (key) => {
          const state = get();
          return state.errorStates[key] || state.globalError;
        },

        // Utility functions
        isMobile: () => {
          const state = get();
          return state.viewport.isMobile;
        },
        
        isTablet: () => {
          const state = get();
          return state.viewport.isTablet;
        },
        
        isDesktop: () => {
          const state = get();
          return state.viewport.isDesktop;
        },
        
        getResponsiveValue: (values) => {
          const state = get();
          if (state.viewport.isMobile) return values.mobile;
          if (state.viewport.isTablet) return values.tablet;
          return values.desktop;
        },
        
        resetUI: () => set({
          layout: {
            sidebarOpen: false,
            headerHeight: 64,
            footerHeight: 48,
          },
          sidebarOpen: false,
          sidebarCollapsed: false,
          headerHeight: 64,
          footerHeight: 48,
          theme: 'dark',
          systemTheme: 'light',
          actualTheme: 'dark',
          viewport: {
            width: typeof window !== 'undefined' ? window.innerWidth : 1024,
            height: typeof window !== 'undefined' ? window.innerHeight : 768,
            isMobile: false,
            isTablet: false,
            isDesktop: true,
          },
          preferences: defaultPreferences,
          notifications: [],
          unreadCount: 0,
          modals: [],
          toasts: [],
          globalLoading: false,
          loadingStates: {},
          loading: {},
          globalError: null,
          errorStates: {},
          errors: {},
          currentStep: 1,
          totalSteps: 1,
          progress: 0,
        }),
      }),
      {
        name: 'ui-store',
        partialize: (state) => ({
          theme: state.theme,
          preferences: state.preferences,
          sidebarCollapsed: state.sidebarCollapsed,
        }),
      }
    ),
    {
      name: 'ui-store',
    }
  )
);
