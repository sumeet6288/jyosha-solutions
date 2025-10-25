import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../utils/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Mock user for development - bypass authentication
  const [user, setUser] = useState({
    id: 'demo-user-123',
    name: 'User demo-use',
    email: 'demo-user-123@botsmith.com',
    created_at: new Date().toISOString(),
    role: 'user',
    status: 'active',
    phone: null,
    avatar_url: null,
    last_login: null
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Set mock token for API calls
    localStorage.setItem('botsmith_token', 'mock-token-for-development');
    localStorage.setItem('botsmith_user', JSON.stringify(user));
    
    // Fetch current user data from API to get latest changes
    fetchCurrentUser();
  }, []);

  const fetchCurrentUser = async () => {
    try {
      // Try to fetch real user data from API using mock endpoint
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/auth/me/mock`);
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        localStorage.setItem('botsmith_user', JSON.stringify(userData));
        return userData;
      } else {
        // If API call fails, return current user
        return user;
      }
    } catch (error) {
      console.error('Error fetching user:', error);
      // Return current user if API fails
      return user;
    }
  };

  const login = async (email, password) => {
    // Mock login
    await fetchCurrentUser(); // Fetch user data after login
    return { data: { access_token: 'mock-token' } };
  };

  const register = async (name, email, password) => {
    // Mock registration
    await fetchCurrentUser(); // Fetch user data after registration
    return { data: { id: 'mock-user-123', name, email } };
  };

  const logout = async () => {
    // Mock logout
    console.log('Logout called');
    // Reset to default mock user
    const defaultUser = {
      id: 'demo-user-123',
      name: 'User demo-use',
      email: 'demo-user-123@botsmith.com',
      created_at: new Date().toISOString(),
      role: 'user',
      status: 'active'
    };
    setUser(defaultUser);
    localStorage.setItem('botsmith_user', JSON.stringify(defaultUser));
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
    localStorage.setItem('botsmith_user', JSON.stringify(updatedUser));
  };

  const refreshUser = async () => {
    // Force refresh user data from API
    return await fetchCurrentUser();
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser,
    fetchCurrentUser,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

