import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const chatAPI = {
  chat: async (message, model = 'meta-llama/llama-2-7b-chat', temperature = 0.7) => {
    const response = await api.post('/chat', {
      message,
      model,
      temperature,
      max_tokens: 1500,
    })
    return response.data
  },

  explain: async (message) => {
    const response = await api.post('/explain', {
      message,
      model: 'meta-llama/llama-2-7b-chat',
      temperature: 0.5,
      max_tokens: 2000,
    })
    return response.data
  },

  codeComplete: async (code) => {
    const response = await api.post('/code-complete', {
      message: code,
      model: 'meta-llama/llama-2-7b-chat',
      temperature: 0.3,
      max_tokens: 1000,
    })
    return response.data
  },

  generateQuiz: async (topic) => {
    const response = await api.post('/quiz', {
      message: topic,
      model: 'meta-llama/llama-2-7b-chat',
      temperature: 0.7,
      max_tokens: 2000,
    })
    return response.data
  },

  health: async () => {
    const response = await api.get('/health')
    return response.data
  },
}

export default api
