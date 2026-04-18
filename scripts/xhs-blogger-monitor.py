#!/usr/bin/env python3
"""
小红书博主监控脚本
- 使用 headless Chrome 抓取博主主页笔记列表
- 对比上次抓取结果，发现新笔记
- 新笔记内容存入 Get 笔记 + AI 知识库
"""

import json
import os
import sys
import time
import hashlib
import requests
from datetime import datetime
from pathlib import Path

# ============ 配置 ============

WORKSPACE = Path("/home/admin/.openclaw/workspace")
CONFIG_FILE = WORKSPACE / "xhs-monitor-config.json"
STATE_FILE = WORKSPACE / "xhs-monitor-state.json"
VENV_AI = WORKSPACE / "venv-ai-news" / "bin" / "python"

# Get 笔记
GETNOTE_API_KEY = "gk_live_9ce62ca78af4c66a.4e084c6e4ae8579e96f59a2b2967ff3d020e0700ed0365c5"
GETNOTE_CLIENT_ID = "cli_a1b2c3d4e5f6789012345678abcdef90"
GETNOTE_TOPIC_ID = "oYpEp190"  # Ai &具身智能

# ============ 工具函数 ============

def load_config():
    """加载监控配置"""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"bloggers": []}

def load_state():
    """加载监控状态（已见过的笔记 ID）"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def save_to_getnote(title, content, tags):
    """保存到 Get 笔记并加入知识库"""
    headers = {
        'Authorization': f'Bearer {GETNOTE_API_KEY}',
        'X-Client-ID': GETNOTE_CLIENT_ID,
        'Content-Type': 'application/json'
    }
    
    # 标签截断到 <= 10 中文字符
    safe_tags = [t[:10] for t in tags]
    
    data = {'title': title, 'content': content, 'tags': safe_tags}
    
    try:
        r = requests.post('https://openapi.biji.com/open/api/v1/resource/note/create',
                         headers=headers, json=data, timeout=30)
        res = r.json()
        if not res.get('success'):
            print(f"  ❌ 创建失败: {res}")
            return None
        
        note_id = res['data']['note_id']
        
        # 加入知识库
        time.sleep(2)
        r2 = requests.post('https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add',
                          headers=headers,
                          json={'topic_id': GETNOTE_TOPIC_ID, 'note_ids': [note_id]},
                          timeout=15)
        
        if r2.json().get('success'):
            print(f"  ✅ 已存到 Get 笔记 (id={note_id})")
        return note_id
    except Exception as e:
        print(f"  ❌ 保存异常: {e}")
        return None

def fetch_user_notes_via_browser(user_id, user_name):
    """通过 headless Chrome 抓取博主主页"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=opts)
    notes = []
    
    try:
        url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
        print(f"  📡 访问: {url}")
        driver.get(url)
        time.sleep(3)
        
        # 滚动加载更多
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(1.5)
        
        # 提取笔记卡片
        cards = driver.find_elements(By.CSS_SELECTOR, "section.note-item a")
        for card in cards:
            try:
                href = card.get_attribute('href') or ''
                title_el = card.find_elements(By.CSS_SELECTOR, ".title, .note-title, span")
                title = title_el[0].text if title_el else ''
                
                # 从链接提取笔记 ID
                note_id = ''
                if '/explore/' in href:
                    note_id = href.split('/explore/')[-1].split('?')[0]
                elif '/discovery/item/' in href:
                    note_id = href.split('/discovery/item/')[-1].split('?')[0]
                
                if note_id and title:
                    notes.append({
                        'note_id': note_id,
                        'title': title,
                        'url': href,
                    })
            except Exception:
                continue
        
        print(f"  📊 抓取到 {len(notes)} 条笔记")
        
    except Exception as e:
        print(f"  ❌ 抓取失败: {e}")
    finally:
        driver.quit()
    
    return notes

def check_blogger(user_id, user_name, state):
    """检查单个博主的新笔记"""
    print(f"\n🔍 检查博主: {user_name} ({user_id})")
    
    notes = fetch_user_notes_via_browser(user_id, user_name)
    if not notes:
        print(f"  ⚠️ 未抓取到笔记，可能需要登录或风控")
        return []
    
    key = user_id
    seen = state.get(key, {}).get('seen_notes', [])
    new_notes = [n for n in notes if n['note_id'] not in seen]
    
    if not new_notes:
        print(f"  ✅ 无新笔记")
        return []
    
    print(f"  🆕 发现 {len(new_notes)} 条新笔记")
    
    saved = []
    for note in new_notes:
        title = f"📕 小红书 | {user_name} | {note['title']}"
        content = f"# {note['title']}\n\n博主: {user_name}\n链接: {note['url']}\n日期: {datetime.now().strftime('%Y-%m-%d')}\n\n---\n\n> 内容需点击链接查看原文"
        tags = ['小红书', '信息源']
        
        note_id = save_to_getnote(title, content, tags)
        if note_id:
            saved.append(note)
    
    # 更新状态
    all_seen = list(set(seen + [n['note_id'] for n in notes]))
    state[key] = {
        'name': user_name,
        'seen_notes': all_seen,
        'last_check': datetime.now().isoformat(),
        'total_seen': len(all_seen)
    }
    
    return saved

def main():
    config = load_config()
    state = load_state()
    
    bloggers = config.get('bloggers', [])
    if not bloggers:
        print("⚠️ 未配置监控博主。请编辑 xhs-monitor-config.json")
        print('格式: {"bloggers": [{"user_id": "xxx", "name": "博主名"}]}')
        return
    
    print(f"📋 监控 {len(bloggers)} 位博主")
    print(f"{'='*50}")
    
    total_new = 0
    for b in bloggers:
        saved = check_blogger(b['user_id'], b['name'], state)
        total_new += len(saved)
        time.sleep(3)  # 礼貌性延迟
    
    save_state(state)
    print(f"\n{'='*50}")
    print(f"✅ 检查完成，本次新增 {total_new} 条笔记")

if __name__ == "__main__":
    main()
