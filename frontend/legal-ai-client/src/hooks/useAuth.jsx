import { createContext, useContext, useState, useEffect } from "react";
import { authAPI } from "../lib/api.js";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem("advocadabra_token");
    const savedUser = localStorage.getItem("advocadabra_user");
    
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        // Verify token with backend
        authAPI.verify().catch(() => {
          // Token invalid, clear storage
          localStorage.removeItem("advocadabra_token");
          localStorage.removeItem("advocadabra_user");
          setUser(null);
        });
      } catch (error) {
        localStorage.removeItem("advocadabra_token");
        localStorage.removeItem("advocadabra_user");
        setUser(null);
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);
      
      if (response.success) {
        const { token, user: userData } = response;
        
        // Store in localStorage
        localStorage.setItem("advocadabra_token", token);
        localStorage.setItem("advocadabra_user", JSON.stringify(userData));
        
        setUser(userData);
        return { success: true };
      } else {
        return { success: false, error: response.error || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed. Please try again.' 
      };
    }
  };

  const signup = async (email, password, name) => {
    try {
      const response = await authAPI.signup(email, password, name);
      
      if (response.success) {
        const { token, user: userData } = response;
        
        // Store in localStorage
        localStorage.setItem("advocadabra_token", token);
        localStorage.setItem("advocadabra_user", JSON.stringify(userData));
        
        setUser(userData);
        return { success: true };
      } else {
        return { success: false, error: response.error || 'Signup failed' };
      }
    } catch (error) {
      console.error('Signup error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Signup failed. Please try again.' 
      };
    }
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
