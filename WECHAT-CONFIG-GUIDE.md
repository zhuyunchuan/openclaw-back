# 📋 微信公众号监控配置指南

## 🎯 目标公众号

**名称：** 路飞的船长日志  
**示例文章：** https://mp.weixin.qq.com/s/Qwr-LFeTWarCHL49U0NXuQ

---

## ⚠️ 当前状态

微信文章链接有反爬保护，无法自动获取公众号信息。

**需要你的帮助：** 获取公众号的 `__biz` 参数（gh_ ID）

---

## 🔑 获取 __biz 参数的方法

### 方法 1：从微信 APP 获取（推荐）

1. **打开微信** → 找到"路飞的船长日志"公众号
2. **打开任意一篇文章**
3. **点击右上角"..."** → **"复制链接"**
4. **粘贴链接**到备忘录或聊天窗口
5. **找到 `__biz=` 后面的值**

**完整链接格式：**
```
https://mp.weixin.qq.com/s/xxx?__biz=MzA4MTQ3MjQwMg==&mid=265xxx&idx=1&xxx
                                              ↑ 这就是 __biz
```

**__biz 格式示例：**
- `MzA4MTQ3MjQwMg==`
- `MjM5MTYwNzQyMQ==`
- `MzIxNDAxODQ4MQ==`

---

### 方法 2：从电脑微信获取

1. **打开电脑微信** → 进入公众号文章
2. **右键复制链接**
3. **粘贴到浏览器地址栏**（先不要回车）
4. **查看 URL 中的 `__biz` 参数**

---

### 方法 3：使用浏览器开发者工具

1. **在电脑浏览器打开文章链接**
2. **按 F12** 打开开发者工具
3. **切换到 Network 标签**
4. **刷新页面**
5. **找到第一个请求**（mp.weixin.qq.com）
6. **查看 Request URL 中的 `__biz` 参数**

---

## 📝 获取到 __biz 后

**请告诉我：**
1. 公众号名称：路飞的船长日志
2. __biz 参数：`MzXXXXXXXXXXXX==`（你获取到的值）

**我会立即：**
1. ✅ 更新配置文件
2. ✅ 测试 RSS 抓取
3. ✅ 配置定时任务
4. ✅ 测试保存到 Get 笔记

---

## 🔧 配置文件位置

```
/home/admin/.openclaw/workspace/scripts/wechat-config.json
```

**配置格式：**
```json
{
  "accounts": [
    {
      "name": "路飞的船长日志",
      "biz_id": "MzA4MTQ3MjQwMg=="
    }
  ]
}
```

---

## 📅 定时任务配置

获取到 __biz 并测试成功后，运行：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每 2 小时检查一次）
0 */2 * * * cd /home/admin/.openclaw/workspace && ./scripts/wechat-monitor.sh run >> /tmp/wechat-monitor.log 2>&1
```

**自定义检查频率：**
- 每 1 小时：`0 * * * *`
- 每 2 小时：`0 */2 * * *`
- 每 6 小时：`0 */6 * * *`
- 每天 3 次：`0 8,14,20 * * *`

---

## 🧪 测试命令

获取 __biz 并更新配置后：

```bash
cd /home/admin/.openclaw/workspace

# 测试模式（只抓取，不保存）
./scripts/wechat-monitor.sh test

# 运行模式（检查新文章并保存到 Get 笔记）
./scripts/wechat-monitor.sh run
```

---

## 💡 临时方案

在获取 __biz 之前，你可以：

**看到好文章时直接发给我：**
> "记一下 https://mp.weixin.qq.com/s/Qwr-LFeTWarCHL49U0NXuQ"

我会立即保存到 Get 笔记！

---

## 📞 下一步

**请提供：**
1. 从微信文章链接中获取的 `__biz` 参数
2. 确认公众号名称是"路飞的船长日志"

**或者告诉我：**
- 如果想换其他公众号，提供新公众号的文章链接
- 如果想用其他方案（自建 RSS、QVeris 等）

---

## 📂 相关文件

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── wechat-monitor.py          # 主脚本
│   ├── wechat-monitor.sh          # Shell 包装器
│   ├── wechat-config.json         # 配置（待创建）
│   └── wechat-config-template.json # 配置模板
├── WECHAT-MONITOR-GUIDE.md        # 完整指南
└── WECHAT-TEST-RESULTS.md         # 测试结果
```
