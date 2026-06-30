<template>
  <div class="detection-page">
    <h2>农业检测</h2>
    <p class="subtitle">根据土壤湿度和温度自动生成异常预警，帮助你快速判断农田状态。</p>

    <div v-if="detectionStore.loading" class="state">加载中...</div>
    <div v-else-if="detectionStore.error" class="state error">{{ detectionStore.error }}</div>
    <div v-else class="content">
      <div class="summary-grid">
        <div class="card">
          <h3>总农田</h3>
          <p class="value">{{ detectionStore.report.summary.total_fields }}</p>
        </div>
        <div class="card warning">
          <h3>预警项</h3>
          <p class="value">{{ detectionStore.report.summary.warning_count }}</p>
        </div>
        <div class="card critical">
          <h3>严重风险</h3>
          <p class="value">{{ detectionStore.report.summary.critical_count }}</p>
        </div>
        <div class="card warning">
          <h3>天气预警</h3>
          <p class="value">{{ detectionStore.report.summary.weather_alert_count }}</p>
        </div>
        <div class="card critical">
          <h3>病虫害风险</h3>
          <p class="value">{{ detectionStore.report.summary.pest_risk_summary || '暂无' }}</p>
        </div>
        <div class="card healthy">
          <h3>健康农田</h3>
          <p class="value">{{ detectionStore.report.summary.healthy_count }}</p>
        </div>
      </div>

      <div v-if="detectionStore.report.summary.pest_risk_summary" class="pest-risk-summary">
        <h4>病虫害风险评估</h4>
        <p>{{ detectionStore.report.summary.pest_risk_summary }}</p>
      </div>

      <div class="alert-list">
        <h3>检测结果</h3>
        <div v-if="detectionStore.report.alerts.length === 0" class="empty">当前暂无异常，农田状态整体良好。</div>
        <div
          v-for="item in sortedAlerts"
          :key="item.field_name + item.title + item.source"
          class="alert-item"
          :class="[{ clickable: item.source === '传感器' && item.field_id }, item.type]"
          @click="gotoDeviceManagement(item)">
          <div class="alert-header">
            <div>
              <strong>{{ item.field_name }}</strong>
              <p>{{ item.title }}</p>
            </div>
            <div class="alert-tags">
              <span :class="['alert-badge', item.type]">{{ alertTypeLabel(item.type) }}</span>
              <span :class="['alert-source', item.source === '气象预警' ? 'weather' : 'sensor']">{{ item.source }}</span>
            </div>
          </div>
          <p class="alert-message">{{ item.message }}</p>
          <p class="alert-detail">{{ item.detail }}</p>
          <div class="alert-recommendation">
            <strong>推荐操作：</strong>{{ item.recommendation }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDetectionStore } from './store'

export default defineComponent({
  name: 'Detection',
  setup() {
    const router = useRouter()
    const detectionStore = useDetectionStore()

    const sortedAlerts = computed(() => {
      return [...(detectionStore.report.alerts || [])].sort((a, b) => {
        const priority = { critical: 0, warning: 1, normal: 2 }
        return (priority[a.type] || 2) - (priority[b.type] || 2)
      })
    })

    const alertTypeLabel = (type) => {
      if (type === 'critical') return '高风险'
      if (type === 'warning') return '警告'
      return '正常'
    }

    const getHighlightTypes = (title) => {
      const types = []
      if (title.includes('湿度')) {
        types.push('irrigation')
      }
      if (title.includes('温度') || title.includes('高温') || title.includes('低温') || title.includes('严寒') || title.includes('极端高温')) {
        types.push('temperature')
      }
      if (title.includes('风') || title.includes('通风')) {
        types.push('ventilation')
      }
      if (title.includes('农药')) {
        types.push('pesticide')
      }
      if (title.includes('补光') || title.includes('照明')) {
        types.push('lighting')
      }
      return [...new Set(types)]
    }

    const gotoDeviceManagement = (item) => {
      if (!item.field_id || item.source !== '传感器') {
        return
      }
      const highlightTypes = getHighlightTypes(item.title)
      const query = {
        field: item.field_id,
      }
      if (highlightTypes.length) {
        query.highlightTypes = highlightTypes.join(',')
      }
      router.push({ name: 'DeviceManagement', query })
    }

    onMounted(() => {
      detectionStore.fetchReport()
    })

    return {
      detectionStore,
      sortedAlerts,
      alertTypeLabel,
      gotoDeviceManagement,
    }
  }
})
</script>

<style scoped>
.detection-page {
  padding: 8px 0;
}
.subtitle {
  color: #666;
  margin-bottom: 24px;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 720px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .field-management,
  .detection-page,
  .weather-page,
  .analytics {
    padding: 0 10px;
  }
}
.card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.card.warning { border-left: 6px solid #f59e0b; }
.card.critical { border-left: 6px solid #ef4444; }
.card.healthy { border-left: 6px solid #10b981; }
.value {
  font-size: 28px;
  font-weight: bold;
  margin: 8px 0 0;
  color: #334155;
}
.alert-list {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.pest-risk-summary {
  margin: 20px 0;
  padding: 16px;
  border-radius: 10px;
  background: #fef9c3;
  color: #92400e;
}
.alert-item {
  border-left: 4px solid #94a3b8;
  padding: 16px;
  margin-top: 12px;
  background: #f8fafc;
  border-radius: 10px;
}
.alert-item.clickable {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.alert-item.clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
}
.alert-item.clickable::after {
  content: '点击查看设备';
  display: inline-block;
  margin-left: 12px;
  color: #2563eb;
  font-size: 12px;
}
.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
.alert-header strong {
  display: block;
  font-size: 15px;
  color: #1f2937;
}
.alert-tags {
  display: flex;
  gap: 8px;
  align-items: center;
}
.alert-badge {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: #ef4444;
}
.alert-badge.warning {
  background: #f59e0b;
}
.alert-badge.normal {
  background: #10b981;
}
.alert-source {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  background: #e2e8f0;
}
.alert-source.weather {
  background: #dbeafe;
  color: #1d4ed8;
}
.alert-source.sensor {
  background: #d1fae5;
  color: #065f46;
}
.alert-message {
  margin: 10px 0 0;
  color: #475569;
  line-height: 1.6;
}
.alert-detail {
  margin-top: 8px;
  color: #334155;
  font-size: 13px;
}
.alert-recommendation {
  margin-top: 10px;
  padding: 12px;
  border-radius: 8px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 14px;
  line-height: 1.6;
}
.alert-item.warning { border-left-color: #f59e0b; }
.alert-item.critical { border-left-color: #ef4444; }
.state { padding: 12px 0; color: #64748b; }
.state.error { color: #dc2626; }
.empty { color: #64748b; padding: 8px 0; }
</style>
