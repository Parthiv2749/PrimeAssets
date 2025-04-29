import { createContext, useState, useEffect } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem("access_token"));

  useEffect(() => {
    if (accessToken) {
      const decoded = jwtDecode(accessToken);
      setUser({ email: decoded.sub });
    }
  }, [accessToken]);

  const login = async (email, password) => {
    const response = await axios.post("http://192.168.83.1:8000/token", 
      { username: email, password: password },
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    );
    setAccessToken(response.data.access_token);
    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("refresh_token", response.data.refresh_token);
    setUser({ email });
  };

  const logout = () => {
    setAccessToken(null);
    setUser(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  // Include setters if you need them directly
  return (
    <AuthContext.Provider value={{ user, accessToken, setUser, setAccessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
