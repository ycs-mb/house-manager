const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const fetchApi = async (endpoint: string, options: RequestInit = {}) => {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || response.statusText);
  }

  return response.json();
};

export const agentApi = {
  submitRequest: (prompt: string, context: any = {}) => 
    fetchApi('/agents/request', {
      method: 'POST',
      body: JSON.stringify({ prompt, context }),
    }),
  getStatus: (taskId: string) => fetchApi(`/agents/status/${taskId}`),
};

export const choresApi = {
  list: () => fetchApi('/chores/'),
  create: (data: any) => fetchApi('/chores/', { method: 'POST', body: JSON.stringify(data) }),
  complete: (id: string) => fetchApi(`/chores/${id}/complete`, { method: 'POST' }),
};

export const inventoryApi = {
  list: () => fetchApi('/inventory/'),
  getLowStock: () => fetchApi('/inventory/low-stock'),
  add: (data: any) => fetchApi('/inventory/', { method: 'POST', body: JSON.stringify(data) }),
};

export const financeApi = {
  getSummary: () => fetchApi('/finance/summary'),
  listTransactions: () => fetchApi('/finance/transactions'),
  record: (data: any) => fetchApi('/finance/transactions', { method: 'POST', body: JSON.stringify(data) }),
};
