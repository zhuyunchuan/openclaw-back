#!/usr/bin/env python3
# filename: /home/admin/.openclaw/workspace/scripts/ai-news-daily.py
# description: 每日自动抓取权威 AI 信息源，生成 Markdown 日报并上传到 Get 笔记

import feedparser
import requests
import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

# ============ 配置区域 ============

# RSS 源列表（按优先级排序）
RSS_FEEDS = {
    # 公司官方博客（一手信息）
    "OpenAI": "https://openai.com/news/rss",
    "Anthropic": "https://www.anthropic.com/news/rss",
    "Google AI": "https://blog.google/technology/ai/rss",
    "DeepMind": "https://deepmind.google/discover/blog/rss",
    "Meta AI": "https://ai.meta.com/blog/rss",
    "Microsoft AI": "https://blogs.microsoft.com/ai/rss",
    "NVIDIA": "https://blogs.nvidia.com/feed",  # GPU、AI 硬件、深度学习、自动驾驶
    # 行业媒体
    "The Batch": "https://www.deeplearning.ai/the-batch/rss",
    "MIT Tech Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "Stanford HAI": "https://hai.stanford.edu/news/rss",
    "Berkeley AI": "https://bair.berkeley.edu/blog/feed.xml",
    # 个人博客（专家观点）
    "Sam Altman": "https://blog.samaltman.com/posts.atom",
    "Lenny Rachitsky": "https://lennysan.substack.com/feed",
    # Andrej Karpathy - 使用 GitHub 博客（有 RSS 源）
    "Andrej Karpathy (Blog)": "https://karpathy.github.io/feed.xml",
}

# 输出目录
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/ai-news")
OUTPUT_DIR.mkdir(exist_ok=True)

# Get 笔记配置
GETNOTE_API_KEY = os.getenv('GETNOTE_API_KEY', 'gk_live_9ce62ca78af4c66a.4e084c6e4ae8579e96f59a2b2967ff3d020e0700ed0365c5')
GETNOTE_CLIENT_ID = os.getenv('GETNOTE_CLIENT_ID', 'cli_a1b2c3d4e5f6789012345678abcdef90')
GETNOTE_TOPIC_ID = "oYpEp190"  # Ai &具身智能知识库

# 智谱 AI API 配置（用于 AI 中文摘要）
GLM_API_KEY = os.getenv('GLM_API_KEY', '91fd8d1779dd426c8053f33b5efc0e0d.K1Wpv14M5T53Pjqi')
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# ============ 核心函数 ============

def is_recent_entry(entry, days=7):
    """检查条目是否是最近 N 天的"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_date = datetime(*entry.published_parsed[:6])
            days_old = (datetime.now() - published_date).days
            return days_old <= days
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            updated_date = datetime(*entry.updated_parsed[:6])
            days_old = (datetime.now() - updated_date).days
            return days_old <= days
        else:
            return True  # 没有时间信息时默认保留
    except:
        return True

def generate_ai_summary(title: str, content: str, max_length: int = 300) -> str:
    """使用智谱 AI 生成中文摘要"""
    try:
        # 清理内容（移除 HTML 标签）
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        # 如果内容太短，直接返回
        if len(clean_content) < 50:
            return clean_content
        
        # 截取前 3000 字（避免 token 过多）
        clean_content = clean_content[:3000]
        
        # 构建提示词
        prompt = f"""请为以下文章生成一个简洁的中文摘要（150-250 字）：

标题：{title}
内容：{clean_content}

