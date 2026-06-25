import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../../services/api'

export const useFieldStore = defineStore('field', () => {
  const fields = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchFields = async () => {
    loading.value = true
    try {
      const response = await api.get('/api/fields')
      fields.value = response.data
      error.value = null
    } catch (err) {
      error.value = err.message
      console.error('获取农田数据失败:', err)
    } finally {
      loading.value = false
    }
  }

  const addField = async (fieldData) => {
    try {
      const response = await api.post('/api/fields', fieldData)
      fields.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('添加农田失败:', err)
      throw err
    }
  }

  const updateField = async (id, fieldData) => {
    try {
      const response = await api.put(`/api/fields/${id}`, fieldData)
      const index = fields.value.findIndex(f => f.id === id)
      if (index !== -1) {
        fields.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('更新农田失败:', err)
      throw err
    }
  }

  const deleteField = async (id) => {
    try {
      await api.delete(`/api/fields/${id}`)
      fields.value = fields.value.filter(f => f.id !== id)
    } catch (err) {
      error.value = err.message
      console.error('删除农田失败:', err)
      throw err
    }
  }

  return {
    fields,
    loading,
    error,
    fetchFields,
    addField,
    updateField,
    deleteField,
  }
})
