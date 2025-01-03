type FetchOptions = {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  headers?: Record<string, string>;
  body?: any;
  token?: string;
};

/**
 * A utility function to simplify backend API calls.
 * @param endpoint - The backend API endpoint.
 * @param options - Options for the fetch request.
 * @returns The parsed JSON response from the API.
 */
export const apiFetch = async <T>(
  endpoint: string,
  options?: FetchOptions,
): Promise<T> => {
  const backendUrl =
    import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

  const response = await fetch(backendUrl + endpoint, {
    method: options?.method || "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: options?.token ? `Bearer ${options.token}` : "",
      ...options?.headers,
    },
    body: options?.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`Error fetching data: ${response.statusText}`);
  }

  return response.json();
};
