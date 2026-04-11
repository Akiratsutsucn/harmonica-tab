# Phase 2 设计文档：数据管线 + 管理后台

**日期**: 2026-04-11
**项目**: 口琴简谱学习工具 (harmonica-tab)
**阶段**: Phase 2

---

## 1. 架构概览

模块化单体 + 内置异步任务。保持单 FastAPI 进程，用 asyncio + SQLite 任务表做轻量任务队列，不引入 Redis/Celery。管理后台作为前端 `/admin` 路由，共享同一套 API。

### 目录结构

```
backend/app/
├── main.py                 # FastAPI app + lifespan（扩展任务消费循环）
├── database.py             # DB schema（扩展 tasks 表）
├── schemas.py              # Pydantic models（扩展）
├── mapping.py              # 孔位映射（不变）
├── routes_songs.py         # 用户端歌曲 API（不变，过滤 verified）
├── routes_mapping.py       # 映射 API（不变）
├── routes_admin.py         # 管理后台 API（新）
├── pipeline/
│   ├── __init__.py
│   ├── llm_provider.py     # LLM 可插拔接口
│   ├── ai_generator.py     # AI 简谱生成 + 规则校验
│   ├── scraper.py          # 网络爬取引擎
│   ├── parser.py           # 简谱页面解析器（多站点）
│   ├── validator.py        # 音乐规则校验器
│   └── importer.py         # 批量导入（JSON/CSV）
└── task_queue.py           # SQLite 轻量任务队列

frontend/src/
├── App.jsx                 # 用户端（不变）
├── admin/
│   ├── AdminApp.jsx        # 后台主框架
│   ├── Dashboard.jsx       # 数据统计
│   ├── SongManager.jsx     # 歌曲管理（CRUD + 审核）
│   ├── NoteEditor.jsx      # 简谱可视化编辑器
│   ├── TaskMonitor.jsx     # 任务监控
│   └── BatchImport.jsx     # 批量导入
└── ...
```

## 2. 数据管线

### 2.1 LLM 可插拔接口

```python
class LLMProvider(ABC):
    async def generate(self, prompt: str) -> str: ...

class ClaudeProvider(LLMProvider): ...
class OpenAIProvider(LLMProvider): ...
class DeepSeekProvider(LLMProvider): ...
```

通过环境变量 `LLM_PROVIDER` + `LLM_API_KEY` 切换。后台管理界面也可动态选择。

### 2.2 AI 生成流程

```
输入: 歌名 + 歌手 + (可选)原调/拍号
  ↓
LLM Prompt → 生成简谱 JSON
  ↓
规则校验 (validator.py):
  ├── 音域检查: C4-C7（口琴可演奏范围）
  ├── 节拍校验: 每小节时值总和 = 拍号要求
  ├── 调性一致性: 音符符合声明调性
  └── 格式校验: JSON schema 验证
  ↓
通过 → 入库 (status=pending, source=ai)
失败 → 记录错误，可选重试
```

### 2.3 爬取流程

目标站点：tan8.com、jianpu.cn、jitashe.org

```
scraper.py: httpx 异步抓取页面
  ↓
parser.py: 站点专用解析器
  ├── Tan8Parser
  ├── JianpuCnParser
  └── JitasheParser
  ↓
标准化音符序列 JSON → validator.py 校验 → 入库 (status=pending, source=crawl)
```

### 2.4 批量导入

支持格式：
- JSON：符合内部 schema 的音符序列
- CSV：歌名/歌手/调性/简谱文本（简化记法 `1 2 3 4 | 5 - - -`）

导入后经 validator 校验，进入审核队列。

### 2.5 任务队列

`tasks` 表：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| type | str | ai_generate / crawl / batch_import |
| status | str | pending / running / done / failed |
| params | json | 任务参数 |
| result | json | 执行结果/错误信息 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

用 `asyncio.create_task()` 在后台消费，lifespan 启动时拉起消费循环。

## 3. 管理后台

### 3.1 API 端点

| Method | Path | 说明 |
|--------|------|------|
| GET | `/api/admin/dashboard` | 统计数据 |
| GET | `/api/admin/songs` | 歌曲列表（分页、筛选 status/source） |
| POST | `/api/admin/songs` | 手动新增歌曲 |
| PUT | `/api/admin/songs/{id}` | 编辑歌曲元信息 |
| DELETE | `/api/admin/songs/{id}` | 删除歌曲 |
| GET | `/api/admin/songs/{id}/notes` | 获取音符序列 |
| PUT | `/api/admin/songs/{id}/notes` | 编辑音符序列 |
| POST | `/api/admin/songs/{id}/verify` | 审核通过 |
| POST | `/api/admin/songs/{id}/reject` | 审核驳回 |
| POST | `/api/admin/tasks/ai-generate` | 提交 AI 生成任务 |
| POST | `/api/admin/tasks/crawl` | 提交爬取任务 |
| POST | `/api/admin/tasks/import` | 提交批量导入任务 |
| GET | `/api/admin/tasks` | 任务列表 |
| GET | `/api/admin/tasks/{id}` | 任务详情 |

### 3.2 前端页面

- **Dashboard**: 数据概览卡片（总曲目、待审核、来源分布饼图、最近任务）
- **SongManager**: 歌曲管理表格（筛选、审核、编辑、删除）
- **NoteEditor**: 简谱可视化编辑器（上方预览复用 JianpuRenderer，下方音符表格编辑，实时预览，校验提示）
- **TaskMonitor**: 任务监控（列表、状态、失败原因、AI 批量提交、爬取配置）
- **BatchImport**: 上传 JSON/CSV → 预览 → 确认导入

### 3.3 权限

简单密码保护，不做用户体系：
- 环境变量 `ADMIN_PASSWORD` 设置密码
- 前端 `/admin` 弹出密码输入框
- 后端 `/api/admin/*` 检查 `Authorization: Bearer {sha256(password)}`

## 4. 数据库迁移

`songs` 表新增：
- `status TEXT DEFAULT 'verified'` — 现有数据自动标记已审核
- `source TEXT DEFAULT 'manual'` — 现有数据标记手动录入

新增 `tasks` 表。

迁移在 `database.py` 的 `init_db()` 中用 `ALTER TABLE` 幂等执行。

用户端 `GET /api/songs` 只返回 `status=verified` 的歌曲。

## 5. 依赖新增

```
httpx           # 异步爬取
beautifulsoup4  # HTML 解析
lxml            # BS4 解析器
```

LLM SDK 按 provider 按需安装。

## 6. 环境变量

```env
ADMIN_PASSWORD=xxx        # 管理后台密码
LLM_PROVIDER=claude       # claude / openai / deepseek
LLM_API_KEY=sk-xxx        # 对应 provider 的 key
LLM_MODEL=                # 可选，覆盖默认模型
```

## 7. 部署

不变：单进程单端口 5123，systemd 服务。新增环境变量写入 service 文件。

## 8. 测试策略

- 单元测试：validator（节拍、音域）、parser（各站点解析，本地 HTML fixture）、LLM 输出格式
- 集成测试：admin API 端点（CRUD、审核流程、任务提交）
- 爬取测试：本地 fixture，不依赖外部网站
