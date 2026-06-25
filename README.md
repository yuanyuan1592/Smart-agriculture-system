# 智慧农业管理系统

一个基于 FastAPI 和 Vue 3 的现代智慧农业管理解决方案，已补齐农业检测模块。

## 项目结构

```
smart-agriculture/
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── models/    # 数据模型
│   │   ├── routes/    # API 路由
│   │   └── schemas/   # 数据验证模式
│   ├── main.py        # 应用入口
│   └── requirements.txt
└── frontend/          # Vue 3 前端
    ├── src/
    │   ├── views/      # 页面
    │   ├── stores/     # 状态管理
    │   ├── router/     # 路由配置
    │   ├── App.vue
    │   └── main.js
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 功能特性

- 🌾 农田信息管理
- 📊 实时数据监测（土壤湿度、温度等）
- 📈 数据分析和统计
- 🔔 农业检测与异常预警
- 📱 响应式设计

## 安装和运行

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务器：
```bash
python main.py
```

服务器将运行在 http://localhost:8000

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端将运行在 http://localhost:5173

## 新增农业检测能力

- 新增检测接口：GET /api/detection/
- 根据土壤湿度和温度生成预警
- 页面入口位于“农业检测”导航
- 支持显示总农田、预警项、严重风险和健康农田数量

## API 文档

### 农田管理 API

- GET /api/fields - 获取所有农田
- GET /api/fields/{id} - 获取特定农田
- POST /api/fields - 创建农田
- PUT /api/fields/{id} - 更新农田
- DELETE /api/fields/{id} - 删除农田

### 农业检测 API

- GET /api/detection/ - 获取农业检测报告

FastAPI 会自动生成交互式 API 文档，访问 http://localhost:8000/docs