要求：
1. 必须用中文输出
2. 概括核心内容
3. 突出关键信息
4. 语言简洁流畅
5. 直接输出摘要，不要有其他说明"""

        headers = {
            'Authorization': f'Bearer {GLM_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'glm-4',
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 400,
            'temperature': 0.7
        }
        
        response = requests.post(GLM_API_URL, headers=headers, json=data, timeout=15)
        result = response.json()
        
        if response.status_code == 200 and 'choices' in result:
            summary = result['choices'][0]['message']['content']
            # 清理摘要
            summary = summary.strip()
            if len(summary) > max_length:
                summary = summary[:max_length] + '...'
            return summary
        else:
            print(f"    ⚠️ API 返回错误：{result}")
            return None
    
    except Exception as e:
        print(f"    ⚠️ 摘要生成失败：{e}")
        return None

def extract_article_body(content: str) -> str:
    """从网页内容中提取正文，去除导航、菜单、页脚等"""
    try:
        # 清理 HTML 标签
        text = re.sub(r'<[^>]+>', '', content)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 清理常见导航文本（多语言）
        patterns_to_remove = [
            r'Skip to.*?(?:content|main)',
            r'Share.*?(?:x\.com|Facebook|LinkedIn|Twitter|Email)',
            r'Home.*?(?:Innovation|Model|Research|Product)',
            r'Follow.*?Us',
            r'Subscribe',
            r'Navigation',
            r'Menu',
            r'Footer',
            r'Copyright.*?\d{4}',
            r'Privacy Policy',
            r'Terms of Service',
            r'All rights reserved',
            r'View all.*?(?:\d+ more)?',
            r'See all',
            r'Learn more',
            r'Read more',
            r'Continue reading',
            r'Next.*?article',
            r'Previous.*?article',
            r'Related.*?articles',
            r'You may also like',
            r'Share this',
            r'Posted by',
            r'Published on',
            r'Last updated',
            r'Categories:',
            r'Tags:',
            r'Comments? \(\d+\)',
            r'Write a comment',
            r'Leave a reply',
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # 清理重复的空格和特殊字符
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[&][a-z]+;', ' ', text)  # HTML 实体如 &amp; &lt;
        
        # 提取看起来像正文的段落（至少 50 个字符的连续文本）
        sentences = re.split(r'[.!?]', text)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 50]
        
        # 取前 10 个有意义的句子
        body = '. '.join(meaningful_sentences[:10])
        
        if len(body) < 100:
            # 如果没有找到足够的正文，返回清理后的前 1000 字符
            body = text[:1000]
        
        return body.strip()
    
    except Exception as e:
        print(f"    ⚠️ 提取正文失败：{e}")
        return content[:1000]

def translate_to_chinese(title: str, content: str) -> str:
    """使用智谱 AI 翻译英文内容为中文（优化版 - 只翻译正文）"""
    try:
        # 先提取正文
        body_content = extract_article_body(content)
        
        # 截取前 1500 字
        if len(body_content) > 1500:
            body_content = body_content[:1500]
        
        # 构建翻译提示词
        prompt = f"""请将以下英文内容翻译成流畅的中文：

文章标题：{title}

文章内容：{body_content}

