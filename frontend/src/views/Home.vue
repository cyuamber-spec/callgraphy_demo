<template>
  <div class="home">
    <!-- Hero 区域 -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-pattern"></div>
      </div>
      <div class="container hero-content">
        <h1 class="hero-title">翰墨千秋</h1>
        <p class="hero-subtitle">历代书法名家作品集</p>
        <p class="hero-desc">从秦篆汉隶到晋唐楷行，从宋人尚意到明清碑学<br/>汇聚千年翰墨精华，传承中华书道神韵</p>
        <div class="hero-actions">
          <router-link to="/calligraphers" class="btn btn-primary btn-lg">浏览书法名家</router-link>
          <router-link to="/works" class="btn btn-lg">欣赏传世之作</router-link>
        </div>
      </div>
    </section>

    <!-- 统计数据 -->
    <section class="container stats-section">
      <div class="stats-grid" v-if="stats">
        <div class="stat-card card">
          <div class="stat-number">{{ stats.dynasties }}</div>
          <div class="stat-label">个朝代</div>
        </div>
        <div class="stat-card card">
          <div class="stat-number">{{ stats.calligraphers }}</div>
          <div class="stat-label">位书法名家</div>
        </div>
        <div class="stat-card card">
          <div class="stat-number">{{ stats.works }}</div>
          <div class="stat-label">件传世之作</div>
        </div>
      </div>
    </section>

    <!-- 朝代时间轴 -->
    <section class="container timeline-section">
      <h2 class="section-title">历代书风</h2>
      <p class="section-subtitle">沿历史长河溯流而上，一览各朝代书法风貌</p>
      <div class="timeline" v-if="dynasties.length">
        <div
          v-for="d in dynasties"
          :key="d.id"
          class="timeline-item"
          @click="$router.push(`/calligraphers?dynasty=${d.name}`)"
        >
          <div class="timeline-dot"></div>
          <div class="timeline-content card">
            <div class="timeline-dynasty">{{ d.name }}</div>
            <div class="timeline-years">{{ formatYear(d.start_year) }} — {{ formatYear(d.end_year) }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 代表书体 -->
    <section class="container styles-section">
      <h2 class="section-title">书体流变</h2>
      <p class="section-subtitle">篆、隶、楷、行、草，各体兼备，各臻其妙</p>
      <div class="styles-grid">
        <div
          v-for="s in styleList"
          :key="s.name"
          class="style-card card"
          @click="$router.push(`/works?style=${s.name}`)"
        >
          <div class="style-char" :style="{ color: s.color }">{{ s.char }}</div>
          <div class="style-name">{{ s.name }}</div>
          <div class="style-desc">{{ s.desc }}</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDynasties, getStats } from '../api'

const dynasties = ref([])
const stats = ref(null)

const styleList = [
  { name: '篆书', char: '篆', desc: '圆转匀称，古意盎然', color: 'var(--color-ochre)' },
  { name: '隶书', char: '隶', desc: '蚕头燕尾，方正朴拙', color: 'var(--color-azure)' },
  { name: '楷书', char: '楷', desc: '法度严谨，端庄严整', color: 'var(--color-vermilion)' },
  { name: '行书', char: '行', desc: '行云流水，自然天成', color: 'var(--color-jade)' },
  { name: '草书', char: '草', desc: '纵横奔放，气势磅礴', color: 'var(--color-gold)' },
  { name: '行草', char: '草', desc: '行草相间，灵动飘逸', color: 'var(--color-jade-light)' },
]

const formatYear = (year) => {
  if (year < 0) return `公元前 ${Math.abs(year)} 年`
  return `${year} 年`
}

onMounted(async () => {
  try {
    const [d, s] = await Promise.all([getDynasties(), getStats()])
    dynasties.value = d
    stats.value = s
  } catch (e) {
    console.error('加载数据失败', e)
  }
})
</script>

<style scoped>
/* Hero */
.hero {
  position: relative;
  height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #faf6ef 0%, #f5efe2 50%, #ede4d0 100%);
  margin-bottom: 40px;
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.06;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Ctext x='100' y='130' font-size='120' text-anchor='middle' fill='%23c3272b' font-family='serif'%3E%E7%BF%B0%3C/text%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 200px;
}

.hero-content {
  position: relative;
  text-align: center;
  z-index: 1;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  color: var(--color-vermilion);
  letter-spacing: 12px;
  margin-bottom: 12px;
  text-shadow: 0 2px 8px rgba(195, 39, 43, 0.15);
}

.hero-subtitle {
  font-size: 20px;
  color: var(--text-secondary);
  letter-spacing: 4px;
  margin-bottom: 16px;
}

.hero-desc {
  font-size: 15px;
  color: var(--text-tertiary);
  line-height: 2;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn-lg {
  padding: 12px 32px;
  font-size: 15px;
}

/* 统计 */
.stats-section {
  margin-bottom: 48px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-card {
  text-align: center;
  padding: 32px 20px;
}

.stat-number {
  font-size: 42px;
  font-weight: 700;
  color: var(--color-vermilion);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 15px;
  color: var(--text-secondary);
  letter-spacing: 2px;
}

/* 时间轴 */
.timeline-section {
  margin-bottom: 48px;
}

.timeline {
  display: flex;
  overflow-x: auto;
  gap: 0;
  padding: 20px 0;
  position: relative;
}

.timeline::before {
  content: "";
  position: absolute;
  top: 40px;
  left: 20px;
  right: 20px;
  height: 2px;
  background: var(--border-color);
}

.timeline-item {
  flex: 0 0 auto;
  width: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-vermilion);
  border: 3px solid var(--bg-paper);
  z-index: 1;
  margin-bottom: 12px;
  transition: var(--transition);
}

.timeline-item:hover .timeline-dot {
  transform: scale(1.3);
  background: var(--color-gold);
}

.timeline-content {
  padding: 16px 12px;
  text-align: center;
  width: 120px;
}

.timeline-dynasty {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.timeline-years {
  font-size: 11px;
  color: var(--text-tertiary);
}

/* 书体 */
.styles-section {
  margin-bottom: 20px;
}

.styles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.style-card {
  text-align: center;
  padding: 28px 20px;
  cursor: pointer;
}

.style-char {
  font-size: 64px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 12px;
}

.style-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.style-desc {
  font-size: 13px;
  color: var(--text-tertiary);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 40px;
    letter-spacing: 8px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .styles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
