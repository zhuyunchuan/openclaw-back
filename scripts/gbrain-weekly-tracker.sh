#!/bin/bash
# GBrain 项目进展周追踪脚本
# 用途：每周自动检查 gbrain 项目状态并记录

set -e

WORKSPACE_DIR="/home/admin/.openclaw/workspace"
TRACKING_FILE="$WORKSPACE_DIR/logs/gbrain-tracking.md"
LOG_DIR="$WORKSPACE_DIR/logs"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
WEEK_NUM=$(date +%Y-W%W)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/gbrain-tracker.log"
}

log "========== GBrain 周追踪 (第 $WEEK_NUM 周) =========="

# 创建或追加追踪文件
if [ ! -f "$TRACKING_FILE" ]; then
    cat > "$TRACKING_FILE" << 'EOF'
# GBrain 项目进展追踪

**开始追踪**: 2026-04-13  
**追踪频率**: 每周一次  
**项目地址**: https://github.com/garrytan/gbrain

---

## 追踪记录

EOF
fi

# 获取 GitHub 数据
log "📊 获取 GitHub 数据..."

# 使用 GitHub API 获取项目数据
STARS=$(curl -s "https://api.github.com/repos/garrytan/gbrain" | grep '"stargazers_count"' | grep -o '[0-9]*' || echo "N/A")
FORKS=$(curl -s "https://api.github.com/repos/garrytan/gbrain" | grep '"forks_count"' | grep -o '[0-9]*' || echo "N/A")
ISSUES=$(curl -s "https://api.github.com/repos/garrytan/gbrain" | grep '"open_issues_count"' | grep -o '[0-9]*' || echo "N/A")
LAST_UPDATE=$(curl -s "https://api.github.com/repos/garrytan/gbrain" | grep '"pushed_at"' | head -1 | cut -d'"' -f4 || echo "N/A")

# 获取最近提交数
COMMITS=$(curl -s "https://api.github.com/repos/garrytan/gbrain/commits?per_page=1" | grep -c '"sha"' || echo "0")

# 生成报告
cat >> "$TRACKING_FILE" << EOF

## 📅 $TIMESTAMP (第 $WEEK_NUM 周)

### 📊 项目指标

| 指标 | 数值 | 变化 |
|------|------|------|
| **Stars** | $STARS | - |
| **Forks** | $FORKS | - |
| **Open Issues** | $ISSUES | - |
| **最后更新** | $LAST_UPDATE | - |

### 🔍 检查项

- [ ] 检查是否有新版本发布
- [ ] 查看是否有重大更新
- [ ] 检查社区讨论热度
- [ ] 评估是否值得升级/采用

### 📝 本周备注

_在此记录本周的观察、发现或决策_

---

EOF

log "✅ 追踪记录已更新：$TRACKING_FILE"

# 显示最新数据
log ""
log "📊 本周数据:"
log "  Stars: $STARS"
log "  Forks: $FORKS"
log "  Open Issues: $ISSUES"
log "  最后更新：$LAST_UPDATE"

log ""
log "========== 追踪完成 =========="
log ""

# 如果有显著变化，可以添加通知逻辑
# 例如：Stars 增长超过 1000 或 新版本发布