翻译要求：
1. 只翻译文章正文内容，不要翻译导航、菜单、页脚、按钮等
2. 准确翻译，保持原意
3. 语言自然流畅，符合中文表达习惯
4. 专业术语保留英文原名（如 Gemini API、AI Agent、LLM 等）
5. 直接输出翻译结果，不要添加"标题："、"内容："等前缀
6. 如果原文包含重复的导航文本，请直接忽略
7. 翻译长度控制在 300-500 字"""

        headers = {
            'Authorization': f'Bearer {GLM_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'glm-4',
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 600,
            'temperature': 0.7
        }
        
        response = requests.post(GLM_API_URL, headers=headers, json=data, timeout=20)
        result = response.json()
        
        if response.status_code == 200 and 'choices' in result:
            translation = result['choices'][0]['message']['content']
            # 清理翻译结果
            translation = translation.strip()
            # 移除可能的前缀
            translation = re.sub(r'^标题 [::]\s*', '', translation)
            translation = re.sub(r'^内容 [::]\s*', '', translation)
            # 如果翻译太长，截取前 500 字
            if len(translation) > 500:
                translation = translation[:500] + '...'
            return translation
        else:
            print(f"    ⚠️ API 返回错误：{result}")
            return None
    
    except Exception as e:
        print(f"    ⚠️ 翻译失败：{e}")
        return None

def fetch_rss_feed(feed_url, max_entries=10, recent_days=7, enable_ai_summary=False, enable_translation=False):
    """抓取单个 RSS 源，只返回最近 N 天的内容"""
    try:
        feed = feedparser.parse(feed_url)
        entries = []
        
        for entry in feed.entries[:max_entries * 2]:  # 多取一些用于过滤
            # 只保留最近的内容
            if not is_recent_entry(entry, days=recent_days):
                continue
            
            # 解析发布时间
            published = ""
            if hasattr(entry, 'published'):
                published = entry.published
            elif hasattr(entry, 'updated'):
                published = entry.updated
            
            # 提取 RSS 中的英文摘要
            original_summary = ""
            if hasattr(entry, 'summary'):
                original_summary = entry.summary[:300]  # 限制 300 字
                # 简单清理 HTML 标签
                original_summary = original_summary.replace('<p>', '').replace('</p>', '')
                original_summary = original_summary.replace('<br>', '\n')
                # 移除图片标签
                original_summary = re.sub(r'<img[^>]*>', '', original_summary)
            
            entry_data = {
                "title": entry.title if hasattr(entry, 'title') else "N/A",
                "link": entry.link if hasattr(entry, 'link') else "N/A",
                "published": published,
                "original_summary": original_summary.strip(),  # RSS 原文摘要（英文）
                "ai_summary": None,  # AI 生成的中文摘要
                "translation": None  # AI 翻译的中文全文
            }
            
            # 如果启用 AI 摘要，抓取全文并生成摘要
            if enable_ai_summary and entry.link != "N/A":
                print(f"    → 生成 AI 摘要...", end=" ")
                article_content = fetch_article_content(entry.link)
                if article_content:
                    ai_summary = generate_ai_summary(entry.title, article_content)
                    if ai_summary:
                        entry_data['ai_summary'] = ai_summary
                        print("✓", end=" ")
                    else:
                        print("✗", end=" ")
                    
                    # 如果启用翻译，翻译全文
                    if enable_translation:
                        print("翻译...", end=" ")
                        translation = translate_to_chinese(entry.title, article_content)
                        if translation:
                            entry_data['translation'] = translation
                            print("✓", end=" ")
                        else:
                            print("✗", end=" ")
                    
                    print("", end=" ")  # 换行
                else:
                    print("✗ (无法抓取)", end=" ")
            
            entries.append(entry_data)
            
            if len(entries) >= max_entries:
                break
        
        return entries
    except Exception as e:
        print(f"❌ Error fetching {feed_url}: {e}")
        return []

def fetch_article_content(url: str, max_chars: int = 3000) -> str:
    """抓取文章全文内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 简单提取正文（移除 HTML 标签）
            content = response.text
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
            content = re.sub(r'<[^>]+>', '', content)
            content = re.sub(r'\s+', ' ', content).strip()
            
            return content[:max_chars]
        else:
            return ""
    except Exception as e:
        print(f"    ⚠️ 抓取文章失败：{e}")
        return ""

def fetch_all_news(enable_ai_summary=False, enable_translation=False):
    """抓取所有 RSS 源"""
    all_news = {}
    
    print("📰 开始抓取 AI 新闻...")
    if enable_ai_summary:
        print("✨ AI 摘要功能已启用（可能需要几分钟）")
    if enable_translation:
        print("🌐 全文翻译功能已启用（可能需要更长时间）")
    
    for source, url in RSS_FEEDS.items():
        print(f"  → {source}...", end=" ")
        entries = fetch_rss_feed(url, max_entries=5, enable_ai_summary=enable_ai_summary, enable_translation=enable_translation)
        all_news[source] = entries
        print(f"✓ {len(entries)} 条")
    
    return all_news

