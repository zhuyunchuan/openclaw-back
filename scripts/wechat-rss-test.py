#!/usr/bin/env python3
"""
微信公众号 RSS 抓取测试脚本
测试"路飞的船长日志"公众号文章抓取
"""

import feedparser
import json
from datetime import datetime

# 尝试多个 RSS 源
RSS_SOURCES = [
    "https://rsshub.app/wechat/mp/gh_8c8b8c8b8c8b",  # RSSHub (需要 gh_ ID)
    "https://feeds.feeddd.org/api/mp/路飞的船长日志",  # feeddd
    "https://mp.weixin.qq.com/mp/profile_engine",  # 官方 (需要 cookie)
]

def test_rss_source(url):
    """测试 RSS 源"""
    print(f"\n🔍 测试源：{url}")
    try:
        feed = feedparser.parse(url, timeout=10)
        if feed.entries:
            print(f"✅ 成功！找到 {len(feed.entries)} 篇文章")
            print(f"📌 公众号：{feed.feed.get('title', 'Unknown')}")
            print("\n📄 最新文章:")
            for i, entry in enumerate(feed.entries[:3], 1):
                print(f"  {i}. {entry.title}")
                print(f"     📅 {entry.get('published', 'Unknown')}")
                print(f"     🔗 {entry.link}")
                print()
            return True
        else:
            print(f"❌ 无文章")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def main():
    print("=" * 60)
    print("微信公众号 RSS 抓取测试")
    print("目标：路飞的船长日志")
    print("=" * 60)
    
    # 需要先获取公众号的 gh_ ID
    print("\n⚠️  需要先获取公众号的 gh_ ID")
    print("方法：")
    print("1. 打开微信公众号文章")
    print("2. 查看 URL 中的 __biz 参数")
    print("3. 或使用工具查询")
    
    # 尝试搜索公众号
    print("\n🔍 尝试搜索公众号...")
    try:
        import requests
        resp = requests.get(
            "https://api.github.com/search/code",
            params={"q": "路飞的船长日志 公众号"},
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            print(f"GitHub 搜索结果：{data.get('total_count', 0)}")
    except:
        pass
    
    print("\n💡 建议方案:")
    print("1. 使用 wewe-rss (https://github.com/cooderl/wewe-rss)")
    print("2. 使用 feeddd (https://github.com/feeddd/feeds)")
    print("3. 手动提供公众号 gh_ ID")

if __name__ == "__main__":
    main()
