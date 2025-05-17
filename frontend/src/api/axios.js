import axios from 'axios'

// 創建 axios 實例
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
/*
有寫登入登出的話，才需要攔截器
api.interceptors.request.use(
  (config) => {
    // 從 localStorage 獲取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
*/ 

// 響應攔截器
api.interceptors.response.use(
  (response) => {
    //請求成功時，直接傳回 response.data，簡化在前端的處理
    console.log('response', response)
    return response.data
  },
  (error) => {
    if (error.response) {
      // 處理錯誤響應
      switch (error.response.status) {
        case 401:
          // 未授權，清除 token 並跳轉到登入頁面
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          // 權限不足
          console.error('權限不足')
          break
        case 404:
          // 資源不存在
          console.error('請求的資源不存在')
          break
        case 500:
          // 服務器錯誤
          console.error('服務器錯誤')
          break
        default:
          console.error('發生錯誤：', error.response.data)
      }
    }
    return Promise.reject(error)
  }
)

export default api 