<<<<<<< HEAD
# -
=======
# 智慧农业管理系统

一个基于 FastAPI 和 Vue 3 的现代智慧农业管理解决方案。

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
    │   ├── components/ # 组件
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
- 🔔 异常预警
- 📱 响应式设计

## 安装和运行

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境（可选）：
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 启动服务器：
```bash
python main.py
```

服务器将运行在 `http://localhost:8000`

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

前端将运行在 `http://localhost:5173`

## API 文档

### 农田管理 API

- **GET** `/api/fields` - 获取所有农田
- **GET** `/api/fields/{id}` - 获取特定农田
- **POST** `/api/fields` - 创建农田
- **PUT** `/api/fields/{id}` - 更新农田
- **DELETE** `/api/fields/{id}` - 删除农田

FastAPI 会自动生成交互式 API 文档，访问 `http://localhost:8000/docs`

## 技术栈

### 后端
- FastAPI 2.0+ - 现代 Python Web 框架
- Uvicorn - ASGI 服务器
- Pydantic - 数据验证
- SQLAlchemy - ORM 框架

### 前端
- Vue 3 - 前端框架
- Vite - 打包工具
- Vue Router - 路由管理
- Pinia - 状态管理
- Axios - HTTP 客户端

## 开发指南

### 添加新的 API 端点

1. 在 `backend/app/schemas/` 中定义数据模型
2. 在 `backend/app/routes/` 中实现路由
3. 在 `backend/app/routes/__init__.py` 中注册路由

### 添加新的页面

1. 在 `frontend/src/views/` 中创建 Vue 组件
2. 在 `frontend/src/router/index.js` 中添加路由
3. 如需全局状态，在 `frontend/src/stores/` 中创建 store

## 生产构建

### 前端构建
```bash
cd frontend
npm run build
```

构建输出将在 `frontend/dist` 目录

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请联系我们。
>>>>>>> 471bc30 (Initial commit)
