<template>
  <div id="app" class="app-container">
    <header class="app-header">
      <h1>🌾 智慧农业管理系统</h1>
      <nav class="nav-menu">
        <router-link to="/">首页</router-link>
        <router-link to="/fields">农田管理</router-link>
        <router-link to="/analytics">数据分析</router-link>
        <router-link to="/detection">农业检测</router-link>
        <router-link to="/weather">天气预报</router-link>
        <router-link to="/devices">设备管理</router-link>
        <router-link to="/farm">农事管理</router-link>
      </nav>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>
    
    <footer class="app-footer">
      <p>&copy; 2024 智慧农业系统. 版权所有</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
:root {
  color-scheme: dark;
  color: #1f2937;
  background-color: #f3f4f6;
  font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

* {
  box-sizing: border-box;
}

html, body, #app {
  min-height: 100%;
  margin: 0;
  padding: 0;
}

body {
  background: radial-gradient(circle at top, rgba(99, 102, 241, 0.12), transparent 32%),
    linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background: linear-gradient(135deg, #4f46e5 0%, #2563eb 100%);
  color: white;
  padding: 24px 20px;
  box-shadow: 0 8px 30px rgba(31, 41, 55, 0.12);
}

.app-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 14px;
}

.nav-menu {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-size: 14px;
  padding: 10px 18px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  transition: transform 0.2s, background-color 0.2s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background-color: rgba(255, 255, 255, 0.24);
  transform: translateY(-1px);
}

.app-main {
  flex: 1;
  padding: 24px 20px 32px;
  max-width: 1240px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: #0f172a;
  color: #e2e8f0;
  text-align: center;
  padding: 18px 20px;
  margin-top: 24px;
  font-size: 14px;
}
</style>
