#!/usr/bin/env python3
# filename: /home/admin/.openclaw/workspace/scripts/xhs-monitor.py
# description: 小红书账号监控脚本 - 定时检查更新并保存到 Get 笔记

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# ============ 配置区域 ============

# XHS-Downloader API 地址
XHS_API_URL = "http://127.0.0.1:5556"

# 要监控的小红书账号列表
# 格式：{"user_id": "小红书用户 ID", "name": "账号名称", "last_check": "上次检查时间"}
MONITOR_USERS = [
    # 示例（请替换为实际要监控的账号）：
    # {"user_id": "5f3b4e5d6c7a8b9c0d1e2f3a", "name": "AI 科技前沿"},
    # {"user_id": "6a7b8c9d0e1f2a3b4c5d6e7f", "name": "产品思维笔记"},
]

# 输出目录
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/xhs-monitor/outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Get 笔记配置
GETNOTE_API_KEY = os.getenv('GETNOTE_API_KEY', 'gk_live_9ce62ca78af4c66a.4e084c6e4ae8579e96f59a2b2967ff3d020e0700ed0365c5')
GETNOTE_CLIENT_ID = os.getenv('GETNOTE_CLIENT_ID', 'cli_a1b2c3d4e5f6789012345678abcdef90')
GETNOTE_TOPIC_ID = "oYpEp190"  # Ai &具身智能知识库

# ============ 核心函数 ============

def get_user_posts(user_id):
    """获取用户作品列表"""
    try:
        response = requests.post(
            f"{XHS_API_URL}/xhs/user",
            json={"user_id": user_id},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {})
        else:
            print(f"❌ API 请求失败：{response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ 获取用户作品失败：{e}")
        return None

def get_post_detail(post_url):
    """获取作品详情"""
    try:
        response = requests.post(
            f"{XHS_API_URL}/xhs/detail",
            json={"url": post_url},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {})
        else:
            print(f"❌ API 请求失败：{response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ 获取作品详情失败：{e}")
        return None

def save_posts_to_file(posts, user_name):
    """保存作品到本地文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"xhs_{user_name}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存到：{filename}")
    return filename

def generate_markdown_report(posts, user_name):
    """生成 Markdown 格式的监控报告"""
    md = f"# 📱 小红书账号监控报告\n\n"
    md += f"**账号**: {user_name}\n"
    md += f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"**作品数量**: {len(posts)}\n\n"
    md += "---\n\n"
    
    # 作品列表
    for i, post in enumerate(posts[:10], 1):  # 最多展示 10 个
        md += f"## {i}. {post.get('title', '无标题')}\n\n"
        
        # 基本信息
        md += f"- 📅 发布时间：{post.get('time', '未知')}\n"
        md += f"- 👍 点赞：{post.get('liked_count', '0')}\n"
        md += f"- ⭐ 收藏：{post.get('collected_count', '0')}\n"
        md += f"- 💬 评论：{post.get('comment_count', '0')}\n"
        
        # 描述
        if post.get('desc'):
            md += f"\n**描述**: {post['desc'][:200]}...\n"
        
        # 链接
        if post.get('url'):
            md += f"\n🔗 [阅读原文]({post['url']})\n"
        
        md += "\n---\n\n"
    
    return md

def upload_to_getnote(md_content, user_name):
    """上传到 Get 笔记"""
    try:
        headers = {
            'Authorization': GETNOTE_API_KEY,
            'X-Client-ID': GETNOTE_CLIENT_ID,
            'Content-Type': 'application/json'
        }
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        data = {
            'title': f'📱 小红书监控 - {user_name} - {timestamp}',
            'content': md_content,
            'note_type': 'plain_text',
            'tags': ['小红书', '监控报告', user_name]
        }
        
        response = requests.post(
            'https://openapi.biji.com/open/api/v1/resource/note/save',
            headers=headers,
            json=data
        )
        
        result = response.json()
        
        if result.get('success'):
            note_id = result['data']['note_id']
            print(f"✅ 已上传到 Get 笔记：{note_id}")
            
            # 添加到知识库
            try:
                add_response = requests.post(
                    'https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add',
                    headers=headers,
                    json={'topic_id': GETNOTE_TOPIC_ID, 'note_ids': [note_id]}
                )
                
                if add_response.json().get('success'):
                    print(f"✅ 已添加到 Ai &具身智能知识库")
            
            except Exception as e:
                print(f"⚠️ 添加到知识库失败：{e}")
            
            return note_id
        else:
            print(f"❌ 上传到 Get 笔记失败：{result}")
            return None
    
    except Exception as e:
        print(f"❌ 上传过程出错：{e}")
        return None

def check_updates(user_id, last_check_time=None):
    """检查用户是否有新作品"""
    posts_data = get_user_posts(user_id)
    
    if not posts_data:
        return []
    
    posts = posts_data.get('posts', [])
    
    if not last_check_time:
        # 首次检查，返回最新 5 个作品
        return posts[:5]
    
    # 检查是否有新作品（比较发布时间）
    new_posts = []
    for post in posts:
        post_time = post.get('time', '')
        if post_time and post_time > last_check_time:
            new_posts.append(post)
    
    return new_posts

# ============ 主流程 ============

def main():
    """主函数"""
    print("=" * 60)
    print("📱 小红书账号监控开始")
    print("=" * 60)
    
    if not MONITOR_USERS:
        print("⚠️ 未配置要监控的账号，请在脚本中添加 MONITOR_USERS 配置")
        print("\n示例配置：")
        print('MONITOR_USERS = [')
        print('    {"user_id": "5f3b4e5d6c7a8b9c0d1e2f3a", "name": "AI 科技前沿"},')
        print('    {"user_id": "6a7b8c9d0e1f2a3b4c5d6e7f", "name": "产品思维笔记"},')
        print(']')
        return
    
    # 检查 API 服务器是否运行
    try:
        response = requests.get(f"{XHS_API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print(f"✅ XHS-Downloader API 服务正常：{XHS_API_URL}")
        else:
            print(f"❌ API 服务异常：{response.status_code}")
            print("\n请先启动 API 服务器：")
            print(f"cd /home/admin/.openclaw/workspace/xhs-monitor")
            print(f"source venv/bin/activate")
            print(f"python main.py api")
            return
    except Exception as e:
        print(f"❌ 无法连接到 API 服务器：{e}")
        print("\n请先启动 API 服务器！")
        return
    
    # 遍历监控列表
    for user in MONITOR_USERS:
        user_id = user.get('user_id')
        user_name = user.get('name')
        last_check = user.get('last_check')
        
        print(f"\n🔍 检查账号：{user_name} ({user_id})")
        
        # 检查新作品
        new_posts = check_updates(user_id, last_check)
        
        if new_posts:
            print(f"✅ 发现 {len(new_posts)} 个新作品")
            
            # 生成报告
            md_content = generate_markdown_report(new_posts, user_name)
            
            # 保存到本地
            save_posts_to_file(new_posts, user_name)
            
            # 上传到 Get 笔记
            upload_to_getnote(md_content, user_name)
            
            # 更新最后检查时间
            user['last_check'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            print("ℹ️ 暂无新作品")
    
    print("\n" + "=" * 60)
    print("✅ 监控完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
