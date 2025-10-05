/**
 * Authentication API Service
 * Handles user authentication, authorization, and session management
 */

import { User, UserProfile, UserPreferences } from '../types/user';
import { ApiResponse, ApiError } from '../types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Token management
const TOKEN_KEY = 'healthiq_auth_token';
const USER_KEY = 'healthiq_user_data';

export class AuthService {
  /**
   * Login with email and password
   */
  static async login(credentials: { email: string; password: string }): Promise<ApiResponse<{ user: User; token: string }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Store token and user data
      if (result.token) {
        localStorage.setItem(TOKEN_KEY, result.token);
      }
      if (result.user) {
        localStorage.setItem(USER_KEY, JSON.stringify(result.user));
      }

      return {
        data: result,
        success: true,
        message: 'Login successful',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Login failed',
      };
    }
  }

  /**
   * Logout and clear session
   */
  static async logout(): Promise<ApiResponse<{ logged_out: boolean }>> {
    try {
      const token = this.getToken();
      
      if (token) {
        // Call logout endpoint if available
        try {
          await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
        } catch (error) {
          // Continue with local logout even if server call fails
          console.warn('Server logout failed, continuing with local logout:', error);
        }
      }

      // Clear local storage
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);

      return {
        data: { logged_out: true },
        success: true,
        message: 'Logout successful',
      };
    } catch (error) {
      return {
        data: { logged_out: false },
        success: false,
        error: error instanceof Error ? error.message : 'Logout failed',
      };
    }
  }

  /**
   * Get current user from stored data
   */
  static getCurrentUser(): User | null {
    try {
      const userData = localStorage.getItem(USER_KEY);
      if (!userData) return null;
      
      return JSON.parse(userData);
    } catch (error) {
      console.error('Failed to parse stored user data:', error);
      return null;
    }
  }

  /**
   * Get current user from server
   */
  static async getCurrentUserFromServer(): Promise<ApiResponse<User>> {
    try {
      const token = this.getToken();
      if (!token) {
        return {
          data: null,
          success: false,
          error: 'No authentication token found',
        };
      }

      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token expired or invalid
          this.clearAuthData();
          return {
            data: null,
            success: false,
            error: 'Authentication expired',
          };
        }
        
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Update stored user data
      if (result.user) {
        localStorage.setItem(USER_KEY, JSON.stringify(result.user));
      }

      return {
        data: result.user || result,
        success: true,
        message: 'User data retrieved successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get current user',
      };
    }
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated(): boolean {
    const token = this.getToken();
    const user = this.getCurrentUser();
    return !!(token && user);
  }

  /**
   * Get authentication token
   */
  static getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Clear all authentication data
   */
  static clearAuthData(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  /**
   * Register new user
   */
  static async register(userData: {
    email: string;
    password: string;
    name: string;
    role?: 'user' | 'admin' | 'researcher';
  }): Promise<ApiResponse<{ user: User; token: string }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Store token and user data
      if (result.token) {
        localStorage.setItem(TOKEN_KEY, result.token);
      }
      if (result.user) {
        localStorage.setItem(USER_KEY, JSON.stringify(result.user));
      }

      return {
        data: result,
        success: true,
        message: 'Registration successful',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Registration failed',
      };
    }
  }

  /**
   * Update user profile
   */
  static async updateProfile(profileData: Partial<UserProfile>): Promise<ApiResponse<User>> {
    try {
      const token = this.getToken();
      if (!token) {
        return {
          data: null,
          success: false,
          error: 'No authentication token found',
        };
      }

      const response = await fetch(`${API_BASE_URL}/auth/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Update stored user data
      if (result.user) {
        localStorage.setItem(USER_KEY, JSON.stringify(result.user));
      }

      return {
        data: result.user || result,
        success: true,
        message: 'Profile updated successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to update profile',
      };
    }
  }

  /**
   * Change password
   */
  static async changePassword(passwordData: {
    currentPassword: string;
    newPassword: string;
  }): Promise<ApiResponse<{ changed: boolean }>> {
    try {
      const token = this.getToken();
      if (!token) {
        return {
          data: null,
          success: false,
          error: 'No authentication token found',
        };
      }

      const response = await fetch(`${API_BASE_URL}/auth/change-password`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(passwordData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();

      return {
        data: result,
        success: true,
        message: 'Password changed successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to change password',
      };
    }
  }

  /**
   * Refresh authentication token
   */
  static async refreshToken(): Promise<ApiResponse<{ token: string }>> {
    try {
      const token = this.getToken();
      if (!token) {
        return {
          data: null,
          success: false,
          error: 'No authentication token found',
        };
      }

      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        this.clearAuthData();
        return {
          data: null,
          success: false,
          error: 'Token refresh failed',
        };
      }

      const result = await response.json();
      
      // Update stored token
      if (result.token) {
        localStorage.setItem(TOKEN_KEY, result.token);
      }

      return {
        data: result,
        success: true,
        message: 'Token refreshed successfully',
      };
    } catch (error) {
      this.clearAuthData();
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to refresh token',
      };
    }
  }
}