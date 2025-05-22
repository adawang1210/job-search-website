import request from './axios'

// 獲取用戶基本信息
export function getUserProfile() {
  return request({
    url: '/api/user/profile',
    method: 'get'
  })
}

// 更新用戶基本信息
export function updateUserProfile(data) {
  return request({
    url: '/api/user/profile',
    method: 'put',
    data
  })
}

// 獲取用戶技能列表
export function getUserSkills() {
  return request({
    url: '/api/user/skills',
    method: 'get'
  })
}

// 更新用戶技能
export function updateUserSkills(data) {
  return request({
    url: '/api/user/skills',
    method: 'put',
    data
  })
}

// 獲取用戶教育經歷
export function getUserEducation() {
  return request({
    url: '/api/user/education',
    method: 'get'
  })
}

// 更新用戶教育經歷
export function updateUserEducation(data) {
  return request({
    url: '/api/user/education',
    method: 'put',
    data
  })
}

// 獲取用戶工作經歷
export function getUserExperience() {
  return request({
    url: '/api/user/experience',
    method: 'get'
  })
}

// 更新用戶工作經歷
export function updateUserExperience(data) {
  return request({
    url: '/api/user/experience',
    method: 'put',
    data
  })
}

// 獲取用戶專案經歷
export function getUserProjects() {
  return request({
    url: '/api/user/projects',
    method: 'get'
  })
}

// 更新用戶專案經歷
export function updateUserProjects(data) {
  return request({
    url: '/api/user/projects',
    method: 'put',
    data
  })
}

// 獲取用戶已收藏的公司
export function getLikedCompanies() {
  return request({
    url: '/api/user/liked-companies',
    method: 'get'
  })
}

// 獲取用戶已追蹤的人
export function getFollowedUsers() {
  return request({
    url: '/api/user/followed-users',
    method: 'get'
  })
} 