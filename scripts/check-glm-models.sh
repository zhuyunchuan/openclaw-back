#!/bin/bash
# GLM 新模型检查脚本
# 每天检查一次智谱 AI 模型页面，发现新模型时通知用户

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
STATE_FILE="$WORKSPACE/memory/glm-models-state.json"
LOG_FILE="$WORKSPACE/memory/glm-models-check.log"
CONFIG_FILE="$WORKSPACE/../openclaw.json"

# 当前已配置的模型列表
CONFIGURED_MODELS=("glm-4-air" "glm-4-plus" "glm-4-flash")

# 智谱官方模型页面
MODEL_PAGE="https://docs.bigmodel.cn/cn/guide/start/model-overview"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "开始检查 GLM 新模型..."

# 获取当前页面内容
CONTENT=$(curl -s "$MODEL_PAGE" | grep -oP '\[GLM[^]]*\]' | sort -u)

if [ -z "$CONTENT" ]; then
    log "错误：无法获取模型页面内容"
    exit 1
fi

# 提取模型名称
NEW_MODELS=()
while IFS= read -r line; do
    # 提取模型名，如 GLM-5.1, GLM-4.7-Flash 等
    model=$(echo "$line" | grep -oP 'GLM-[\w\.\-]+' | head -1)
    if [ -n "$model" ]; then
        # 转换为 OpenClaw 格式：glm-5-1, glm-4-7-flash
        model_id=$(echo "$model" | tr '[:upper:]' '[:lower:]' | sed 's/glm-/glm-/g' | sed 's/\./-/g')
        
        # 检查是否已配置
        found=0
        for configured in "${CONFIGURED_MODELS[@]}"; do
            if [[ "$configured" == *"$model_id"* ]] || [[ "$model_id" == *"$configured"* ]]; then
                found=1
                break
            fi
        done
        
        if [ $found -eq 0 ]; then
            NEW_MODELS+=("$model ($model_id)")
            log "发现新模型：$model ($model_id)"
        fi
    fi
done <<< "$CONTENT"

# 保存状态
if [ ${#NEW_MODELS[@]} -gt 0 ]; then
    log "发现 ${#NEW_MODELS[@]} 个新模型"
    
    # 创建通知消息
    MESSAGE="🔔 GLM 新模型发现通知\n\n"
    MESSAGE+="发现以下新模型：\n"
    for model in "${NEW_MODELS[@]}"; do
        MESSAGE+="• $model\n"
    done
    MESSAGE+="\n⚠️ 注意：你订阅的是 Code Plan Lite 版本\n"
    MESSAGE+="切换前请确认新模型在订阅范围内\n\n"
    MESSAGE+="备份命令：cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.\$(date +%Y%m%d)\n"
    MESSAGE+="切换命令：/model zhipu/<model-id>"
    
    echo "$MESSAGE" > "$WORKSPACE/memory/glm-new-models-notify.txt"
    log "通知已保存到：$WORKSPACE/memory/glm-new-models-notify.txt"
    
    # 输出到 stdout（供 cron 使用）
    echo "$MESSAGE"
else
    log "未发现新模型"
    echo "未发现 GLM 新模型"
fi

log "检查完成"
