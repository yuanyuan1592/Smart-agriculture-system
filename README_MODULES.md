# 智慧农业系统模块协作说明

## 项目结构说明

后端模块：
- `backend/app/common/`
  - 公共数据存储和辅助接口
- `backend/app/modules/fields/`
  - 农田管理接口与逻辑
- `backend/app/modules/detection/`
  - 农田检测接口与逻辑
- `backend/app/modules/analytics/`
  - 数据分析接口与逻辑
- `backend/app/core/router.py`
  - 主应用路由注册器，将各模块路由组合到 `/api` 下

前端模块：
- `frontend/src/modules/fields/`
  - `FieldManagement.vue`：农田管理页面
  - `store.js`：字段管理状态与接口调用
- `frontend/src/modules/detection/`
  - `Detection.vue`：检测结果页面
  - `store.js`：检测报告状态与接口调用
- `frontend/src/modules/analytics/`
  - `Analytics.vue`：数据分析页面
  - `store.js`：分析结果状态与接口调用

## 模块协作方式

### 后端协作
- 每个模块单独负责自己的路由与服务：
  - `fields` 模块负责 `/api/fields`
  - `detection` 模块负责 `/api/detection`
  - `analytics` 模块负责 `/api/analytics`
- 所有模块共用 `backend/app/common/` 里的公共接口：
  - `field_store.py`：统一农田数据存储
  - `detection_report.py`：统一检测报告生成逻辑

### 前端协作
- 每个模块独立一个目录，并且只负责自己的视图与状态管理
- `frontend/src/router/index.js` 负责统一路由映射
- 可以按模块拆分开发，减少冲突

## 代码提交规范

- 每个人维护自己模块目录下的文件，避免跨模块修改
- 公共数据变化需先沟通，统一放在 `backend/app/common/`
- 前端状态或页面逻辑改动应写清模块名称

## CI 验证

建议 CI 任务包含：
- 后端语法检查与测试
- 前端构建校验
- 如果可行，加入接口联通检查

例如：
- `python -m py_compile backend/main.py backend/app/core/router.py ...`
- `npm install --prefix frontend && npm run build --prefix frontend`
