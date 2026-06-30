<template>
  <div class="device-management">
    <h2>自动化设备管理</h2>

    <div class="device-summary">
      <div class="summary-card">
        <span class="summary-title">设备总数</span>
        <span class="summary-value">{{ devices.length }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">在线设备</span>
        <span class="summary-value">{{ onlineCount }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">离线设备</span>
        <span class="summary-value">{{ offlineCount }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">关联农田</span>
        <span class="summary-value">{{ fieldCount }}</span>
      </div>
    </div>

    <div class="field-list">
      <button
        :class="['field-chip', { active: selectedFieldId === 0 }]"
        @click="selectField(0)">
        全部农田
      </button>
      <button
        v-for="field in fields"
        :key="field.id"
        :class="['field-chip', { active: selectedFieldId === field.id }]"
        @click="selectField(field.id)">
        {{ field.name }}
      </button>
    </div>

    <div class="device-grid">
      <div v-for="device in filteredDevices" :key="device.id" class="device-card">
        <div class="device-card-header">
          <div>
            <div class="device-name">{{ device.name }}</div>
            <div class="device-type">{{ device.type_name }}</div>
          </div>
          <span :class="['device-status', device.status]">{{ device.status === 'on' ? '运行中' : '已停止' }}</span>
        </div>
        <div class="device-description">{{ device.description }}</div>
        <div class="device-info-row">
          <div><strong>设备ID</strong><br>{{ device.id }}</div>
          <div><strong>所属农田</strong><br>{{ fieldName(device.field_id) }}</div>
          <div><strong>控制模式</strong><br>{{ device.mode === 'auto' ? '自动' : '手动' }}</div>
          <div><strong>功率等级</strong><br>{{ device.power_level }}%</div>
        </div>
        <div class="device-actions">
          <button @click="togglePower(device)" class="btn-action">{{ device.status === 'on' ? '停止' : '启动' }}</button>
          <button @click="switchMode(device)" class="btn-action btn-secondary">{{ device.mode === 'auto' ? '切换手动' : '切换自动' }}</button>
          <button @click="openAdjustDialog(device)" class="btn-action btn-light">调节功率</button>
        </div>
      </div>
    </div>

    <div v-if="showAdjustDialog" class="dialog-overlay" @click.self="closeAdjustDialog">
      <div class="dialog-card">
        <div class="dialog-header">
          <h3>调节设备功率</h3>
          <button class="dialog-close" type="button" @click="closeAdjustDialog">×</button>
        </div>
        <div class="dialog-body">
          <p><strong>{{ currentDevice.name }}</strong></p>
          <p>{{ currentDevice.description }}</p>
          <div class="slider-row">
            <label>功率等级: {{ currentDevice.power_level }}%</label>
            <input type="range" min="0" max="100" v-model.number="currentDevice.power_level" />
          </div>
          <div class="mode-row">
            <label>控制模式:</label>
            <select v-model="currentDevice.mode">
              <option value="auto">自动</option>
              <option value="manual">手动</option>
            </select>
          </div>
        </div>
        <div class="dialog-actions">
          <button @click="saveDeviceSettings" class="btn-action">保存</button>
          <button @click="closeAdjustDialog" class="btn-action btn-secondary">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../services/api'
import { useFieldStore } from '../fields/store'

export default defineComponent({
  name: 'DeviceManagement',
  setup() {
    const fieldStore = useFieldStore()
    const route = useRoute()
    const devices = ref([])
    const selectedFieldId = ref(0)
    const highlightTypes = ref([])
    const showAdjustDialog = ref(false)
    const currentDevice = ref(null)

    const fetchDevices = async () => {
      try {
        const response = await api.get('/api/devices')
        devices.value = response.data
      } catch (err) {
        console.error('获取设备数据失败:', err)
      }
    }

    const loadDevicesByField = async () => {
      if (selectedFieldId.value > 0) {
        const response = await api.get(`/api/devices/field/${selectedFieldId.value}`)
        devices.value = response.data
      } else {
        await fetchDevices()
      }
    }

    const processRouteQuery = async () => {
      const fieldId = Number(route.query.field || 0)
      const types = String(route.query.highlightTypes || '')
        .split(',')
        .map((type) => type.trim())
        .filter(Boolean)

      selectedFieldId.value = Number.isNaN(fieldId) ? 0 : fieldId
      highlightTypes.value = types
      await loadDevicesByField()
    }

    const filteredDevices = computed(() => devices.value)
    const onlineCount = computed(() => devices.value.filter(d => d.status === 'on').length)
    const offlineCount = computed(() => devices.value.filter(d => d.status !== 'on').length)
    const fieldCount = computed(() => new Set(devices.value.map(d => d.field_id)).size)

    const fieldName = (fieldId) => {
      const field = fieldStore.fields.find(item => item.id === fieldId)
      return field ? field.name : '未知农田'
    }

    const selectField = async (fieldId) => {
      selectedFieldId.value = fieldId
      highlightTypes.value = []
      await loadDevicesByField()
    }

    const isHighlighted = (device) => {
      return highlightTypes.value.includes(device.type)
    }

    const togglePower = async (device) => {
      const updated = { status: device.status === 'on' ? 'off' : 'on' }
      await updateDevice(device, updated)
    }

    const switchMode = async (device) => {
      const updated = { mode: device.mode === 'auto' ? 'manual' : 'auto' }
      await updateDevice(device, updated)
    }

    const openAdjustDialog = (device) => {
      currentDevice.value = { ...device }
      showAdjustDialog.value = true
    }

    const closeAdjustDialog = () => {
      showAdjustDialog.value = false
      currentDevice.value = null
    }

    const saveDeviceSettings = async () => {
      if (!currentDevice.value) return
      await updateDevice(currentDevice.value, {
        power_level: currentDevice.value.power_level,
        mode: currentDevice.value.mode,
      })
      closeAdjustDialog()
    }

    const updateDevice = async (device, payload) => {
      try {
        const response = await api.put(`/api/devices/${device.id}`, payload)
        const index = devices.value.findIndex(item => item.id === device.id)
        if (index !== -1) {
          devices.value[index] = response.data
        }
        if (currentDevice.value && currentDevice.value.id === device.id) {
          currentDevice.value = response.data
        }
      } catch (err) {
        console.error('更新设备失败:', err)
      }
    }

    onMounted(async () => {
      await fieldStore.fetchFields()
      await processRouteQuery()
    })

    watch(
      () => route.query,
      () => {
        processRouteQuery()
      },
      { deep: true }
    )

    return {
      devices,
      selectedFieldId,
      showAdjustDialog,
      currentDevice,
      filteredDevices,
      onlineCount,
      offlineCount,
      fieldCount,
      fields: fieldStore.fields,
      fieldName,
      selectField,
      isHighlighted,
      togglePower,
      switchMode,
      openAdjustDialog,
      closeAdjustDialog,
      saveDeviceSettings,
    }
  },
})
</script>

<style scoped>
.device-management {
  display: grid;
  gap: 24px;
}

.device-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.summary-card {
  background: #fff;
  padding: 18px;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.summary-title {
  display: block;
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
}

.summary-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
}

.field-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 0;
}

.field-chip {
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #334155;
  padding: 10px 14px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.device-card.highlight {
  animation: pulse-highlight 0.6s ease-in-out 3;
  border-color: #4338ca;
}

@keyframes pulse-highlight {
  0%, 100% {
    box-shadow: 0 0 0 rgba(79, 70, 229, 0.18);
  }
  50% {
    box-shadow: 0 0 0 18px rgba(79, 70, 229, 0.08);
  }
}

.field-chip:hover {
  background: #eef2ff;
}

.field-chip.active {
  background: #4f46e5;
  color: white;
  border-color: #4338ca;
}

.device-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

.device-card {
  background: white;
  border-radius: 18px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

.device-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.device-name {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.device-type {
  font-size: 13px;
  color: #64748b;
}

.device-status {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.device-status.on {
  background: #d1fae5;
  color: #047857;
}

.device-status.off {
  background: #fee2e2;
  color: #b91c1c;
}

.device-description {
  margin-bottom: 18px;
  color: #475569;
  line-height: 1.75;
}

.device-info-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.device-info-row div {
  font-size: 13px;
  color: #334155;
}

.device-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.btn-action {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  background: #4f46e5;
  color: white;
  font-weight: 700;
}

.btn-secondary {
  background: #e2e8f0;
  color: #334155;
}

.btn-light {
  background: #f8fafc;
  color: #334155;
}

.dialog-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.dialog-card {
  width: min(100%, 520px);
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(15, 23, 42, 0.18);
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
}

.dialog-close {
  border: none;
  background: transparent;
  color: #475569;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

.dialog-body {
  padding: 22px 24px;
}

.slider-row,
.mode-row {
  display: grid;
  gap: 12px;
  margin-top: 16px;
}

.slider-row input,
.mode-row select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
}

.dialog-actions {
  display: flex;
  gap: 12px;
  padding: 18px 24px 24px;
}

.dialog-actions .btn-action {
  flex: 1;
}
</style>
