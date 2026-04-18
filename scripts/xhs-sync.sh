#!/bin/bash
# ============================================
# 小红书博主监控 - 定时同步脚本
# 运行环境：MacBook（Chrome 已登录 + OpenCLI 已安装）
# 
# 使用方式：
#   1. 编辑 xhs-bloggers.conf 添加博主
#   2. ./xhs-sync.sh
#   3. 配置 LaunchAgent 每天自动运行
#
# 新笔记自动存入 Get 笔记 + 发钉钉通知
# 只抓新发布的笔记，跳过历史笔记
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONF_FILE="$SCRIPT_DIR/xhs-bloggers.conf"
STATE_FILE="$SCRIPT_DIR/xhs-sync-state.json"
LOG_FILE="$SCRIPT_DIR/xhs-sync.log"

# Get 笔记 API
GETNOTE_API_KEY="gk_live_9ce62ca78af4c66a.4e084c6e4ae8579e96f59a2b2967ff3d020e0700ed0365c5"
GETNOTE_CLIENT_ID="cli_a1b2c3d4e5f6789012345678abcdef90"

# 默认知识库：Ai &具身智能
DEFAULT_TOPIC_ID="oYpEp190"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 初始化状态文件
init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        echo '{}' > "$STATE_FILE"
    fi
}

# 获取博主最新笔记列表
# 参数: $1=user_id
fetch_notes() {
    local user_id="$1"
    opencli xiaohongshu creator-notes --user "$user_id" --limit 10 2>/dev/null
}

# 保存笔记到 Get 笔记
# 参数: $1=title, $2=content, $3=tags(JSON array), $4=topic_id
save_to_getnote() {
    local title="$1"
    local content="$2"
    local tags="$3"
    local topic_id="$4"
    
    curl -s -X POST 'https://openapi.biji.com/open/api/v1/resource/note/create' \
        -H "Authorization: Bearer $GETNOTE_API_KEY" \
        -H "X-Client-ID: $GETNOTE_CLIENT_ID" \
        -H 'Content-Type: application/json' \
        -d "{\"title\":\"$title\",\"content\":$(echo "$content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),\"tags\":$tags}" \
        --max-time 30 | python3 -c "
