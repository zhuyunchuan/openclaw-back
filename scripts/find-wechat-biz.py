#!/usr/bin/env python3
"""
搜索微信公众号的 gh_ ID (__biz 参数)
"""

import urllib.request
import urllib.parse
import re
import json

def search_wechat_account(account_name):
    """搜索公众号"""
    print(f"\n🔍 搜索公众号：{account_name}")
    
    # 尝试从 GitHub 搜索
    encoded = urllib.parse.quote(account_name)
    urls = [
        f"https://api.github.com/search/code?q={encoded}+公众号",
        f"https://api.github.com/search/repositories?q={encoded}+wechat",
    ]
    
    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "Mozilla/5.0"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if 'items' in data and data['items']:
                    print(f"✅ GitHub 找到 {len(data['items'])} 个结果")
                    for item in data['items'][:3]:
                        print(f"  - {item.get('name', '')}: {item.get('html_url', '')}")
        except Exception as e:
            print(f"GitHub 搜索失败：{e}")
    
    # 尝试从微信读书搜索
    print(f"\n📖 尝试微信读书搜索...")
    try:
        # wewe-rss 使用微信读书 API
        url = f"https://weread.qq.com/web/search/books?keyword={encoded}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data:
                print(f"✅ 微信读书找到 {len(data)} 个结果")
                for book in data[:3]:
                    title = book.get('title', '')
                    author = book.get('author', '')
                    print(f"  - {title} by {author}")
    except Exception as e:
        print(f"微信读书搜索失败：{e}")
    
    print("\n💡 获取 gh_ ID 的最佳方法:")
    print("1. 打开微信公众号任意文章")
    print("2. 复制链接")
    print("3. 找到 __biz= 后面的值")
    print("4. 格式如：MzA4MTQ3MjQwMg==")
    print("\n或者在微信中:")
    print("1. 进入公众号主页")
    print("2. 点击右上角 ...")
    print("3. 查看公众号信息")

if __name__ == "__main__":
    account = "路飞的船长日志"
    if len(__import__('sys').argv) > 1:
        account = __import__('sys').argv[1]
    
    search_wechat_account(account)
