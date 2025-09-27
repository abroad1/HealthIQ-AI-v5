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
  
  // Error states
  globalError: string | null;
  errorStates: Record<string, string | null>;
  
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
        sidebarOpen: false,
        sidebarCollapsed: false,
        headerHeight: 64,
        footerHeight: 48,
        theme: 'system',
        systemTheme: 'light',
        actualTheme: 'light',
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
        globalError: null,
        errorStates: {},

        // Layout actions
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        
        toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
        
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
          loadingStates: { ...state.loadingStates, [key]: loading }
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
          errorStates: { ...state.errorStates, [key]: error }
        })),
        
        clearError: (key) => {
          if (key) {
            set((state) => ({
              errorStates: { ...state.errorStates, [key]: null }
            }));
          } else {
            set({ globalError: null, errorStates: {} });
          }
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
          sidebarOpen: false,
          sidebarCollapsed: false,
          headerHeight: 64,
          footerHeight: 48,
          theme: 'system',
          systemTheme: 'light',
          actualTheme: 'light',
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
          globalError: null,
          errorStates: {},
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
