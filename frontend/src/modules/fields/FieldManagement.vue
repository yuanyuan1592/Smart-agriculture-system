<template>
  <div class="field-management">
    <h2>农田管理</h2>
    
    <div class="action-bar">
      <button @click="showAddForm = true" class="btn-primary">+ 添加农田</button>
    </div>

    <!-- 添加/编辑表单 -->
    <div v-if="showAddForm" class="form-container">
      <h3>{{ isEditing ? '编辑农田' : '添加新农田' }}</h3>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>农田名称:</label>
          <input v-model="formData.name" type="text" required>
        </div>
        <div class="form-group">
          <label>位置:</label>
          <input v-model="formData.location" type="text" required>
        </div>
        <div class="form-group">
          <label>面积 (亩):</label>
          <input v-model.number="formData.area" type="number" step="0.1" required>
        </div>
        <div class="form-group">
          <label>作物类型:</label>
          <input v-model="formData.crop_type" type="text" required>
        </div>
        <div class="form-group">
          <label>土壤湿度 (%):</label>
          <input v-model.number="formData.soil_moisture" type="number" step="0.1" required>
        </div>
        <div class="form-group">
          <label>温度 (℃):</label>
          <input v-model.number="formData.temperature" type="number" step="0.1" required>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-submit">提交</button>
          <button type="button" @click="cancelForm" class="btn-cancel">取消</button>
        </div>
      </form>
    </div>

    <!-- 农田列表 -->
    <div v-if="fieldStore.loading" class="loading">加载中...</div>
    <div v-else-if="fieldStore.error" class="error">{{ fieldStore.error }}</div>
    <div v-else class="fields-list">
      <div v-if="fieldStore.fields.length === 0" class="empty">暂无农田数据</div>
      <div v-for="field in fieldStore.fields" :key="field.id" class="field-card">
        <div class="field-info">
          <h3>{{ field.name }}</h3>
          <p><strong>位置:</strong> {{ field.location }}</p>
          <p><strong>面积:</strong> {{ field.area }} 亩</p>
          <p><strong>作物:</strong> {{ field.crop_type }}</p>
          <p><strong>土壤湿度:</strong> {{ field.soil_moisture }}%</p>
          <p><strong>温度:</strong> {{ field.temperature }}℃</p>
          <p><strong>状态:</strong> <span :class="['field-status', field.status]">{{ field.status }}</span></p>
        </div>
        <div class="field-actions">
          <button @click="editField(field)" class="btn-edit">编辑</button>
          <button @click="removeField(field.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useFieldStore } from './store'

export default defineComponent({
  name: 'FieldManagement',
  setup() {
    const fieldStore = useFieldStore()
    const showAddForm = ref(false)
    const isEditing = ref(false)
    const editingId = ref(null)
    const formData = ref({
      name: '',
      location: '',
      area: 0,
      crop_type: '',
      soil_moisture: 0,
      temperature: 0
    })

    const resetForm = () => {
      formData.value = {
        name: '',
        location: '',
        area: 0,
        crop_type: '',
        soil_moisture: 0,
        temperature: 0
      }
      isEditing.value = false
      editingId.value = null
    }

    const submitForm = async () => {
      try {
        if (isEditing.value) {
          await fieldStore.updateField(editingId.value, formData.value)
        } else {
          await fieldStore.addField(formData.value)
        }
        showAddForm.value = false
        resetForm()
      } catch (err) {
        console.error(err)
      }
    }

    const editField = (field) => {
      formData.value = { ...field }
      isEditing.value = true
      editingId.value = field.id
      showAddForm.value = true
    }

    const removeField = async (id) => {
      if (confirm('确定要删除该农田吗？')) {
        try {
          await fieldStore.deleteField(id)
        } catch (err) {
          console.error(err)
        }
      }
    }

    const cancelForm = () => {
      showAddForm.value = false
      resetForm()
    }

    onMounted(() => {
      fieldStore.fetchFields()
    })

    return {
      fieldStore,
      showAddForm,
      isEditing,
      formData,
      resetForm,
      submitForm,
      editField,
      removeField,
      cancelForm
    }
  }
})
</script>

<style scoped>
h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.action-bar {
  margin-bottom: 20px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  opacity: 0.9;
}

.form-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  background: #ccc;
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.field-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  text-transform: capitalize;
}

.field-status.normal {
  background: #d1fae5;
  color: #065f46;
}

.field-status.warning {
  background: #fef3c7;
  color: #92400e;
}

.field-status.alert {
  background: #fecaca;
  color: #991b1b;
}

.fields-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.field-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s;
}

.field-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.field-info {
  padding: 20px;
}

.field-info h3 {
  margin-bottom: 10px;
  color: #667eea;
}

.field-info p {
  margin: 8px 0;
  font-size: 14px;
}

.field-actions {
  display: flex;
  gap: 10px;
  padding: 10px 20px;
  border-top: 1px solid #eee;
  background: #f9f9f9;
}

.btn-edit, .btn-delete {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-edit {
  background: #667eea;
  color: white;
}

.btn-delete {
  background: #f56565;
  color: white;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
}
</style>
