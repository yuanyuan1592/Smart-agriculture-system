import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useFieldStore = defineStore('field', () => {
  const fields = ref([])
  const loading = ref(false)
  const error = ref(null)

  const API_URL = 'http://localhost:8000/api/fields'

  const fetchFields = async () => {
    loading.value = true
    try {
      const response = await axios.get(API_URL)
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
      const response = await axios.post(API_URL, fieldData)
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
      const response = await axios.put(`${API_URL}/${id}`, fieldData)
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
      await axios.delete(`${API_URL}/${id}`)
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
    deleteField
  }
})
