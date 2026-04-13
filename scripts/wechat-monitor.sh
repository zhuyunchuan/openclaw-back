#!/bin/bash
# 微信公众号监控脚本 - 定时任务版本
# 使用方法：
# 1. 测试：./wechat-monitor.sh test
# 2. 运行：./wechat-monitor.sh run
# 3. 定时任务：crontab -e
#    0 */2 * * * /home/admin/.openclaw/workspace/scripts/wechat-monitor.sh run

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_FILE="/tmp/wechat-monitor.log"
CONFIG_FILE="$SCRIPT_DIR/wechat-config.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 测试模式
test_mode() {
    log "========== 测试模式开始 =========="
    python3 wechat-monitor.py test 2>&1 | tee -a "$LOG_FILE"
}

# 运行模式
run_mode() {
    log "========== 运行模式开始 =========="
    python3 wechat-monitor.py run 2>&1 | tee -a "$LOG_FILE"
    log "========== 运行模式结束 =========="
}

# 主逻辑
case "$1" in
    test)
        test_mode
        ;;
    run)
        run_mode
        ;;
    *)
        echo "用法：$0 {test|run}"
        echo "  test - 测试模式"
        echo "  run  - 运行模式（保存新文章到 Get 笔记）"
        exit 1
        ;;
esac
