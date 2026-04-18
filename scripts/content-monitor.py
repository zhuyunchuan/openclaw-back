#!/usr/bin/env python3
"""
统一信息源监控脚本
- 知识星球（API 直连）
- 微信公众号（RSSHub）
- 未来可扩展：B站、知乎等

运行环境：服务器端，无需浏览器
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
CONFIG_FILE = WORKSPACE / "scripts/content-sources.json"
STATE_FILE = WORKSPACE / "scripts/content-sources-state.json"
LOG_FILE = WORKSPACE / "logs/content-monitor.log"

# Get 笔记
GETNOTE_API_KEY = "gk_live_9ce62ca78af4c66a.4e084c6e4ae8579e96f59a2b2967ff3d020e0700ed0365c5"
GETNOTE_CLIENT_ID = "cli_a1b2c3d4e5f6789012345678abcdef90"

# RSSHub
RSSHUB_URL = "http://localhost:1200"

# ============ 工具函数 ============

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def safe_tags(tags):
    """标签截断到 <= 10 中文字符"""
    return [t[:10] for t in tags]

def save_to_getnote(title, content, tags, topic_id):
    """保存到 Get 笔记"""
    headers = {
        'Authorization': f'Bearer {GETNOTE_API_KEY}',
        'X-Client-ID': GETNOTE_CLIENT_ID,
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': title[:80],
        'content': content[:8000],  # 内容长度限制
        'tags': safe_tags(tags)
    }
    
    try:
        r = requests.post('https://openapi.biji.com/open/api/v1/resource/note/create',
                         headers=headers, json=data, timeout=30)
        res = r.json()
        if not res.get('success'):
            log(f"  ❌ 创建失败: {res}")
            return None
        
        note_id = res['data']['note_id']
        
        if topic_id:
            time.sleep(1.5)
            requests.post('https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add',
                         headers=headers,
                         json={'topic_id': topic_id, 'note_ids': [note_id]},
                         timeout=15)
        
        log(f"  ✅ 已存到 Get 笔记 (id={note_id})")
        return note_id
    except Exception as e:
        log(f"  ❌ 保存异常: {e}")
        return None

# ============ 知识星球 ============

def fetch_zsxq_topics(group_id, access_token):
    """获取知识星球最新主题"""
    url = f"https://api.zsxq.com/v2/groups/{group_id}/topics"
    params = {'scope': 'all', 'count': 20}
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get('resp_data', {}).get('topics', [])
        else:
            log(f"  ❌ 知识星球 API 返回 {r.status_code}")
            return []
    except Exception as e:
        log(f"  ❌ 知识星球请求异常: {e}")
        return []

def process_zsxq_topic(topic):
    """提取知识星球主题关键信息"""
    topic_id = str(topic.get('topic_id', ''))
    create_time = topic.get('create_time', '')
    
    # 提取内容
    talk = topic.get('talk', {})
    text = talk.get('text', '')
    author = talk.get('owner', {}).get('name', '未知')
    
    # 提取文章（如果有）
    article = talk.get('article', {})
    article_url = article.get('article_url', '')
    article_title = article.get('title', '')
    
    title = article_title if article_title else text[:50]
    
    return {
        'topic_id': topic_id,
        'title': title,
        'text': text[:2000],
        'author': author,
        'url': article_url,
        'create_time': create_time,
    }

def check_zsxq(source, state):
    """检查知识星球更新"""
    name = source['name']
    group_id = source['group_id']
    access_token = source.get('access_token', '')
    topic_id = source.get('topic_id', 'XyYvqPnN')
    
    if not access_token:
        log(f"  ⚠️ {name}: 未配置 access_token")
        return
    
    log(f"🔍 知识星球: {name}")
    
    topics = fetch_zsxq_topics(group_id, access_token)
    if not topics:
        log(f"  无新内容")
        return
    
    state_key = f"zsxq_{group_id}"
    seen = state.get(state_key, {}).get('seen_ids', [])
    
    # 首次运行：只标记
    if not seen:
        all_ids = [str(t.get('topic_id', '')) for t in topics]
        state[state_key] = {
            'name': name,
            'seen_ids': all_ids,
            'last_check': datetime.now().isoformat()
        }
        log(f"  📌 首次运行，标记 {len(all_ids)} 条历史主题")
        return
    
    new_count = 0
    for topic in topics:
        info = process_zsxq_topic(topic)
        if info['topic_id'] in seen:
            continue
        
        # 新主题
        new_count += 1
        full_title = f"🌐 知识星球 | {name} | {info['title']}"
        content = f"# {info['title']}\n\n"
        content += f"来源: {name}（知识星球）\n"
        content += f"作者: {info['author']}\n"
        content += f"日期: {info['create_time']}\n"
        if info['url']:
            content += f"链接: {info['url']}\n"
        content += f"\n---\n\n{info['text']}"
        
        tags = ['知识星球', name[:8]]
        save_to_getnote(full_title, content, tags, topic_id)
        time.sleep(2)
    
    # 更新状态
    all_ids = list(set(seen + [str(t.get('topic_id', '')) for t in topics]))
    state[state_key] = {
        'name': name,
        'seen_ids': all_ids,
        'last_check': datetime.now().isoformat()
    }
    
    if new_count:
        log(f"  🆕 {new_count} 条新内容")
    else:
        log(f"  ✅ 无新内容")

# ============ 微信公众号 ============

def check_wechat(source, state):
    """通过 RSSHub 检查微信公众号更新"""
    name = source['name']
    mp_id = source.get('mp_id', source.get('biz_id', ''))
    topic_id = source.get('topic_id', 'XyYvqPnN')
    
    if not mp_id:
        log(f"  ⚠️ {name}: 未配置 mp_id 或 biz_id")
        return
    
    log(f"🔍 微信公众号: {name}")
    
    # RSSHub 微信公众号路由
    feed_url = f"{RSSHUB_URL}/wechat/mp/{mp_id}"
    
    try:
        import feedparser
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            log(f"  ⚠️ 未获取到文章，可能需要配置 cookie")
            return
        
        state_key = f"wechat_{mp_id}"
        seen = state.get(state_key, {}).get('seen_ids', [])
        
        # 首次运行：只标记
        if not seen:
            all_ids = [e.get('id', '') for e in feed.entries]
            state[state_key] = {
                'name': name,
                'seen_ids': all_ids,
                'last_check': datetime.now().isoformat()
            }
            log(f"  📌 首次运行，标记 {len(all_ids)} 篇历史文章")
            return
        
        new_count = 0
        for entry in feed.entries:
            entry_id = entry.get('id', '')
            if entry_id in seen:
                continue
            
            new_count += 1
            title = entry.get('title', '无标题')
            link = entry.get('link', '')
            summary = entry.get('summary', '')[:2000]
            published = entry.get('published', '')
            
            full_title = f"📢 公众号 | {name} | {title}"
            content = f"# {title}\n\n"
            content += f"来源: {name}（微信公众号）\n"
            content += f"日期: {published}\n"
            content += f"链接: {link}\n"
            content += f"\n---\n\n{summary}"
            
            tags = ['公众号', name[:8]]
            save_to_getnote(full_title, content, tags, topic_id)
            time.sleep(2)
        
        # 更新状态
        all_ids = list(set(seen + [e.get('id', '') for e in feed.entries]))
        state[state_key] = {
            'name': name,
            'seen_ids': all_ids,
            'last_check': datetime.now().isoformat()
        }
        
        if new_count:
            log(f"  🆕 {new_count} 篇新文章")
        else:
            log(f"  ✅ 无新文章")
            
    except ImportError:
        # 没有feedparser，用XML解析
        log(f"  ⚠️ 需要 feedparser: pip install feedparser")
    except Exception as e:
        log(f"  ❌ 获取失败: {e}")

# ============ 通用 RSS ============

def check_rss(source, state):
    """检查通用 RSS 源"""
    name = source['name']
    url = source.get('url', source.get('rss_url', ''))
    topic_id = source.get('topic_id', 'XyYvqPnN')
    tag = source.get('tag', 'RSS')
    
    if not url:
        return
    
    log(f"🔍 RSS: {name}")
    
    try:
        import feedparser
        feed = feedparser.parse(url)
        
        if not feed.entries:
            log(f"  ⚠️ 未获取到内容")
            return
        
        state_key = f"rss_{hashlib.md5(url.encode()).hexdigest()[:12]}"
        seen = state.get(state_key, {}).get('seen_ids', [])
        
        if not seen:
            all_ids = [e.get('id', '') for e in feed.entries]
            state[state_key] = {
                'name': name,
                'seen_ids': all_ids,
                'last_check': datetime.now().isoformat()
            }
            log(f"  📌 首次运行，标记 {len(all_ids)} 条")
            return
        
        new_count = 0
        for entry in feed.entries[:10]:
            entry_id = entry.get('id', '')
            if entry_id in seen:
                continue
            
            new_count += 1
            title = entry.get('title', '无标题')
            link = entry.get('link', '')
            summary = entry.get('summary', '')[:2000]
            
            full_title = f"📡 {tag} | {name} | {title}"
            content = f"# {title}\n\n来源: {name}\n链接: {link}\n\n---\n\n{summary}"
            
            tags = [tag[:10], name[:8]]
            save_to_getnote(full_title, content, tags, topic_id)
            time.sleep(2)
        
        all_ids = list(set(seen + [e.get('id', '') for e in feed.entries]))
        state[state_key] = {
            'name': name,
            'seen_ids': all_ids,
            'last_check': datetime.now().isoformat()
        }
        
        if new_count:
            log(f"  🆕 {new_count} 条新内容")
        else:
            log(f"  ✅ 无新内容")
            
    except Exception as e:
        log(f"  ❌ 获取失败: {e}")

# ============ 主流程 ============

def main():
    config = load_json(CONFIG_FILE)
    state = load_json(STATE_FILE)
    
    if not config.get('sources'):
        log("⚠️ 未配置信息源")
        log(f"请编辑 {CONFIG_FILE}")
        return
    
    log(f"{'='*50}")
    log(f"📋 开始同步 {len(config['sources'])} 个信息源")
    log(f"{'='*50}")
    
    for source in config['sources']:
        source_type = source.get('type', '')
        
        if source_type == 'zsxq':
            check_zsxq(source, state)
        elif source_type == 'wechat':
            check_wechat(source, state)
        elif source_type == 'rss':
            check_rss(source, state)
        else:
            log(f"⚠️ 未知类型: {source_type}")
        
        time.sleep(3)
    
    save_json(STATE_FILE, state)
    log(f"{'='*50}")
    log(f"✅ 同步完成")

if __name__ == "__main__":
    main()
