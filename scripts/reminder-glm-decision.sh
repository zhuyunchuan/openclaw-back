#!/bin/bash
# 4 月 23 日提醒 - 确认是否更换大模型为 GLM（智谱 AI）

echo "=============================================="
echo "🔔 提醒：确认是否更换大模型"
echo "=============================================="
echo ""
echo "📅 日期：2026-04-23"
echo ""
echo "🤖 当前模型：通义千问 (dashscope-coding/qwen3.5-plus)"
echo ""
echo "🔄 拟更换为：智谱 AI (GLM)"
echo ""
echo "✅ GLM API Key 已配置：是"
echo ""
echo "📋 需要确认的事项："
echo "1. 是否要切换主力模型为 GLM？"
echo "2. GLM-4 还是 GLM-4-Flash？"
echo "3. 测试效果是否符合预期？"
echo ""
echo "🔧 切换命令："
echo "   openclaw configure --section models"
echo ""
echo "=============================================="

# 发送 DingTalk 通知（如果配置了）
# 这里可以添加通知逻辑
