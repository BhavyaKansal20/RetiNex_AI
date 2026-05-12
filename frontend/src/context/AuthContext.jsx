import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('retinex_token');
    const savedUser = localStorage.getItem('retinex_user');
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('retinex_token');
        localStorage.removeItem('retinex_user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login({ email, password });
    const { access_token, user: userData } = res.data;
    localStorage.setItem('retinex_token', access_token);
    localStorage.setItem('retinex_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const register = async (username, email, password) => {
    const res = await authAPI.register({ username, email, password });
    const { access_token, user: userData } = res.data;
    localStorage.setItem('retinex_token', access_token);
    localStorage.setItem('retinex_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const logout = () => {
    localStorage.removeItem('retinex_token');
    localStorage.removeItem('retinex_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
