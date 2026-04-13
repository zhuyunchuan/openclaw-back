# 🐦 Twitter/X 爬虫解决方案 - 2026 年版

## 📋 问题现状

Twitter/X 在 2023 年后实施了严格的反爬虫措施：
- ❌ 未登录用户无法查看内容
- ❌ 传统 API 需要付费（$100/月起）
- ❌ 浏览器自动化容易被检测
- ❌ 公共搜索引擎无法抓取实时内容

## ✅ 可行方案（已验证）

经过调研，找到 **2 个最活跃的开源项目**，均支持**Cookie 认证**方式抓取：

---

## 方案一：Scweet（推荐 ⭐）

**GitHub**: https://github.com/Altimis/Scweet  
**状态**: ✅ 2026 年 3 月最新验证可用  
**特点**: 
- 使用 X 的内部 GraphQL API
- 支持 Cookie 认证（无需官方 API Key）
- 多账号池 + 代理支持
- 自动速率限制和冷却
- 支持断点续传
- 同步/异步双 API

### 📦 安装

```bash
pip install -U Scweet
```

### 🔑 获取 Cookie（auth_token）

1. 浏览器访问 https://x.com 并登录
2. 按 F12 打开开发者工具
3. 点击 **Application** → **Cookies** → **https://x.com**
4. 找到 `auth_token` 值，复制保存

### 💻 使用示例

#### 基础用法（单账号）

```python
from Scweet import Scweet

# 使用 auth_token（ct0 会自动生成）
s = Scweet(auth_token="YOUR_AUTH_TOKEN")

# 搜索推文
tweets = s.search("AI news", since="2026-04-01", limit=100)

# 获取用户推文
tweets = s.get_profile_tweets(["OpenAI", "AnthropicAI"], limit=50)

# 获取关注者
followers = s.get_followers(["elonmusk"], limit=1000)
```

#### 高级用法（多账号 + 代理）

```python
# 多账号配置（减少封号风险）
cookies = [
    {
        "username": "account1",
        "cookies": {"auth_token": "token1", "ct0": "ct0_1"},
        "proxy": "http://user1:pass1@host1:port1"
    },
    {
        "username": "account2",
        "cookies": {"auth_token": "token2", "ct0": "ct0_2"},
        "proxy": "http://user2:pass2@host2:port2"
    }
]

s = Scweet(cookies=cookies)

# 搜索并保存到文件
tweets = s.search(
    "AI tools",
    since="2026-04-01",
    limit=500,
    save=True,           # 保存到文件
    save_format="json"   # 或 "csv" / "both"
)
```

#### CLI 用法（无需写代码）

```bash
# 搜索并保存
scweet --auth-token YOUR_TOKEN search "AI news" \
  --since 2026-04-01 \
  --limit 200 \
  --save \
  --save-format json

# 获取用户推文
scweet --auth-token YOUR_TOKEN profile-tweets OpenAI \
  --limit 100 \
  --save

# 高级搜索（带过滤）
scweet --auth-token YOUR_TOKEN search "AI tools" \
  --from OpenAI AnthropicAI \
  --min-likes 50 \
  --has-images \
  --limit 100 \
  --save
```

### 📊 搜索过滤参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `since` | 开始日期 | `"2026-04-01"` |
| `until` | 结束日期 | `"2026-04-09"` |
| `from_users` | 指定用户 | `["OpenAI", "AnthropicAI"]` |
| `min_likes` | 最少点赞 | `50` |
| `min_retweets` | 最少转发 | `20` |
| `has_images` | 包含图片 | `True` |
| `has_videos` | 包含视频 | `True` |
| `lang` | 语言 | `"en"` |
| `verified_only` | 仅认证用户 | `True` |

### ⚠️ 注意事项

1. **不要用个人主账号** - 使用专门注册的小号
2. **配置代理** - 避免同一 IP 频繁请求
3. **设置 limit** - 避免触发每日上限
4. **多账号轮换** - 单账号每日建议 < 1000 条推文

