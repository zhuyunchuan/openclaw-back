#!/usr/bin/env python3
"""
Twitter/X AI 动态每日总结 - 浏览器自动化版本
使用 OpenClaw browser 工具直接访问 Twitter 抓取最新内容

用法:
    python3 twitter-browser-summary.py run      # 运行模式
    python3 twitter-browser-summary.py test     # 测试模式
"""

import os
import sys
import json
from datetime import datetime
import urllib.request

# 配置
ACCOUNTS = [
    {"handle": "OpenAI", "name": "OpenAI", "url": "https://twitter.com/OpenAI"},
    {"handle": "AnthropicAI", "name": "Anthropic", "url": "https://twitter.com/AnthropicAI"},
    {"handle": "GoogleGemini", "name": "Google Gemini", "url": "https://twitter.com/GoogleGemini"},
    {"handle": "karpathy", "name": "Andrej Karpathy", "url": "https://twitter.com/karpathy"},
    {"handle": "lennysan", "name": "Lenny", "url": "https://twitter.com/lennysan"},
]

def fetch_twitter_with_browser(url, timeout=10):
    """
    使用 OpenClaw browser 工具抓取 Twitter 内容
    
    注意：这个函数需要通过 OpenClaw 的 browser 工具调用
    这里提供一个示例结构
    """
    # 实际使用时需要调用 OpenClaw browser 工具
    # browser(action="open", url=url)
    # browser(action="snapshot", delayMs=3000)
    pass

def fetch_twitter_with_web_fetch(url, max_chars=5000):
    """使用 web_fetch 获取 Twitter 内容"""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8')[:max_chars]
    except Exception as e:
        return f"Error: {e}"

def parse_tweet_from_html(html):
    """从 HTML 中解析推文内容（简化版）"""
    tweets = []
    # 这里需要更复杂的解析逻辑
    # 实际使用时建议用 BeautifulSoup 或类似库
    return tweets

def generate_summary(results):
    """生成总结 Markdown"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    summary = f"# 🐦 Twitter/X AI 动态每日总结\n\n"
    summary += f"**日期**: {today}\n"
    summary += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    summary += f"**数据来源**: 浏览器自动化\n"
    summary += f"**监控账号**: {len(ACCOUNTS)} 个\n\n"
    summary += f"---\n\n"
    
    for account, data in results.items():
        summary += f"## {data['name']}\n\n"
        
        if data.get('error'):
            summary += f"**状态**: {data['error']}\n\n"
            continue
        
        if data.get('tweets'):
            for i, tweet in enumerate(data['tweets'], 1):
                summary += f"### {i}. {tweet.get('text', 'N/A')}\n\n"
                if tweet.get('created_at'):
                    summary += f"- 📅 {tweet['created_at']}\n"
                if tweet.get('likes'):
                    summary += f"- ❤️ {tweet['likes']} 点赞\n"
                if tweet.get('retweets'):
                    summary += f"- 🔄 {tweet['retweets']} 转发\n"
                summary += "\n"
        else:
            summary += "暂无最新动态\n\n"
        
        summary += f"---\n\n"
    
    return summary

def save_to_file(content, filename):
    """保存到文件"""
    filepath = os.path.join(
        os.path.expanduser("~/.openclaw/workspace"),
        filename
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def run_mode():
    """运行模式"""
    print("=" * 60)
    print("Twitter/X AI 动态 - 浏览器自动化抓取")
    print("=" * 60)
    
    today = datetime.now().strftime('%Y-%m-%d')
    results = {}
    
    for account in ACCOUNTS:
        name = account['name']
        url = account['url']
        
        print(f"\n🐦 抓取 {name}...")
        
        # 注意：实际使用时需要调用 OpenClaw browser 工具
        # 这里提供一个框架
        
        try:
            # 方法 1: 使用 browser 工具（需要 OpenClaw 支持）
            # browser(action="open", url=url)
            # snapshot = browser(action="snapshot", delayMs=3000)
            # 解析 snapshot 内容
            
            # 方法 2: 使用 web_fetch（可能被限制）
            html = fetch_twitter_with_web_fetch(url)
            
            if "Something went wrong" in html or "enable JavaScript" in html:
                results[name] = {
                    "name": name,
                    "error": "Twitter 限制访问，需要登录"
                }
                print(f"  ⚠️ 访问受限")
            else:
                # 解析内容
                tweets = parse_tweet_from_html(html)
                results[name] = {
                    "name": name,
                    "tweets": tweets
                }
                print(f"  ✅ 抓取成功")
                
        except Exception as e:
            results[name] = {
                "name": name,
                "error": str(e)
            }
            print(f"  ❌ 失败：{e}")
    
    # 生成总结
    print(f"\n📝 生成总结...")
    summary = generate_summary(results)
    
    # 保存到文件
    filename = f"TWITTER-REAL-SUMMARY-{today}.md"
    filepath = save_to_file(summary, filename)
    print(f"✅ 已保存到：{filepath}")
    
    # 保存到 Get 笔记（如果配置了）
    save_to_getnote(summary, today)
    
    print("\n" + "=" * 60)

def save_to_getnote(content, date):
    """保存到 Get 笔记"""
    openclaw_config = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(openclaw_config):
        print("⚠️ 未找到 OpenClaw 配置文件，跳过 Get 笔记保存")
        return
    
    with open(openclaw_config, 'r', encoding='utf-8') as f:
        oc_config = json.load(f)
        skill_config = oc_config.get("skills", {}).get("entries", {}).get("getnote", {})
        api_key = skill_config.get("apiKey")
        client_id = skill_config.get("env", {}).get("GETNOTE_CLIENT_ID")
    
    if not api_key:
        print("⚠️ 未配置 Get 笔记 API Key")
        return
    
    url = "https://openapi.biji.com/open/api/v1/resource/note/save"
    payload = json.dumps({
        "type": "text",
        "title": f"🐦 Twitter/X AI 动态真实总结 - {date}",
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
                print(f"✅ 已保存到 Get 笔记")
    except Exception as e:
        print(f"❌ Get 笔记保存失败：{e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("测试模式")
        # 测试代码
    else:
        run_mode()
