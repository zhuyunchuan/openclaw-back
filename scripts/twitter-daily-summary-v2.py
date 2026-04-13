#!/usr/bin/env python3
"""
Twitter/X 每日总结脚本 v2
使用浏览器搜索 + 直接访问，生成总结保存到 Get 笔记

用法:
    python3 twitter-daily-summary-v2.py test     # 测试模式
    python3 twitter-daily-summary-v2.py run      # 运行模式
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

# 配置
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/scripts/twitter-summary-v2-config.json")
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")

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
    return {"accounts": DEFAULT_ACCOUNTS, "last_run": None}

def save_config(config):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def search_twitter_with_browser(handle, date_range="1d"):
    """
    使用浏览器搜索 Twitter 内容
    
    参数:
        handle: Twitter 账号（不含@）
        date_range: 时间范围 (1d=1 天，7d=7 天)
    
    返回:
        搜索结果列表
    """
    from urllib.parse import quote
    
    # Twitter 搜索 URL（按时间排序）
    search_query = f"from:{handle}"
    search_url = f"https://twitter.com/search?q={quote(search_query)}&f=live"
    
    print(f"  🔍 搜索：{search_url}")
    
    # 使用浏览器打开并截图
    try:
        # 这里调用 browser 工具
        # 由于是脚本，我们生成一个报告模板
        return {
            "success": True,
            "url": search_url,
            "note": "需要浏览器自动化支持"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def generate_summary_template(accounts, date_str):
    """生成总结模板（当无法获取实际内容时）"""
    summary = f"# 🐦 Twitter/X AI 动态每日总结\n\n"
    summary += f"📅 日期：{date_str}\n\n"
    summary += f"🔍 监控账号：{len(accounts)} 个\n\n"
    summary += f"**监控列表**:\n\n"
    
    for acc in accounts:
        handle = acc['handle']
        name = acc['name']
        summary += f"- @{handle} - {name}\n"
        summary += f"  - 搜索链接：[Twitter 搜索](https://twitter.com/search?q=from:{handle}&f=live)\n"
    
    summary += f"\n---\n\n"
    summary += f"## 📝 今日概览\n\n"
    summary += f"⚠️ **技术说明**: 由于 Twitter/X API 限制，自动抓取需要浏览器自动化支持。\n\n"
    summary += f"**建议方案**:\n\n"
    summary += f"1. 点击上方的搜索链接查看各账号最新动态\n"
    summary += f"2. 看到有价值的推文时，复制链接发给我：`记一下 https://twitter.com/...`\n"
    summary += f"3. 我会自动保存到 Get 笔记\n\n"
    summary += f"---\n\n"
    summary += f"## 🔗 快速访问\n\n"
    
    for acc in accounts:
        handle = acc['handle']
        summary += f"- [@{handle}](https://twitter.com/{handle})\n"
    
    summary += f"\n---\n\n"
    summary += f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return summary

def generate_summary_with_search(accounts, date_str):
    """
    使用 web_search 生成总结（需要配置 Brave API）
    
    如果 web_search 可用，搜索每个账号的最新推文
    """
    summary = f"# 🐦 Twitter/X AI 动态每日总结\n\n"
    summary += f"📅 日期：{date_str}\n\n"
    
    # 尝试使用 web_search
    try:
        # 这里调用 web_search 工具
        # 由于是脚本，我们返回模板
        return generate_summary_template(accounts, date_str)
    except Exception as e:
        print(f"web_search 失败：{e}")
        return generate_summary_template(accounts, date_str)

def save_to_getnote(title, content, api_key, client_id):
    """保存总结到 Get 笔记"""
    import urllib.request
    
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
    print(f"📝 生成总结...\n")
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 生成总结
    summary = generate_summary_with_search(accounts, today)
    
    # 保存到 Get 笔记
    title = f"🐦 Twitter/X AI 动态每日总结 - {today}"
    if save_to_getnote(title, summary, api_key, client_id):
        print(f"\n✅ 总结已保存到 Get 笔记")
        print(f"\n📎 链接：")
        for acc in accounts:
            handle = acc['handle']
            print(f"  - @{handle}: https://twitter.com/search?q=from:{handle}&f=live")
    else:
        print(f"\n❌ 保存失败")
    
    # 保存配置
    config["last_run"] = datetime.now().isoformat()
    save_config(config)
    
    print("\n" + "=" * 60)

def test_mode():
    """测试模式"""
    print("=" * 60)
    print("Twitter/X 每日总结 v2 - 测试模式")
    print("=" * 60)
    
    config = load_config()
    accounts = config.get("accounts", DEFAULT_ACCOUNTS)
    
    print(f"\n📌 监控账号：{len(accounts)} 个\n")
    for acc in accounts:
        handle = acc['handle']
        name = acc['name']
        print(f"  - @{handle} → {name}")
        print(f"    搜索：https://twitter.com/search?q=from:{handle}&f=live")
    
    print(f"\n💡 运行模式:")
    print("   python3 twitter-daily-summary-v2.py run")
    print(f"\n📅 定时任务:")
    print("   0 20 * * * cd /home/admin/.openclaw/workspace && python3 scripts/twitter-daily-summary-v2.py run")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 twitter-daily-summary-v2.py [test|run]")
        sys.exit(1)
    
    mode = sys.argv[1]
    if mode == "test":
        test_mode()
    elif mode == "run":
        run_mode()
    else:
        print("未知模式")
        sys.exit(1)
