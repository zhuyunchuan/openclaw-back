# 📱 小红书监控工具 - 配置指南

**配置时间**: 2026-04-09 21:35  
**状态**: ✅ 安装完成，等待配置

---

## 📋 已完成步骤

### ✅ 1. 安装 XHS-Downloader

```bash
cd /home/admin/.openclaw/workspace
git clone https://github.com/JoeanAmier/XHS-Downloader.git xhs-monitor
cd xhs-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ✅ 2. 测试 API 服务器

```bash
cd xhs-monitor
source venv/bin/activate
python main.py api
```

**测试结果**: ✅ API 服务器启动成功，监听端口 5556

### ✅ 3. 创建监控脚本

**脚本位置**: `/home/admin/.openclaw/workspace/scripts/xhs-monitor.py`

**功能**:
- ✅ 定时检查指定账号更新
- ✅ 生成 Markdown 监控报告
- ✅ 保存到本地文件
- ✅ 上传到 Get 笔记

---

## ⚠️ 待完成配置

### 1️⃣ 获取小红书 Cookie（必需）

**步骤**:

1. 打开浏览器访问 https://www.xiaohongshu.com
2. 按 F12 打开开发者工具
3. 选择 **Network** 标签
4. 刷新页面
5. 选择任意请求
6. 复制 **Request Headers** 中的 Cookie
7. 保存到配置文件

**或者运行命令**:
```bash
cd /home/admin/.openclaw/workspace/xhs-monitor
source venv/bin/activate
python main.py --browser_cookie Chrome --update_settings
```

### 2️⃣ 配置监控账号

编辑 `/home/admin/.openclaw/workspace/scripts/xhs-monitor.py`:

```python
MONITOR_USERS = [
    # 替换为实际要监控的账号
    {"user_id": "用户 ID 1", "name": "账号名称 1"},
    {"user_id": "用户 ID 2", "name": "账号名称 2"},
]
```

**如何获取用户 ID**:
1. 访问小红书用户主页
2. URL 格式：`https://www.xiaohongshu.com/user/profile/用户 ID`
3. 复制用户 ID 部分

### 3️⃣ 启动 API 服务器

**方法 1：手动启动**
```bash
cd /home/admin/.openclaw/workspace/xhs-monitor
source venv/bin/activate
python main.py api
```

**方法 2：后台运行（推荐）**
```bash
cd /home/admin/.openclaw/workspace/xhs-monitor
source venv/bin/activate
nohup python main.py api > logs/xhs-api.log 2>&1 &
```

**方法 3： systemd 服务（最稳定）**
```bash
sudo nano /etc/systemd/system/xhs-api.service
```

内容：
```ini
[Unit]
Description=XHS-Downloader API Service
After=network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/.openclaw/workspace/xhs-monitor
Environment="PATH=/home/admin/.openclaw/workspace/xhs-monitor/venv/bin"
ExecStart=/home/admin/.openclaw/workspace/xhs-monitor/venv/bin/python main.py api
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable xhs-api
sudo systemctl start xhs-api
sudo systemctl status xhs-api
```

---

## 🧪 测试步骤

### 1. 测试 API 连接

```bash
curl http://127.0.0.1:5556/docs
```

如果返回 API 文档页面，说明 API 服务正常。

### 2. 测试监控脚本

编辑脚本，添加测试账号后运行：

```bash
cd /home/admin/.openclaw/workspace
source venv-ai-news/bin/activate  # 或直接使用系统 Python
python scripts/xhs-monitor.py
```

### 3. 查看输出

**本地文件**: `/home/admin/.openclaw/workspace/xhs-monitor/outputs/`  
**Get 笔记**: 搜索"小红书监控"

---

## ⏰ 设置定时任务

```bash
crontab -e
```

添加以下行：

```bash
# 每天早上 9 点检查小红书更新
0 9 * * * cd /home/admin/.openclaw/workspace && python scripts/xhs-monitor.py >> logs/xhs-monitor.log 2>&1

# 或者每小时检查一次（更频繁）
0 * * * * cd /home/admin/.openclaw/workspace && python scripts/xhs-monitor.py >> logs/xhs-monitor.log 2>&1
```

