# 📦 OpenClaw 配置备份与迁移指南

**创建时间**: 2026-04-13  
**用途**: 快速备份配置到 GitHub，便于服务器迁移

---

## 🎯 备份内容

### ✅ 会备份的内容

| 类别 | 说明 |
|------|------|
| **Skill 文件** | `skills/` 目录下的所有技能 |
| **Extensions** | `extensions/` 下的扩展配置 |
| **Workspace** | 工作区配置文件（SOUL.md、AGENTS.md 等） |
| **脚本** | `scripts/` 目录下的自动化脚本 |
| **文档** | 各类 setup guide、README |

### ❌ 不备份的内容（敏感信息）

| 类别 | 说明 |
|------|------|
| **API Keys** | Get 笔记、智谱 AI、通义千问等 API 密钥 |
| **账号配置** | 飞书、钉钉、企业微信等账号信息 |
| **个人笔记** | `memory/`、`MEMORY.md` |
| **媒体文件** | 语音、图片、视频 |
| **日志** | `logs/` 目录 |
| **虚拟环境** | `venv*/` 目录 |

---

## 📤 首次备份到 GitHub

### 步骤 1: 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库（私有推荐）
# 例如：openclaw-config
```

### 步骤 2: 初始化并上传

```bash
cd /home/admin/.openclaw/workspace

# 添加所有文件
git add -A

# 首次提交
git commit -m "Initial backup: OpenClaw config and skills"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/openclaw-config.git

# 推送
git push -u origin master
```

---

## 📥 在新服务器上恢复

### 步骤 1: 克隆配置

```bash
# 在新服务器上克隆
git clone https://github.com/YOUR_USERNAME/openclaw-config.git
cd openclaw-config
```

### 步骤 2: 安装 OpenClaw

```bash
# 安装 OpenClaw（如果还没安装）
npm install -g openclaw

# 或使用官方安装脚本
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 步骤 3: 复制配置文件

```bash
# 复制 skill 文件到 OpenClaw 目录
cp -r skills/* ~/.openclaw/workspace/skills/

# 复制 extensions
cp -r extensions/* ~/.openclaw/extensions/

# 复制 workspace 配置
cp AGENTS.md SOUL.md USER.md TOOLS.md ~/.openclaw/workspace/
cp HEARTBEAT.md ~/.openclaw/workspace/
```

### 步骤 4: 重新配置敏感信息

```bash
# 配置 API Keys
openclaw configure --section models
openclaw configure --section web

# 配置飞书/钉钉/企业微信
openclaw configure --section lark
openclaw configure --section dingtalk
openclaw configure --section wecom
```

### 步骤 5: 安装依赖

```bash
# AI News 脚本依赖
cd scripts
pip3 install feedparser requests

# Get 笔记技能依赖
cd ~/.openclaw/workspace/skills/getnote
pip3 install requests

# 其他虚拟环境
cd ~/.openclaw/workspace/venv-ai-news
source bin/activate
pip install -r requirements.txt 2>/dev/null || pip install feedparser requests beautifulsoup4
```

### 步骤 6: 重启 Gateway

```bash
# 重启 OpenClaw Gateway
openclaw gateway restart

# 检查状态
openclaw status
```

---

## 🔄 日常更新备份

### 有变更时推送

```bash
cd /home/admin/.openclaw/workspace

# 查看变更
git status

# 添加并提交
git add -A
git commit -m "Update: $(date +%Y-%m-%d) - 简要描述变更"

# 推送
git push
```

### 定时备份（可选）

```bash
# 添加到 crontab，每天凌晨 2 点自动备份
crontab -e

# 添加以下行
0 2 * * * cd /home/admin/.openclaw/workspace && git add -A && git commit -m "Auto backup $(date +\%Y-\%m-\%d)" && git push 2>/dev/null || true
```

---

## 📋 迁移检查清单

在新服务器上完成以下检查：

- [ ] OpenClaw 已安装 (`openclaw --version`)
- [ ] Gateway 正常运行 (`openclaw gateway status`)
- [ ] API Keys 已配置
- [ ] Skill 文件已复制
- [ ] Extensions 已复制
- [ ] 虚拟环境依赖已安装
- [ ] 定时任务已恢复 (`crontab -l`)
- [ ] 消息渠道已连接（飞书/钉钉/微信等）
- [ ] 测试发送消息
- [ ] 测试 AI 日报脚本

---

## 🔐 安全建议

1. **使用私有仓库** - 配置可能包含敏感信息
2. **定期轮换 API Keys** - 即使不小心泄露也能降低风险
3. **不要提交 `.env` 文件** - 已在 .gitignore 中排除
4. **使用 GitHub Secrets** - 如果做 CI/CD 自动化

---

## 📞 快速参考

### 当前配置位置

```
OpenClaw 主目录：~/.openclaw/
Workspace:        ~/.openclaw/workspace/
Skills:           ~/.openclaw/workspace/skills/
Extensions:       ~/.openclaw/extensions/
Memory:           ~/.openclaw/workspace/memory/
Logs:             ~/.openclaw/logs/
```

### 常用命令

```bash
# 查看状态
openclaw status

# 重启 Gateway
openclaw gateway restart

# 查看日志
tail -f ~/.openclaw/logs/gateway.log

# 配置管理
openclaw configure

# 技能管理
clawhub list
clawhub install <skill-name>
```

---

## 🆘 故障排查

### Gateway 无法启动

```bash
# 检查配置
openclaw gateway status

# 查看详细日志
journalctl -u openclaw-gateway -n 50

# 手动启动调试
openclaw gateway start --debug
```

### Skill 不生效

```bash
# 检查技能文件
ls -la ~/.openclaw/workspace/skills/

# 重新加载
openclaw gateway restart
```

### API 调用失败

```bash
# 检查 API Key 配置
openclaw configure --section models

# 测试 API 连通性
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.example.com/health
```

---

*最后更新：2026-04-13*
