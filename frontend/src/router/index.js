import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/calligraphers',
    name: 'Calligraphers',
    component: () => import('../views/Calligraphers.vue')
  },
  {
    path: '/calligrapher/:id',
    name: 'CalligrapherDetail',
    component: () => import('../views/CalligrapherDetail.vue')
  },
  {
    path: '/works',
    name: 'Works',
    component: () => import('../views/Works.vue')
  },
  {
    path: '/work/:id',
    name: 'WorkDetail',
    component: () => import('../views/WorkDetail.vue')
  }
]

const router = createRouter({
  // 使用 hash 模式，GitHub Pages 上刷新子路由不会 404
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
