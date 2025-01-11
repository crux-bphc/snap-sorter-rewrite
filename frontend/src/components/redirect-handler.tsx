import { useAuth } from "./auth-context";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const RedirectHandler: React.FC = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    if (token) {
      setToken(token);
      navigate("/results");
    } else {
      console.error("No token found in URL");
    }
  }, [setToken, navigate]);

  return <p>Redirecting...</p>;
};

export default RedirectHandler;
