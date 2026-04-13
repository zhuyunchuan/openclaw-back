# 📱 小红书监控方案调研报告

**调研时间**: 2026-04-09 13:28  
**需求**: 订阅小红书特定账号/关键词的更新

---

## 🎯 核心结论

**小红书没有官方 RSS 源**，但有以下可行方案：

### 方案对比

| 方案 | 难度 | 稳定性 | 成本 | 推荐度 |
|------|------|--------|------|--------|
| **方案 1: XHS-Downloader** | ⭐⭐ | ⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ |
| **方案 2: xiaohongshu-skill** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐ |
| **方案 3: RSSWorker** | ⭐⭐⭐⭐ | ⭐⭐⭐ | 免费 | ⭐⭐⭐ |
| **方案 4: 第三方 API** | ⭐ | ⭐⭐⭐ | 付费 | ⭐⭐ |

---

## 📋 方案详解

### 方案 1: XHS-Downloader（强烈推荐 ⭐⭐⭐⭐⭐）

**GitHub**: https://github.com/JoeanAmier/XHS-Downloader  
**状态**: ✅ 2026-04-08 最新维护  
**语言**: Python

#### 核心功能

✅ 采集小红书作品信息  
✅ 提取账号发布/收藏/点赞作品链接  
✅ 提取搜索结果作品/用户链接  
✅ 下载小红书作品文件（图文/视频）  
✅ 支持 API 调用  
✅ 支持 MCP 调用  
✅ 后台监听剪贴板  
✅ 自动跳过已下载作品  

#### 使用方法

```bash
# 1. 安装依赖
git clone https://github.com/JoeanAmier/XHS-Downloader.git
cd XHS-Downloader
pip install -r requirements.txt

# 2. 运行（TUI 模式）
python main.py

# 3. 运行（API 模式）
python main.py api

# 4. 运行（MCP 模式）
python main.py mcp
```

#### API 调用示例

```python
import requests

# 启动 API 服务器后
server = "http://127.0.0.1:5556/xhs/detail"
data = {
    "url": "https://www.xiaohongshu.com/explore/作品 ID",
    "download": False,  # 不下载文件，只获取信息
}
response = requests.post(server, json=data)
print(response.json())
```

#### 定时监控脚本

```python
#!/usr/bin/env python3
# 监控特定小红书账号

import requests
import time
from datetime import datetime

# 配置
MONITOR_USERS = [
    "用户 ID 1",
    "用户 ID 2",
]
CHECK_INTERVAL = 3600  # 每小时检查一次

def check_user_updates(user_id):
    """检查用户是否有新作品"""
    # 调用 XHS-Downloader API
    response = requests.post(
        "http://127.0.0.1:5556/xhs/user",
        json={"user_id": user_id}
    )
    data = response.json()
    return data

def main():
    while True:
        for user_id in MONITOR_USERS:
            updates = check_user_updates(user_id)
            if updates:
                print(f"用户 {user_id} 有新作品！")
                # 发送到 Get 笔记或其他通知
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
```

#### 优点

- ✅ 功能最全面
- ✅ 维护活跃（最后更新：2026-04-08）
- ✅ 支持多种运行模式
- ✅ 有详细的 API 文档
- ✅ 免费开源
- ✅ 支持 MCP 协议（可与 AI Agent 集成）

#### 缺点

- ⚠️ 需要 Cookie（无需登录，但需要获取）
- ⚠️ 有反爬限制（内置延时保护）

---

### 方案 2: xiaohongshu-skill（推荐 ⭐⭐⭐⭐）

**GitHub**: https://github.com/DeliciousBuding/xiaohongshu-skill  
**状态**: ✅ 2026-02-23 维护  
**语言**: Python + Playwright

#### 核心功能

✅ 二维码扫码登录  
✅ 搜索笔记（支持筛选）  
✅ 提取帖子详情  
✅ 查看用户主页  
✅ 反爬保护机制  

#### 使用方法

```bash
# 1. 克隆仓库
git clone https://github.com/DeliciousBuding/xiaohongshu-skill.git
cd xiaohongshu-skill

# 2. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 3. 扫码登录
python -m scripts qrcode --headless=false

# 4. 搜索笔记
python -m scripts search "美食推荐" --limit=5

# 5. 查看用户主页
python -m scripts user <user_id>
```

#### 集成到 OpenClaw

```bash
# 克隆到 OpenClaw Skills 目录
git clone https://github.com/DeliciousBuding/xiaohongshu-skill.git ~/.openclaw/workspace/skills/xiaohongshu-skill
```

#### 优点

- ✅ 兼容 OpenClaw
- ✅ 支持扫码登录（更稳定）
- ✅ 内置反爬保护
- ✅ 支持搜索功能

#### 缺点

- ⚠️ 需要 Playwright 浏览器
- ⚠️ 需要扫码登录（需人工介入）

---

### 方案 3: RSSWorker（技术向 ⭐⭐⭐）

**GitHub**: https://github.com/yllhwa/RSSWorker  
**状态**: ✅ 2026-03-28 维护  
**语言**: JavaScript

#### 核心功能

