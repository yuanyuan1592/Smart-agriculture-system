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
        <div class="card healthy">
          <h3>健康农田</h3>
          <p class="value">{{ detectionStore.report.summary.healthy_count }}</p>
        </div>
      </div>

      <div class="alert-list">
        <h3>检测结果</h3>
        <div v-if="detectionStore.report.alerts.length === 0" class="empty">当前暂无异常，农田状态整体良好。</div>
        <div v-for="item in detectionStore.report.alerts" :key="item.field_name + item.title" class="alert-item" :class="item.type">
          <div>
            <strong>{{ item.field_name }}</strong>
            <p>{{ item.title }}</p>
            <span>{{ item.message }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted } from 'vue'
import { useDetectionStore } from './store'

export default defineComponent({
  name: 'Detection',
  setup() {
    const detectionStore = useDetectionStore()

    onMounted(() => {
      detectionStore.fetchReport()
    })

    return {
      detectionStore,
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
.alert-item {
  border-left: 4px solid #94a3b8;
  padding: 12px 14px;
  margin-top: 12px;
  background: #f8fafc;
  border-radius: 6px;
}
.alert-item.warning { border-left-color: #f59e0b; }
.alert-item.critical { border-left-color: #ef4444; }
.state { padding: 12px 0; color: #64748b; }
.state.error { color: #dc2626; }
.empty { color: #64748b; padding: 8px 0; }
</style>