def generate_markdown(all_news, date_str, enable_translation=False):
    """生成 Markdown 格式的日报（保留英文摘要 + AI 中文摘要 + 翻译）"""
    md = f"# 📰 AI 领域每日动态\n\n"
    md += f"**📅 日期**: {date_str}\n"
    md += f"**🕐 生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"**📊 信息源**: {len(RSS_FEEDS)} 个\n\n"
    
    # 统计总数
    total_count = sum(len(entries) for entries in all_news.values())
    md += f"**📈 总计**: {total_count} 条动态\n\n"
    md += "---\n\n"
    
    # 按来源分类展示
    for source, entries in all_news.items():
        if not entries:
            continue
        
        md += f"## {source}\n\n"
        
        for i, entry in enumerate(entries[:5], 1):  # 每个源最多展示 5 条
            md += f"### {i}. {entry['title']}\n\n"
            
            if entry['published']:
                md += f"- 📅 {entry['published']}\n"
            
            md += f"- 🔗 [阅读原文]({entry['link']})\n"
            
            # 显示英文原文摘要（来自 RSS）
            if entry.get('original_summary'):
                md += f"- 📝 **原文摘要**: {entry['original_summary']}\n"
            
            # AI 生成的中文摘要
            if entry.get('ai_summary'):
                md += f"- 🤖 **AI 中文摘要**: {entry['ai_summary']}\n"
            
            md += "\n"
            
            # 如果有翻译，添加翻译部分
            if enable_translation and entry.get('translation'):
                md += f"**📖 中文翻译**:\n\n"
                md += f"{entry['translation']}\n\n"
            
            md += "---\n\n"
    
    # 添加页脚
    md += "## 📝 说明\n\n"
    md += "本日报自动抓取以下权威信息源：\n\n"
    for source in RSS_FEEDS.keys():
        md += f"- {source}\n"
    
    if enable_translation:
        md += "\n**✨ 特性**: 每篇文章均保留英文原文摘要 + AI 生成中文摘要 + 全文翻译，方便快速阅读\n"
    else:
        md += "\n**✨ 特性**: 每篇文章均保留英文原文摘要 + AI 生成中文摘要，方便快速阅读\n"
    
    md += "\n---\n\n"
    md += f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return md

def save_to_file(md_content, date_str):
    """保存到本地文件"""
    # Markdown 文件
    md_file = OUTPUT_DIR / f"AI-NEWS-DAILY-{date_str}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"✅ 已保存到：{md_file}")
    
    return md_file

def upload_to_getnote(md_content, date_str):
    """上传到 Get 笔记"""
    try:
        headers = {
            'Authorization': GETNOTE_API_KEY,
            'X-Client-ID': GETNOTE_CLIENT_ID,
            'Content-Type': 'application/json'
        }
        
        # 创建笔记
        data = {
            'title': f'📰 AI 领域每日动态 - {date_str}',
            'content': md_content,
            'note_type': 'plain_text',
            'tags': ['AI 动态', '每日总结', '行业资讯', 'RSS']
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
                
                add_result = add_response.json()
                if add_result.get('success'):
                    print(f"✅ 已添加到 Ai &具身智能知识库")
                else:
                    print(f"⚠️ 添加到知识库失败：{add_result}")
            
            except Exception as e:
                print(f"⚠️ 添加到知识库出错：{e}")
            
            return note_id
        else:
            print(f"❌ 上传到 Get 笔记失败：{result}")
            return None
    
    except Exception as e:
        print(f"❌ 上传过程出错：{e}")
        return None

def send_dingtalk_notification(note_id, date_str):
    """发送 DingTalk 通知（可选）"""
    # 这里可以集成 DingTalk 消息通知
    # 由于需要配置 webhook，暂时跳过
    print(f"ℹ️ 如需 DingTalk 通知，请配置 webhook")

# ============ 主流程 ============

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 AI 领域每日动态抓取开始")
    print("=" * 60)
    
    # 计算日期
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 抓取新闻（启用 AI 摘要 + 全文翻译）
    all_news = fetch_all_news(enable_ai_summary=True, enable_translation=True)
    
    # 2. 生成 Markdown
    md_content = generate_markdown(all_news, date_str, enable_translation=True)
    
    # 3. 保存到文件
    md_file = save_to_file(md_content, date_str)
    
    # 4. 上传到 Get 笔记
    note_id = upload_to_getnote(md_content, date_str)
    
    # 5. 发送通知（可选）
    if note_id:
        send_dingtalk_notification(note_id, date_str)
    
    print("=" * 60)
    print("✅ 抓取完成！")
    print("=" * 60)
    
    # 返回统计信息
    total_count = sum(len(entries) for entries in all_news.values())
    return {
        "date": date_str,
        "sources": len(RSS_FEEDS),
        "total_news": total_count,
        "note_id": note_id,
        "file": str(md_file)
    }

if __name__ == "__main__":
    result = main()
    print(f"\n📊 统计：{json.dumps(result, ensure_ascii=False, indent=2)}")