import sys, json
try:
    r = json.load(sys.stdin)
    if r.get('success'):
        nid = r['data']['note_id']
        # 加入知识库
        import urllib.request
        req = urllib.request.Request(
            'https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add',
            data=json.dumps({'topic_id': '$topic_id', 'note_ids': [nid]}).encode(),
            headers={
                'Authorization': 'Bearer $GETNOTE_API_KEY',
                'X-Client-ID': '$GETNOTE_CLIENT_ID',
                'Content-Type': 'application/json'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            kb = json.loads(resp.read()).get('success', False)
        print(f'OK:{nid}:kb={kb}')
    else:
        print(f'FAIL:{r}')
except Exception as e:
    print(f'ERROR:{e}')
"
}

# 检查单个博主
check_blogger() {
    local user_id="$1"
    local name="$2"
    local topic_id="$3"
    local tags_raw="$4"
    
    [ -z "$topic_id" ] && topic_id="$DEFAULT_TOPIC_ID"
    
    log "检查博主: $name ($user_id)"
    
    # 抓取笔记列表
    local notes_json
    notes_json=$(fetch_notes "$user_id")
    
    if [ -z "$notes_json" ]; then
        log "  ⚠️ 未抓取到笔记"
        return
    fi
    
    # 解析并对比
    local seen_key="${user_id}"
    local seen_ids
    seen_ids=$(python3 -c "
import json, sys
state = json.load(open('$STATE_FILE'))
seen = state.get('$seen_key', {}).get('seen_ids', [])
# 首次运行：标记所有为已见，不存历史
print(json.dumps(seen))
")
    
    local result
    result=$(python3 << PYEOF
import json, sys, subprocess, os

notes_raw = '''$notes_json'''
seen_ids = json.loads('''$seen_ids''')
name = "$name"
topic_id = "$topic_id"
tags_raw = "$tags_raw"
state_file = "$STATE_FILE"
user_id = "$user_id"

# 尝试解析笔记列表
try:
    notes = json.loads(notes_raw)
    if isinstance(notes, dict):
        notes = notes.get('data', notes.get('notes', notes.get('items', [])))
    if not isinstance(notes, list):
        print(f"WARN: 无法解析笔记列表: {type(notes)}")
        sys.exit(0)
except:
    print(f"WARN: JSON 解析失败")
    sys.exit(0)

new_notes = []
for note in notes:
    nid = note.get('note_id', note.get('id', ''))
    if nid and nid not in seen_ids:
        new_notes.append(note)

if not new_notes:
    print("NO_NEW")
    # 更新状态
    all_ids = list(set(seen_ids + [n.get('note_id', n.get('id', '')) for n in notes]))
    try:
        state = json.load(open(state_file))
    except:
        state = {}
    state[user_id] = {
        'name': name,
        'seen_ids': all_ids,
        'last_check': __import__('datetime').datetime.now().isoformat(),
        'total_seen': len(all_ids)
    }
    with open(state_file, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    sys.exit(0)

# 首次运行：只标记，不保存
if not seen_ids:
    all_ids = [n.get('note_id', n.get('id', '')) for n in notes]
    try:
        state = json.load(open(state_file))
    except:
        state = {}
    state[user_id] = {
        'name': name,
        'seen_ids': all_ids,
        'last_check': __import__('datetime').datetime.now().isoformat(),
        'total_seen': len(all_ids),
        'first_run': True
    }
    with open(state_file, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"FIRST_RUN: 标记 {len(all_ids)} 条历史笔记")
    sys.exit(0)

# 有新笔记
print(f"NEW:{len(new_notes)}")
for note in new_notes:
    nid = note.get('note_id', note.get('id', ''))
    title = note.get('title', note.get('desc', ''))[:50]
    url = note.get('url', note.get('note_url', f"https://www.xiaohongshu.com/explore/{nid}"))
    desc = note.get('desc', note.get('content', ''))
    print(f"NOTE:{nid}|{title}|{url}|{desc[:200]}")

# 更新状态
all_ids = list(set(seen_ids + [n.get('note_id', n.get('id', '')) for n in notes]))
try:
    state = json.load(open(state_file))
except:
    state = {}
state[user_id] = {
    'name': name,
    'seen_ids': all_ids,
    'last_check': __import__('datetime').datetime.now().isoformat(),
    'total_seen': len(all_ids)
}
with open(state_file, 'w') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
PYEOF
)
    
    echo "$result" | while IFS= read -r line; do
        case "$line" in
            NO_NEW)
                log "  ✅ 无新笔记"
                ;;
            FIRST_RUN*)
                log "  📌 首次运行: ${line#FIRST_RUN: }"
                ;;
            NEW:*)
                log "  🆕 发现 ${line#NEW:} 条新笔记"
                ;;
            NOTE:*)
                local note_data="${line#NOTE:}"
                local nid=$(echo "$note_data" | cut -d'|' -f1)
                local ntitle=$(echo "$note_data" | cut -d'|' -f2)
                local nurl=$(echo "$note_data" | cut -d'|' -f3)
                local ndesc=$(echo "$note_data" | cut -d'|' -f4-)
                
                local full_title="📕 小红书 | ${name} | ${ntitle}"
                local content="# ${ntitle}\n\n博主: ${name}\n链接: ${nurl}\n日期: $(date '+%Y-%m-%d')\n\n---\n\n${ndesc}"
                local tags='["小红书","信息源"]'
                
                log "  💾 保存: ${ntitle}"
                local save_result
                save_result=$(save_to_getnote "$full_title" "$content" "$tags" "$topic_id")
                log "  → $save_result"
                ;;
        esac
    done
}

# ============ 主流程 ============

log "========== 开始同步 =========="
init_state

if [ ! -f "$CONF_FILE" ]; then
    log "❌ 配置文件不存在: $CONF_FILE"
    exit 1
fi

# 读取配置并逐个检查
# 配置格式: user_id|name|topic_id|tags
while IFS='|' read -r user_id name topic_id tags; do
    # 跳过注释和空行
    [[ -z "$user_id" || "$user_id" == \#* ]] && continue
    
    check_blogger "$user_id" "$name" "$topic_id" "$tags"
    sleep 5  # 礼貌性延迟
done < "$CONF_FILE"

log "========== 同步完成 =========="
