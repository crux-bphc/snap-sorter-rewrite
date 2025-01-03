import React, {
  createContext,
  useState,
  useContext,
  ReactNode,
  useEffect,
} from "react";
import { getCookie, setCookie, deleteCookie } from "../utils/cookieUtils";
import { jwtDecode } from "jwt-decode";

interface AuthContextProps {
  token: string | null;
  setToken: (token: string | null) => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

const isValid = (token: string): boolean => {
  try {
    const { exp } = jwtDecode(token);
    return !!exp && exp > Date.now() / 1000;
  } catch {
    return false;
  }
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [token, setTokenState] = useState<string | null>(getCookie("token"));

  useEffect(() => {
    const token = getCookie("token");
    if (token && !isValid(token)) {
      setToken(null);
    }
  }, []);

  const setToken = (newToken: string | null) => {
    if (newToken && isValid(newToken)) {
      setCookie("token", newToken, 7); // 7 days
    } else {
      deleteCookie("token");
    }
    setTokenState(newToken);
  };

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextProps => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
