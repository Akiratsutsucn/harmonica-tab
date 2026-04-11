# Phase 3 设计文档：UI升级 + 播放练习 + 爬取器 + 曲库扩充

**日期**: 2026-04-11
**项目**: 口琴简谱学习工具 (harmonica-tab)
**阶段**: Phase 3

---

## 1. 总览

| 模块 | 方案 |
|------|------|
| UI 风格 | 清爽白净风，纯白底 + 微阴影卡片 |
| 播放 | Web Audio API 合成单音，节拍逐音高亮 |
| 练习模式 | 分段循环 + 调速(0.5x~1.5x) + 难度标记(入门/初级/中级) |
| 爬取器 | 单站点 jianpu.cn |
| 曲库扩充 | seed data 手动添加至 30+ 首经典曲目 |

## 2. UI/视觉升级

### 2.1 设计语言

- 风格：清爽白净，纯白底 + 微阴影卡片
- 主色：品牌蓝 `#4A90D9`，吹音红 `#e74c3c`，吸音蓝 `#2980b9`
- 背景：`#f8f9fa`，卡片：`#fff` + `box-shadow: 0 2px 8px rgba(0,0,0,0.04)`
- 圆角：卡片 14px，按钮 10px，搜索框 12px
- 字体：系统字体栈，简谱数字用等宽或加粗衬线

### 2.2 页面结构

**首页（歌曲列表）：**
- 顶部：白底 header，品牌色标题 + 副标题
- 搜索框：白底带边框，圆角，placeholder 带搜索图标
- 筛选栏：难度筛选 tag（全部/入门/初级/中级）+ 收藏 tab
- 歌曲卡片：白底圆角 + 轻阴影，显示标题、歌手、调性、难度 badge
- 卡片点击态：微上浮 + 阴影加深

**简谱页面：**
- 顶部：返回按钮 + 歌曲信息 + 收藏按钮
- 控制栏：调性选择、调音方式选择
- 简谱区域：更大的音符字号(24px)，吹/吸颜色对比鲜明
- 底部固定：播放控制栏

### 2.3 响应式

- 移动端优先：320~480px
- max-width: 480px 居中布局（保持当前方案）

## 3. 播放 & 练习模式

### 3.1 音频引擎

使用 Web Audio API：
- `OscillatorNode` 正弦波合成，按音符频率播放
- 音符频率映射：A4=440Hz 为基准，十二平均律计算
- 每个音符播放时长由 BPM + duration 计算
- 音符之间有 20ms 间隔避免粘连
- `GainNode` 控制音量，带 attack/release 包络避免爆音

```
频率计算: f = 440 * 2^((midi_number - 69) / 12)
音符时长: quarter_duration = 60 / bpm (秒)
```

### 3.2 播放控制

底部固定播放栏：
- 播放/暂停按钮
- 进度指示（当前小节 / 总小节）
- 速度调节：0.5x / 0.75x / 1.0x / 1.25x / 1.5x
- 播放时当前音符高亮（背景色变化 + 轻微放大），自动滚动跟随

### 3.3 分段练习

- 点击小节线选择起始小节，再点击选择结束小节
- 选中区间高亮显示
- 循环播放选中区间，直到用户停止
- 清除选区按钮

### 3.4 难度系统

- 数据库 `songs.difficulty`：1=入门, 2=初级, 3=中级
- 入门：音域窄(C4-G4)，节奏简单(四分/二分音符为主)，≤8小节
- 初级：音域中等(C4-C5)，有八分音符，8-16小节
- 中级：音域宽(C4-E5+)，有十六分音符/附点，>16小节
- 歌曲列表支持按难度筛选
- 卡片上显示难度 badge（绿/蓝/橙）

## 4. 爬取器 (jianpu.cn)

### 4.1 架构

```
scraper.py (httpx 异步抓取)
  ↓ HTML
parser.py (BeautifulSoup 解析 jianpu.cn 页面结构)
  ↓ 标准化音符 JSON
validator.py (已有，音乐规则校验)
  ↓ 校验通过
database (status=pending, source=crawl)
```

