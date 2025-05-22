import request from './axios'

// 獲取推薦職缺
export function getRecommendedJobs(params) {
  return request({
    url: '/api/jobs/recommended',
    method: 'get',
    params
  })
}

// 獲取熱門職缺
export function getHotJobs(params) {
  return request({
    url: '/api/jobs/hot',
    method: 'get',
    params
  })
}

// 獲取最新職缺
export function getLatestJobs(params) {
  return request({
    url: '/api/jobs/latest',
    method: 'get',
    params
  })
}

// 獲取優質企業列表
export function getTopCompanies() {
  return request({
    url: '/api/companies/top',
    method: 'get'
  })
}

// 獲取最愛職缺
export function getFavoriteJobs() {
  return request({
    url: '/api/jobs/favorite',
    method: 'get'
  })
}

// 收藏職缺
export function likeJob(jobId) {
  return request({
    url: `/api/jobs/${jobId}/like`,
    method: 'post'
  })
}

// 取消收藏職缺
export function unlikeJob(jobId) {
  return request({
    url: `/api/jobs/${jobId}/unlike`,
    method: 'post'
  })
}

// 獲取職缺詳情
export function getJobDetail(jobId) {
  return request({
    url: `/api/jobs/${jobId}`,
    method: 'get'
  })
} 