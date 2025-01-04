import axios from "axios";
import { backendUrl } from "./constants";
import { deleteCookie, getCookie } from "./cookieUtils";

const api = axios.create({
  baseURL: backendUrl,
});

api.interceptors.request.use(
  (config) => {
    const accessToken = getCookie("token");
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error: Error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (res) => res,
  async (error: Error) => {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 401) {
        deleteCookie("token");
        window.location.href = "/login";
      } // else if (error.code === "ERR_NETWORK")
    }
    return Promise.reject(error);
  },
);

export default api;
