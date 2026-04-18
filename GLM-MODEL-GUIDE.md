# GLM 模型管理指南

## 📋 当前配置

**订阅计划：** Code Plan Lite  
**已配置模型：**
- `zhipu/glm-4-air` (alias: `glm-4-air`)
- `zhipu/glm-4-plus` (alias: `glm-4-plus`)
- `zhipu/glm-4-flash` (alias: `glm-4-flash`)

## 🔍 自动检查

**Cron 任务：** 每天上午 10:00 自动检查 GLM 官网新模型

```bash
# 检查日志
tail -f /home/admin/.openclaw/workspace/logs/glm-models-check.log

# 查看最新发现
cat /home/admin/.openclaw/workspace/memory/glm-new-models-notify.txt
```

## 📦 官方模型列表（2026-04-15 更新）

### 文本模型
| 模型 | 特点 | 上下文 | Code Plan Lite 可用性 |
|------|------|--------|----------------------|
| GLM-5.1 | 最新旗舰，Coding 对齐 Claude Opus 4.6 | 200K | ⚠️ 需确认 |
| GLM-5 | 高智能基座，Agentic 长程规划 | 200K | ⚠️ 需确认 |
| GLM-5-Turbo | 龙虾增强基座 | 200K | ⚠️ 需确认 |
| GLM-4.7 | 高智能模型，编程更强 | 200K | ✅ 可能可用 |
| GLM-4.7-Flash | 轻量高速 | 200K | ✅ 可能可用 |
| GLM-4.6 | 超强性能 | 200K | ✅ 可能可用 |
| GLM-4.5-Air | 高性价比 | 128K | ✅ 可用 |
| GLM-4-Long | 超长输入（1M 上下文） | 1M | ⚠️ 需确认 |
| GLM-4.7-Flash | 免费模型 | 200K | ✅ 免费 |

### 免费模型
- `GLM-4.7-Flash` - 最新基座普惠版本
- `GLM-4.5-Flash` - 即将下线
- `GLM-4-Flash-250414` - 超长上下文

## 🔄 切换模型流程

### 1. 发现新模型
当 cron 检测到新模型时，会生成通知文件：
```
/home/admin/.openclaw/workspace/memory/glm-new-models-notify.txt
```

### 2. 确认订阅范围
**Code Plan Lite** 通常包含：
- ✅ GLM-4-Air 系列
- ✅ GLM-4-Flash 系列
- ⚠️ GLM-5 系列（需确认）

查看订阅详情：https://open.bigmodel.cn/usercenter/packages

### 3. 备份配置
```bash
# 手动备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)

# 或使用脚本（自动备份）
/home/admin/.openclaw/workspace/scripts/switch-glm-model.sh glm-4-7
```

### 4. 添加新模型到配置
编辑 `~/.openclaw/openclaw.json`，在 `models.providers.zhipu.models` 数组中添加：

```json
{
  "id": "glm-4-7",
  "name": "GLM-4-7",
  "api": "openai-completions",
  "reasoning": false,
  "input": ["text", "image"],
  "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
  "contextWindow": 200000,
  "maxTokens": 128000
}
```

并在 `agents.defaults.models` 中添加别名：
```json
"zhipu/glm-4-7": {"alias": "glm-4-7"}
```

### 5. 切换模型
```bash
# 方法 1：聊天命令
/model zhipu/glm-4-7

# 方法 2：CLI 命令
openclaw models set zhipu/glm-4-7
```

### 6. 重启 Gateway
```bash
openclaw gateway restart
```

## 🔄 回滚（如新模型不可用）

```bash
# 查看备份列表
ls -la ~/.openclaw/backups/

# 恢复最近的备份
cp ~/.openclaw/backups/openclaw.json.20260415_100000 ~/.openclaw/openclaw.json

# 重启 Gateway
openclaw gateway restart
```

## 📅 已设置的定时任务

| 任务 | 时间 | 说明 |
|------|------|------|
| GLM 新模型检查 | 每天 10:00 | 自动检查官网新模型 |
| GLM 切换提醒 | 4 月 23 日 9:00 | 提醒切换到 GLM 主力模型 |

## 🔗 相关链接

- 智谱 AI 开放平台：https://open.bigmodel.cn/
- 模型概览：https://docs.bigmodel.cn/cn/guide/start/model-overview
- 我的订阅：https://open.bigmodel.cn/usercenter/packages
- API 文档：https://docs.bigmodel.cn/

## 📝 注意事项

1. **Code Plan Lite 限制** - 部分旗舰模型可能不在订阅范围内
2. **免费模型** - GLM-4.7-Flash 等免费模型可优先尝试
3. **备份优先** - 切换前务必备份配置
4. **逐步验证** - 先切换到新模型测试，确认无误后再设为默认

---
*最后更新：2026-04-15*
