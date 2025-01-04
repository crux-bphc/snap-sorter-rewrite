import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./auth-context";

const Protected = () => {
  const { token } = useAuth();
  return token ? <Outlet /> : <Navigate to="/" />;
};

export default Protected;