---

## 方案二：twscrape

**GitHub**: https://github.com/vladkens/twscrape  
**状态**: ✅ 2025 年 4 月更新  
**特点**:
- 支持 GraphQL API
- 异步并发
- 自动账号轮换
- 支持邮箱验证码登录

### 📦 安装

```bash
pip install twscrape
```

### 🔑 配置账号

```python
import asyncio
from twscrape import API

async def main():
    api = API()
    
    # 方式 1：使用 Cookie（更稳定）
    cookies = "abc=12; ct0=xyz"
    await api.pool.add_account("user1", "pass1", "email1@mail.com", "mail_pass1", cookies=cookies)
    
    # 方式 2：账号密码登录（需要接收验证码）
    await api.pool.add_account("user2", "pass2", "email2@mail.com", "mail_pass2")
    await api.pool.login_all()
    
    # 搜索推文
    async for tweet in api.search("AI news", limit=20):
        print(tweet.id, tweet.user.username, tweet.rawContent)

asyncio.run(main())
```

### CLI 用法

```bash
# 添加账号
twscrape add_accounts accounts.txt username:password:email:email_password:cookies

# 登录
twscrape login_accounts

# 搜索
twscrape search "AI news" --limit 20 > tweets.txt

# 获取用户推文
twscrape user_tweets OpenAI --limit 50
```

---

## 🚀 实施方案（为您的 Twitter 总结）

### 步骤 1：准备 Twitter 账号

1. **注册 1-2 个 Twitter 小号**（或使用现有账号）
2. **获取 auth_token**（按上述方法）
3. **可选**：配置住宅代理（降低封号风险）

### 步骤 2：安装 Python 环境

```bash
# 创建虚拟环境
cd /home/admin/.openclaw/workspace
python3 -m venv venv-twitter
source venv-twitter/bin/activate

# 安装 Scweet
pip install -U Scweet
```

### 步骤 3：创建爬虫脚本

```python
#!/usr/bin/env python3
# filename: /home/admin/.openclaw/workspace/scripts/twitter-daily-summary.py

from Scweet import Scweet
import json
from datetime import datetime, timedelta

# 配置
AUTH_TOKEN = "YOUR_AUTH_TOKEN"  # 替换为您的 auth_token
OUTPUT_DIR = "/home/admin/.openclaw/workspace/twitter-data"

# 监控账号列表
ACCOUNTS = ["OpenAI", "AnthropicAI", "GoogleGemini", "karpathy", "lennysan"]

def fetch_daily_summary():
    """获取昨日至今日的 AI 动态"""
    s = Scweet(auth_token=AUTH_TOKEN)
    
    # 计算日期范围（昨天到今天）
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    all_tweets = []
    
    # 遍历监控账号
    for account in ACCOUNTS:
        try:
            print(f"Fetching tweets from @{account}...")
            tweets = s.get_profile_tweets(
                [account],
                since=yesterday,
                until=today,
                limit=20,  # 每个账号最多 20 条
                save=False
            )
            
            for tweet in tweets:
                tweet['source_account'] = account
                all_tweets.append(tweet)
                
        except Exception as e:
            print(f"Error fetching {account}: {e}")
    
    # 保存到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{OUTPUT_DIR}/tweets_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(all_tweets)} tweets to {output_file}")
    return output_file

def generate_markdown_summary(tweet_file):
    """生成 Markdown 格式的每日总结"""
    with open(tweet_file, 'r', encoding='utf-8') as f:
        tweets = json.load(f)
    
    # 按账号分组
    by_account = {}
    for tweet in tweets:
        account = tweet.get('source_account', 'Unknown')
        if account not in by_account:
            by_account[account] = []
        by_account[account].append(tweet)
    
    # 生成 Markdown
    md = f"# 🐦 Twitter/X AI 动态每日总结\n\n"
    md += f"**📅 日期**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    md += f"**📊 总计**: {len(tweets)} 条推文\n\n"
    md += "---\n\n"
    
    for account, account_tweets in by_account.items():
        md += f"## @{account}\n\n"
        md += f"**推文数**: {len(account_tweets)}\n\n"
        
        for i, tweet in enumerate(account_tweets[:10], 1):  # 最多展示 10 条
            md += f"### {i}. {tweet.get('text', '')[:100]}...\n\n"
            md += f"- 👍 {tweet.get('likes', 0)} | 🔄 {tweet.get('retweets', 0)} | 💬 {tweet.get('comments', 0)}\n"
            md += f"- 🔗 [{tweet.get('tweet_url', '')}]\n\n"
        
        md += "---\n\n"
    
    # 保存 Markdown
    md_file = tweet_file.replace('.json', '.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"Generated summary: {md_file}")
    return md_file

if __name__ == "__main__":
    tweet_file = fetch_daily_summary()
    generate_markdown_summary(tweet_file)
```

