<template>
  <div class="container calligraphers-page">
    <h1 class="section-title">书法名家</h1>
    <p class="section-subtitle">历代书法大家，按朝代时间排列，一览千年书道传承</p>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <button
        class="filter-item"
        :class="{ active: !selectedDynasty }"
        @click="selectDynasty('')"
      >全部</button>
      <button
        v-for="d in dynasties"
        :key="d.id"
        class="filter-item"
        :class="{ active: selectedDynasty === d.name }"
        @click="selectDynasty(d.name)"
      >{{ d.name }}</button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">正在加载...</div>

    <!-- 空状态 -->
    <div v-else-if="calligraphers.length === 0" class="empty-state">暂无数据</div>

    <!-- 书法家列表 -->
    <div v-else class="calligraphers-grid">
      <div
        v-for="c in calligraphers"
        :key="c.id"
        class="calligrapher-card card"
        @click="$router.push(`/calligrapher/${c.id}`)"
      >
        <div class="card-seal">
          <span class="seal-text">{{ c.name.charAt(0) }}</span>
        </div>
        <div class="card-body">
          <h3 class="card-name">{{ c.name }}</h3>
          <div class="card-meta">
            <span class="dynasty-tag">{{ c.dynasty_name }}</span>
            <span class="style-tag" v-if="c.style">{{ c.style }}</span>
          </div>
          <p class="card-years">{{ formatYears(c.birth_year, c.death_year) }}</p>
          <p class="card-intro">{{ truncate(c.introduction, 60) }}</p>
        </div>
        <div class="card-footer">
          <span class="card-link">查看详情 →</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCalligraphers, getDynasties } from '../api'

const route = useRoute()
const router = useRouter()

const calligraphers = ref([])
const dynasties = ref([])
const loading = ref(true)
const selectedDynasty = ref(route.query.dynasty || '')

const formatYears = (birth, death) => {
  const b = birth !== null && birth !== undefined ? (birth < 0 ? `前${Math.abs(birth)}` : `${birth}`) : '?'
  const d = death !== null && death !== undefined ? (death < 0 ? `前${Math.abs(death)}` : `${death}`) : '?'
  return `${b} — ${d} 年`
}

const truncate = (text, len) => {
  if (!text) return ''
  return text.length > len ? text.substring(0, len) + '...' : text
}

const selectDynasty = (dynasty) => {
  selectedDynasty.value = dynasty
  if (dynasty) {
    router.replace({ query: { dynasty } })
  } else {
    router.replace({ query: {} })
  }
}

const loadData = async () => {
  loading.value = true
  try {
    const params = selectedDynasty.value ? { dynasty: selectedDynasty.value } : {}
    calligraphers.value = await getCalligraphers(params)
  } catch (e) {
    console.error('加载书法家失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    dynasties.value = await getDynasties()
  } catch (e) {
    console.error('加载朝代失败', e)
  }
  await loadData()
})

watch(() => route.query.dynasty, (val) => {
  selectedDynasty.value = val || ''
  loadData()
})
</script>

<style scoped>
.calligraphers-page {
  padding-bottom: 20px;
}

.calligraphers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.calligrapher-card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-seal {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-paper-warm) 0%, #ede4d0 100%);
  border-bottom: 1px solid var(--border-color);
}

.seal-text {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-vermilion);
  color: var(--text-inverse);
  font-size: 30px;
  font-weight: 700;
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 8px rgba(195, 39, 43, 0.2);
}

.card-body {
  padding: 16px 20px;
  flex: 1;
}

.card-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.card-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.card-years {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.card-intro {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.card-footer {
  padding: 10px 20px;
  border-top: 1px solid var(--border-color);
  background: var(--bg-paper-warm);
}

.card-link {
  font-size: 13px;
  color: var(--color-vermilion);
  font-weight: 500;
}

@media (max-width: 768px) {
  .calligraphers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
