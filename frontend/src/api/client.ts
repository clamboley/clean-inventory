// api/client.ts
const API_BASE = 'http://localhost:8000/api';

export async function apiFetch<T>(
  url: string,
  options: RequestInit = {},
): Promise<T> {
  const headers: HeadersInit = {
    ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  // Detect content type
  const contentType = res.headers.get('content-type') || '';

  if (contentType.includes('application/json')) {
    return (await res.json()) as T;
  }

  // Handle CSV / Excel / binary
  if (
    contentType.includes('text/csv') ||
    contentType.includes('application/vnd.ms-excel') ||
    contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  ) {
    return (await res.blob()) as unknown as T;
  }

  // Default fallback: try text
  const text = await res.text();
  return text as unknown as T;
}
