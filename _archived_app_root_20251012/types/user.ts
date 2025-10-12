// TODO: Define user types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'researcher';
  created_at: string;
  updated_at: string;
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
