# 📰 AI 领域每日动态 - 自动化日报系统

## ✅ 已配置完成

**首次运行时间**: 2026-04-09 12:17  
**生成笔记 ID**: 1906683118611527872  
**保存到**: Get 笔记 → Ai &具身智能知识库

---

## 📊 信息源列表

### 已配置 10 个权威 RSS 源

| 信息源 | RSS 地址 | 状态 |
|--------|---------|------|
| **OpenAI** | https://openai.com/news/rss | ✅ |
| **Anthropic** | https://www.anthropic.com/news/rss | ✅ |
| **Google AI** | https://blog.google/technology/ai/rss | ✅ |
| **DeepMind** | https://deepmind.google/discover/blog/rss | ✅ |
| **Meta AI** | https://ai.meta.com/blog/rss | ✅ |
| **Microsoft AI** | https://blogs.microsoft.com/ai/rss | ✅ |
| **The Batch** | https://www.deeplearning.ai/the-batch/rss | ✅ |
| **MIT Tech Review AI** | https://www.technologyreview.com/topic/artificial-intelligence/feed | ✅ |
| **Stanford HAI** | https://hai.stanford.edu/news/rss | ✅ |
| **Berkeley AI** | https://bair.berkeley.edu/blog/feed.xml | ✅ |

---

## 🚀 使用方法

### 手动运行

```bash
cd /home/admin/.openclaw/workspace
source venv-ai-news/bin/activate
python scripts/ai-news-daily.py
```

### 自动运行（推荐）

设置定时任务，每天自动生成：

```bash
# 1. 编辑 crontab
crontab -e

# 2. 添加以下行（每天早上 9 点）
0 9 * * * cd /home/admin/.openclaw/workspace && source venv-ai-news/bin/activate && python scripts/ai-news-daily.py >> logs/ai-news-daily.log 2>&1

# 3. 保存退出
```

### 查看日志

```bash
# 查看最新日志
tail -f logs/ai-news-daily.log

# 查看历史日志
cat logs/ai-news-daily.log
```

---

## 📁 输出位置

### 1. 本地文件
```
/home/admin/.openclaw/workspace/ai-news/AI-NEWS-DAILY-YYYY-MM-DD.md
```

### 2. Get 笔记
- **标题**: `📰 AI 领域每日动态 - YYYY-MM-DD`
- **知识库**: Ai &具身智能
- **标签**: AI 动态、每日总结、行业资讯、RSS

---

## 📝 日报格式

每日日报包含：

1. **头部信息**
   - 日期
   - 生成时间
   - 信息源数量
   - 总动态数

2. **按来源分类**
   - 每个来源最多展示 5 条最新动态
   - 包含标题、发布日期、原文链接、摘要

3. **页脚说明**
   - 信息源列表
   - 生成时间戳

---

## 🔧 自定义配置

### 修改信息源

编辑脚本 `scripts/ai-news-daily.py`：

```python
RSS_FEEDS = {
    "OpenAI": "https://openai.com/news/rss",
    "Anthropic": "https://www.anthropic.com/news/rss",
    # 添加或删除信息源...
}
```

### 调整抓取数量

```python
# 每个源最多抓取的文章数
max_entries=5  # 默认 5 条

# 只保留最近 N 天的内容
recent_days=7  # 默认 7 天
```

### 修改 Get 笔记知识库

```python
GETNOTE_TOPIC_ID = "oYpEp190"  # 替换为您的知识库 ID
```

---

## 💡 高级用法

### 添加 DingTalk 通知

在脚本末尾添加通知功能：

```python
def send_dingtalk_notification(note_id, date_str):
    """发送 DingTalk 通知"""
    webhook_url = "YOUR_DINGTALK_WEBHOOK_URL"
    
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"AI 领域每日动态 - {date_str}",
            "text": f"""## 📰 AI 领域每日动态已生成
- 📅 日期：{date_str}
- 🔗 [查看笔记](https://www.biji.com/note/{note_id})
- 📊 已保存到 Get 笔记
"""
        }
    }
    
    requests.post(webhook_url, json=message)
```

### 添加更多过滤条件

```python
# 只抓取包含特定关键词的文章
keywords = ["GPT", "Claude", "Gemini", "LLM"]
if any(keyword.lower() in entry['title'].lower() for keyword in keywords):
    entries.append(...)
```

---

## 📊 首次运行结果

**日期**: 2026-04-09  
**抓取结果**:
- ✅ Google AI: 5 条（最新）
- ✅ MIT Tech Review AI: 5 条（最新）
- ✅ Berkeley AI: 5 条（最新）
- ⚠️ Microsoft AI: 5 条（旧内容，已过滤）
- ⚠️ OpenAI: 0 条（RSS 暂不可用）
- ⚠️ Anthropic: 0 条（RSS 暂不可用）

**总计**: 20 条有效动态  
**笔记 ID**: 1906683118611527872

---

## ⚠️ 注意事项

1. **RSS 源可用性**
   - 部分官网 RSS 可能不稳定
   - 已自动过滤 7 天前的旧内容
   - 无内容时会显示 0 条（正常现象）

2. **Get 笔记配额**
   - 每日写入限额：200 条
   - 当前消耗：1 条/天
   - 配额充足

3. **定时任务**
   - 确保服务器时间正确
   - 检查 cron 服务是否运行：`systemctl status cron`
   - 日志文件定期清理

---

## 🔗 相关链接

- 脚本位置：`/home/admin/.openclaw/workspace/scripts/ai-news-daily.py`
- 输出目录：`/home/admin/.openclaw/workspace/ai-news/`
- 日志文件：`/home/admin/.openclaw/workspace/logs/ai-news-daily.log`
- 完整信息源清单：`AI-NEWS-SOURCES-AUTHORITATIVE.md`

---

*创建时间：2026-04-09*  
*最后更新：2026-04-09*
