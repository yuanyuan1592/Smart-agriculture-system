import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../../services/api'

export const useAnalyticsStore = defineStore('analytics', () => {
  const summary = ref({})
  const loading = ref(false)
  const error = ref('')

  const fetchSummary = async (days = 7) => {
    loading.value = true
    error.value = ''
    try {
      const response = await api.get('/api/analytics/', { params: { days } })
      summary.value = response.data
    } catch (err) {
      error.value = err.message || '获取分析数据失败'
      console.error('获取分析数据失败:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    summary,
    loading,
    error,
    fetchSummary,
  }
})
