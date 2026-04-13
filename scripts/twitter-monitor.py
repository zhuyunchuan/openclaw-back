#!/usr/bin/env python3
"""
Twitter/X 监控脚本
定时抓取指定账号的推文，每天总结保存到 Get 笔记

用法:
    python3 twitter-monitor.py test     # 测试模式
    python3 twitter-monitor.py run      # 运行模式（保存总结）
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from html import unescape

# 配置
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/scripts/twitter-config.json")
DEFAULT_ACCOUNTS = [
    {"handle": "GoogleGemini", "name": "Google Gemini"},
    {"handle": "OpenAI", "name": "OpenAI"},
    {"handle": "AnthropicAI", "name": "Claude (Anthropic)"},
    {"handle": "karpathy", "name": "Andrej Karpathy"},
    {"handle": "lennysan", "name": "Lenny"},
]

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"accounts": DEFAULT_ACCOUNTS, "last_checked": {}}

def save_config(config):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_twitter_tweets(handle, count=20):
    """
    获取 Twitter 账号推文
    使用 RSSHub 的 Twitter RSS（无需 API）
    """
    # RSSHub Twitter RSS
    url = f"https://rsshub.app/twitter/user/{handle}"
    
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
        print(f"❌ RSSHub 失败：{e}")
        return []

def parse_rss(rss_content, count=20):
    """解析 RSS 内容"""
    import re
    
    items = []
    
    # 提取 title
    title_match = re.search(r'<title>([^<]+)</title>', rss_content)
    feed_title = title_match.group(1) if title_match else "Unknown"
    
    # 提取 item
    item_pattern = r'<item>.*?<title>([^<]+)</title>.*?<link>([^<]+)</link>.*?<pubDate>([^<]+)</pubDate>.*?<description>(.*?)</description>.*?</item>'
    matches = re.findall(item_pattern, rss_content, re.DOTALL)
    
    for match in matches[:count]:
        title, link, pub_date, description = match
        
        # 清理 HTML
        description = re.sub(r'<[^>]+>', '', description)
        description = unescape(description)
        title = unescape(title)
        
        # 限制描述长度
        if len(description) > 500:
            description = description[:500] + "..."
        
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

def generate_daily_summary(tweets_by_account, date_str):
    """生成每日总结"""
    summary = f"# Twitter/X 每日监控总结\n\n"
    summary += f"📅 日期：{date_str}\n\n"
    summary += f"🔍 监控账号：{len(tweets_by_account)} 个\n\n"
    summary += "---\n\n"
    
    for account, tweets in tweets_by_account.items():
        if not tweets:
            continue
        
        summary += f"## {account}\n\n"
        summary += f"📊 今日推文：{len(tweets)} 条\n\n"
        
        for i, tweet in enumerate(tweets[:5], 1):  # 最多展示 5 条
            summary += f"### {i}. {tweet['title'][:100]}\n\n"
            summary += f"- 📅 {tweet['pub_date']}\n"
            summary += f"- 🔗 [查看原文]({tweet['link']})\n\n"
            if tweet['description']:
                summary += f"> {tweet['description'][:200]}...\n\n"
        
        summary += "---\n\n"
    
    return summary

def test_mode():
    """测试模式"""
    print("=" * 60)
    print("Twitter/X 监控 - 测试模式")
    print("=" * 60)
    
    config = load_config()
    accounts = config.get("accounts", DEFAULT_ACCOUNTS)
    
    print(f"\n📌 监控账号：{len(accounts)} 个")
    for acc in accounts:
        print(f"  - @{acc['handle']} ({acc['name']})")
    
    print(f"\n🔍 开始测试抓取...\n")
    
    for account in accounts:
        handle = account['handle']
        name = account['name']
        
        print(f"\n🐦 @{handle} ({name})")
        tweets = get_twitter_tweets(handle, count=3)
        
        if tweets:
            print(f"✅ 成功！获取到 {len(tweets)} 条推文")
            print("\n📄 最新推文:")
            for i, tweet in enumerate(tweets, 1):
                print(f"  {i}. {tweet['title'][:80]}...")
                print(f"     📅 {tweet['pub_date']}")
        else:
            print(f"❌ 未获取到推文，RSSHub 可能限流")
    
    print("\n" + "=" * 60)
    print("💡 下一步:")
    print("1. 确认能抓取到推文后，运行：python3 twitter-monitor.py run")
    print("2. 确保已配置 Get 笔记 API Key")
    print("3. 设置定时任务：crontab -e")
    print("   0 20 * * * cd /home/admin/.openclaw/workspace && python3 scripts/twitter-monitor.py run")
    print("=" * 60)

def run_mode():
    """运行模式 - 获取今日推文并生成总结"""
    print("=" * 60)
    print("Twitter/X 监控 - 运行模式")
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
    print(f"🔍 开始抓取推文...\n")
    
    tweets_by_account = {}
    today = datetime.now().strftime('%Y-%m-%d')
    
    for account in accounts:
        handle = account['handle']
        name = account['name']
        
        print(f"🐦 @{handle} ({name})...")
        tweets = get_twitter_tweets(handle, count=10)
        
        # 过滤今日推文
        today_tweets = []
        for tweet in tweets:
            # 解析日期
            try:
                tweet_date = datetime.strptime(tweet['pub_date'], '%a, %d %b %Y %H:%M:%S %Z')
                if tweet_date.strftime('%Y-%m-%d') == today:
                    today_tweets.append(tweet)
            except:
                # 如果解析失败，也加入
                today_tweets.append(tweet)
        
        tweets_by_account[name] = today_tweets
        print(f"  ✅ 今日推文：{len(today_tweets)} 条")
    
    # 生成总结
    if any(tweets_by_account.values()):
        print(f"\n📝 生成每日总结...")
        summary = generate_daily_summary(tweets_by_account, today)
        
        # 保存到 Get 笔记
        title = f"Twitter/X 每日监控总结 - {today}"
        if save_to_getnote(title, summary, api_key, client_id):
            print(f"\n✅ 总结已保存到 Get 笔记")
        else:
            print(f"\n❌ 保存失败")
    else:
        print(f"\n⚠️ 今日没有新推文或抓取失败")
    
    # 保存配置
    config["last_checked"] = {today: datetime.now().isoformat()}
    save_config(config)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 twitter-monitor.py [test|run]")
        print("  test - 测试模式（只抓取，不保存）")
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
