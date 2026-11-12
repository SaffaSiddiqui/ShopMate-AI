/**
 * ShopMate AI — Frontend API Client
 * Connects to the FastAPI backend at http://127.0.0.1:8000/api
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(url, config)
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`
      try {
        const errorData = await response.json()
        errorMessage = errorData.message || errorMessage
      } catch (_) {}
      throw new Error(errorMessage)
    }
    return await response.json()
  } catch (error) {
    console.warn(`[ShopMate API] Error connecting to ${endpoint}:`, error.message)
    throw error
  }
}

export const api = {
  // --- Health Check ---
  checkHealth: async () => {
    try {
      const res = await request('/health')
      return res.status === 'ok'
    } catch {
      return false
    }
  },

  // --- Products ---
  getProducts: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.search) params.append('search', filters.search)
    if (filters.category) params.append('category', filters.category)
    if (filters.low_stock) params.append('low_stock', 'true')
    const query = params.toString() ? `?${params.toString()}` : ''
    return request(`/products${query}`)
  },

  getProduct: (sku) => request(`/products/${encodeURIComponent(sku)}`),

  createProduct: (productData) =>
    request('/products', {
      method: 'POST',
      body: JSON.stringify(productData),
    }),

  updateProduct: (sku, updateData) =>
    request(`/products/${encodeURIComponent(sku)}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    }),

  deleteProduct: (sku) =>
    request(`/products/${encodeURIComponent(sku)}`, {
      method: 'DELETE',
    }),

  // --- Inventory & Restock ---
  getInventorySummary: () => request('/inventory'),

  getLowStock: (threshold = 10) => request(`/inventory/low-stock?threshold=${threshold}`),

  restockProduct: (sku, quantity = 20) =>
    request(`/inventory/${encodeURIComponent(sku)}/restock`, {
      method: 'POST',
      body: JSON.stringify({ quantity: Number(quantity) }),
    }),

  // --- Orders ---
  getOrders: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.status) params.append('status', filters.status)
    if (filters.customer) params.append('customer', filters.customer)
    if (filters.search) params.append('search', filters.search)
    const query = params.toString() ? `?${params.toString()}` : ''
    return request(`/orders${query}`)
  },

  getOrder: (orderId) => {
    const cleanId = orderId.replace(/^#/, '')
    return request(`/orders/${encodeURIComponent(cleanId)}`)
  },

  createOrder: (orderData) =>
    request('/orders', {
      method: 'POST',
      body: JSON.stringify(orderData),
    }),

  updateOrderStatus: (orderId, newStatus) => {
    const cleanId = orderId.replace(/^#/, '')
    return request(`/orders/${encodeURIComponent(cleanId)}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status: newStatus }),
    })
  },

  deleteOrder: (orderId) => {
    const cleanId = orderId.replace(/^#/, '')
    return request(`/orders/${encodeURIComponent(cleanId)}`, {
      method: 'DELETE',
    })
  },

  // --- Customers ---
  getCustomers: async (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.search) params.append('search', filters.search)
    if (filters.city) params.append('city', filters.city)
    const query = params.toString() ? `?${params.toString()}` : ''
    return request(`/customers${query}`)
  },

  createCustomer: (customerData) =>
    request('/customers', {
      method: 'POST',
      body: JSON.stringify(customerData),
    }),

  // --- Analytics ---
  getAnalyticsOverview: (period = '7 days') =>
    request(`/analytics/overview?period=${encodeURIComponent(period)}`),

  getSalesTrend: (period = '7 days') =>
    request(`/analytics/sales?period=${encodeURIComponent(period)}`),

  // --- AI Agent ---
  chatWithAgent: (message) =>
    request('/agent/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    }),

  getAgentRecommendations: () => request('/agent/recommendations'),
}
