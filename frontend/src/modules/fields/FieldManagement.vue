<template>
  <div class="field-management">
    <h2>农田管理</h2>
    
    <div class="action-bar">
      <button @click="showAddForm = true" class="btn-primary">+ 添加农田</button>
    </div>

    <div class="field-summary">
      <div class="summary-card">
        <span class="summary-title">总农田</span>
        <span class="summary-value">{{ totalFields }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">异常农田</span>
        <span class="summary-value">{{ alertFields }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">健康农田</span>
        <span class="summary-value">{{ normalFields }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">最新传感</span>
        <span class="summary-value">{{ formatTime(latestUpdate) }}</span>
      </div>
    </div>

    <!-- 添加/编辑模态弹窗 -->
    <div v-if="showAddForm" class="modal-overlay" @click.self="cancelForm">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑农田' : '添加新农田' }}</h3>
          <button class="modal-close" type="button" @click="cancelForm">×</button>
        </div>
        <form @submit.prevent="submitForm" class="modal-form">
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
          <div class="form-group">
            <label>光照强度 (lux):</label>
            <input v-model.number="formData.light_intensity" type="number" step="1" required>
          </div>
          <div class="form-group">
            <label>土壤 pH:</label>
            <input v-model.number="formData.soil_ph" type="number" step="0.1" required>
          </div>
          <div class="form-group threshold-group span-full">
            <label>土壤湿度阈值:</label>
            <div class="threshold-inputs">
              <input v-model.number="formData.moisture_threshold_low" type="number" step="0.1" placeholder="下限">
              <span>~</span>
              <input v-model.number="formData.moisture_threshold_high" type="number" step="0.1" placeholder="上限">
            </div>
          </div>
          <div class="form-group threshold-group span-full">
            <label>温度阈值:</label>
            <div class="threshold-inputs">
              <input v-model.number="formData.temperature_threshold_low" type="number" step="0.1" placeholder="下限">
              <span>~</span>
              <input v-model.number="formData.temperature_threshold_high" type="number" step="0.1" placeholder="上限">
            </div>
          </div>
          <div class="form-group threshold-group span-full">
            <label>光照阈值 (lux):</label>
            <div class="threshold-inputs">
              <input v-model.number="formData.light_threshold_low" type="number" step="1" placeholder="下限">
              <span>~</span>
              <input v-model.number="formData.light_threshold_high" type="number" step="1" placeholder="上限">
            </div>
          </div>
          <div class="form-group threshold-group span-full">
            <label>土壤 pH 阈值:</label>
            <div class="threshold-inputs">
              <input v-model.number="formData.ph_threshold_low" type="number" step="0.1" placeholder="下限">
              <span>~</span>
              <input v-model.number="formData.ph_threshold_high" type="number" step="0.1" placeholder="上限">
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">提交</button>
            <button type="button" @click="cancelForm" class="btn-cancel">取消</button>
          </div>
        </form>
      </div>
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
          <p><strong>光照强度:</strong> {{ field.light_intensity || 0 }} lux</p>
          <p><strong>土壤 pH:</strong> {{ field.soil_ph || 0 }}</p>
          <div class="field-status-row">
            <p><strong>状态:</strong> <span :class="['field-status', field.status]">{{ field.status }}</span></p>
            <span :class="['risk-pill', field.status]">{{ formatRiskLabel(field.status) }}</span>
          </div>
        <p><strong>湿度阈值:</strong> {{ field.moisture_threshold_low }}% ~ {{ field.moisture_threshold_high }}%</p>
        <p><strong>温度阈值:</strong> {{ field.temperature_threshold_low }}℃ ~ {{ field.temperature_threshold_high }}℃</p>
        <p><strong>光照阈值:</strong> {{ field.light_threshold_low || 8000 }} ~ {{ field.light_threshold_high || 30000 }} lux</p>
        <p><strong>pH 阈值:</strong> {{ field.ph_threshold_low || 6 }} ~ {{ field.ph_threshold_high || 7.5 }}</p>
        <p><strong>最新测量:</strong> {{ formatTime(field.last_measurement_at) }}</p>
        <div v-if="field.status !== 'normal'" class="status-note">当前测量值已超出阈值范围，请及时调整管理。</div>
        <div class="history-section">
          <h4>最近趋势</h4>
          <div v-if="getFieldTrend(field)" class="mini-trend">
            <div class="trend-chart-wrapper" @mousemove="handleTrendMouseMove(field, $event)" @mouseleave="clearTrendHover">
              <svg :width="160" :height="48" viewBox="0 0 160 48" preserveAspectRatio="none">
                <polyline :points="buildSparklinePath(getFieldTrend(field).avg_moisture, 160, 44)"
                          fill="none" stroke="#0ea5e9" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
                <polyline :points="buildSparklinePath(getFieldTrend(field).avg_temperature, 160, 44)"
                          fill="none" stroke="#f97316" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
              </svg>
              <div v-if="trendHover.visible && trendHover.fieldId === String(field.id || field.name)" class="trend-tooltip" :style="{ left: trendHover.x + 'px', top: trendHover.y + 'px' }">
                <div class="tooltip-date">{{ getFieldTrend(field).dates[trendHover.index] }}</div>
                <div>湿度：{{ getFieldTrend(field).avg_moisture[trendHover.index] }}%</div>
                <div>温度：{{ getFieldTrend(field).avg_temperature[trendHover.index] }}℃</div>
              </div>
            </div>
            <div class="trend-legend">
              <span><em class="legend-dot blue"></em>湿度</span>
              <span><em class="legend-dot orange"></em>温度</span>
            </div>
          </div>
          <div class="history-list" v-else>
            <div v-for="item in field.history" :key="field.id + item.timestamp" class="history-item">
              <span>{{ formatTime(item.timestamp) }}</span>
              <span>湿度 {{ item.soil_moisture }}%</span>
              <span>温度 {{ item.temperature }}℃</span>
            </div>
          </div>
        </div>
        </div>
        <div class="field-actions">
          <button @click="openDetailModal(field)" class="btn-view-detail">详情</button>
          <button @click="editField(field)" class="btn-edit">编辑</button>
          <button @click="removeField(field.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>

    <div v-if="showDetailModal && selectedField" class="modal-overlay" @click.self="closeDetailModal">
      <div class="detail-modal-container">
        <div class="modal-header">
          <h3>{{ selectedField.name }} 趋势详情</h3>
          <button class="modal-close" type="button" @click="closeDetailModal">×</button>
        </div>
        <div class="detail-modal-body">
          <div class="detail-summary">
            <div><strong>位置</strong>：{{ selectedField.location }}</div>
            <div><strong>作物</strong>：{{ selectedField.crop_type }}</div>
            <div><strong>最新湿度</strong>：{{ selectedField.soil_moisture }}%</div>
            <div><strong>最新温度</strong>：{{ selectedField.temperature }}℃</div>
          </div>
          <div class="detail-chart-card">
            <h4>农田趋势曲线</h4>
            <div v-if="getDetailTrend()" class="detail-chart-wrapper">
              <svg :width="540" :height="260" viewBox="0 0 540 260" preserveAspectRatio="none">
                <polyline :points="buildDetailPath(getDetailTrend().avg_moisture, 520, 220)"
                          fill="none" stroke="#0ea5e9" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
                <polyline :points="buildDetailPath(getDetailTrend().avg_temperature, 520, 220)"
                          fill="none" stroke="#f97316" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
              </svg>
              <div class="detail-trend-legend">
                <span><em class="legend-dot blue"></em>湿度</span>
                <span><em class="legend-dot orange"></em>温度</span>
              </div>
              <div class="detail-axis-labels">
                <span v-for="date in getDetailTrend().dates" :key="date">{{ date }}</span>
              </div>
            </div>
            <div v-else class="empty">暂无趋势数据</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useFieldStore } from './store'
import { useAnalyticsStore } from '../analytics/store'

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
      temperature: 0,
      light_intensity: 12000,
      soil_ph: 6.7,
      moisture_threshold_low: 30.0,
      moisture_threshold_high: 70.0,
      temperature_threshold_low: 15.0,
      temperature_threshold_high: 35.0,
      light_threshold_low: 8000.0,
      light_threshold_high: 30000.0,
      ph_threshold_low: 6.0,
      ph_threshold_high: 7.5,
    })

    const resetForm = () => {
      formData.value = {
        name: '',
        location: '',
        area: 0,
        crop_type: '',
        soil_moisture: 0,
        temperature: 0,
        light_intensity: 12000,
        soil_ph: 6.7,
        moisture_threshold_low: 30.0,
        moisture_threshold_high: 70.0,
        temperature_threshold_low: 15.0,
        temperature_threshold_high: 35.0,
        light_threshold_low: 8000.0,
        light_threshold_high: 30000.0,
        ph_threshold_low: 6.0,
        ph_threshold_high: 7.5,
      }
      isEditing.value = false
      editingId.value = null
    }

    const totalFields = computed(() => fieldStore.fields.length)
    const alertFields = computed(() => fieldStore.fields.filter((field) => field.status !== 'normal').length)
    const normalFields = computed(() => fieldStore.fields.filter((field) => field.status === 'normal').length)
    const latestUpdate = computed(() => {
      return fieldStore.fields.reduce((latest, field) => {
        if (!field.last_measurement_at) return latest
        const current = new Date(field.last_measurement_at)
        return !latest || current > new Date(latest) ? field.last_measurement_at : latest
      }, null)
    })

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

    const formatTime = (value) => {
      if (!value) return ''
      return new Date(value).toLocaleString()
    }

    const formatRiskLabel = (status) => {
      if (status === 'alert') return '高风险'
      if (status === 'warning') return '注意'
      return '正常'
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

    const analyticsStore = useAnalyticsStore()

    const perFieldTrends = ref({})
    const trendHover = ref({
      visible: false,
      x: 0,
      y: 0,
      fieldId: '',
      index: 0,
    })

    const normalizeValues = (values = []) => {
      if (!values.length) return []
      const max = Math.max(...values)
      const min = Math.min(...values)
      const range = max - min || 1
      return values.map((value) => (value - min) / range)
    }

    const buildSparklinePath = (values = [], width = 160, height = 44) => {
      if (!values || values.length === 0) return ''
      const normalized = normalizeValues(values)
      const step = width / Math.max(values.length - 1, 1)
      return normalized.map((ratio, i) => {
        const x = i * step
        const y = height - ratio * height
        return `${x},${y}`
      }).join(' ')
    }

    const getFieldTrend = (field) => {
      if (!field) return null
      const fid = String(field.id || field.name)
      return perFieldTrends.value[fid] || null
    }

    const handleTrendMouseMove = (field, event) => {
      const fieldTrend = getFieldTrend(field)
      if (!fieldTrend) return
      const rect = event.currentTarget.getBoundingClientRect()
      const width = rect.width
      const x = event.clientX - rect.left
      const index = Math.round(Math.min(fieldTrend.dates.length - 1, Math.max(0, x / (width / Math.max(fieldTrend.dates.length - 1, 1)))))
      trendHover.value = {
        visible: true,
        x: Math.min(width - 120, x + 10),
        y: 8,
        fieldId: String(field.id || field.name),
        index,
      }
    }

    const selectedField = ref(null)
    const showDetailModal = ref(false)

    const getDetailTrend = () => {
      if (!selectedField.value) return null
      return getFieldTrend(selectedField.value)
    }

    const buildDetailPath = (values = [], width = 520, height = 220, padding = 20) => {
      if (!values || values.length === 0) return ''
      const max = Math.max(...values)
      const min = Math.min(...values)
      const range = max - min || 1
      const step = (width - padding * 2) / Math.max(values.length - 1, 1)
      return values.map((value, index) => {
        const x = padding + index * step
        const y = padding + (height - padding * 2) * (1 - (value - min) / range)
        return `${x},${y}`
      }).join(' ')
    }

    const openDetailModal = (field) => {
      selectedField.value = field
      showDetailModal.value = true
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedField.value = null
    }

    const clearTrendHover = () => {
      trendHover.value.visible = false
    }

    onMounted(async () => {
      await fieldStore.fetchFields()
      try {
        if (analyticsStore && analyticsStore.fetchSummary) {
          await analyticsStore.fetchSummary(7)
          perFieldTrends.value = analyticsStore.summary.per_field_trends || {}
        }
      } catch (err) {
        console.error('加载 per_field_trends 失败', err)
      }
    })

    return {
      fieldStore,
      perFieldTrends,
      selectedField,
      showDetailModal,
      trendHover,
      showAddForm,
      isEditing,
      formData,
      resetForm,
      submitForm,
      editField,
      formatTime,
      formatRiskLabel,
      removeField,
      cancelForm,
      totalFields,
      alertFields,
      normalFields,
      latestUpdate,
      buildSparklinePath,
      buildDetailPath,
      getFieldTrend,
      getDetailTrend,
      handleTrendMouseMove,
      clearTrendHover,
      openDetailModal,
      closeDetailModal,
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

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}

.modal-container {
  width: min(100%, 820px);
  max-height: calc(100vh - 40px);
  background: white;
  border-radius: 16px;
  box-shadow: 0 16px 48px rgba(15, 23, 42, 0.18);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  color: #111827;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 24px;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 20;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #111827;
}

.modal-close {
  background: transparent;
  border: none;
  font-size: 24px;
  color: #475569;
  cursor: pointer;
}

.modal-form {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-auto-rows: minmax(min-content, max-content);
  gap: 20px;
  max-height: calc(100vh - 140px);
}

.form-group {
  margin-bottom: 15px;
}

.form-group.span-full,
.form-actions {
  grid-column: span 2;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  background: #f8fafc;
  color: #111827;
}

.threshold-inputs input {
  min-width: 0;
}

.threshold-group {
  gap: 10px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.form-actions button {
  flex: 1 1 160px;
}

.summary-card {
  background: #ffffff;
  padding: 18px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  text-align: left;
}

.summary-title {
  display: block;
  font-size: 13px;
  color: #68718a;
  margin-bottom: 8px;
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  color: #334155;
}

.threshold-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

@media (max-width: 840px) {
  .modal-form {
    grid-template-columns: 1fr;
  }
  .form-actions {
    grid-column: span 1;
  }
  .form-group.span-full {
    grid-column: span 1;
  }
}

.threshold-inputs {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 10px;
  align-items: center;
}

.threshold-inputs input {
  width: 100%;
  min-width: 0;
  margin-top: 16px;
  padding: 14px;
  background: #f8fafc;
  border-radius: 8px;
}

.history-list {
  display: grid;
  gap: 10px;
}

.mini-trend {
  margin: 8px 0 12px 0;
}

.trend-chart-wrapper {
  position: relative;
  width: 100%;
  max-width: 160px;
  min-height: 48px;
}

.mini-trend svg {
  background: #f8fafc;
  border-radius: 6px;
  display: block;
}

.trend-tooltip {
  position: absolute;
  z-index: 10;
  background: rgba(15, 23, 42, 0.95);
  color: white;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
  pointer-events: none;
}

.trend-tooltip .tooltip-date {
  font-weight: 700;
  margin-bottom: 4px;
}

.trend-legend,
.detail-trend-legend {
  display: flex;
  gap: 10px;
  margin-top: 8px;
  font-size: 12px;
  color: #475569;
}

.legend-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 999px;
  margin-right: 4px;
}

.legend-dot.blue {
  background: #0ea5e9;
}

.legend-dot.orange {
  background: #f97316;
}

.detail-modal-container {
  width: min(100%, 880px);
  max-width: 880px;
  background: white;
  border-radius: 18px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.detail-modal-body {
  padding: 24px;
  display: grid;
  gap: 24px;
}

.detail-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 24px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  color: #334155;
}

.detail-chart-card {
  background: #ffffff;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
}

.detail-chart-card h4 {
  margin: 0 0 16px;
  font-size: 16px;
}

.detail-chart-wrapper {
  position: relative;
}

.detail-axis-labels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 6px;
  margin-top: 12px;
  font-size: 12px;
  color: #6b7280;
}

.detail-axis-labels span {
  text-align: center;
}

.history-item {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  font-size: 13px;
  color: #475569;
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

.btn-view-detail {
  background: #10b981;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-view-detail:hover {
  opacity: 0.9;
}

.field-status-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.field-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  text-transform: capitalize;
}

.risk-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  color: white;
}

.risk-pill.normal {
  background: #10b981;
}

.risk-pill.warning {
  background: #f59e0b;
}

.risk-pill.alert {
  background: #ef4444;
}

.status-note {
  margin: 12px 0 0;
  padding: 12px;
  border-radius: 10px;
  background: #fff7ed;
  color: #92400e;
  font-size: 13px;
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
