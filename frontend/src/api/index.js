import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 生产环境（GitHub Pages）使用静态 JSON 数据，开发环境走后端 API
const isProd = import.meta.env.PROD
const BASE = import.meta.env.BASE_URL // 开发: '/'  生产: '/callgraphy_demo/'

// 静态数据加载辅助函数
const fetchStatic = async (path) => {
  const res = await fetch(`${BASE}data/${path}`)
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`)
  return res.json()
}

export const getDynasties = () =>
  isProd
    ? fetchStatic('dynasties.json')
    : api.get('/dynasties').then(res => res.data)

export const getCalligraphers = (params) =>
  isProd
    ? fetchStatic('calligraphers.json').then(list => {
        if (!params?.dynasty) return list
        return list.filter(c => c.dynasty_name === params.dynasty)
      })
    : api.get('/calligraphers', { params }).then(res => res.data)

export const getCalligrapherDetail = (id) =>
  isProd
    ? fetchStatic(`calligrapher_${id}.json`)
    : api.get(`/calligraphers/${id}`).then(res => res.data)

export const getWorks = (params) =>
  isProd
    ? fetchStatic('works.json').then(list => {
        let result = list
        if (params?.dynasty) result = result.filter(w => w.dynasty_name === params.dynasty)
        if (params?.style) result = result.filter(w => w.style === params.style)
        return result
      })
    : api.get('/works', { params }).then(res => res.data)

export const getWorkDetail = (id) =>
  isProd
    ? fetchStatic(`work_${id}.json`)
    : api.get(`/works/${id}`).then(res => res.data)

// 没有真实图片的作品 ID（回退到 SVG 占位图）
// 来源：中华珍宝馆搜索无匹配结果的 6 件作品
const NO_IMAGE_IDS = new Set([32, 38, 40, 44, 45, 51])

// 作品图片 URL
// size: 'thumbnail' 列表缩略图 | 'large' 详情高清大图
export const getWorkImageUrl = (id, size = 'thumbnail') => {
  if (isProd) {
    const suffix = size === 'thumbnail' ? 'thumb' : 'large'
    const ext = NO_IMAGE_IDS.has(id) ? 'svg' : 'jpg'
    return `${BASE}images/work_${id}_${suffix}.${ext}`
  }
  return `/api/works/${id}/image?size=${size}`
}

export const getStyles = () =>
  isProd
    ? fetchStatic('styles.json')
    : api.get('/styles').then(res => res.data)

export const getStats = () =>
  isProd
    ? fetchStatic('stats.json')
    : api.get('/stats').then(res => res.data)

export default api
