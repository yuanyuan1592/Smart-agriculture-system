import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useExampleStore = defineStore('example', () => {
  const data = ref([])
  const loading = ref(false)
  const error = ref('')

  const fetchData = async () => {
    loading.value = true
    try {
      // TODO: 接入接口
      data.value = []
    } catch (err) {
      error.value = err.message || '加载失败'
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
})
