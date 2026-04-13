#!/usr/bin/env python3
# filename: /home/admin/.openclaw/workspace/scripts/ai-news-notify.py
# description: 发送 AI 日报生成通知到 DingTalk

import requests
import os
from datetime import datetime

# ============ 配置区域 ============

# DingTalk Webhook URL（需要用户配置）
DINGTALK_WEBHOOK = os.getenv('DINGTALK_WEBHOOK', '')

# Get 笔记配置
GETNOTE_API_KEY = os.getenv('GETNOTE_API_KEY', 'gk_live_9ce62ca78af4c66a.4e084c6e4ae8579e96f59a2b2967ff3d020e0700ed0365c5')
GETNOTE_CLIENT_ID = os.getenv('GETNOTE_CLIENT_ID', 'cli_a1b2c3d4e5f6789012345678abcdef90')

# ============ 函数定义 ============

def get_latest_note_id():
    """获取最新生成的笔记 ID"""
    try:
        # 读取最新日志
        log_file = '/home/admin/.openclaw/workspace/logs/ai-news-daily.log'
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找笔记 ID
        for line in reversed(lines):
            if '已上传到 Get 笔记' in line:
                # 提取笔记 ID
                parts = line.split('已上传到 Get 笔记：')
                if len(parts) > 1:
                    note_id = parts[1].strip()
                    return note_id
        
        return None
    except Exception as e:
        print(f"Error getting note ID: {e}")
        return None

def get_today_stats():
    """获取今日统计信息"""
    try:
        log_file = '/home/admin/.openclaw/workspace/logs/ai-news-daily.log'
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单解析统计信息
        stats = {
            'sources': 10,
            'total_news': 0,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # 从日志中提取
        if '"total_news":' in content:
            import re
            match = re.search(r'"total_news":\s*(\d+)', content)
            if match:
                stats['total_news'] = int(match.group(1))
        
        return stats
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {'sources': 10, 'total_news': 0, 'date': datetime.now().strftime('%Y-%m-%d')}

def send_dingtalk_notification(note_id, stats):
    """发送 DingTalk 通知"""
    if not DINGTALK_WEBHOOK:
        print("⚠️ 未配置 DingTalk Webhook，跳过通知")
        print("💡 配置方法：export DINGTALK_WEBHOOK='https://oapi.dingtalk.com/robot/send?access_token=xxx'")
        return False
    
    date_str = stats['date']
    total_news = stats['total_news']
    
    # 构建消息内容
    markdown_content = f"""## 📰 AI 领域每日动态已生成

**📅 日期**: {date_str}
**📊 信息源**: {stats['sources']} 个权威来源
**📈 动态数**: {total_news} 条

**🔗 查看笔记**: 
- 笔记 ID: `{note_id}`
- 已自动保存到 Get 笔记
- 位置：Ai &具身智能知识库

---
*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    # 发送请求
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"AI 领域每日动态 - {date_str}",
            "text": markdown_content
        },
        "at": {
            "isAtAll": True  # @所有人
        }
    }
    
    try:
        response = requests.post(DINGTALK_WEBHOOK, headers=headers, json=data)
        result = response.json()
        
        if result.get('errcode') == 0:
            print("✅ DingTalk 通知发送成功！")
            return True
        else:
            print(f"❌ DingTalk 通知发送失败：{result}")
            return False
    
    except Exception as e:
        print(f"❌ 发送通知时出错：{e}")
        return False

# ============ 主流程 ============

def main():
    print("=" * 60)
    print("🔔 发送 AI 日报通知")
    print("=" * 60)
    
    # 1. 获取最新笔记 ID
    note_id = get_latest_note_id()
    
    if not note_id:
        print("⚠️ 未找到最新笔记 ID，可能日报尚未生成")
        return
    
    print(f"✅ 找到笔记 ID: {note_id}")
    
    # 2. 获取统计信息
    stats = get_today_stats()
    print(f"📊 今日统计：{stats['total_news']} 条动态")
    
    # 3. 发送通知
    success = send_dingtalk_notification(note_id, stats)
    
    print("=" * 60)
    if success:
        print("✅ 通知发送完成！")
    else:
        print("⚠️ 通知未发送（可能未配置 Webhook）")
    
    return success

if __name__ == "__main__":
    main()
