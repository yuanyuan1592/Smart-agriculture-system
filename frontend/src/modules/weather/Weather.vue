<template>
  <div class="weather-page">
    <h2>天气预报与灾害预测</h2>
    <p class="subtitle">提供温度、湿度、风向、风力、空气质量、紫外线指数，以及灾害预警。</p>

    <div v-if="weatherStore.loading" class="state">加载中...</div>
    <div v-else-if="weatherStore.error" class="state error">{{ weatherStore.error }}</div>
    <div v-else>
      <div class="weather-list">
        <div v-for="item in weatherStore.weatherData.weather" :key="item.id" class="weather-card">
          <div class="weather-header">
            <div>
              <h3>{{ item.location }}</h3>
              <p>{{ item.condition }} · 更新时间 {{ formatTime(item.generated_at) }}</p>
            </div>
            <div class="temperature">{{ item.temperature }}℃</div>
          </div>

          <div class="weather-stats">
            <div class="stat-item"><strong>湿度</strong><span>{{ item.humidity }}%</span></div>
            <div class="stat-item"><strong>风向</strong><span>{{ item.wind_direction }}</span></div>
            <div class="stat-item"><strong>风力</strong><span>{{ item.wind_strength }}</span></div>
            <div class="stat-item"><strong>空气质量</strong><span>{{ item.air_quality }} (AQI {{ item.aqi }})</span></div>
            <div class="stat-item"><strong>紫外线</strong><span>{{ item.uv_index }}</span></div>
          </div>

          <div class="forecast-section">
            <h4>未来三天天气</h4>
            <div class="forecast-grid">
              <div v-for="day in item.forecast" :key="day.day" class="forecast-card">
                <div class="day-label">{{ day.day }}</div>
                <div>{{ day.condition }}</div>
                <div>{{ day.low }}℃ ~ {{ day.high }}℃</div>
                <div>{{ day.wind_direction }} {{ day.wind_strength }}</div>
                <div>AQI {{ day.aqi }} · UV {{ day.uv_index }}</div>
              </div>
            </div>
          </div>

          <div class="warning-section">
            <h4>灾害预测</h4>
            <div v-if="item.disaster_predictions.length === 0" class="no-warning">暂无异常预警，当前环境稳定。</div>
            <div v-else class="warning-tags">
              <span v-for="warning in item.disaster_predictions" :key="warning" class="warning-tag">{{ warning }}</span>
            </div>
            <div v-if="item.disaster_predictions.length > 0" class="alert-note">
              已自动推送到智能预警模块，相关异常会同步显示在“智能预警”页面中。
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted } from 'vue'
import { useWeatherStore } from './store'

export default defineComponent({
  name: 'Weather',
  setup() {
    const weatherStore = useWeatherStore()

    onMounted(() => {
      weatherStore.fetchWeather()
    })

    const formatTime = (value) => {
      if (!value) return ''
      return new Date(value).toLocaleString()
    }

    return {
      weatherStore,
      formatTime,
    }
  }
})
</script>

<style scoped>
.weather-page {
  padding: 8px 0;
}
.subtitle {
  color: #666;
  margin-bottom: 24px;
}
.weather-list {
  display: grid;
  gap: 24px;
}
.weather-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.08);
}
.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}
.weather-header h3 {
  margin: 0;
  font-size: 20px;
}
.temperature {
  font-size: 40px;
  font-weight: bold;
  color: #f97316;
}
.weather-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}
.stat-item {
  padding: 14px;
  border-radius: 10px;
  background: #f8fafc;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}
.forecast-section {
  margin-bottom: 20px;
}
.forecast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}
.forecast-card {
  background: #f8fafc;
  border-radius: 10px;
  padding: 14px;
  text-align: center;
  font-size: 14px;
}
.day-label {
  font-weight: 700;
  margin-bottom: 8px;
}
.warning-section {
  padding: 16px;
  border-radius: 10px;
  background: #fff7ed;
}

.alert-note {
  margin-top: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #fef9c3;
  color: #92400e;
  font-size: 13px;
}
.warning-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.warning-tag {
  background: #fef3c7;
  border: 1px solid #fcd34d;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 13px;
  color: #92400e;
}
.no-warning {
  color: #4b5563;
}
.state {
  padding: 12px 0;
  color: #64748b;
}
.state.error {
  color: #dc2626;
}
</style>
