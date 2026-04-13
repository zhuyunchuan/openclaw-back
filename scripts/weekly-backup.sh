#!/bin/bash
# OpenClaw 周备份脚本
# 用途：每周自动备份配置到 GitHub
# 添加到 crontab: 0 2 * * 0 /home/admin/.openclaw/workspace/scripts/weekly-backup.sh

set -e

WORKSPACE_DIR="/home/admin/.openclaw/workspace"
LOG_FILE="/home/admin/.openclaw/workspace/logs/weekly-backup.log"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
WEEK_NUM=$(date +%Y-W%W)

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========== 周备份开始 (第 $WEEK_NUM 周) =========="

cd "$WORKSPACE_DIR"

# 检查 git 状态
if ! git status &>/dev/null; then
    log "❌ 错误：不是 git 仓库"
    exit 1
fi

# 查看是否有变更
git add -A
CHANGES=$(git status --short)

if [ -z "$CHANGES" ]; then
    log "ℹ️  无变更，跳过备份"
    log "========== 周备份完成 (无变更) =========="
    exit 0
fi

log "📋 检测到变更:"
echo "$CHANGES" | tee -a "$LOG_FILE"

# 生成提交信息
COMMIT_MSG="Weekly backup $WEEK_NUM - $TIMESTAMP

Automated weekly backup of OpenClaw configuration.

Changes:
$(git status --short | head -20)"

# 提交
git commit -m "$COMMIT_MSG"
log "✅ 提交完成"

# 推送
if git push origin master 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ 推送成功"
    log "📍 仓库：https://github.com/zhuyunchuan/openclaw-back"
else
    log "❌ 推送失败，请检查网络连接"
    exit 1
fi

log "========== 周备份完成 =========="
log ""
