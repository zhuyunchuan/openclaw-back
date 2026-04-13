#!/bin/bash
# Twitter/X AI 动态 - 每日通知脚本
# 发送 DingTalk 消息提醒用户查看最新总结

# 获取昨天的日期
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

# 检查是否有昨天的总结文件
SUMMARY_FILE="/home/admin/.openclaw/workspace/TWITTER-REAL-SUMMARY-${YESTERDAY}.md"

if [ -f "$SUMMARY_FILE" ]; then
    # 总结已生成，发送通知
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发送通知：Twitter/X AI 动态 ${YESTERDAY} 已更新" >> /tmp/twitter-notify.log
    
    # 使用 OpenClaw message 工具发送 DingTalk 消息
    # 注意：这里需要通过 OpenClaw 内部调用，实际使用时由 agent 处理
    echo "🐦 Twitter/X AI 动态 (${YESTERDAY}) 已生成并保存到 Get 笔记，请查看！"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 未找到总结文件：${SUMMARY_FILE}" >> /tmp/twitter-notify.log
fi
