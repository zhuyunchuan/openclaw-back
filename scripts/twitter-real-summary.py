#!/usr/bin/env python3
"""
Twitter/X AI 动态真实总结脚本
使用 web_search 搜索各账号的最新动态和新闻

用法:
    python3 twitter-real-summary.py run      # 运行模式
"""

import os
import sys
import json
import urllib.request
from datetime import datetime

# 配置
DEFAULT_ACCOUNTS = [
    {"handle": "GoogleGemini", "name": "Google Gemini", "search": "Google Gemini AI announcement site:twitter.com"},
    {"handle": "OpenAI", "name": "OpenAI", "search": "OpenAI GPT release site:twitter.com"},
    {"handle": "AnthropicAI", "name": "Claude", "search": "Anthropic Claude update site:twitter.com"},
    {"handle": "karpathy", "name": "Andrej Karpathy", "search": "karpathy AI tweet site:twitter.com"},
    {"handle": "lennysan", "name": "Lenny", "search": "lennysan AI product site:twitter.com"},
]

def search_web(query, count=5):
    """
    使用 web_search 搜索
    需要配置 BRAVE_API_KEY 或使用 searxng
    """
    # 尝试使用 searxng
    import urllib.parse
    
    searxng_url = os.environ.get("SEARXNG_URL", "http://localhost:8080")
    encoded_query = urllib.parse.quote(query)
    url = f"{searxng_url}/search?q={encoded_query}&format=json"
    
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = []
            for result in data.get('results', [])[:count]:
                results.append({
                    "title": result.get('title', ''),
                    "url": result.get('url', ''),
                    "content": result.get('content', '')
                })
            return results
    except Exception as e:
        print(f"  searxng 失败：{e}")
        return []

def generate_real_summary(search_results_by_account, date_str):
    """生成真实内容的总结"""
    summary = f"# 🐦 Twitter/X AI 动态每日总结\n\n"
    summary += f"📅 日期：{date_str}\n\n"
    summary += f"**自动生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    summary += f"---\n\n"
    
    has_content = False
    
    for account_name, results in search_results_by_account.items():
        if not results:
            summary += f"## ❌ {account_name} - 暂无最新动态\n\n"
            continue
        
        has_content = True
        summary += f"## 🐦 {account_name} - {len(results)} 条相关动态\n\n"
        
        for i, result in enumerate(results, 1):
            summary += f"### {i}. {result['title']}\n\n"
            summary += f"- 🔗 [查看链接]({result['url']})\n\n"
            if result['content']:
                # 清理 HTML 标签
                import re
                content = re.sub(r'<[^>]+>', '', result['content'])
                if len(content) > 200:
                    content = content[:200] + "..."
                summary += f"> {content}\n\n"
        
        summary += f"---\n\n"
    
    if not has_content:
        summary += "⚠️ **提示**: 未能获取到最新推文内容。\n\n"
        summary += "**建议**:\n"
        summary += "1. 检查 searxng 服务是否运行\n"
        summary += "2. 手动访问 Twitter 查看\n"
        summary += "3. 看到好推文时对我说：`记一下 https://twitter.com/...`\n"
    
    return summary

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
                print(f"✅ 已保存到 Get 笔记")
                return True
    except Exception as e:
        print(f"❌ 保存失败：{e}")
    return False

def run_mode():
    """运行模式"""
    print("=" * 60)
    print("Twitter/X AI 动态 - 真实内容搜索")
    print("=" * 60)
    
    # 获取 Get 笔记配置
    openclaw_config = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(openclaw_config):
        with open(openclaw_config, 'r', encoding='utf-8') as f:
            oc_config = json.load(f)
            skill_config = oc_config.get("skills", {}).get("entries", {}).get("getnote", {})
            api_key = skill_config.get("apiKey")
            client_id = skill_config.get("env", {}).get("GETNOTE_CLIENT_ID")
    else:
        print("❌ 未找到配置文件")
        return
    
    if not api_key:
        print("❌ 未配置 Get 笔记 API Key")
        return
    
    print(f"\n🔍 开始搜索各账号最新动态...\n")
    
    search_results = {}
    today = datetime.now().strftime('%Y-%m-%d')
    
    for account in DEFAULT_ACCOUNTS:
        name = account['name']
        search = account['search']
        
        print(f"🐦 {name}...")
        results = search_web(search, count=3)
        search_results[name] = results
        print(f"  ✅ 找到 {len(results)} 条")
    
    # 生成总结
    print(f"\n📝 生成总结...")
    summary = generate_real_summary(search_results, today)
    
    # 保存
    title = f"🐦 Twitter/X AI 动态真实总结 - {today}"
    if save_to_getnote(title, summary, api_key, client_id):
        print(f"\n✅ 总结已保存到 Get 笔记")
    else:
        print(f"\n❌ 保存失败")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_mode()
