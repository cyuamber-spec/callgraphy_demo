import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // GitHub Pages 部署在子路径 /callgraphy_demo/ 下，base 必须与之匹配
  base: '/callgraphy_demo/',
  plugins: [vue()],
  server: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})
