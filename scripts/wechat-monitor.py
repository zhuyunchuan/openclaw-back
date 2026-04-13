#!/usr/bin/env python3
"""
微信公众号监控脚本
定时抓取指定公众号文章，自动保存到 Get 笔记

用法:
    python3 wechat-monitor.py test     # 测试模式
    python3 wechat-monitor.py run      # 运行模式（保存笔记）
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# 配置
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/scripts/wechat-config.json")
DEFAULT_ACCOUNTS = ["路飞的船长日志"]

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"accounts": DEFAULT_ACCOUNTS, "last_checked": {}}

def save_config(config):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_wechat_articles(account_name, biz_id=None):
    """
    获取微信公众号文章
    
    参数:
        account_name: 公众号名称
        biz_id: 公众号 gh_ ID（可选，如 MzA4MTQ3MjQwMg==）
    """
    import urllib.parse
    
    # 如果提供了 biz_id，优先使用
    if biz_id:
        # 使用 RSSHub 的 gh_ ID 方式
        url = f"https://rsshub.app/wechat/mp/{biz_id}"
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if isinstance(data, dict) and "items" in data:
                    return data["items"]
        except Exception as e:
            print(f"RSSHub (biz_id) 失败：{e}")
    
    # URL 编码中文公众号名
    encoded_name = urllib.parse.quote(account_name)
    
    # 尝试多个 RSS 源
    sources = [
        f"https://feeds.feeddd.org/api/mp/{encoded_name}",
        f"https://rsshub.app/wechat/mp/{encoded_name}",
        f"https://wewe-rss.vercel.app/api/mp/{encoded_name}",
    ]
    
    for url in sources:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if isinstance(data, dict) and "items" in data:
                    return data["items"]
                elif isinstance(data, list):
                    return data
        except Exception as e:
            print(f"源 {url} 失败：{e}")
            continue
    
    return []

def save_to_getnote(title, link, api_key, client_id):
    """保存文章到 Get 笔记"""
    url = "https://openapi.biji.com/open/api/v1/resource/note/save"
    
    payload = json.dumps({
        "type": "link",
        "title": title,
        "link_url": link
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

def test_mode():
    """测试模式"""
    print("=" * 60)
    print("微信公众号监控 - 测试模式")
    print("=" * 60)
    
    config = load_config()
    accounts = config.get("accounts", DEFAULT_ACCOUNTS)
    
    print(f"\n📌 监控公众号：{accounts}")
    print(f"🔍 开始测试抓取...\n")
    
    for account in accounts:
        print(f"\n📖 公众号：{account}")
        articles = get_wechat_articles(account)
        
        if articles:
            print(f"✅ 成功！找到 {len(articles)} 篇文章")
            print("\n📄 最新 3 篇:")
            for i, article in enumerate(articles[:3], 1):
                title = article.get('title', '无标题')
                link = article.get('link', '')
                date = article.get('date_published', article.get('pubDate', 'Unknown'))
                print(f"  {i}. {title}")
                print(f"     📅 {date}")
                print(f"     🔗 {link}")
        else:
            print(f"❌ 未找到文章，可能需要检查公众号名称或更换 RSS 源")
    
    print("\n" + "=" * 60)
    print("💡 下一步:")
    print("1. 确认能抓取到文章后，运行：python3 wechat-monitor.py run")
    print("2. 确保已配置 Get 笔记 API Key")
    print("3. 设置定时任务：crontab -e")
    print("   0 */2 * * * cd /home/admin/.openclaw/workspace && python3 scripts/wechat-monitor.py run")
    print("=" * 60)

def run_mode():
    """运行模式 - 检查新文章并保存"""
    print("=" * 60)
    print("微信公众号监控 - 运行模式")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    accounts = config.get("accounts", DEFAULT_ACCOUNTS)
    last_checked = config.get("last_checked", {})
    
    # 获取 Get 笔记配置
    openclaw_config = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(openclaw_config):
        with open(openclaw_config, 'r') as f:
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
    
    print(f"\n📌 监控公众号：{accounts}")
    print(f"🔍 开始检查新文章...\n")
    
    new_articles = []
    
    for account in accounts:
        print(f"\n📖 公众号：{account}")
        articles = get_wechat_articles(account)
        
        if not articles:
            print(f"  ⚠️ 无法获取文章")
            continue
        
        # 获取上次检查时间
        last_time = last_checked.get(account, "")
        print(f"  上次检查：{last_time or '首次运行'}")
        
        # 检查新文章
        for article in articles:
            article_link = article.get('link', '')
            article_date = article.get('date_published', article.get('pubDate', ''))
            
            # 如果是新文章（在上次检查之后）
            if last_time and article_date and article_date <= last_time:
                break
            
            new_articles.append({
                "account": account,
                "title": article.get('title', '无标题'),
                "link": article_link,
                "date": article_date
            })
        
        # 更新最后检查时间
        if articles:
            last_checked[account] = articles[0].get('date_published', articles[0].get('pubDate', ''))
    
    # 保存新文章到 Get 笔记
    if new_articles:
        print(f"\n🎉 发现 {len(new_articles)} 篇新文章")
        saved_count = 0
        for article in new_articles:
            title = f"[{article['account']}] {article['title']}"
            if save_to_getnote(title, article['link'], api_key, client_id):
                saved_count += 1
        
        print(f"\n✅ 成功保存 {saved_count}/{len(new_articles)} 篇")
    else:
        print(f"\n✅ 没有新文章")
    
    # 保存配置
    config["last_checked"] = last_checked
    save_config(config)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 wechat-monitor.py [test|run]")
        print("  test - 测试模式（只抓取，不保存）")
        print("  run  - 运行模式（检查并保存新文章）")
        sys.exit(1)
    
    mode = sys.argv[1]
    if mode == "test":
        test_mode()
    elif mode == "run":
        run_mode()
    else:
        print("未知模式，请使用 test 或 run")
        sys.exit(1)