---

## 📊 预期输出

### 控制台输出

```
============================================================
📱 小红书账号监控开始
============================================================
✅ XHS-Downloader API 服务正常：http://127.0.0.1:5556

🔍 检查账号：AI 科技前沿 (5f3b4e5d6c7a8b9c0d1e2f3a)
✅ 发现 3 个新作品
✅ 已保存到：outputs/xhs_AI 科技前沿_20260409_213500.json
✅ 已上传到 Get 笔记：1906687170912081184
✅ 已添加到 Ai &具身智能知识库

============================================================
✅ 监控完成！
============================================================
```

### Get 笔记内容

```markdown
# 📱 小红书账号监控报告

**账号**: AI 科技前沿
**检查时间**: 2026-04-09 21:35
**作品数量**: 3

---

## 1. 最新 AI 工具推荐

- 📅 发布时间：2026-04-09
- 👍 点赞：1234
- ⭐ 收藏：567
- 💬 评论：89

**描述**: 今天给大家推荐几款超好用的 AI 工具...

🔗 [阅读原文](https://www.xiaohongshu.com/explore/xxx)
```

---

## 🔧 故障排查

### Q: API 服务无法启动？

**检查**:
```bash
cd /home/admin/.openclaw/workspace/xhs-monitor
source venv/bin/activate
python main.py api
```

查看错误信息，可能是端口被占用或依赖缺失。

### Q: 获取用户作品失败？

**可能原因**:
1. Cookie 过期或未配置
2. 用户 ID 错误
3. 账号被风控

**解决方法**:
1. 重新获取 Cookie
2. 检查用户 ID 是否正确
3. 降低检查频率

### Q: 触发验证码？

小红书有严格的反爬机制，如果触发验证码：

1. 等待几分钟再试
2. 降低检查频率（建议每天 1-2 次）
3. 手动打开浏览器完成验证

---

## 📁 文件结构

```
/home/admin/.openclaw/workspace/
├── xhs-monitor/              # XHS-Downloader 主程序
│   ├── venv/                 # Python 虚拟环境
│   ├── main.py               # 主程序入口
│   ├── requirements.txt      # 依赖列表
│   ├── Volume/               # 数据和配置
│   └── logs/                 # 日志目录
│
├── scripts/
│   └── xhs-monitor.py        # 监控脚本
│
└── logs/
    └── xhs-monitor.log       # 监控日志
```

---

## 💡 最佳实践

### 1. Cookie 管理

- Cookie 会过期，建议每周更新一次
- 可以使用浏览器的"记住我"功能延长有效期
- 如果频繁失效，考虑扫码登录方案

### 2. 监控频率

- 建议每天检查 1-2 次
- 过于频繁可能触发风控
- 重要账号可以单独设置更高频率

### 3. 数据存储

- 本地文件定期备份
- Get 笔记作为主要存储
- 可以导出为 SQLite 数据库

---

## 📞 相关资源

- **XHS-Downloader**: https://github.com/JoeanAmier/XHS-Downloader
- **配置教程**: https://github.com/JoeanAmier/XHS-Downloader/blob/master/README.md
- **API 文档**: http://127.0.0.1:5556/docs（启动 API 后访问）

---

## ⚠️ 重要提醒

### 法律合规

- ✅ 仅用于个人学习和研究
- ✅ 遵守小红书使用条款
- ❌ 不得用于商业用途
- ❌ 不得侵犯知识产权

### 技术限制

- ⚠️ Cookie 会过期，需要定期更新
- ⚠️ 频繁请求可能触发验证码
- ⚠️ 建议设置合理的检查间隔
- ⚠️ 部分功能需要登录状态

---

**下一步**: 
1. 获取 Cookie 并配置
2. 添加要监控的账号
3. 启动 API 服务器
4. 测试运行监控脚本

*创建时间：2026-04-09 21:35*  
*最后更新：2026-04-09 21:35*