### 步骤 4：设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加每日凌晨 2 点运行的任务
0 2 * * * cd /home/admin/.openclaw/workspace && /home/admin/.openclaw/workspace/venv-twitter/bin/python scripts/twitter-daily-summary.py
```

### 步骤 5：集成到 Get 笔记

修改脚本，在生成 Markdown 后自动上传到 Get 笔记：

```python
import requests
import os

def upload_to_getnote(md_file):
    """上传总结到 Get 笔记"""
    API_KEY = os.getenv('GETNOTE_API_KEY')
    CLIENT_ID = os.getenv('GETNOTE_CLIENT_ID')
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    headers = {
        'Authorization': API_KEY,
        'X-Client-ID': CLIENT_ID,
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': f'🐦 Twitter/X AI 动态每日总结 - {datetime.now().strftime("%Y-%m-%d")}',
        'content': content,
        'note_type': 'plain_text',
        'tags': ['AI 动态', 'Twitter', '每日总结']
    }
    
    response = requests.post(
        'https://openapi.biji.com/open/api/v1/resource/note/save',
        headers=headers,
        json=data
    )
    
    result = response.json()
    if result.get('success'):
        note_id = result['data']['note_id']
        print(f"Uploaded to Get 笔记：{note_id}")
        
        # 添加到知识库
        requests.post(
            'https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add',
            headers=headers,
            json={'topic_id': 'oYpEp190', 'note_ids': [note_id]}  # Ai &具身智能知识库
        )
    else:
        print(f"Upload failed: {result}")
```

---

## 💰 成本估算

| 项目 | 费用 | 说明 |
|------|------|------|
| Twitter 账号 | ¥0 | 免费注册（需要手机号验证） |
| 住宅代理 | ¥50-200/月 | 可选，降低封号风险 |
| 服务器 | ¥0 | 使用现有服务器 |
| **总计** | **¥0-200/月** | 远低于官方 API（$100/月 ≈ ¥720/月） |

---

## ⚠️ 风险提示

1. **账号封禁风险** - Twitter 可能封禁爬虫账号
   - 缓解：使用小号、配置代理、限制抓取频率
   
2. **API 变更风险** - Twitter 可能更新 API
   - 缓解：Scweet 项目会及时更新适配

3. **法律风险** - 违反 Twitter 服务条款
   - 缓解：仅用于个人研究，不商业使用

---

## 📚 参考资料

- [Scweet GitHub](https://github.com/Altimis/Scweet)
- [twscrape GitHub](https://github.com/vladkens/twscrape)
- [Twitter 高级搜索语法](https://github.com/igorbrigadir/twitter-advanced-search)
- [Scweet 完整文档](https://github.com/Altimis/Scweet/blob/master/DOCUMENTATION.md)

---

*创建时间：2026-04-09*  
*最后更新：2026-04-09*
