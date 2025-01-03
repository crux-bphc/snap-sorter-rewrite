import { useAuth } from "./auth-context";
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

const RedirectHandler: React.FC = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const token = params.get("token");

  useEffect(() => {
    if (token) {
      setToken(token);
      navigate("/results");
    } else {
      console.error("No token found in URL");
    }
  }, [setToken, navigate, token]);

  return <p>Redirecting...</p>;
};

export default RedirectHandler;
