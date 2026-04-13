# 微信公众号监控自动保存指南

## 📋 目标

定时抓取指定微信公众号（如：路飞的船长日志），发现新文章自动保存到 Get 笔记。

---

## ⚠️ 现状说明

微信公众号 RSS 抓取有以下几种方案：

### 方案 1：公共 RSS 服务（推荐先测试）

| 服务 | 地址 | 状态 |
|------|------|------|
| **feeddd** | `https://feeds.feeddd.org/api/mp/{公众号名}` | ⚠️ 有时不稳定 |
| **RSSHub** | `https://rsshub.app/wechat/mp/{公众号名}` | ❌ 需要 gh_ ID |
| **wewe-rss** | `https://wewe-rss.vercel.app` | ✅ 推荐，支持微信读书 |

### 方案 2：自建 wewe-rss（最可靠）

- GitHub: https://github.com/cooderl/wewe-rss
- 支持私有化部署
- 基于微信读书，稳定性高

### 方案 3：手动提供 gh_ ID

1. 打开公众号任意文章
2. 查看 URL 中的 `__biz` 参数
3. 格式如：`MzA4MTQ3MjQwMg==`

---

## 🔧 已创建的文件

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── wechat-monitor.py      # 主脚本
│   └── wechat-monitor.sh      # Shell 包装器
├── scripts/wechat-config.json  # 配置文件（运行后自动生成）
└── WECHAT-MONITOR-GUIDE.md    # 本文档
```

---

## 📝 使用步骤

### 步骤 1：获取公众号 gh_ ID

**方法 A：从文章 URL 获取**
1. 在微信中打开"路飞的船长日志"任意文章
2. 复制链接，找到 `__biz=` 后面的值
3. 如：`__biz=MzA4MTQ3MjQwMg==`

**方法 B：使用 wewe-rss 查询**
1. 访问 https://github.com/cooderl/wewe-rss
2. 使用其提供的查询工具

### 步骤 2：更新配置

编辑 `scripts/wechat-config.json`：

```json
{
  "accounts": [
    {
      "name": "路飞的船长日志",
      "biz_id": "MzA4MTQ3MjQwMg=="  // 替换为实际的 gh_ ID
    }
  ],
  "last_checked": {}
}
```

### 步骤 3：测试抓取

```bash
cd /home/admin/.openclaw/workspace
./scripts/wechat-monitor.sh test
```

### 步骤 4：运行保存

```bash
./scripts/wechat-monitor.sh run
```

### 步骤 5：设置定时任务

```bash
crontab -e
```

添加以下内容（每 2 小时检查一次）：

```cron
0 */2 * * * cd /home/admin/.openclaw/workspace && ./scripts/wechat-monitor.sh run >> /tmp/wechat-monitor.log 2>&1
```

---

## 🔄 替代方案

如果上述方案都不可用，考虑：

### 方案 A：使用 QVeris 技能

QVeris 支持监控微信公众号（需要 API Key）：

```bash
clawhub install qveris-official
```

### 方案 B：使用 IFTTT/Zapier

1. 注册 https://ifttt.com
2. 创建 Applet：微信 → Get 笔记
3. 需要 Get 笔记支持 Webhook

### 方案 C：手动保存（临时）

看到好文章时，直接对我说：
- "记一下 https://mp.weixin.qq.com/s/xxx"
- 我会自动保存到 Get 笔记

---

## 📞 下一步

请提供：
1. "路飞的船长日志"公众号的 gh_ ID（从文章 URL 获取）
2. 或者选择自建 wewe-rss 服务
3. 或者使用 QVeris 商业服务

获取到 gh_ ID 后，我可以立即完成配置并测试。
