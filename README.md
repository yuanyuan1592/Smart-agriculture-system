# 智慧农业管理系统

一个基于 FastAPI 与 Vue 3 的智慧农业管理平台，当前已具备模块化结构，便于后续持续扩展新功能。

## 项目结构

```text
smart-agriculture/
├── backend/
│   ├── app/
│   │   ├── core/          # 配置与注册中心
│   │   ├── modules/       # 功能模块目录
│   │   ├── routes/        # API 路由
│   │   ├── schemas/       # 请求/响应模型
│   │   └── services/      # 业务服务层
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── modules/       # 前端模块目录
│   │   ├── services/      # API 服务层
│   │   ├── stores/        # 兼容入口
│   │   ├── views/         # 页面组件
│   │   └── router/        # 路由
└── README.md
```

## 当前已实现功能

- 农田管理
- 数据分析
- 农业检测与预警

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

## 扩展建议

新增功能时建议按以下顺序进行：
1. 在 backend/app/modules 下新增模块目录
2. 在 backend/app/routes 下增加路由
3. 在 frontend/src/modules 下增加模块状态与服务
4. 在 frontend/src/views 下新增页面
