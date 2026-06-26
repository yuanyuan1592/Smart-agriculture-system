<template>
  <div class="analytics">
    <h2>数据分析</h2>
    
    <div v-if="analyticsStore.loading" class="state">加载中...</div>
  <div v-else-if="analyticsStore.error" class="state error">{{ analyticsStore.error }}</div>
  <div v-else class="stats-grid">
      <div class="stat-card">
        <h3>总农田数</h3>
        <p class="stat-value">{{ analyticsStore.summary.total_fields || 0 }}</p>
      </div>
      
      <div class="stat-card">
        <h3>平均面积</h3>
        <p class="stat-value">{{ averageArea }} 亩</p>
      </div>
      
      <div class="stat-card">
        <h3>平均湿度</h3>
        <p class="stat-value">{{ averageMoisture }}%</p>
      </div>
      
      <div class="stat-card">
        <h3>平均温度</h3>
        <p class="stat-value">{{ averageTemperature }}℃</p>
      </div>
    </div>

    <div v-if="!analyticsStore.loading && !analyticsStore.error" class="crops-analysis">
      <h3>作物分布</h3>
      <div class="crop-list">
        <div v-for="crop in cropDistribution" :key="crop.type" class="crop-item">
          <span class="crop-name">{{ crop.type }}</span>
          <div class="crop-bar">
            <div class="crop-progress" :style="{ width: crop.percentage + '%' }"></div>
          </div>
          <span class="crop-count">{{ crop.count }} 个</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed, onMounted } from 'vue'
import { useAnalyticsStore } from './store'

export default defineComponent({
  name: 'Analytics',
  setup() {
    const analyticsStore = useAnalyticsStore()

    const averageArea = computed(() => analyticsStore.summary.average_area || 0)
    const averageMoisture = computed(() => analyticsStore.summary.average_moisture || 0)
    const averageTemperature = computed(() => analyticsStore.summary.average_temperature || 0)

    const cropDistribution = computed(() => {
      const distribution = analyticsStore.summary.crop_distribution || {}
      return Object.entries(distribution).map(([type, count]) => ({
        type,
        count,
        percentage: analyticsStore.summary.total_fields
          ? Math.round((count / analyticsStore.summary.total_fields) * 100)
          : 0
      }))
    })

    onMounted(() => {
      analyticsStore.fetchSummary()
    })

    return {
      analyticsStore,
      averageArea,
      averageMoisture,
      averageTemperature,
      cropDistribution
    }
  }
})
</script>

<style scoped>
h2 {
  font-size: 24px;
  margin-bottom: 30px;
}

h3 {
  font-size: 18px;
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 32px;
  color: #667eea;
  font-weight: bold;
  margin: 0;
}

.crops-analysis {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.crop-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.crop-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.crop-name {
  min-width: 100px;
  font-weight: bold;
}

.crop-bar {
  flex: 1;
  height: 24px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.crop-progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.crop-count {
  min-width: 60px;
  text-align: right;
  color: #666;
}
</style>
