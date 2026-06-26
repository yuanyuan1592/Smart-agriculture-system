import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import FieldManagement from '../modules/fields/FieldManagement.vue'
import Analytics from '../modules/analytics/Analytics.vue'
import Detection from '../modules/detection/Detection.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/fields',
    name: 'FieldManagement',
    component: FieldManagement
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics
  },
  {
    path: '/detection',
    name: 'Detection',
    component: Detection
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
