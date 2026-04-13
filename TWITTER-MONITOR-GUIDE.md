# 🐦 Twitter/X AI 动态监控指南

## 📋 监控目标

| 账号 | Handle | 说明 |
|------|--------|------|
| **Google Gemini** | @GoogleGemini | Google AI 官方账号 |
| **OpenAI** | @OpenAI | OpenAI 官方账号 |
| **Claude** | @AnthropicAI | Anthropic 官方账号 |
| **Andrej Karpathy** | @karpathy | AI 教父，前 OpenAI 总监 |
| **Lenny** | @lennysan | 产品顾问，AI 评论家 |

---

## ⚠️ 技术限制

**Twitter/X API 变更导致的问题：**

1. ❌ **官方 API 需要付费** - 免费额度极低
2. ❌ **RSSHub 需要认证** - Twitter 路由需要 cookie
3. ❌ **Nitter 实例不稳定** - 大多数已关闭
4. ❌ **浏览器自动化需要登录** - Twitter 强制登录

---

## ✅ 可用方案

### 方案 1：使用 web_search 搜索（推荐）

每天搜索这些账号的最新动态，生成总结。

**优点：**
- ✅ 无需 API
- ✅ 简单可靠
- ✅ 可以搜索多个来源

**缺点：**
- ❌ 不是实时
- ❌ 依赖搜索引擎

**实施：**
```bash
# 手动运行
python3 scripts/twitter-daily-summary.py run

# 或设置定时任务
crontab -e
0 20 * * * cd /home/admin/.openclaw/workspace && python3 scripts/twitter-daily-summary.py run
```

---

### 方案 2：使用 Twitter API（需要 Key）

申请 Twitter API 免费额度：
1. 访问 https://developer.twitter.com
2. 创建应用
3. 获取 API Key

**优点：**
- ✅ 官方 API
- ✅ 数据完整

**缺点：**
- ❌ 免费额度有限（每月 1000 条）
- ❌ 需要申请

---

### 方案 3：使用第三方服务

| 服务 | 价格 | 说明 |
|------|------|------|
| **QVeris** | 免费额度 | 支持 Twitter 监控 |
| **Apify** | $5/月 | Twitter scraper |
| **Bright Data** | 付费 | 数据采集 |

---

### 方案 4：手动查看 + 自动保存

**最简单方案：**

看到有趣的推文时，直接对我说：
> "记一下 https://twitter.com/GoogleGemini/status/xxx"

我会立即保存到 Get 笔记！✅

---

## 📝 已创建的文件

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── twitter-monitor.py           # 主脚本（需要 RSS）
│   ├── twitter-daily-summary.py     # 每日总结脚本
│   └── twitter-summary-config.json  # 配置
└── TWITTER-MONITOR-GUIDE.md         # 本文档
```

---

## 🎯 推荐方案

### 立即可用：方案 4（手动保存）

看到好推文直接发给我，我保存到 Get 笔记。

### 短期方案：方案 1（搜索总结）

使用 web_search 搜索最新动态，每天生成总结。

### 长期方案：方案 2（Twitter API）

申请 API Key，实现完整监控。

---

## 📅 定时任务配置

**每天 20:00 生成总结：**

```bash
crontab -e

# 添加
0 20 * * * cd /home/admin/.openclaw/workspace && python3 scripts/twitter-daily-summary.py run >> /tmp/twitter-summary.log 2>&1
```

**频率选项：**
- 每天 1 次：`0 20 * * *`
- 每天 2 次：`0 8,20 * * *`
- 每 6 小时：`0 */6 * * *`

---

## 🧪 测试命令

```bash
cd /home/admin/.openclaw/workspace

# 测试模式
python3 scripts/twitter-daily-summary.py test

# 运行模式
python3 scripts/twitter-daily-summary.py run
```

---

## 💡 下一步

**请选择：**

1. **手动保存** → 看到推文直接发给我
2. **搜索总结** → 我优化脚本使用 web_search
3. **申请 API** → 你提供 Twitter API Key，我完成配置
4. **使用 QVeris** → 安装 qveris-official 技能

---

## 📞 相关技能

- **getnote** ✅ 已安装 - 保存总结
- **qveris-official** - 支持 Twitter 监控（可选）
- **web_search** - 搜索推文（需要配置）

---

*最后更新：2026-03-27*
