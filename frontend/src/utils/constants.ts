export const backendUrl: string =
  (import.meta.env.VITE_BACKEND_URL as string) ?? "http://127.0.0.1:8000";

export const loginEndpoint = `${backendUrl}/google-login`;
export const resultsEndpoint = `${backendUrl}/get_user_results`;
export const uploadEndpoint = `${backendUrl}/upload`;
export const clusterSamplesEndpoint = `${backendUrl}/cluster_samples`;
export const submitSamplesEndpoint = `${backendUrl}/update_user_selected_images`;
