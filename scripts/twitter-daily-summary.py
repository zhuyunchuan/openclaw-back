#!/usr/bin/env python3
"""
Twitter/X 每日总结脚本
搜索指定账号的最新动态，生成总结保存到 Get 笔记

用法:
    python3 twitter-daily-summary.py test     # 测试模式
    python3 twitter-daily-summary.py run      # 运行模式
"""

import os
import sys
import json
import urllib.request
from datetime import datetime

# 配置
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/scripts/twitter-summary-config.json")
DEFAULT_ACCOUNTS = [
    {"handle": "GoogleGemini", "name": "Google Gemini", "search": "from:GoogleGemini"},
    {"handle": "OpenAI", "name": "OpenAI", "search": "from:OpenAI"},
    {"handle": "AnthropicAI", "name": "Claude (Anthropic)", "search": "from:AnthropicAI"},
    {"handle": "karpathy", "name": "Andrej Karpathy", "search": "from:karpathy"},
    {"handle": "lennysan", "name": "Lenny", "search": "from:lennysan"},
]

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"accounts": DEFAULT_ACCOUNTS, "last_run": None}

def save_config(config):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_twitter_search_results(search_query, count=5):
    """
    搜索 Twitter 内容
    使用 RSSHub 的 Twitter 搜索 RSS
    """
    import urllib.parse
    
    # RSSHub Twitter Search RSS
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://rsshub.app/twitter/search/{encoded_query}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/rss+xml,application/xml"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            rss_content = resp.read().decode('utf-8')
            return parse_rss(rss_content, count)
    except Exception as e:
        print(f"  ❌ RSSHub 搜索失败：{e}")
        return []

def parse_rss(rss_content, count=5):
    """解析 RSS 内容"""
    import re
    from html import unescape
    
    items = []
    
    # 提取 item
    item_pattern = r'<item>.*?<title>([^<]+)</title>.*?<link>([^<]+)</link>.*?<pubDate>([^<]+)</pubDate>.*?<description>(.*?)</description>.*?</item>'
    matches = re.findall(item_pattern, rss_content, re.DOTALL)
    
    for match in matches[:count]:
        title, link, pub_date, description = match
        
        # 清理 HTML
        description = re.sub(r'<[^>]+>', '', description)
        description = unescape(description)
        title = unescape(title)
        
        # 限制长度
        if len(description) > 300:
            description = description[:300] + "..."
        
        items.append({
            "title": title,
            "link": link,
            "pub_date": pub_date,
            "description": description.strip()
        })
    
    return items

