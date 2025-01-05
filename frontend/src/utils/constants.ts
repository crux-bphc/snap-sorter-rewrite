export const backendUrl: string =
  (import.meta.env.VITE_BACKEND_URL as string) ?? "http://127.0.0.1:8000";

export const loginEndpoint = `/google-login`;
export const resultsEndpoint = `/get_user_results`;
export const uploadEndpoint = `/upload`;
export const clusterSamplesEndpoint = `/cluster_samples`;
export const submitSamplesEndpoint = `/update_user_selected_images`;
export const falsePositiveEndpoint = `/false_positive`;