### 4.2 爬取流程

1. 搜索接口：构造 jianpu.cn 搜索 URL，抓取搜索结果列表
2. 详情页：逐个抓取简谱详情页
3. 解析：提取标题、歌手、调性、拍号、音符序列
4. 校验 + 入库

### 4.3 限流与容错

- 请求间隔：2 秒
- 单次任务最多爬取 20 首
- 失败重试 1 次
- 解析失败记录错误日志，跳过继续
- User-Agent 设置为正常浏览器标识

### 4.4 管理后台集成

- 已有的 TaskMonitor 页面可查看爬取任务状态
- 爬取结果进入 pending 队列，管理员审核后上线

## 5. 曲库扩充

### 5.1 目标

从当前 8 首扩充到 30+ 首，覆盖四个分类：

**儿歌经典（补充 5 首）：**
- 找朋友、粉刷匠、小毛驴、数鸭子、拔萝卜

**流行金曲（10 首）：**
- 甜蜜蜜(邓丽君)、朋友(周华健)、童年(罗大佑)、同桌的你(老狼)
- 晴天(周杰伦)、小幸运(田馥甄)、后来(刘若英)、平凡之路(朴树)
- 夜空中最亮的星(逃跑计划)、成都(赵雷)

**民歌/经典（5 首）：**
- 茉莉花、送别、康定情歌、南泥湾、映山红

**外国经典（5 首）：**
- Amazing Grace、Edelweiss、Yesterday(Beatles)、My Heart Will Go On、Auld Lang Syne

### 5.2 数据格式

沿用现有 seed data 格式，每首歌增加 difficulty 字段：
```python
{
    "title": "...", "artist": "...", "key": "C", "ts": "4/4", "bpm": 100,
    "difficulty": 1,  # 新增
    "notes": [(measure, position, pitch, duration, dot, tie), ...]
}
```

### 5.3 难度分配

- 入门(1)：小星星、两只老虎、找朋友、粉刷匠、数鸭子、拔萝卜、小毛驴、Auld Lang Syne
- 初级(2)：欢乐颂、世上只有妈妈好、甜蜜蜜、送别、茉莉花、Amazing Grace、Edelweiss、童年、同桌的你、康定情歌
- 中级(3)：月亮代表我的心、晴天、小幸运、后来、平凡之路、夜空中最亮的星、成都、Yesterday、My Heart Will Go On、朋友、南泥湾、映山红

## 6. 数据库变更

```sql
-- songs 表新增 difficulty 字段
ALTER TABLE songs ADD COLUMN difficulty INTEGER DEFAULT 1;
```

在 `init_db()` 中幂等执行迁移。

## 7. 新增文件

### 前端

| 文件 | 职责 |
|------|------|
| `frontend/src/AudioEngine.js` | Web Audio API 封装，频率计算，播放控制 |
| `frontend/src/PlayBar.jsx` | 底部播放控制栏组件 |
| `frontend/src/PracticeMode.jsx` | 分段练习选择 + 循环逻辑 |
| `frontend/src/DifficultyBadge.jsx` | 难度标签组件 |

### 后端

| 文件 | 职责 |
|------|------|
| `backend/app/pipeline/scraper.py` | 重写：jianpu.cn 真实爬取 |
| `backend/app/pipeline/parser.py` | 重写：jianpu.cn HTML 解析 |

### 修改文件

| 文件 | 变更 |
|------|------|
| `frontend/src/index.css` | 全面重写，白净风格 |
| `frontend/src/App.jsx` | 难度筛选、新 UI 结构 |
| `frontend/src/JianpuRenderer.jsx` | 播放高亮、分段选择、更大字号 |
| `backend/app/database.py` | difficulty 字段迁移 |
| `backend/app/main.py` | seed data 扩充 + difficulty |
| `backend/app/routes_songs.py` | 支持 difficulty 筛选参数 |
| `backend/app/schemas.py` | SongOut 增加 difficulty 字段 |

## 8. 部署

不变：单进程单端口 5123，systemd 服务。无新增环境变量。
