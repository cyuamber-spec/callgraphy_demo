<template>
  <div class="container detail-page">
    <!-- 返回 -->
    <div class="back-bar">
      <button class="btn" @click="$router.back()">← 返回</button>
    </div>

    <div v-if="loading" class="loading">正在加载...</div>

    <div v-else-if="!calligrapher" class="empty-state">书法家不存在</div>

    <template v-else>
      <!-- 书法家信息 -->
      <div class="detail-header card">
        <div class="header-seal">
          <span class="seal-char">{{ calligrapher.name.charAt(0) }}</span>
        </div>
        <div class="header-info">
          <h1 class="header-name">{{ calligrapher.name }}</h1>
          <div class="header-meta">
            <span class="dynasty-tag">{{ calligrapher.dynasty_name }}</span>
            <span class="style-tag">{{ calligrapher.style }}</span>
            <span class="header-years">{{ formatYears(calligrapher.birth_year, calligrapher.death_year) }}</span>
          </div>
          <p class="header-intro">{{ calligrapher.introduction }}</p>
        </div>
      </div>

      <!-- 代表作品 -->
      <div class="works-section">
        <h2 class="section-title">代表作品</h2>
        <p class="section-subtitle">{{ calligrapher.name }}的传世之作，共 {{ calligrapher.works.length }} 件</p>

        <div v-if="calligrapher.works.length === 0" class="empty-state">暂无作品数据</div>

        <div v-else class="works-grid">
          <div
            v-for="w in calligrapher.works"
            :key="w.id"
            class="work-card card"
            @click="$router.push(`/work/${w.id}`)"
          >
            <div class="work-visual" :style="{ background: getWorkBg(w.style) }">
              <span class="work-char">{{ w.name.charAt(0) }}</span>
              <span class="work-style-label">{{ w.style }}</span>
            </div>
            <div class="work-info">
              <h3 class="work-name">{{ w.name }}</h3>
              <p class="work-year">{{ formatYear(w.creation_year) }} 创作</p>
              <p class="work-desc">{{ truncate(w.description, 50) }}</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCalligrapherDetail } from '../api'

const route = useRoute()
const calligrapher = ref(null)
const loading = ref(true)

const formatYears = (birth, death) => {
  const b = birth !== null && birth !== undefined ? (birth < 0 ? `公元前 ${Math.abs(birth)}` : `${birth}`) : '?'
  const d = death !== null && death !== undefined ? (death < 0 ? `公元前 ${Math.abs(death)}` : `${death}`) : '?'
  return `${b} — ${d} 年`
}

const formatYear = (year) => {
  if (year === null || year === undefined) return '年代不详'
  if (year < 0) return `公元前 ${Math.abs(year)} 年`
  return `${year} 年`
}

const truncate = (text, len) => {
  if (!text) return ''
  return text.length > len ? text.substring(0, len) + '...' : text
}

const styleColors = {
  '小篆': '#b0693a',
  '隶书': '#2b4a6f',
  '楷书': '#c3272b',
  '行书': '#5fa383',
  '行楷': '#5fa383',
  '行草': '#7fb89a',
  '草书': '#d4a017',
  '狂草': '#d4a017',
  '六分半书': '#b0693a',
  '标准草书': '#d4a017',
  '篆书': '#b0693a',
}

const getWorkBg = (style) => {
  const color = styleColors[style] || '#c3272b'
  return `linear-gradient(135deg, ${color}15 0%, ${color}25 100%)`
}

onMounted(async () => {
  try {
    calligrapher.value = await getCalligrapherDetail(route.params.id)
  } catch (e) {
    console.error('加载详情失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.detail-page {
  padding-bottom: 20px;
}

.back-bar {
  margin-bottom: 20px;
}

.detail-header {
  display: flex;
  gap: 24px;
  padding: 32px;
  margin-bottom: 40px;
}

.header-seal {
  flex: 0 0 auto;
}

.seal-char {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-vermilion);
  color: var(--text-inverse);
  font-size: 42px;
  font-weight: 700;
  border-radius: var(--radius-md);
  box-shadow: 0 4px 12px rgba(195, 39, 43, 0.25);
}

.header-info {
  flex: 1;
}

.header-name {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.header-years {
  font-size: 14px;
  color: var(--text-tertiary);
}

.header-intro {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.9;
}

.works-section {
  margin-bottom: 20px;
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.work-card {
  cursor: pointer;
  overflow: hidden;
}

.work-visual {
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  border-bottom: 1px solid var(--border-color);
}

.work-char {
  font-size: 56px;
  font-weight: 700;
  color: var(--color-ink);
  line-height: 1;
}

.work-style-label {
  margin-top: 8px;
  font-size: 13px;
  color: var(--text-tertiary);
  letter-spacing: 2px;
}

.work-info {
  padding: 16px 20px;
}

.work-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.work-year {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.work-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
}

@media (max-width: 768px) {
  .detail-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 24px 20px;
  }

  .header-meta {
    justify-content: center;
  }
}
</style>
