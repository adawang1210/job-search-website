import axios from 'axios'

// 創建 axios 實例
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 響應攔截器
api.interceptors.response.use(
  (response) => {
    //請求成功時，直接傳回 response.data，簡化在前端的處理
    return response.data
  },
  (error) => {
    if (error.response) {
      // 處理錯誤響應
      switch (error.response.status) {
        case 401:
          console.error('請求未授權')
          break
        case 403:
          console.error('權限不足')
          break
        case 404:
          console.error('請求的資源不存在')
          break
        case 500:
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