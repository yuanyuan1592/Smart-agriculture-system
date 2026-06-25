# FastAPI 后端

FastAPI 后端服务，提供智慧农业系统的 API 接口。

## 快速开始

### 环境要求
- Python 3.8+
- pip 或 conda

### 安装步骤

1. 创建虚拟环境：
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行服务器：
```bash
python main.py
```

或者：
```bash
uvicorn app.main:app --reload
```

服务器默认运行在 `http://localhost:8000`

## API 端点

### 根路由
- **GET** `/` - 获取 API 信息

### 健康检查
- **GET** `/health` - 检查服务器状态

### 农田管理
- **GET** `/api/fields` - 获取所有农田
- **GET** `/api/fields/{field_id}` - 获取特定农田
- **POST** `/api/fields` - 创建新农田
- **PUT** `/api/fields/{field_id}` - 更新农田
- **DELETE** `/api/fields/{field_id}` - 删除农田

## 交互式 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── models/       # 数据库模型
│   │   ├── __init__.py
│   │   └── field.py
│   ├── schemas/      # Pydantic 数据验证模式
│   │   ├── __init__.py
│   │   └── field.py
│   ├── routes/       # API 路由
│   │   ├── __init__.py
│   │   └── field.py
│   └── __init__.py
├── main.py          # 应用入口
└── requirements.txt
```

## 开发

### 添加新的 API 端点

1. 在 `app/models/` 中定义数据库模型（如需）
2. 在 `app/schemas/` 中定义请求/响应数据模型
3. 在 `app/routes/` 中实现路由处理函数
4. 在 `app/routes/__init__.py` 中导入并注册路由

## 配置

复制 `.env.example` 为 `.env` 并修改配置值：

```bash
cp .env.example .env
```

## 依赖说明

- **FastAPI**: 现代、快速的 Web 框架
- **Uvicorn**: 轻量级 ASGI 服务器
- **Pydantic**: 数据验证和设置管理
- **SQLAlchemy**: SQL 工具包和 ORM
- **python-dotenv**: 环境变量管理
- **CORS**: 跨域资源共享中间件
