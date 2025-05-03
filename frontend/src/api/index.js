import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // 根據您的後端 API 地址進行調整
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 請求攔截器
api.interceptors.request.use(
  config => {
    // 在這裡可以添加 token 等認證信息
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 響應攔截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 在這裡處理錯誤響應
    return Promise.reject(error)
  }
)

export default api