def save_to_getnote(title, content, api_key, client_id):
    """保存总结到 Get 笔记"""
    url = "https://openapi.biji.com/open/api/v1/resource/note/save"
    
    payload = json.dumps({
        "type": "text",
        "title": title,
        "content": content
    }).encode('utf-8')
    
    headers = {
        "Authorization": api_key,
        "X-Client-ID": client_id,
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("success"):
                print(f"✅ 已保存到 Get 笔记：{title}")
                return True
            else:
                print(f"❌ 保存失败：{data.get('error', {})}")
                return False
    except Exception as e:
        print(f"❌ 保存异常：{e}")
        return False

def generate_summary(results_by_account, date_str):
    """生成每日总结"""
    summary = f"# 🐦 Twitter/X AI 动态每日总结\n\n"
    summary += f"📅 日期：{date_str}\n\n"
    summary += f"🔍 监控账号：{len(results_by_account)} 个\n\n"
    summary += f"**监控列表**: "
    summary += ", ".join([f"@{acc['handle']}" for acc in DEFAULT_ACCOUNTS])
    summary += "\n\n---\n\n"
    
    has_content = False
    for account, tweets in results_by_account.items():
        if not tweets:
            summary += f"## ❌ @{account} - 今日无更新\n\n"
            continue
        
        has_content = True
        summary += f"## 🐦 @{account} - {len(tweets)} 条动态\n\n"
        
        for i, tweet in enumerate(tweets, 1):
            summary += f"### {i}. {tweet['title']}\n\n"
            summary += f"- 📅 {tweet['pub_date']}\n"
            summary += f"- 🔗 [查看原文]({tweet['link']})\n\n"
            if tweet['description']:
                # 清理描述中的多余内容
                desc = tweet['description'].split('pic.twitter.com')[0].strip()
                if desc:
                    summary += f"> {desc}\n\n"
        
        summary += "---\n\n"
    
    if not has_content:
        summary += "⚠️ **注意**: 今日所有账号均无新动态，或 RSSHub 服务暂时不可用。\n\n"
        summary += "建议:\n"
        summary += "1. 稍后重试\n"
        summary += "2. 直接访问 Twitter 查看\n"
        summary += "3. 检查 RSSHub 服务状态\n"
    
    summary += f"\n---\n\n"
    summary += f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return summary

def test_mode():
    """测试模式"""
    print("=" * 60)
    print("Twitter/X 每日总结 - 测试模式")
    print("=" * 60)
    
    config = load_config()
    accounts = config.get("accounts", DEFAULT_ACCOUNTS)
    
    print(f"\n📌 监控账号：{len(accounts)} 个\n")
    for acc in accounts:
        print(f"  - @{acc['handle']} → {acc['name']}")
    
    print(f"\n🔍 开始测试搜索...\n")
    
    for account in accounts:
        handle = account['handle']
        name = account['name']
        search = account['search']
        
        print(f"🐦 @{handle} ({name})")
        print(f"   搜索：{search}")
        
        tweets = get_twitter_search_results(search, count=2)
        
        if tweets:
            print(f"   ✅ 成功！获取到 {len(tweets)} 条推文")
            for i, tweet in enumerate(tweets, 1):
                print(f"   {i}. {tweet['title'][:60]}...")
        else:
            print(f"   ❌ 未获取到推文")
        print()
    
    print("=" * 60)
    print("💡 下一步:")
    print("1. 确认能抓取到推文后，运行：python3 twitter-daily-summary.py run")
    print("2. 设置定时任务（每天 20:00 生成总结）:")
    print("   crontab -e")
    print("   0 20 * * * cd /home/admin/.openclaw/workspace && python3 scripts/twitter-daily-summary.py run")
    print("=" * 60)

def run_mode():
    """运行模式 - 生成每日总结"""
    print("=" * 60)
    print("Twitter/X 每日总结 - 运行模式")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    accounts = config.get("accounts", DEFAULT_ACCOUNTS)
    
    # 获取 Get 笔记配置
    openclaw_config = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(openclaw_config):
        with open(openclaw_config, 'r', encoding='utf-8') as f:
            oc_config = json.load(f)
            skill_config = oc_config.get("skills", {}).get("entries", {}).get("getnote", {})
            api_key = skill_config.get("apiKey")
            client_id = skill_config.get("env", {}).get("GETNOTE_CLIENT_ID")
    else:
        print("❌ 未找到 OpenClaw 配置文件")
        return
    
    if not api_key:
        print("❌ 未配置 Get 笔记 API Key")
        return
    
    print(f"\n📌 监控账号：{len(accounts)} 个")
    print(f"🔍 开始搜索推文...\n")
    
    results_by_account = {}
    today = datetime.now().strftime('%Y-%m-%d')
    
    for account in accounts:
        handle = account['handle']
        name = account['name']
        search = account['search']
        
        print(f"🐦 @{handle}...")
        tweets = get_twitter_search_results(search, count=5)
        results_by_account[handle] = tweets
        print(f"  ✅ 获取到 {len(tweets)} 条")
    
    # 生成总结
    print(f"\n📝 生成总结...")
    summary = generate_summary(results_by_account, today)
    
    # 保存到 Get 笔记
    title = f"🐦 Twitter/X AI 动态每日总结 - {today}"
    if save_to_getnote(title, summary, api_key, client_id):
        print(f"\n✅ 总结已保存到 Get 笔记")
    else:
        print(f"\n❌ 保存失败")
    
    # 保存配置
    config["last_run"] = datetime.now().isoformat()
    save_config(config)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 twitter-daily-summary.py [test|run]")
        print("  test - 测试模式")
        print("  run  - 运行模式（生成总结并保存）")
        sys.exit(1)
    
    mode = sys.argv[1]
    if mode == "test":
        test_mode()
    elif mode == "run":
        run_mode()
    else:
        print("未知模式，请使用 test 或 run")
        sys.exit(1)
