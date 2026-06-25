import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../../services/api'

export const useDetectionStore = defineStore('detection', () => {
  const report = ref({ summary: {}, alerts: [] })
  const loading = ref(false)
  const error = ref('')

  const fetchReport = async () => {
    loading.value = true
    error.value = ''
    try {
      const response = await api.get('/api/detection/')
      report.value = response.data
    } catch (err) {
      error.value = err.message || '获取检测报告失败'
      console.error('获取检测报告失败:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    report,
    loading,
    error,
    fetchReport,
  }
})
