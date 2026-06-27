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

      <div class="recommendation-panel">
        <h3>智能建议</h3>
        <div class="recommendation-item">
          <h4>生长预测</h4>
          <p>{{ growthPrediction }}</p>
        </div>
        <div class="recommendation-item">
          <h4>产量估算</h4>
          <p>{{ estimatedYield }} 预估单位</p>
        </div>
        <div class="recommendation-item">
          <h4>肥水建议</h4>
          <p>{{ fertilizerAdvice }}</p>
        </div>
        <div class="recommendation-item">
          <h4>灌溉建议</h4>
          <p>{{ irrigationAdvice }}</p>
        </div>
        <div class="recommendation-item">
          <h4>灌溉规则建议</h4>
          <p>{{ irrigationRecommendation }}</p>
        </div>
        <div class="recommendation-item">
          <h4>病虫害预警</h4>
          <p>{{ pestRiskWarnings }}</p>
        </div>
      </div>

      <div class="trend-panel" v-if="trendDates.length">
        <h3>历史趋势</h3>
        <div class="chart-area">
          <svg :width="chartWidth" :height="chartHeight" :viewBox="`0 0 ${chartWidth} ${chartHeight}`">
            <g class="grid-lines">
              <line v-for="(label, index) in yAxisLabels" :key="label" :x1="chartPadding" :x2="chartWidth - chartPadding" :y1="chartHeight - chartPadding - (index * ((chartHeight - chartPadding * 2) / (yAxisLabels.length - 1)))" :y2="chartHeight - chartPadding - (index * ((chartHeight - chartPadding * 2) / (yAxisLabels.length - 1)))" stroke="#e5e7eb" stroke-dasharray="4 4" />
            </g>
            <path :d="moisturePath" class="line moisture-line" fill="none" stroke="#0ea5e9" stroke-width="3" />
            <path :d="temperaturePath" class="line temperature-line" fill="none" stroke="#f97316" stroke-width="3" />
            <g>
              <circle
                v-for="(point, index) in moisturePoints"
                :key="`moisture-${index}`"
                :cx="point.x"
                :cy="point.y"
                r="3"
                fill="#0ea5e9"
              />
              <circle
                v-for="(point, index) in temperaturePoints"
                :key="`temperature-${index}`"
                :cx="point.x"
                :cy="point.y"
                r="3"
                fill="#f97316"
              />
            </g>
          </svg>
          <div class="chart-legend">
            <span class="legend-item"><span class="legend-color moisture"></span>平均湿度</span>
            <span class="legend-item"><span class="legend-color temperature"></span>平均温度</span>
          </div>
          <div class="chart-xaxis">
            <span v-for="date in trendDates" :key="date">{{ date }}</span>
          </div>
        </div>
      </div>

      <div class="comparison-panel" v-if="fieldComparison.length">
        <h3>农田对比</h3>
        <table>
          <thead>
            <tr>
              <th>名称</th>
              <th>作物</th>
              <th>湿度 / 状态</th>
              <th>温度 / 状态</th>
              <th>风险等级</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="field in fieldComparison" :key="field.name">
              <td>{{ field.name }}</td>
              <td>{{ field.crop_type }}</td>
              <td>{{ field.moisture }}%（{{ field.moisture_status }}）</td>
              <td>{{ field.temperature }}℃（{{ field.temperature_status }}）</td>
              <td>{{ field.risk_level }}</td>
            </tr>
          </tbody>
        </table>
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

    const growthPrediction = computed(() => analyticsStore.summary.growth_prediction || '暂无预测结果')
    const estimatedYield = computed(() => analyticsStore.summary.estimated_yield || 0)
    const fertilizerAdvice = computed(() => analyticsStore.summary.fertilizer_advice || '暂无肥水建议')
    const irrigationAdvice = computed(() => analyticsStore.summary.irrigation_advice || '暂无灌溉建议')
    const irrigationRecommendation = computed(() => analyticsStore.summary.irrigation_recommendation || '暂无灌溉建议')
    const pestRiskWarnings = computed(() => analyticsStore.summary.pest_risk_warnings || '暂无病虫害风险')
    const trendSeries = computed(() => analyticsStore.summary.trend_series || { dates: [], avg_moisture: [], avg_temperature: [] })
    const fieldComparison = computed(() => analyticsStore.summary.field_comparison || [])

    const chartWidth = 660
    const chartHeight = 260
    const chartPadding = 40

    const chartValues = computed(() => {
      const moisture = trendSeries.value.avg_moisture
      const temperature = trendSeries.value.avg_temperature
      const values = [...moisture, ...temperature]
      const maxValue = Math.max(50, ...values)
      return {
        moisture,
        temperature,
        maxValue,
      }
    })

    const trendDates = computed(() => trendSeries.value.dates.slice(-7))
    const moisturePoints = computed(() => {
      const values = chartValues.value.moisture.slice(-7)
      const maxValue = chartValues.value.maxValue
      const length = values.length
      const stepX = length > 1 ? (chartWidth - chartPadding * 2) / (length - 1) : 0
      return values.map((value, index) => {
        const x = chartPadding + index * stepX
        const y = chartHeight - chartPadding - (value / maxValue) * (chartHeight - chartPadding * 2)
        return { x, y }
      })
    })
    const temperaturePoints = computed(() => {
      const values = chartValues.value.temperature.slice(-7)
      const maxValue = chartValues.value.maxValue
      const length = values.length
      const stepX = length > 1 ? (chartWidth - chartPadding * 2) / (length - 1) : 0
      return values.map((value, index) => {
        const x = chartPadding + index * stepX
        const y = chartHeight - chartPadding - (value / maxValue) * (chartHeight - chartPadding * 2)
        return { x, y }
      })
    })

    const linePath = (points) => {
      if (!points.length) return ''
      return points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' ')
    }

    const moisturePath = computed(() => linePath(moisturePoints.value))
    const temperaturePath = computed(() => linePath(temperaturePoints.value))

    const yAxisLabels = computed(() => {
      const maxValue = chartValues.value.maxValue
      return [0, Math.round(maxValue * 0.33), Math.round(maxValue * 0.66), Math.round(maxValue)]
    })

    onMounted(() => {
      analyticsStore.fetchSummary()
    })

    return {
      analyticsStore,
      averageArea,
      averageMoisture,
      averageTemperature,
      cropDistribution,
      growthPrediction,
      estimatedYield,
      fertilizerAdvice,
      irrigationAdvice,
      irrigationRecommendation,
      pestRiskWarnings,
      trendSeries,
      fieldComparison,
      chartWidth,
      chartHeight,
      chartPadding,
      trendDates,
      moisturePath,
      temperaturePath,
      temperaturePoints,
      yAxisLabels,
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

.recommendation-panel {
  margin-top: 30px;
  display: grid;
  gap: 20px;
}

.trend-panel {
  margin-top: 30px;
}

.chart-area {
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.chart-xaxis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 8px;
  margin-top: 12px;
  font-size: 12px;
  color: #64748b;
}

.chart-legend {
  display: flex;
  gap: 20px;
  margin-top: 12px;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #475569;
}

.legend-color {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  display: inline-block;
}

.legend-color.moisture {
  background: #0ea5e9;
}

.legend-color.temperature {
  background: #f97316;
}

.comparison-panel {
  margin-top: 30px;
}

.comparison-panel table {
  width: 100%;
  border-collapse: collapse;
}

.comparison-panel th,
.comparison-panel td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 14px;
}

.comparison-panel th {
  background: #f8fafc;
  color: #334155;
}

.comparison-panel tr:hover {
  background: #f9fafb;
}

.recommendation-item {
  background: #f8fafc;
  padding: 18px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.recommendation-item h4 {
  margin: 0 0 8px;
  font-size: 16px;
}

.recommendation-item p {
  margin: 0;
  color: #475569;
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
