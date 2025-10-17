import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../utils/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Mock user for development - bypass authentication
  const [user, setUser] = useState({
    id: 'mock-user-123',
    name: 'Demo User',
    email: 'demo@chatbase.com',
    created_at: new Date().toISOString()
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Set mock token for API calls
    localStorage.setItem('chatbase_token', 'mock-token-for-development');
    localStorage.setItem('chatbase_user', JSON.stringify(user));
  }, []);

  const fetchCurrentUser = async () => {
    // Mock implementation
    return user;
  };

  const login = async (email, password) => {
    // Mock login
    return { data: { access_token: 'mock-token' } };
  };

  const register = async (name, email, password) => {
    // Mock registration
    return { data: { id: 'mock-user-123', name, email } };
  };

  const logout = async () => {
    // Mock logout
    console.log('Logout called');
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
    localStorage.setItem('chatbase_user', JSON.stringify(updatedUser));
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser,
    fetchCurrentUser,
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
