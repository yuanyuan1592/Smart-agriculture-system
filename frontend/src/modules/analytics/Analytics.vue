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

      <div class="stat-card">
        <h3>平均光照</h3>
        <p class="stat-value">{{ averageLight }} lux</p>
      </div>

      <div class="stat-card">
        <h3>平均土壤 pH</h3>
        <p class="stat-value">{{ averagePh }}</p>
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
          <span class="crop-count">{{ crop.area.toFixed(2) }} 亩</span>
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
        <p class="panel-subtitle">查看过去一段时间内农田湿度、温度、光照与 pH 的变化曲线，便于判断环境是否持续稳定。</p>
        <div class="trend-controls">
          <div class="range-buttons">
            <button
              v-for="option in rangeOptions"
              :key="option"
              :class="['range-button', { active: selectedDays === option }]"
              @click="setRange(option)">
              {{ option }} 天
            </button>
          </div>
          <div class="trend-tip">当前高亮最新日期：{{ latestMetrics.date || '无数据' }}</div>
        </div>
        <div class="chart-area">
          <svg :width="chartWidth" :height="chartHeight" :viewBox="`0 0 ${chartWidth} ${chartHeight}`">
            <g class="axis-lines">
              <line :x1="chartPadding" :x2="chartPadding" :y1="chartPadding" :y2="chartHeight - chartPadding" stroke="#94a3b8" stroke-width="1" opacity="0.7" />
              <line :x1="chartPadding" :x2="chartWidth - chartPadding" :y1="chartHeight - chartPadding" :y2="chartHeight - chartPadding" stroke="#94a3b8" stroke-width="1" opacity="0.7" />
            </g>
            <g class="grid-lines">
              <line v-for="(label, index) in yAxisLabels" :key="label" :x1="chartPadding" :x2="chartWidth - chartPadding" :y1="chartHeight - chartPadding - (index * ((chartHeight - chartPadding * 2) / (yAxisLabels.length - 1)))" :y2="chartHeight - chartPadding - (index * ((chartHeight - chartPadding * 2) / (yAxisLabels.length - 1)))" stroke="#e5e7eb" stroke-dasharray="4 4" />
              <text
                v-for="(label, index) in yAxisLabels"
                :key="`y-label-${index}`"
                :x="chartPadding - 12"
                :y="chartHeight - chartPadding - (index * ((chartHeight - chartPadding * 2) / (yAxisLabels.length - 1))) + 4"
                text-anchor="end"
                fill="#475569"
                font-size="12">
                {{ label }}
              </text>
            </g>
            <g class="x-ticks">
              <line
                v-for="(point, index) in moisturePoints"
                :key="`tick-${index}`"
                :x1="point.x"
                :x2="point.x"
                :y1="chartHeight - chartPadding"
                :y2="chartHeight - chartPadding + 6"
                stroke="#cbd5e1"
                stroke-width="1" />
            </g>
            <path v-if="showSeries.moisture" :d="moisturePath" class="line moisture-line" fill="none" stroke="#0ea5e9" stroke-width="3" />
            <path v-if="showSeries.temperature" :d="temperaturePath" class="line temperature-line" fill="none" stroke="#f97316" stroke-width="3" />
            <path v-if="showSeries.light" :d="lightPath" class="line light-line" fill="none" stroke="#10b981" stroke-width="3" />
            <path v-if="showSeries.ph" :d="phPath" class="line ph-line" fill="none" stroke="#8b5cf6" stroke-width="3" />
            <line v-if="latestLineX !== null" :x1="latestLineX" :x2="latestLineX" :y1="chartPadding" :y2="chartHeight - chartPadding" stroke="#94a3b8" stroke-dasharray="3 3" />
            <line v-if="hoverLineX !== null" :x1="hoverLineX" :x2="hoverLineX" :y1="chartPadding" :y2="chartHeight - chartPadding" stroke="#2563eb" stroke-width="1" opacity="0.75" />
            <g>
              <circle
                v-if="showSeries.moisture"
                v-for="(point, index) in moisturePoints"
                :key="`moisture-${index}`"
                :cx="point.x"
                :cy="point.y"
                :r="index === activeIndex ? 5 : index === hoveredIndex ? 6 : 3"
                :fill="index === activeIndex ? '#ffffff' : '#0ea5e9'"
                :stroke="index === activeIndex || index === hoveredIndex ? '#0ea5e9' : 'transparent'"
                stroke-width="2"
                @mouseenter="setHoveredIndex(index)"
                @mouseleave="clearHoveredIndex"
              />
              <circle
                v-if="showSeries.temperature"
                v-for="(point, index) in temperaturePoints"
                :key="`temperature-${index}`"
                :cx="point.x"
                :cy="point.y"
                :r="index === activeIndex ? 5 : index === hoveredIndex ? 6 : 3"
                :fill="index === activeIndex ? '#ffffff' : '#f97316'"
                :stroke="index === activeIndex || index === hoveredIndex ? '#f97316' : 'transparent'"
                stroke-width="2"
                @mouseenter="setHoveredIndex(index)"
                @mouseleave="clearHoveredIndex"
              />
              <circle
                v-if="showSeries.light"
                v-for="(point, index) in lightPoints"
                :key="`light-${index}`"
                :cx="point.x"
                :cy="point.y"
                :r="index === activeIndex ? 5 : index === hoveredIndex ? 6 : 3"
                :fill="index === activeIndex ? '#ffffff' : '#10b981'"
                :stroke="index === activeIndex || index === hoveredIndex ? '#10b981' : 'transparent'"
                stroke-width="2"
                @mouseenter="setHoveredIndex(index)"
                @mouseleave="clearHoveredIndex"
              />
              <circle
                v-if="showSeries.ph"
                v-for="(point, index) in phPoints"
                :key="`ph-${index}`"
                :cx="point.x"
                :cy="point.y"
                :r="index === activeIndex ? 5 : index === hoveredIndex ? 6 : 3"
                :fill="index === activeIndex ? '#ffffff' : '#8b5cf6'"
                :stroke="index === activeIndex || index === hoveredIndex ? '#8b5cf6' : 'transparent'"
                stroke-width="2"
                @mouseenter="setHoveredIndex(index)"
                @mouseleave="clearHoveredIndex"
              />
            </g>
          </svg>
          <div v-if="hoveredIndex !== null" class="chart-tooltip" :style="tooltipStyle">
            <div class="tooltip-title">{{ trendDates[hoveredIndex] || '无日期' }}</div>
            <div class="tooltip-row"><span class="tooltip-label"><span class="tooltip-dot moisture"></span>湿度</span><span>{{ chartValues.moisture[hoveredIndex] ?? 0 }}%</span></div>
            <div class="tooltip-row"><span class="tooltip-label"><span class="tooltip-dot temperature"></span>温度</span><span>{{ chartValues.temperature[hoveredIndex] ?? 0 }}℃</span></div>
            <div class="tooltip-row"><span class="tooltip-label"><span class="tooltip-dot light"></span>光照</span><span>{{ chartValues.light[hoveredIndex] ?? 0 }} lx</span></div>
            <div class="tooltip-row"><span class="tooltip-label"><span class="tooltip-dot ph"></span>土壤 pH</span><span>{{ chartValues.ph[hoveredIndex] ?? 0 }}</span></div>
          </div>
          <div class="chart-legend">
            <button type="button" class="legend-item" :class="{ active: showSeries.moisture }" @click="toggleSeries('moisture')">
              <span class="legend-color moisture"></span>平均湿度
            </button>
            <button type="button" class="legend-item" :class="{ active: showSeries.temperature }" @click="toggleSeries('temperature')">
              <span class="legend-color temperature"></span>平均温度
            </button>
            <button type="button" class="legend-item" :class="{ active: showSeries.light }" @click="toggleSeries('light')">
              <span class="legend-color light"></span>平均光照
            </button>
            <button type="button" class="legend-item" :class="{ active: showSeries.ph }" @click="toggleSeries('ph')">
              <span class="legend-color ph"></span>平均pH
            </button>
          </div>
          <div class="chart-xaxis">
            <span v-for="label in xAxisLabels" :key="label.index" :class="{ active: label.index === activeIndex, hover: label.index === hoveredIndex }">{{ label.date }}</span>
          </div>
          <div class="trend-summary">
            <div class="summary-card">
              <div class="summary-title">最新日期</div>
              <div class="summary-value">{{ latestMetrics.date || '—' }}</div>
            </div>
            <div class="summary-card">
              <div class="summary-title">湿度</div>
              <div class="summary-value">{{ latestMetrics.moisture }}%</div>
            </div>
            <div class="summary-card">
              <div class="summary-title">温度</div>
              <div class="summary-value">{{ latestMetrics.temperature }}℃</div>
            </div>
            <div class="summary-card">
              <div class="summary-title">光照</div>
              <div class="summary-value">{{ latestMetrics.light }} lx</div>
            </div>
            <div class="summary-card">
              <div class="summary-title">土壤 pH</div>
              <div class="summary-value">{{ latestMetrics.ph }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="comparison-panel" v-if="fieldComparison.length">
        <h3>农田对比报表</h3>
        <p class="panel-subtitle">从多块农田的环境状态出发，快速发现需要重点关注的区域。</p>
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
import { defineComponent, computed, onMounted, ref } from 'vue'
import { useAnalyticsStore } from './store'

export default defineComponent({
  name: 'Analytics',
  setup() {
    const analyticsStore = useAnalyticsStore()
    const selectedDays = ref(7)
    const rangeOptions = [7, 14, 30]

    const formatNumber = (value) => {
      if (value === null || value === undefined || Number.isNaN(Number(value))) {
        return '0.00'
      }
      return Number(value).toFixed(2)
    }

    const averageArea = computed(() => formatNumber(analyticsStore.summary.average_area))
    const averageMoisture = computed(() => formatNumber(analyticsStore.summary.average_moisture))
    const averageTemperature = computed(() => formatNumber(analyticsStore.summary.average_temperature))
    const averageLight = computed(() => formatNumber(analyticsStore.summary.average_light))
    const averagePh = computed(() => formatNumber(analyticsStore.summary.average_ph))

    const totalArea = computed(() => Number(analyticsStore.summary.total_area || 0))

    const cropDistribution = computed(() => {
      const distribution = analyticsStore.summary.crop_distribution || {}
      const areaTotal = totalArea.value || Object.values(distribution).reduce((sum, area) => sum + Number(area || 0), 0)
      return Object.entries(distribution).map(([type, area]) => ({
        type,
        area: Number(area || 0),
        percentage: areaTotal ? Math.round((Number(area || 0) / areaTotal) * 100) : 0
      }))
    })

    const growthPrediction = computed(() => analyticsStore.summary.growth_prediction || '暂无预测结果')
    const estimatedYield = computed(() => analyticsStore.summary.estimated_yield || 0)
    const fertilizerAdvice = computed(() => analyticsStore.summary.fertilizer_advice || '暂无肥水建议')
    const irrigationAdvice = computed(() => analyticsStore.summary.irrigation_advice || '暂无灌溉建议')
    const irrigationRecommendation = computed(() => analyticsStore.summary.irrigation_recommendation || '暂无灌溉建议')
    const pestRiskWarnings = computed(() => analyticsStore.summary.pest_risk_warnings || '暂无病虫害风险')
    const trendSeries = computed(() => analyticsStore.summary.trend_series || { dates: [], avg_moisture: [], avg_temperature: [], avg_light: [], avg_ph: [] })
    const fieldComparison = computed(() => analyticsStore.summary.field_comparison || [])

    const chartWidth = 660
    const chartHeight = 260
    const chartPadding = 40

    const chartValues = computed(() => {
      const moisture = trendSeries.value.avg_moisture || []
      const temperature = trendSeries.value.avg_temperature || []
      const light = trendSeries.value.avg_light || []
      const ph = trendSeries.value.avg_ph || []
      const values = [...moisture, ...temperature, ...light, ...ph]
      const maxValue = Math.max(50, ...values)
      return {
        moisture,
        temperature,
        light,
        ph,
        maxValue,
      }
    })

    const trendDates = computed(() => trendSeries.value.dates || [])
    const seriesToPoints = (values) => {
      const length = values.length
      const stepX = length > 1 ? (chartWidth - chartPadding * 2) / (length - 1) : 0
      return values.map((value, index) => {
        const x = chartPadding + index * stepX
        const y = chartHeight - chartPadding - (value / chartValues.value.maxValue) * (chartHeight - chartPadding * 2)
        return { x, y }
      })
    }

    const moisturePoints = computed(() => seriesToPoints(chartValues.value.moisture))
    const temperaturePoints = computed(() => seriesToPoints(chartValues.value.temperature))
    const lightPoints = computed(() => seriesToPoints(chartValues.value.light))
    const phPoints = computed(() => seriesToPoints(chartValues.value.ph))

    const linePath = (points) => {
      if (!points.length) return ''
      return points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' ')
    }

    const moisturePath = computed(() => linePath(moisturePoints.value))
    const temperaturePath = computed(() => linePath(temperaturePoints.value))
    const lightPath = computed(() => linePath(lightPoints.value))
    const phPath = computed(() => linePath(phPoints.value))

    const hoveredIndex = ref(null)
    const showSeries = ref({
      moisture: true,
      temperature: true,
      light: true,
      ph: true,
    })
    const activeIndex = computed(() => Math.max(0, trendDates.value.length - 1))
    const latestMetrics = computed(() => {
      const index = activeIndex.value
      return {
        date: trendDates.value[index] || '',
        moisture: chartValues.value.moisture[index] ?? 0,
        temperature: chartValues.value.temperature[index] ?? 0,
        light: chartValues.value.light[index] ?? 0,
        ph: chartValues.value.ph[index] ?? 0,
      }
    })

    const latestLineX = computed(() => {
      if (trendDates.value.length <= 1) return null
      return chartPadding + activeIndex.value * ((chartWidth - chartPadding * 2) / (trendDates.value.length - 1))
    })

    const hoverLineX = computed(() => {
      if (hoveredIndex.value === null || trendDates.value.length <= 1) return null
      return chartPadding + hoveredIndex.value * ((chartWidth - chartPadding * 2) / (trendDates.value.length - 1))
    })

    const tooltipStyle = computed(() => {
      if (hoveredIndex.value === null) return {}
      const x = chartPadding + hoveredIndex.value * ((chartWidth - chartPadding * 2) / Math.max(1, trendDates.value.length - 1))
      const left = Math.min(chartWidth - 220, Math.max(10, x + 10))
      return {
        left: `${left}px`,
        top: '18px',
      }
    })

    const setHoveredIndex = (index) => {
      hoveredIndex.value = index
    }

    const clearHoveredIndex = () => {
      hoveredIndex.value = null
    }

    const toggleSeries = (name) => {
      if (name in showSeries.value) {
        showSeries.value[name] = !showSeries.value[name]
      }
    }

    const yAxisLabels = computed(() => {
      const maxValue = chartValues.value.maxValue
      return [0, Math.round(maxValue * 0.33), Math.round(maxValue * 0.66), Math.round(maxValue)]
    })

    const xAxisLabels = computed(() => {
      const dates = trendDates.value
      const count = dates.length
      if (count <= 7) {
        return dates.map((date, index) => ({ date, index }))
      }
      const maxLabels = 7
      const step = Math.max(1, Math.ceil((count - 1) / (maxLabels - 1)))
      const indices = []
      for (let i = 0; i < count; i += step) {
        indices.push(i)
      }
      if (indices[indices.length - 1] !== count - 1) {
        indices.push(count - 1)
      }
      return indices.map((index) => ({ date: dates[index], index }))
    })

    const setRange = async (days) => {
      selectedDays.value = days
      await analyticsStore.fetchSummary(days)
    }

    onMounted(() => {
      analyticsStore.fetchSummary(selectedDays.value)
    })

    return {
      analyticsStore,
      selectedDays,
      rangeOptions,
      averageArea,
      averageMoisture,
      averageTemperature,
      averageLight,
      averagePh,
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
      lightPath,
      phPath,
      temperaturePoints,
      lightPoints,
      phPoints,
      yAxisLabels,
      activeIndex,
      latestMetrics,
      latestLineX,
      hoveredIndex,
      tooltipStyle,
      showSeries,
      setRange,
      setHoveredIndex,
      clearHoveredIndex,
      toggleSeries,
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
  margin-bottom: 12px;
}

.panel-subtitle {
  margin: 0 0 16px;
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
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

.trend-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.range-buttons {
  display: flex;
  gap: 10px;
}

.range-button {
  padding: 8px 14px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #334155;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}

.range-button:hover,
.range-button.active {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}

.trend-tip {
  color: #475569;
  font-size: 14px;
}

.chart-area {
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.chart-xaxis {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
  font-size: 12px;
  color: #64748b;
  align-items: flex-end;
}

.chart-xaxis span {
  display: inline-block;
  transform: rotate(-22deg);
  transform-origin: left center;
  white-space: nowrap;
  padding-right: 6px;
}

.chart-xaxis span.active,
.chart-xaxis span.hover {
  color: #0f172a;
  font-weight: 600;
}

.trend-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 14px;
  margin-top: 18px;
}

.summary-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;
  text-align: center;
}

.summary-title {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 6px;
}

.summary-value {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
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
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  font: inherit;
}

.legend-item.active {
  color: #0f172a;
  font-weight: 700;
}

.chart-tooltip {
  position: absolute;
  z-index: 10;
  min-width: 200px;
  background: rgba(15, 23, 42, 0.96);
  color: white;
  padding: 12px 14px;
  border-radius: 10px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18);
  font-size: 13px;
}

.tooltip-title {
  font-weight: 700;
  margin-bottom: 8px;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.tooltip-row:last-child {
  margin-bottom: 0;
}

.tooltip-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #e2e8f0;
}

.tooltip-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.tooltip-dot.moisture {
  background: #0ea5e9;
}

.tooltip-dot.temperature {
  background: #f97316;
}

.tooltip-dot.light {
  background: #10b981;
}

.tooltip-dot.ph {
  background: #8b5cf6;
}

.chart-area {
  position: relative;
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
.legend-color.light {
  background: #10b981;
}
.legend-color.ph {
  background: #8b5cf6;
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
