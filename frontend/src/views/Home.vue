<template>
  <div class="home-container">
    <h2>欢迎来到智慧农业管理系统</h2>
    <p>这是一个基于现代技术的农业管理解决方案</p>
    
    <div class="feature-grid">
      <div class="feature-card">
        <h3>🌱 农田监测</h3>
        <p>实时监测土壤湿度、温度等参数</p>
      </div>
      
      <div class="feature-card">
        <h3>📊 数据分析</h3>
        <p>深度分析农业数据，优化种植方案</p>
      </div>
      
      <div class="feature-card">
        <h3>🔔 智能预警</h3>
        <p>异常情况提前预警，保护作物生长</p>
      </div>
      
      <div class="feature-card">
        <h3>📱 移动访问</h3>
        <p>随时随地管理您的农田</p>
      </div>
    </div>
    
    <div class="quick-start">
      <h3>快速开始</h3>
      <router-link to="/fields" class="btn">进入农田管理</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home-container {
  text-align: center;
}

h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  color: #666;
  margin-bottom: 40px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 40px 0;
}

.feature-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.feature-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #667eea;
}

.feature-card p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.quick-start {
  margin-top: 40px;
}

.quick-start h3 {
  font-size: 20px;
  margin-bottom: 20px;
}

.btn {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 30px;
  border-radius: 4px;
  text-decoration: none;
  transition: transform 0.3s, box-shadow 0.3s;
}

.btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
