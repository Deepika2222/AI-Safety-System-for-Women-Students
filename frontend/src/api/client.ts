import { API_BASE_URL, API_TOKEN } from '../config';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

type RequestOptions = {
  method?: HttpMethod;
  body?: unknown;
  headers?: Record<string, string>;
};

async function parseJson(response: Response) {
  const text = await response.text();
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text);
  } catch (error) {
    return text;
  }
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (API_TOKEN) {
    headers.Authorization = `Bearer ${API_TOKEN}`;
  }

  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), 15000); // Increased timeout to 15s

  try {
    console.log(`[API] Requesting: ${options.method || 'GET'} ${url}`);
    const response = await fetch(url, {
      method: options.method ?? 'GET',
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: controller.signal,
    });
    clearTimeout(id);

    const payload = await parseJson(response);

    if (!response.ok) {
      const message = typeof payload === 'string'
        ? payload
        : payload?.error || payload?.detail || `Request failed with status ${response.status}`;
      console.error(`[API Error] ${url}: ${message}`);
      throw new Error(message);
    }

    return payload as T;
  } catch (error: any) {
    clearTimeout(id);
    console.error(`[Network Error] ${url}:`, error);
    const errorMsg = error.message === 'Aborted'
      ? `Request timeout: ${url} took too long to respond`
      : `Network error: ${error.message}. Check if server is running at ${API_BASE_URL}`;
    throw new Error(errorMsg);
  }
}
