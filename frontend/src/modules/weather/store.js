import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../../services/api'

export const useWeatherStore = defineStore('weather', () => {
  const weatherData = ref({ weather: [], generated_at: '' })
  const loading = ref(false)
  const error = ref('')

  const fetchWeather = async () => {
    loading.value = true
    error.value = ''
    try {
      const response = await api.get('/api/weather/')
      weatherData.value = response.data
    } catch (err) {
      error.value = err.message || '获取天气数据失败'
      console.error('获取天气数据失败:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    weatherData,
    loading,
    error,
    fetchWeather,
  }
})
