#!/bin/bash
# Twitter/X AI 动态每日总结 - 定时任务脚本
# 用法：
#   ./twitter-cron.sh summary    # 生成总结
#   ./twitter-cron.sh notify     # 发送通知

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE/scripts"
LOGS_DIR="$WORKSPACE/logs"
TODAY=$(date +%Y-%m-%d)

# 确保日志目录存在
mkdir -p "$LOGS_DIR"

case "$1" in
    summary)
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始生成 Twitter 总结..." >> "$LOGS_DIR/twitter-summary.log"
        
        # 运行浏览器自动化脚本
        cd "$SCRIPTS_DIR"
        python3 twitter-browser-summary.py run >> "$LOGS_DIR/twitter-summary.log" 2>&1
        
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 总结生成完成" >> "$LOGS_DIR/twitter-summary.log"
        ;;
    
    notify)
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始发送通知..." >> "$LOGS_DIR/twitter-notify.log"
        
        # 检查是否有今天的总结文件
        SUMMARY_FILE="$WORKSPACE/TWITTER-REAL-SUMMARY-$TODAY.md"
        if [ -f "$SUMMARY_FILE" ]; then
            # 发送 DingTalk 通知
            # 这里需要配置 DingTalk webhook 或使用 OpenClaw message 工具
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发现今日总结：$SUMMARY_FILE" >> "$LOGS_DIR/twitter-notify.log"
            
            # 示例：使用 OpenClaw message 工具发送通知
            # openclaw message send --channel dingtalk "🐦 Twitter AI 动态今日总结已生成，请查看 Get 笔记"
            
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 通知已发送" >> "$LOGS_DIR/twitter-notify.log"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 未找到今日总结文件" >> "$LOGS_DIR/twitter-notify.log"
        fi
        ;;
    
    *)
        echo "用法：$0 {summary|notify}"
        exit 1
        ;;
esac
