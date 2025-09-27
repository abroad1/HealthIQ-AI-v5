// ARCHIVED TEST
// Reason: Medium-value test (API mock, not critical path)
// Archived: 2025-01-27
// Original Path: frontend/tests/services/auth.test.ts

/**
 * Auth Service Tests
 * Tests for frontend/app/services/auth.ts
 */

import { AuthService } from '../../../../app/services/auth';
import { User } from '../../../../app/types/user';

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

// Mock fetch globally
global.fetch = jest.fn();

describe('AuthService', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    localStorageMock.removeItem.mockClear();
  });

  describe('login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        user: {
          id: 'user-123',
          email: 'test@example.com',
          name: 'Test User',
          role: 'user' as const,
          created_at: '2025-01-27T00:00:00Z',
          updated_at: '2025-01-27T00:00:00Z',
        },
        token: 'jwt-token-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const credentials = { email: 'test@example.com', password: 'password123' };
      const result = await AuthService.login(credentials);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse);
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_auth_token', 'jwt-token-123');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_user_data', JSON.stringify(mockResponse.user));
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/login',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials),
        })
      );
    });

    it('should handle login errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: 'Invalid credentials' }),
      });

      const credentials = { email: 'test@example.com', password: 'wrong' };
      const result = await AuthService.login(credentials);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid credentials');
      expect(localStorageMock.setItem).not.toHaveBeenCalled();
    });

    it('should handle network errors', async () => {
      (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      const credentials = { email: 'test@example.com', password: 'password123' };
      const result = await AuthService.login(credentials);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Network error');
    });
  });

  describe('logout', () => {
    it('should logout successfully with token', async () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true }),
      });

      const result = await AuthService.logout();

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ logged_out: true });
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/logout',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Authorization': 'Bearer jwt-token-123' },
        })
      );
    });

    it('should logout locally when no token', async () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = await AuthService.logout();

      expect(result.success).toBe(true);
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should continue with local logout on server error', async () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');

      (fetch as jest.Mock).mockRejectedValueOnce(new Error('Server error'));

      const result = await AuthService.logout();

      expect(result.success).toBe(true);
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });
  });

  describe('getCurrentUser', () => {
    it('should return user from localStorage', () => {
      const mockUser: User = {
        id: 'user-123',
        email: 'test@example.com',
        name: 'Test User',
        role: 'user',
        created_at: '2025-01-27T00:00:00Z',
        updated_at: '2025-01-27T00:00:00Z',
      };

      localStorageMock.getItem.mockReturnValue(JSON.stringify(mockUser));

      const result = AuthService.getCurrentUser();

      expect(result).toEqual(mockUser);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should return null when no user data', () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = AuthService.getCurrentUser();

      expect(result).toBeNull();
    });

    it('should return null on JSON parse error', () => {
      localStorageMock.getItem.mockReturnValue('invalid-json');

      const result = AuthService.getCurrentUser();

      expect(result).toBeNull();
    });
  });

  describe('getCurrentUserFromServer', () => {
    it('should get user from server successfully', async () => {
      const mockUser: User = {
        id: 'user-123',
        email: 'test@example.com',
        name: 'Test User',
        role: 'user',
        created_at: '2025-01-27T00:00:00Z',
        updated_at: '2025-01-27T00:00:00Z',
      };

      localStorageMock.getItem.mockReturnValue('jwt-token-123');
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ user: mockUser }),
      });

      const result = await AuthService.getCurrentUserFromServer();

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockUser);
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_user_data', JSON.stringify(mockUser));
    });

    it('should handle 401 unauthorized', async () => {
      localStorageMock.getItem.mockReturnValue('invalid-token');
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 401,
      });

      const result = await AuthService.getCurrentUserFromServer();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Authentication expired');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should handle no token', async () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = await AuthService.getCurrentUserFromServer();

      expect(result.success).toBe(false);
      expect(result.error).toBe('No authentication token found');
    });
  });

  describe('isAuthenticated', () => {
    it('should return true when token and user exist', () => {
      localStorageMock.getItem
        .mockReturnValueOnce('jwt-token-123')
        .mockReturnValueOnce(JSON.stringify({ id: 'user-123' }));

      const result = AuthService.isAuthenticated();

      expect(result).toBe(true);
    });

    it('should return false when no token', () => {
      localStorageMock.getItem
        .mockReturnValueOnce(null)
        .mockReturnValueOnce(JSON.stringify({ id: 'user-123' }));

      const result = AuthService.isAuthenticated();

      expect(result).toBe(false);
    });

    it('should return false when no user', () => {
      localStorageMock.getItem
        .mockReturnValueOnce('jwt-token-123')
        .mockReturnValueOnce(null);

      const result = AuthService.isAuthenticated();

      expect(result).toBe(false);
    });
  });

  describe('getToken', () => {
    it('should return token from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');

      const result = AuthService.getToken();

      expect(result).toBe('jwt-token-123');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('healthiq_auth_token');
    });
  });

  describe('clearAuthData', () => {
    it('should clear all auth data', () => {
      AuthService.clearAuthData();

      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });
  });

  describe('register', () => {
    it('should register successfully', async () => {
      const mockResponse = {
        user: {
          id: 'user-123',
          email: 'test@example.com',
          name: 'Test User',
          role: 'user' as const,
          created_at: '2025-01-27T00:00:00Z',
          updated_at: '2025-01-27T00:00:00Z',
        },
        token: 'jwt-token-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
        role: 'user' as const,
      };

      const result = await AuthService.register(userData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse);
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_auth_token', 'jwt-token-123');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_user_data', JSON.stringify(mockResponse.user));
    });

    it('should handle registration errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Email already exists' }),
      });

      const userData = {
        email: 'existing@example.com',
        password: 'password123',
        name: 'Test User',
      };

      const result = await AuthService.register(userData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Email already exists');
    });
  });

  describe('updateProfile', () => {
    it('should update profile successfully', async () => {
      const mockUser: User = {
        id: 'user-123',
        email: 'test@example.com',
        name: 'Updated Name',
        role: 'user',
        created_at: '2025-01-27T00:00:00Z',
        updated_at: '2025-01-27T00:00:00Z',
      };

      localStorageMock.getItem.mockReturnValue('jwt-token-123');
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ user: mockUser }),
      });

      const profileData = { name: 'Updated Name' };
      const result = await AuthService.updateProfile(profileData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockUser);
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_user_data', JSON.stringify(mockUser));
    });

    it('should handle no token', async () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = await AuthService.updateProfile({ name: 'Updated Name' });

      expect(result.success).toBe(false);
      expect(result.error).toBe('No authentication token found');
    });
  });

  describe('changePassword', () => {
    it('should change password successfully', async () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ changed: true }),
      });

      const passwordData = {
        currentPassword: 'old-password',
        newPassword: 'new-password',
      };

      const result = await AuthService.changePassword(passwordData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ changed: true });
    });

    it('should handle no token', async () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = await AuthService.changePassword({
        currentPassword: 'old',
        newPassword: 'new',
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('No authentication token found');
    });
  });

  describe('refreshToken', () => {
    it('should refresh token successfully', async () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ token: 'new-jwt-token-123' }),
      });

      const result = await AuthService.refreshToken();

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ token: 'new-jwt-token-123' });
      expect(localStorageMock.setItem).toHaveBeenCalledWith('healthiq_auth_token', 'new-jwt-token-123');
    });

    it('should handle refresh failure', async () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 401,
      });

      const result = await AuthService.refreshToken();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Token refresh failed');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });

    it('should handle no token', async () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = await AuthService.refreshToken();

      expect(result.success).toBe(false);
      expect(result.error).toBe('No authentication token found');
    });
  });
});
