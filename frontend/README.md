# Vue 3 前端

基于 Vue 3 和 Vite 的现代前端应用。

## 快速开始

### 环境要求
- Node.js 14.0+
- npm 或 yarn

### 安装步骤

1. 安装依赖：
```bash
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

前端将运行在 `http://localhost:5173`

3. 生产构建：
```bash
npm run build
```

构建输出在 `dist/` 目录

## 项目结构

```
frontend/
├── src/
│   ├── components/    # 可复用组件
│   ├── views/         # 页面组件
│   ├── stores/        # Pinia 状态管理
│   ├── router/        # Vue Router 路由配置
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
├── index.html         # HTML 模板
├── vite.config.js     # Vite 配置
├── package.json       # 项目依赖
└── .gitignore         # Git 忽略文件
```

## 脚本

- `npm run dev` - 启动开发服务器
- `npm run build` - 生产构建
- `npm run preview` - 预览构建结果

## 功能

- ✨ Vue 3 组合式 API
- ⚡ Vite 快速开发体验
- 🛣️ Vue Router 客户端路由
- 📦 Pinia 状态管理
- 🌐 Axios HTTP 客户端
- 📱 响应式设计

## 页面

- **首页** (`/`) - 系统介绍和快速导航
- **农田管理** (`/fields`) - 创建、编辑、删除农田信息
- **数据分析** (`/analytics`) - 农业数据统计和分析

## 配置

复制 `.env.example` 为 `.env` 并配置 API URL：

```bash
cp .env.example .env
```

## 开发指南

### 创建新页面

1. 在 `src/views/` 中创建 `.vue` 文件
2. 在 `src/router/index.js` 中添加路由
3. 在 `App.vue` 中添加导航菜单

### 创建新组件

1. 在 `src/components/` 中创建 `.vue` 文件
2. 在需要的页面中导入并使用

### 状态管理

使用 Pinia 进行全局状态管理，在 `src/stores/` 目录创建 store 文件。

## 依赖说明

- **Vue 3**: 渐进式 JavaScript 框架
- **Vite**: 下一代前端构建工具
- **Vue Router**: 官方路由库
- **Pinia**: Vue 状态管理库
- **Axios**: Promise 型 HTTP 库
