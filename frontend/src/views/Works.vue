<template>
  <div class="container works-page">
    <h1 class="section-title">传世之作</h1>
    <p class="section-subtitle">历代书法名作，按年代排序，纵览千年书法瑰宝</p>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-group">
        <span class="filter-label">朝代：</span>
        <button class="filter-item" :class="{ active: !selectedDynasty }" @click="selectDynasty('')">全部</button>
        <button
          v-for="d in dynasties"
          :key="d.id"
          class="filter-item"
          :class="{ active: selectedDynasty === d.name }"
          @click="selectDynasty(d.name)"
        >{{ d.name }}</button>
      </div>
    </div>
    <div class="filter-bar">
      <div class="filter-group">
        <span class="filter-label">书体：</span>
        <button class="filter-item" :class="{ active: !selectedStyle }" @click="selectStyle('')">全部</button>
        <button
          v-for="s in styles"
          :key="s"
          class="filter-item"
          :class="{ active: selectedStyle === s }"
          @click="selectStyle(s)"
        >{{ s }}</button>
      </div>
    </div>

    <!-- 加载 -->
    <div v-if="loading" class="loading">正在加载...</div>

    <!-- 空 -->
    <div v-else-if="works.length === 0" class="empty-state">暂无作品数据</div>

    <!-- 作品列表 - 按朝代分组展示 -->
    <div v-else class="works-list">
      <div v-for="group in groupedWorks" :key="group.dynasty" class="dynasty-group">
        <div class="group-header">
          <h2 class="group-title">{{ group.dynasty }}</h2>
          <span class="group-count">{{ group.works.length }} 件作品</span>
        </div>
        <div class="works-grid">
          <div
            v-for="w in group.works"
            :key="w.id"
            class="work-card card"
            @click="$router.push(`/work/${w.id}`)"
          >
            <div class="work-thumb">
              <img
                :src="getWorkImageUrl(w.id, 'thumbnail')"
                :alt="w.name"
                class="work-thumb-img"
                loading="lazy"
              />
              <span class="work-style-label">{{ w.style }}</span>
            </div>
            <div class="work-info">
              <h3 class="work-name">{{ w.name }}</h3>
              <p class="work-author">{{ w.calligrapher_name }} · {{ formatYear(w.creation_year) }}</p>
              <p class="work-desc">{{ truncate(w.description, 40) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getWorks, getDynasties, getStyles, getWorkImageUrl } from '../api'

const route = useRoute()
const router = useRouter()

const works = ref([])
const dynasties = ref([])
const styles = ref([])
const loading = ref(true)
const selectedDynasty = ref(route.query.dynasty || '')
const selectedStyle = ref(route.query.style || '')

const formatYear = (year) => {
  if (year === null || year === undefined) return '年代不详'
  if (year < 0) return `公元前${Math.abs(year)}年`
  return `${year}年`
}

const truncate = (text, len) => {
  if (!text) return ''
  return text.length > len ? text.substring(0, len) + '...' : text
}

// 按朝代分组
const groupedWorks = computed(() => {
  const groups = {}
  works.value.forEach(w => {
    if (!groups[w.dynasty_name]) {
      groups[w.dynasty_name] = { dynasty: w.dynasty_name, works: [] }
    }
    groups[w.dynasty_name].works.push(w)
  })
  return Object.values(groups).sort((a, b) => {
    const da = dynasties.value.find(d => d.name === a.dynasty)
    const db = dynasties.value.find(d => d.name === b.dynasty)
    return (da?.sort_order || 0) - (db?.sort_order || 0)
  })
})

const selectDynasty = (val) => {
  selectedDynasty.value = val
  updateQuery()
}

const selectStyle = (val) => {
  selectedStyle.value = val
  updateQuery()
}

const updateQuery = () => {
  const query = {}
  if (selectedDynasty.value) query.dynasty = selectedDynasty.value
  if (selectedStyle.value) query.style = selectedStyle.value
  router.replace({ query })
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedDynasty.value) params.dynasty = selectedDynasty.value
    if (selectedStyle.value) params.style = selectedStyle.value
    works.value = await getWorks(params)
  } catch (e) {
    console.error('加载作品失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const [d, s] = await Promise.all([getDynasties(), getStyles()])
    dynasties.value = d
    styles.value = s
  } catch (e) {
    console.error('加载筛选数据失败', e)
  }
  await loadData()
})

watch(() => route.query, () => {
  selectedDynasty.value = route.query.dynasty || ''
  selectedStyle.value = route.query.style || ''
  loadData()
})
</script>

<style scoped>
.works-page {
  padding-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-right: 4px;
  white-space: nowrap;
}

.dynasty-group {
  margin-bottom: 40px;
}

.group-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.group-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-vermilion);
}

.group-count {
  font-size: 13px;
  color: var(--text-tertiary);
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.work-card {
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.work-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(139, 112, 66, 0.18);
}

.work-thumb {
  position: relative;
  height: 180px;
  overflow: hidden;
  background: #f3ebdd;
  border-bottom: 1px solid var(--border-color);
}

.work-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.work-card:hover .work-thumb-img {
  transform: scale(1.04);
}

.work-style-label {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 3px 10px;
  font-size: 12px;
  color: var(--text-inverse);
  background: rgba(139, 112, 66, 0.78);
  border-radius: var(--radius-sm);
  letter-spacing: 2px;
}

.work-info {
  padding: 14px 18px;
}

.work-name {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.work-author {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 6px;
}

.work-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .works-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
