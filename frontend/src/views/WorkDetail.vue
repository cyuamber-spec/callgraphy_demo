<template>
  <div class="container detail-page">
    <div class="back-bar">
      <button class="btn" @click="$router.back()">← 返回</button>
    </div>

    <div v-if="loading" class="loading">正在加载...</div>

    <div v-else-if="!work" class="empty-state">作品不存在</div>

    <template v-else>
      <!-- 作品展示 -->
      <div class="work-showcase card">
        <div class="showcase-image">
          <img
            :src="getWorkImageUrl(work.id, 'large')"
            :alt="work.name"
            class="showcase-img"
          />
        </div>
        <div class="showcase-info">
          <h1 class="showcase-name">{{ work.name }}</h1>
          <div class="showcase-meta">
            <span class="dynasty-tag">{{ work.dynasty_name }}</span>
            <span class="style-tag">{{ work.style }}</span>
          </div>
          <p class="showcase-author">
            <span class="author-label">作者：</span>
            <router-link :to="`/calligrapher/${work.calligrapher_id}`" class="author-link">
              {{ work.calligrapher_name }}
            </router-link>
          </p>
          <p class="showcase-year">
            <span class="year-label">创作年代：</span>{{ formatYear(work.creation_year) }}
          </p>
          <div class="showcase-desc">
            <h3 class="desc-title">作品赏析</h3>
            <p class="desc-text">{{ work.description }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getWorkDetail, getWorkImageUrl } from '../api'

const route = useRoute()
const work = ref(null)
const loading = ref(true)

const formatYear = (year) => {
  if (year === null || year === undefined) return '年代不详'
  if (year < 0) return `公元前 ${Math.abs(year)} 年`
  return `${year} 年`
}

onMounted(async () => {
  try {
    work.value = await getWorkDetail(route.params.id)
  } catch (e) {
    console.error('加载作品详情失败', e)
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

.work-showcase {
  overflow: hidden;
}

.showcase-image {
  width: 100%;
  background: #f3ebdd;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

.showcase-img {
  max-width: 100%;
  max-height: 720px;
  object-fit: contain;
  display: block;
  box-shadow: 0 6px 24px rgba(60, 45, 20, 0.18);
}

.showcase-info {
  padding: 28px 32px;
}

.showcase-name {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.showcase-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.showcase-author,
.showcase-year {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.author-label,
.year-label {
  color: var(--text-tertiary);
}

.author-link {
  font-weight: 500;
}

.showcase-desc {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.desc-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-vermilion);
  margin-bottom: 12px;
}

.desc-text {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 2;
  text-align: justify;
}

@media (max-width: 768px) {
  .showcase-img {
    max-height: 520px;
  }

  .showcase-info {
    padding: 20px;
  }
}
</style>
