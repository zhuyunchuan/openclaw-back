# 小红书自动化监控 - Mac 端部署指南

_创建时间：2026-04-17_

## 架构

```
MacBook（Chrome 登录态）
  → OpenCLI 抓取博主最新笔记
  → xhs-sync.sh 对比已见笔记
  → 新笔记 → Get 笔记 API 存储
  → 钉钉通知用户
```

## 一次性配置（30 分钟）

### 1. Mac 防休眠

```bash
# 插电时永不休眠，合盖也不休眠
sudo pmset -c sleep 0 disablesleep 1 displaysleep 5
```

### 2. 安装 OpenCLI

```bash
npm install -g @jackwener/opencli

# 下载浏览器扩展
# → GitHub Releases: https://github.com/jackwener/opencli/releases
# → 下载 opencli-extension-v*.zip
# → 解压后 chrome://extensions → 开发者模式 → 加载已解压的扩展

# 验证
opencli doctor
opencli xiaohongshu search "测试" --limit 1
```

### 3. 部署脚本

```bash
# 创建目录
mkdir -p ~/xhs-monitor

# 从服务器拷贝脚本
scp admin@服务器:/home/admin/.openclaw/workspace/scripts/xhs-sync.sh ~/xhs-monitor/
scp admin@服务器:/home/admin/.openclaw/workspace/scripts/xhs-bloggers.conf ~/xhs-monitor/

# 验证
cd ~/xhs-monitor
./xhs-sync.sh
```

### 4. 配置定时运行（LaunchAgent）

创建 `~/Library/LaunchAgents/com.xhs-sync.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.xhs-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/YOUR_USERNAME/xhs-monitor/xhs-sync.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>21</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/xhs-monitor/xhs-sync-launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/xhs-monitor/xhs-sync-error.log</string>
</dict>
</plist>
```

```bash
# 加载
launchctl load ~/Library/LaunchAgents/com.xhs-sync.plist

# 验证
launchctl list | grep xhs
```

### 5. 添加博主

编辑 `~/xhs-monitor/xhs-bloggers.conf`，每行一个博主：

```
# user_id|博主名称|知识库topic_id|标签
5b0e9e5e11be1045|某博主||投资
```

user_id 从博主主页 URL 获取。

## 运行逻辑

- **首次运行**：标记所有历史笔记为已见，不保存（跳过旧内容）
- **后续运行**：只抓新发布的笔记，自动存入 Get 笔记
- **每天运行 2 次**：9:00 和 21:00
- **只通知新内容**：你在钉钉收到摘要，想看详情点击链接

## 文件说明

| 文件 | 说明 |
|------|------|
| `xhs-sync.sh` | 主脚本 |
| `xhs-bloggers.conf` | 博主配置 |
| `xhs-sync-state.json` | 已见笔记 ID 状态（自动生成） |
| `xhs-sync.log` | 运行日志 |

## 故障排查

```bash
# 检查 OpenCLI 连接
opencli doctor

# 手动测试
opencli xiaohongshu creator-notes --user USER_ID --limit 5

# 查看日志
tail -50 ~/xhs-monitor/xhs-sync.log

# 查看状态
cat ~/xhs-monitor/xhs-sync-state.json | python3 -m json.tool
```
