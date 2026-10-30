import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getDynasties = () => api.get('/dynasties').then(res => res.data)

export const getCalligraphers = (params) =>
  api.get('/calligraphers', { params }).then(res => res.data)

export const getCalligrapherDetail = (id) =>
  api.get(`/calligraphers/${id}`).then(res => res.data)

export const getWorks = (params) =>
  api.get('/works', { params }).then(res => res.data)

export const getWorkDetail = (id) =>
  api.get(`/works/${id}`).then(res => res.data)

// 作品图片 URL（后端动态生成 SVG，无需外部资源）
// size: 'thumbnail' 列表缩略图 | 'large' 详情高清大图
export const getWorkImageUrl = (id, size = 'thumbnail') =>
  `/api/works/${id}/image?size=${size}`

export const getStyles = () => api.get('/styles').then(res => res.data)

export const getStats = () => api.get('/stats').then(res => res.data)

export default api
