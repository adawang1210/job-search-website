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
    url: `/api/companies/${companyId}/jobs`,
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

// 關注公司
export function followCompany(companyId) {
  return request({
    url: `/api/companies/${companyId}/follow`,
    method: 'post'
  })
}

// 取消關注公司
export function unfollowCompany(companyId) {
  return request({
    url: `/api/companies/${companyId}/unfollow`,
    method: 'post'
  })
} 