✅ 在 Cloudflare Worker 上运行  
✅ 生成 RSS 订阅源  
✅ 支持多个平台（包括小红书）  

#### 部署方法

1. Fork 项目到 GitHub
2. 部署到 Cloudflare Workers
3. 配置小红书账号/关键词
4. 获取 RSS 订阅链接

#### 优点

- ✅ 生成标准 RSS
- ✅ 可集成到现有 RSS 阅读器
- ✅ 免费（Cloudflare 免费额度）

#### 缺点

- ⚠️ 需要 Cloudflare 账号
- ⚠️ 配置复杂
- ⚠️ 稳定性依赖 Cloudflare

---

### 方案 4: 第三方 API 服务（付费 ⭐⭐）

**服务商**:
- TikHub: https://github.com/TikHub/TikHub-API-Python-SDK
- JustOneAPI: https://github.com/justoneapi/data-api

#### 使用示例

```python
from tikhub import TikHub

client = TikHub(api_key="your_key")
user_posts = client.xiaohongshu.get_user_posts(user_id="xxx")
```

#### 优点

- ✅ 简单易用
- ✅ 无需维护

#### 缺点

- ⚠️ 需要付费
- ⚠️ 依赖第三方服务
- ⚠️ 可能不稳定

---

## 🎯 推荐实施方案

### 方案 1: XHS-Downloader + 定时任务（最佳选择）

**步骤**:

1. **安装 XHS-Downloader**
```bash
cd /home/admin/.openclaw/workspace
git clone https://github.com/JoeanAmier/XHS-Downloader.git xhs-monitor
cd xhs-monitor
pip install -r requirements.txt
```

2. **获取 Cookie**
   - 打开浏览器访问小红书
   - F12 → Network → 复制 Cookie
   - 写入配置文件

3. **创建监控脚本**
```python
#!/usr/bin/env python3
# /home/admin/.openclaw/workspace/scripts/xhs-monitor.py

import requests
import json
from datetime import datetime

# 配置
XHS_API_URL = "http://127.0.0.1:5556/xhs"
MONITOR_USERS = [
    {"user_id": "用户 ID 1", "name": "账号名 1"},
    {"user_id": "用户 ID 2", "name": "账号名 2"},
]

def get_user_posts(user_id):
    """获取用户作品列表"""
    response = requests.post(
        f"{XHS_API_URL}/user",
        json={"user_id": user_id}
    )
    return response.json()

def save_to_getnote(posts, user_name):
    """保存到 Get 笔记"""
    # TODO: 实现
    pass

def main():
    for user in MONITOR_USERS:
        posts = get_user_posts(user["user_id"])
        if posts:
            print(f"用户 {user['name']} 有 {len(posts)} 个作品")
            save_to_getnote(posts, user["name"])

if __name__ == "__main__":
    main()
```

4. **设置定时任务**
```bash
crontab -e
# 每天早上 9 点检查更新
0 9 * * * cd /home/admin/.openclaw/workspace/xhs-monitor && python scripts/xhs-monitor.py
```

---

### 方案 2: xiaohongshu-skill + OpenClaw（备选）

**适用场景**: 需要搜索功能或更稳定的登录

**步骤**:

1. **安装 Skill**
```bash
git clone https://github.com/DeliciousBuding/xiaohongshu-skill.git ~/.openclaw/workspace/skills/xiaohongshu-skill
```

2. **扫码登录**
```bash
cd ~/.openclaw/workspace/skills/xiaohongshu-skill
python -m scripts qrcode
# 扫描二维码
```

3. **在 OpenClaw 中使用**
```
@xiaohongshu-skill 搜索"AI 工具"
@xiaohongshu-skill 查看用户主页 user_xxx
```

---

## 💡 实施建议

### 立即可用（推荐）

1. **安装 XHS-Downloader** - 功能最全，维护活跃
2. **手动检查** - 先测试功能是否正常
3. **配置 Cookie** - 获取网页版 Cookie
4. **创建监控列表** - 确定要监控的账号

### 后续优化

1. **自动化脚本** - 定时检查更新
2. **集成 Get 笔记** - 自动保存新作品
3. **通知功能** - 发现更新时推送通知

---

## ⚠️ 注意事项

### 法律合规

- ✅ 仅用于个人学习和研究
- ✅ 遵守小红书使用条款
- ❌ 不得用于商业用途
- ❌ 不得侵犯知识产权

### 技术限制

- ⚠️ 小红书有严格的反爬机制
- ⚠️ Cookie 会过期，需要定期更新
- ⚠️ 频繁请求可能触发验证码
- ⚠️ 建议设置合理的检查间隔（如每天 1-2 次）

---

## 📞 相关资源

- **XHS-Downloader**: https://github.com/JoeanAmier/XHS-Downloader
- **xiaohongshu-skill**: https://github.com/DeliciousBuding/xiaohongshu-skill
- **RSSWorker**: https://github.com/yllhwa/RSSWorker
- **TikHub API**: https://github.com/TikHub/TikHub-API-Python-SDK

---

*创建时间：2026-04-09 13:30*  
*最后更新：2026-04-09 13:30*
