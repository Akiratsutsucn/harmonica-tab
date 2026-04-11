# Phase 2 数据管线 + 管理后台 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为口琴简谱学习工具添加完整数据管线（AI 生成、网络爬取、批量导入）和管理后台，将曲库从 8 首扩展到数百首。

**Architecture:** 模块化单体，保持单 FastAPI 进程。用 asyncio + SQLite tasks 表做轻量任务队列。管理后台作为前端 `/admin` 路由，共享 API。

**Tech Stack:** FastAPI, aiosqlite, httpx, BeautifulSoup4, React 19, Ant Design Mobile, Vite 8

---

## File Structure

### Backend — 新增/修改

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `backend/app/database.py` | 新增 tasks 表，songs 表加 status/source 字段 |
| Modify | `backend/app/schemas.py` | 新增 Admin/Task 相关 Pydantic models |
| Modify | `backend/app/main.py` | 注册 admin router，启动任务消费循环 |
| Modify | `backend/app/routes_songs.py` | 用户端只返回 verified 歌曲 |
| Create | `backend/app/auth.py` | 简单密码认证中间件 |
| Create | `backend/app/routes_admin.py` | 管理后台 API 路由 |
| Create | `backend/app/task_queue.py` | SQLite 轻量任务队列 |
| Create | `backend/app/pipeline/__init__.py` | Pipeline 包 |
| Create | `backend/app/pipeline/validator.py` | 音乐规则校验器 |
| Create | `backend/app/pipeline/llm_provider.py` | LLM 可插拔接口 |
| Create | `backend/app/pipeline/ai_generator.py` | AI 简谱生成 |
| Create | `backend/app/pipeline/scraper.py` | 网络爬取引擎 |
| Create | `backend/app/pipeline/parser.py` | 简谱页面解析器 |
| Create | `backend/app/pipeline/importer.py` | 批量导入（JSON/CSV） |
| Modify | `backend/requirements.txt` | 新增 httpx, beautifulsoup4, lxml |

### Backend — 测试

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `backend/tests/__init__.py` | Tests 包 |
| Create | `backend/tests/conftest.py` | pytest fixtures（内存 DB） |
| Create | `backend/tests/test_validator.py` | 校验器测试 |
| Create | `backend/tests/test_task_queue.py` | 任务队列测试 |
| Create | `backend/tests/test_importer.py` | 导入器测试 |
| Create | `backend/tests/test_admin_api.py` | Admin API 集成测试 |

### Frontend — 新增/修改

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `frontend/src/main.jsx` | 添加路由（用户端 / 管理端） |
| Create | `frontend/src/adminApi.js` | 管理后台 API 客户端 |
| Create | `frontend/src/admin/AdminApp.jsx` | 后台主框架（侧边栏+内容区） |
| Create | `frontend/src/admin/AdminLogin.jsx` | 密码登录页 |
| Create | `frontend/src/admin/Dashboard.jsx` | 数据统计面板 |
| Create | `frontend/src/admin/SongManager.jsx` | 歌曲管理表格 |
| Create | `frontend/src/admin/NoteEditor.jsx` | 简谱可视化编辑器 |
| Create | `frontend/src/admin/TaskMonitor.jsx` | 任务监控 |
| Create | `frontend/src/admin/BatchImport.jsx` | 批量导入 |
| Modify | `frontend/package.json` | 添加 react-router-dom |

---
