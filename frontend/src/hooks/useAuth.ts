import { useState, useEffect } from 'react';
import { authService } from '../services';
import type { SessionResponse } from '../services';

interface UseAuthReturn {
  isAuthenticated: boolean | null;
  user: SessionResponse['user'] | null;
  loading: boolean;
  error: string | null;
  checkSession: () => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [user, setUser] = useState<SessionResponse['user'] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkSession = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await authService.checkSession();
      
      setIsAuthenticated(response.authenticated);
      setUser(response.user || null);
      
      if (!response.authenticated && response.message) {
        setError(response.message);
      }
    } catch (err) {
      setError('Failed to check session');
      setIsAuthenticated(false);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      const success = await authService.logout();
      
      if (success) {
        setIsAuthenticated(false);
        setUser(null);
        setError(null);
      } else {
        setError('Failed to logout');
      }
    } catch (err) {
      setError('Failed to logout');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkSession();
  }, []);

  return {
    isAuthenticated,
    user,
    loading,
    error,
    checkSession,
    logout,
  };
};

