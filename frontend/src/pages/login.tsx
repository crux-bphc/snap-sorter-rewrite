import React, { useEffect } from "react";

const LoginPage: React.FC = () => {
  useEffect(() => {
    handleLogin();
  }, []);

  const handleLogin = () => {
    const backendUrl =
      import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

    console.log(backendUrl);
    window.location.href = `${backendUrl}/google-login`;
  };

  return <></>;
};

export default LoginPage;
