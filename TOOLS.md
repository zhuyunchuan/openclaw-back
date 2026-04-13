# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 📚 Get 笔记能力清单

**已配置 API**：✅ 已认证（`gk_live_9ce62ca...` / `cli_a1b2c3d...`）  
**Base URL**：`https://openapi.biji.com`  
**审计时间**：2026-04-07（已完成首次完整审计）

### 核心能力

| 能力 | API | 说明 |
|-----|-----|------|
| 📚 知识库列表 | `GET /knowledge/list` | 获取我的知识库（每页 20 条） |
| 📚 订阅知识库 | `GET /knowledge/subscribe/list` | 获取订阅的知识库（只读） |
| 📝 知识库笔记 | `GET /knowledge/notes?topic_id=` | 获取库内笔记列表 |
| ➕ 创建知识库 | `POST /knowledge/create` | 每天最多 50 个 |
| ➕ 添加笔记到库 | `POST /knowledge/note/batch-add` | 每批最多 20 条 |
| ➖ 移除笔记 | `POST /knowledge/note/remove` | 从知识库移除 |
| 🏷️ 添加标签 | `POST /note/tags/add` | 为笔记添加标签 |
| 🏷️ 删除标签 | `POST /note/tags/delete` | 删除标签（system 类型不可删） |
| 📝 笔记列表 | `GET /note/list` | 获取笔记列表 |
| 📝 笔记详情 | `GET /note/detail?id=` | 获取笔记详情（含原文） |
| 🔍 全局搜索 | `GET /recall/search` | 语义搜索 |
| 🔍 知识库搜索 | `GET /recall/knowledge` | 库内语义搜索 |
| 📺 博主订阅 | `GET /knowledge/bloggers?topic_id=` | 获取订阅博主列表 |
| 📺 博主内容 | `GET /knowledge/blogger/contents` | 获取博主内容列表 |
| 📺 直播订阅 | `GET /knowledge/lives?topic_id=` | 获取已完成直播列表 |

### 当前知识库状态（2026-04-07）

| 知识库 | 笔记数 | 文件数 | 说明 |
|-------|-------|-------|------|
| 价值投资 | 48 | 24 | 主力库，建议拆分 |
| 投资标的资料库 | 7 | 5 | 安克创新等标的 |
| Ai &具身智能 | 4 | 4 | AI 课程、技术 |
| 硬件产品经理 | 1 | 0 | 待合并或扩展 |
| 个人成长 | 0 | 1 | 空库，待删除 |

### 标签规范（建议）

```
格式：[领域]/[子领域]/[具体主题]
示例：
- 投资/价值投资/公司估值
- 投资/案例/安克创新
- AI/生成式 AI/Prompt
- 学习来源/得到
- 内容类型/链接笔记
```

### 注意事项

1. **笔记 ID 是大整数** - API 返回时需用字符串处理（Python 原生支持）
2. **限流配额** - 读：1000/日，写：200/日，写笔记：50/日
3. **非会员限制** - 部分功能需会员（错误码 10201）
4. **订阅库只读** - 不能向订阅的知识库添加笔记

### 快捷命令参考

```bash
# 知识库列表
curl 'https://openapi.biji.com/open/api/v1/resource/knowledge/list?page=1' \
  -H 'Authorization: $GETNOTE_API_KEY' \
  -H 'X-Client-ID: $GETNOTE_CLIENT_ID'

# 知识库笔记
curl "https://openapi.biji.com/open/api/v1/resource/knowledge/notes?topic_id={ID}&page=1" \
  -H 'Authorization: $GETNOTE_API_KEY' \
  -H 'X-Client-ID: $GETNOTE_CLIENT_ID'
```

---
*完整审计报告：`GETNOTE-AUDIT-REPORT.md`*
