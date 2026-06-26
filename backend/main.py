from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import config
from app.core.router import register_routes

app = FastAPI(
    title="智慧农业系统 API",
    description="Smart Agriculture Management System",
    version="1.0.0",
    debug=config.debug,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册模块化路由
register_routes(app)


@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "Welcome to Smart Agriculture System",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
