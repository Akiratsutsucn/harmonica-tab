# 口琴练习 APP 设计文档

> 日期：2026-04-19
> 状态：已确认

## 1. 项目概述

个人口琴练习工具。用户上传歌曲简谱图片和音频（MP3 文件或音频链接），在同一页面边看谱边听歌练习。支持电脑和手机访问。

**不包含：** 用户系统、管理后台、AI 生成、爬虫、孔位映射引擎、曲库搜索等旧版功能。

## 2. 核心功能

### 2.1 我的曲库（首页）

- 歌曲卡片列表，显示标题、歌手、简谱缩略图
- 搜索框按歌名/歌手筛选
- 点击卡片进入练习页
- 浮动"添加歌曲"按钮

### 2.2 添加歌曲

- 填写歌名（必填）、歌手（可选）
- 上传简谱图片：支持多张，可拖拽排序，支持 JPG/PNG/WebP
- 音频来源：上传 MP3 文件 或 填写音频链接（二选一或都填）
- 保存后跳转到练习页

### 2.3 练习页

- 上方：简谱图片展示区
  - 多张图片可左右滑动切换（指示器显示当前页）
  - 支持双指缩放（移动端）和滚轮缩放（桌面端）
- 下方固定：音频播放器
  - 播放/暂停按钮
  - 进度条（可拖拽跳转）
  - 当前时间 / 总时长
  - 倍速切换：0.5x / 0.75x / 1.0x / 1.25x / 1.5x / 2.0x
- 顶部导航栏：歌曲标题 + 返回按钮 + 编辑/删除

### 2.4 编辑歌曲

- 复用添加歌曲的表单
- 可修改标题、歌手
- 可增删简谱图片、调整排序
- 可更换音频

## 3. 架构设计

```
口琴练习 APP（Next.js 全栈）
├── 前端页面（App Router）
│   ├── /              首页（我的曲库）
│   ├── /add           添加歌曲
│   ├── /song/[id]     练习页
│   └── /song/[id]/edit 编辑歌曲
├── API Routes
│   ├── GET    /api/songs          歌曲列表（支持搜索）
│   ├── POST   /api/songs          创建歌曲
│   ├── GET    /api/songs/[id]     歌曲详情
│   ├── PUT    /api/songs/[id]     更新歌曲
│   ├── DELETE /api/songs/[id]     删除歌曲（含文件清理）
│   ├── POST   /api/upload/image   上传简谱图片
│   ├── POST   /api/upload/audio   上传音频文件
│   └── DELETE /api/upload/[...path] 删除已上传文件
├── 静态文件服务
│   └── /uploads/...   通过 Next.js public 或自定义路由提供
└── 数据存储
    ├── SQLite（better-sqlite3）— 歌曲元数据
    └── 磁盘目录 — 上传的图片和音频
```

## 4. 数据模型

### songs 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| title | TEXT NOT NULL | 歌名 |
| artist | TEXT | 歌手（可选） |
| audioType | TEXT | 'file' \| 'url' \| null |
| audioPath | TEXT | 上传文件路径或外部 URL |
| createdAt | TEXT | ISO 8601 创建时间 |
| updatedAt | TEXT | ISO 8601 更新时间 |

### images 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| songId | INTEGER FK | 关联 songs.id，CASCADE 删除 |
| path | TEXT NOT NULL | 图片文件相对路径 |
| sortOrder | INTEGER | 排序序号（从 0 开始） |

## 5. 文件存储

```
uploads/
├── images/
│   └── {songId}/
│       ├── {uuid}.jpg
│       └── {uuid}.png
└── audio/
    └── {songId}/
        └── {uuid}.mp3
```

- 上传目录位于项目根目录下的 `uploads/`
- 服务器部署时位于 `/var/www/harmonica-app/uploads/`
- 文件名使用 UUID 避免冲突
- 删除歌曲时级联删除对应目录

## 6. UI 设计

### 视觉风格：暖纸质感

- 底色：米白 `#faf6f0`
- 主色：暖棕 `#8b6914` → `#a67c2e`
- 卡片背景：白色，圆角 12px，轻阴影
- 字体：系统默认字体栈
- 整体感觉：像翻开一本乐谱，温暖舒适

### 布局：上下分栏

- 练习页：简谱图片占主体区域，音频播放器固定在底部
- 响应式：电脑和手机共用同一套布局，不做左右分栏切换
- 播放器高度固定约 64px，不遮挡谱面内容（谱面区域留出底部 padding）

### 交互细节

- 图片查看：swipe 切换 + pinch-to-zoom
- 播放器：大播放按钮 + 进度条 + 时间 + 倍速按钮
- 添加歌曲：图片上传支持拖拽，上传后可拖拽排序
- 删除确认：二次确认弹窗

## 7. 技术栈

| 层 | 技术 | 理由 |
|----|------|------|
| 框架 | Next.js 14 (App Router) | 全栈一体，部署简单 |
| 语言 | TypeScript | 类型安全 |
| 样式 | Tailwind CSS | 快速开发，暖色主题定制方便 |
| 数据库 | better-sqlite3 | 同步 API，适合 Next.js Route Handlers |
| 文件上传 | formidable | 成熟的 multipart 解析库 |
| 图片查看 | swiper 或 react-photo-view | 滑动 + 缩放 |
| 音频播放 | HTML5 Audio API | 原生够用，不需要额外库 |
| 部署 | PM2 + Node.js | 进程管理，自动重启 |
| 端口 | 5123 | 沿用旧项目端口 |

## 8. 部署方案

- 服务器：115.190.112.212（Ubuntu 24.04）
- 路径：`/var/www/harmonica-app/`
- 进程管理：PM2
- 端口：5123
- GitHub 仓库：沿用 Akiratsutsucn/harmonica-tab 或新建

## 9. 不做的事情

- 不做用户注册/登录（个人工具）
- 不做孔位映射引擎（旧版功能，不再需要）
- 不做 AI 简谱生成
- 不做网络爬虫
- 不做简谱数据结构化（直接用图片）
- 不做音频与谱面同步
- 不做离线缓存（Service Worker）
- 不做微信小程序
