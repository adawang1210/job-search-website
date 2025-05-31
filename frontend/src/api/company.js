import request from './axios'
//requset是從axios.js導入的實例


// 獲取公司基本信息
//有用
export function getCompanyInfo(companyId) {
  return request({
    url: `/api/companies/${companyId}`,
    method: 'get'
  })
}

// 獲取公司職缺列表
export function getCompanyJobs(companyId, params) {
  return request({
    url: `/api/jobs`,
    method: 'get',
    params
  })
}

// 獲取公司福利信息
export function getCompanyBenefits(companyId) {
  return request({
    url: `/api/companies/${companyId}/benefits`,
    method: 'get'
  })
}

// 獲取公司圖片集
export function getCompanyGallery(companyId) {
  return request({
    url: `/api/companies/${companyId}/gallery`,
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