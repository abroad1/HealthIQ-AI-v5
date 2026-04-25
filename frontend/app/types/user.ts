// TODO: Define user types
export type SubscriptionStatusV1 = 'free' | 'active' | 'cancelled';

export interface User {
  id: string;
  email: string;
  name?: string;
  role?: 'admin' | 'user' | 'researcher';
  /** From `profiles.subscription_status` when loaded via `/api/auth/me`. */
  subscription_status?: SubscriptionStatusV1;
  created_at?: string;
  updated_at?: string;
}

export interface UserPreferences {
  theme: 'light' | 'dark';
  notifications: boolean;
  language: string;
  timezone: string;
}

export interface UserProfile extends User {
  preferences: UserPreferences;
  last_login?: string;
}
