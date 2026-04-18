#!/bin/bash
# GLM 模型切换脚本（带备份）
# 用法：./switch-glm-model.sh <model-id>

set -e

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -z "$1" ]; then
    echo "用法：$0 <model-id>"
    echo "示例：$0 glm-5-1"
    echo ""
    echo "可用模型："
    echo "  glm-5-1          - 最新旗舰（Coding 对齐 Claude Opus 4.6）"
    echo "  glm-5            - 高智能基座（Agentic 长程规划）"
    echo "  glm-5-turbo      - 龙虾增强基座"
    echo "  glm-4-7          - 高智能模型（编程更强）"
    echo "  glm-4-7-flash    - 轻量高速"
    echo "  glm-4-6          - 超强性能"
    echo "  glm-4-5-air      - 高性价比"
    echo "  glm-4-long       - 超长输入（1M 上下文）"
    exit 1
fi

MODEL_ID="$1"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份当前配置
BACKUP_FILE="$BACKUP_DIR/openclaw.json.$TIMESTAMP"
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "✅ 配置已备份：$BACKUP_FILE"

# 检查模型是否在配置中
if grep -q "zhipu/$MODEL_ID" "$CONFIG_FILE"; then
    echo "✅ 模型 zhipu/$MODEL_ID 已在配置中"
else
    echo "⚠️  模型 zhipu/$MODEL_ID 不在当前配置中"
    echo "需要先添加到 openclaw.json 的 models.providers.zhipu.models 数组"
    exit 1
fi

# 提示用户手动切换
echo ""
echo "📋 切换模型命令："
echo "  /model zhipu/$MODEL_ID"
echo ""
echo "📁 备份文件位置：$BACKUP_FILE"
echo ""
echo "🔄 恢复命令（如需回滚）："
echo "  cp $BACKUP_FILE $CONFIG_FILE"
echo "  openclaw gateway restart"
