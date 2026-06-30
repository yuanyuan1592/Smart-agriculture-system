<template>
  <div class="home-container">
    <section class="hero-panel">
      <div class="hero-copy">
        <p class="eyebrow">模拟数据展示</p>
        <h2>智慧农业系统 · 统一监控与预警</h2>
        <p>实时展示农田、气象、异常检测和分析数据，支持快速验证和界面体验优化。</p>
        <div class="hero-actions">
          <router-link to="/fields" class="btn btn-primary">查看农田管理</router-link>
          <router-link to="/analytics" class="btn btn-secondary">查看数据分析</router-link>
        </div>
      </div>
      <div class="hero-cards">
        <div class="hero-card" v-for="item in stats" :key="item.label">
          <span class="hero-card-label">{{ item.label }}</span>
          <div class="hero-card-value">{{ item.value }}</div>
          <p>{{ item.description }}</p>
        </div>
      </div>
    </section>

    <section class="feature-grid">
      <router-link to="/fields" class="feature-card">
        <span>🌱</span>
        <h3>农田监测</h3>
        <p>查看土壤湿度、温度及健康状态。</p>
      </router-link>
      <router-link to="/analytics" class="feature-card">
        <span>📊</span>
        <h3>数据分析</h3>
        <p>展示作物分布、趋势和智能建议。</p>
      </router-link>
      <router-link to="/weather" class="feature-card">
        <span>🌤</span>
        <h3>天气预报</h3>
        <p>展示未来天气与灾害预警。</p>
      </router-link>
      <router-link to="/detection" class="feature-card">
        <span>🔔</span>
        <h3>智能预警</h3>
        <p>自动生成高风险和病虫害告警。</p>
      </router-link>
      <router-link to="/devices" class="feature-card">
        <span>⚙️</span>
        <h3>设备管理</h3>
        <p>控制灌溉、温度、农药和补光设备。</p>
      </router-link>
    </section>

    <section class="note-panel">
      <h3>已启用模拟数据</h3>
      <p>后端已使用真实结构的模拟农田和天气数据填充，页面加载即展示预设内容，便于快速验证功能。</p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      stats: [
        { label: '农田数量', value: 6, description: '当前系统中模拟多个农田记录' },
        { label: '异常预警', value: 4, description: '展示传感器与气象预警数据' },
        { label: '健康农田', value: 2, description: '正常状态的农田数量' },
        { label: '气象站点', value: 4, description: '模拟天气数据覆盖多个园区' },
      ],
    }
  },
}
</script>

<style scoped>
.home-container {
  display: grid;
  gap: 28px;
}

.hero-panel {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 24px;
  align-items: center;
  padding: 28px;
  border-radius: 24px;
  background: linear-gradient(135deg, #eef2ff 0%, #ffffff 100%);
  box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
}

.hero-copy {
  max-width: 560px;
}

.eyebrow {
  display: inline-block;
  margin-bottom: 16px;
  padding: 6px 16px;
  border-radius: 999px;
  background: rgba(59, 130, 246, 0.12);
  color: #1d4ed8;
  font-size: 13px;
  font-weight: 700;
}

.hero-panel h2 {
  font-size: 38px;
  margin: 0 0 18px;
  color: #0f172a;
  line-height: 1.05;
}

.hero-panel p {
  color: #475569;
  font-size: 16px;
  line-height: 1.75;
  margin: 0 0 24px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 999px;
  padding: 12px 26px;
  font-weight: 700;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #4f46e5 0%, #2563eb 100%);
  color: white;
}

.btn-secondary {
  background: #e0e7ff;
  color: #3730a3;
}

.hero-cards {
  display: grid;
  gap: 18px;
}

.hero-card {
  padding: 22px;
  border-radius: 20px;
  background: white;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
  min-height: 140px;
}

.hero-card-label {
  display: block;
  color: #667eea;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 12px;
}

.hero-card-value {
  font-size: 36px;
  color: #0f172a;
  font-weight: 800;
  margin-bottom: 10px;
}

.hero-card p {
  margin: 0;
  color: #475569;
  font-size: 14px;
  line-height: 1.6;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.feature-card {
  display: grid;
  gap: 12px;
  padding: 22px;
  border-radius: 22px;
  background: white;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
  transition: transform 0.25s, box-shadow 0.25s;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 25px 55px rgba(15, 23, 42, 0.12);
}

.feature-card span {
  display: inline-flex;
  width: 46px;
  height: 46px;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: #eef2ff;
  font-size: 20px;
}

.feature-card h3 {
  margin: 0;
  font-size: 20px;
  color: #0f172a;
}

.feature-card p {
  margin: 0;
  color: #475569;
  font-size: 14px;
}

.note-panel {
  padding: 24px;
  border-radius: 20px;
  background: white;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.05);
}

.note-panel h3 {
  margin: 0 0 12px;
  font-size: 22px;
  color: #0f172a;
}

.note-panel p {
  margin: 0;
  color: #475569;
  line-height: 1.7;
}

@media (max-width: 960px) {
  .hero-panel {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .hero-panel {
    padding: 20px;
  }
}
</style>
