<template>
  <div class="app-wrapper">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="container header-inner">
        <router-link to="/" class="logo">
          <span class="logo-icon">翰</span>
          <span class="logo-text">翰墨千秋</span>
        </router-link>
        <nav class="nav-links">
          <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
          <router-link to="/calligraphers" class="nav-link" active-class="active">书法名家</router-link>
          <router-link to="/works" class="nav-link" active-class="active">传世之作</router-link>
        </nav>
      </div>
    </header>

    <!-- 路由内容 -->
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部 -->
    <footer class="app-footer">
      <div class="container">
        <p class="footer-text">翰墨千秋 · 历代书法名家作品集 — 汇聚千年翰墨，传承中华书道</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// 应用根组件
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 导航栏 */
.app-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
}

.logo-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-vermilion);
  color: var(--text-inverse);
  font-size: 20px;
  font-weight: 700;
  border-radius: var(--radius-sm);
}

.logo-text {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 2px;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  padding: 8px 20px;
  font-size: 15px;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.nav-link:hover {
  color: var(--color-vermilion);
  background: rgba(195, 39, 43, 0.06);
}

.nav-link.active {
  color: var(--color-vermilion);
  font-weight: 600;
}

/* 主体 */
.app-main {
  flex: 1;
  padding: 32px 0 48px;
}

/* 底部 */
.app-footer {
  border-top: 1px solid var(--border-color);
  background: var(--bg-paper-warm);
  padding: 24px 0;
}

.footer-text {
  text-align: center;
  font-size: 13px;
  color: var(--text-tertiary);
  letter-spacing: 1px;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .logo-text {
    display: none;
  }

  .nav-link {
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>
