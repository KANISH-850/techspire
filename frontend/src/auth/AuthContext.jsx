import React, { createContext, useContext, useState, useEffect } from 'react';
import authApi from '../api/auth';
import authStorage from './authStorage';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => authStorage.getUser());
  const [token, setToken] = useState(() => authStorage.getToken());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = authStorage.getToken();
      if (storedToken) {
        try {
          const currentUser = await authApi.getCurrentUser();
          setUser(currentUser);
          authStorage.setUser(currentUser);
        } catch (err) {
          console.error("Token verification failed", err);
          authStorage.clear();
          setUser(null);
          setToken(null);
        }
      }
      setLoading(false);
    };

    initAuth();

    const handleUnauthorized = () => {
      authStorage.clear();
      setUser(null);
      setToken(null);
    };

    window.addEventListener('techspire_unauthorized', handleUnauthorized);
    return () => window.removeEventListener('techspire_unauthorized', handleUnauthorized);
  }, []);

  const login = async (username, password) => {
    const data = await authApi.login(username, password);
    const accessToken = data.access_token;
    authStorage.setToken(accessToken);
    setToken(accessToken);

    const currentUser = await authApi.getCurrentUser();
    setUser(currentUser);
    authStorage.setUser(currentUser);
    return currentUser;
  };

  const logout = () => {
    authStorage.clear();
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!token && !!user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
