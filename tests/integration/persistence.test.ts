/**
 * Persistence Integration Tests
 * Tests localStorage persistence across stores
 */

import { useUIStore } from '../../app/state/uiStore';
import { AuthService } from '../../app/services/auth';

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

// Mock the auth service
jest.mock('../../app/services/auth');

describe('Persistence Integration', () => {
  beforeEach(() => {
    // Reset store state
    useUIStore.getState().resetUI();
    jest.clearAllMocks();
  });

  describe('UI Store Persistence', () => {
    it('should persist theme preference', () => {
      useUIStore.getState().setTheme('light');
      
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'ui-store',
        expect.stringContaining('"theme":"light"')
      );
    });

    it('should persist user preferences', () => {
      const preferences = {
        language: 'es',
        timezone: 'America/New_York',
        dateFormat: 'DD/MM/YYYY' as const,
        timeFormat: '24h' as const,
        notifications: {
          email: false,
          push: true,
          analysis: true,
          alerts: false,
        },
        accessibility: {
          highContrast: true,
          reducedMotion: false,
          fontSize: 'large' as const,
        },
      };

      useUIStore.getState().setPreferences(preferences);
      
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'ui-store',
        expect.stringContaining('"preferences"')
      );
    });

    it('should persist sidebar state', () => {
      useUIStore.getState().setSidebarCollapsed(true);
      
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'ui-store',
        expect.stringContaining('"sidebarCollapsed":true')
      );
    });

    it('should restore state from localStorage on initialization', () => {
      const persistedState = {
        theme: 'light',
        preferences: {
          language: 'fr',
          timezone: 'Europe/Paris',
          dateFormat: 'DD/MM/YYYY',
          timeFormat: '24h',
          notifications: {
            email: true,
            push: false,
            analysis: true,
            alerts: false,
          },
          accessibility: {
            highContrast: false,
            reducedMotion: true,
            fontSize: 'small',
          },
        },
        sidebarCollapsed: true,
      };

      localStorageMock.getItem.mockReturnValue(JSON.stringify(persistedState));

      // Re-initialize store to test persistence
      const store = useUIStore.getState();
      
      expect(store.theme).toBe('light');
      expect(store.preferences.language).toBe('fr');
      expect(store.preferences.timezone).toBe('Europe/Paris');
      expect(store.sidebarCollapsed).toBe(true);
    });

    it('should handle corrupted localStorage data gracefully', () => {
      localStorageMock.getItem.mockReturnValue('invalid json');

      // Should not throw error
      expect(() => {
        useUIStore.getState();
      }).not.toThrow();

      // Should use default values
      const store = useUIStore.getState();
      expect(store.theme).toBe('dark'); // Default value
    });

    it('should handle missing localStorage gracefully', () => {
      localStorageMock.getItem.mockReturnValue(null);

      // Should not throw error
      expect(() => {
        useUIStore.getState();
      }).not.toThrow();

      // Should use default values
      const store = useUIStore.getState();
      expect(store.theme).toBe('dark'); // Default value
    });
  });

  describe('Auth Service Persistence', () => {
    it('should persist authentication token', async () => {
      const mockResponse = {
        success: true,
        data: {
          user: {
            id: 'user-123',
            email: 'test@example.com',
            name: 'Test User',
            role: 'user' as const,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
          token: 'mock-jwt-token',
        },
        message: 'Login successful',
      };

      (AuthService.login as jest.Mock).mockResolvedValue(mockResponse);

      await AuthService.login({
        email: 'test@example.com',
        password: 'password123',
      });

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'healthiq_auth_token',
        'mock-jwt-token'
      );
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'healthiq_user_data',
        JSON.stringify(mockResponse.data.user)
      );
    });

    it('should clear authentication data on logout', async () => {
      // Set up initial auth data
      localStorageMock.getItem
        .mockReturnValueOnce('mock-jwt-token') // getToken
        .mockReturnValueOnce(JSON.stringify({ id: 'user-123' })); // getCurrentUser

      (AuthService.logout as jest.Mock).mockResolvedValue({
        success: true,
        data: { logged_out: true },
        message: 'Logout successful',
      });

      await AuthService.logout();

      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should retrieve current user from localStorage', () => {
      const mockUser = {
        id: 'user-123',
        email: 'test@example.com',
        name: 'Test User',
        role: 'user',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      localStorageMock.getItem.mockReturnValue(JSON.stringify(mockUser));

      const currentUser = AuthService.getCurrentUser();

      expect(currentUser).toEqual(mockUser);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should handle corrupted user data gracefully', () => {
      localStorageMock.getItem.mockReturnValue('invalid json');

      const currentUser = AuthService.getCurrentUser();

      expect(currentUser).toBeNull();
    });

    it('should check authentication status correctly', () => {
      // Authenticated case
      localStorageMock.getItem
        .mockReturnValueOnce('mock-token')
        .mockReturnValueOnce(JSON.stringify({ id: 'user-123' }));

      expect(AuthService.isAuthenticated()).toBe(true);

      // Not authenticated - no token
      localStorageMock.getItem
        .mockReturnValueOnce(null)
        .mockReturnValueOnce(JSON.stringify({ id: 'user-123' }));

      expect(AuthService.isAuthenticated()).toBe(false);

      // Not authenticated - no user
      localStorageMock.getItem
        .mockReturnValueOnce('mock-token')
        .mockReturnValueOnce(null);

      expect(AuthService.isAuthenticated()).toBe(false);
    });
  });

  describe('Cross-Store Persistence', () => {
    it('should persist multiple store states independently', () => {
      // UI Store persistence
      useUIStore.getState().setTheme('light');
      useUIStore.getState().setSidebarCollapsed(true);

      // Auth persistence
      localStorageMock.setItem.mockClear();
      AuthService.clearAuthData();

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'ui-store',
        expect.stringContaining('"theme":"light"')
      );
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should handle localStorage quota exceeded error', () => {
      // Mock localStorage quota exceeded error
      localStorageMock.setItem.mockImplementation(() => {
        throw new Error('QuotaExceededError');
      });

      // Should not throw error
      expect(() => {
        useUIStore.getState().setTheme('light');
      }).not.toThrow();
    });

    it('should handle localStorage unavailable (private browsing)', () => {
      // Mock localStorage unavailable
      const originalLocalStorage = window.localStorage;
      Object.defineProperty(window, 'localStorage', {
        value: undefined,
        writable: true,
      });

      // Should not throw error
      expect(() => {
        useUIStore.getState().setTheme('light');
      }).not.toThrow();

      // Restore localStorage
      Object.defineProperty(window, 'localStorage', {
        value: originalLocalStorage,
        writable: true,
      });
    });
  });

  describe('Data Migration', () => {
    it('should handle version changes in persisted data', () => {
      const oldVersionData = {
        theme: 'light',
        // Missing new fields
      };

      localStorageMock.getItem.mockReturnValue(JSON.stringify(oldVersionData));

      // Should not throw error and use defaults for missing fields
      expect(() => {
        useUIStore.getState();
      }).not.toThrow();

      const store = useUIStore.getState();
      expect(store.theme).toBe('light'); // Preserved
      expect(store.preferences).toBeDefined(); // Default values
    });

    it('should handle malformed persisted data', () => {
      const malformedData = {
        theme: 'invalid-theme', // Invalid value
        preferences: 'not-an-object', // Wrong type
      };

      localStorageMock.getItem.mockReturnValue(JSON.stringify(malformedData));

      // Should not throw error and use defaults
      expect(() => {
        useUIStore.getState();
      }).not.toThrow();

      const store = useUIStore.getState();
      expect(store.theme).toBe('dark'); // Default value
      expect(store.preferences).toBeDefined(); // Default object
    });
  });
});
