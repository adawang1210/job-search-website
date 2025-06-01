import request from './axios'

// 獲取推薦職缺
export function getJobs(params) {
  return request({
    url: '/api/jobs',
    method: 'get',
    params
  })
}

// 獲取優質企業列表
export function getGreatCompanies() {
  return request({
    url: '/api/companies',
    method: 'get'
  })
}

// 更新公司按讚狀態
export function updateLikedCompanies(companyId, isLiked) {
  return request({
    url: `/api/companies/${companyId}/isLiked/`,
    method: 'post',
    data: {
      isLiked: isLiked
    }
  })
}
/*
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
*/
// 獲取職缺詳情
export function getJobDetail(jobId) {
  return request({
    url: `/api/jobs/${jobId}`,
    method: 'get'
  })
}