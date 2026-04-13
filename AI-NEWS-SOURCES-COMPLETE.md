# 📰 AI 领域每日动态 - 完整信息源清单

**更新时间**: 2026-04-09 13:15  
**信息源总数**: 13 个

---

## 📊 信息源分类

### 🏢 公司官方博客（7 个）

| 信息源 | RSS 地址 | 更新频率 | 说明 |
|--------|---------|---------|------|
| **OpenAI** | https://openai.com/news/rss | 每周 2-5 篇 | GPT、Codex、AI 安全 |
| **Anthropic** | https://www.anthropic.com/news/rss | 每周 1-3 篇 | Claude、AI 安全研究 |
| **Google AI** | https://blog.google/technology/ai/rss | 每周 2-4 篇 | Gemini、Google AI 研究 |
| **DeepMind** | https://deepmind.google/discover/blog/rss | 每月 2-4 篇 | 前沿 AI 研究、科学突破 |
| **Meta AI** | https://ai.meta.com/blog/rss | 每周 1-2 篇 | Llama、开源模型 |
| **Microsoft AI** | https://blogs.microsoft.com/ai/rss | 每周 2-3 篇 | Copilot、Azure AI |
| **NVIDIA** | https://blogs.nvidia.com/feed | 每周 3-5 篇 | GPU、AI 硬件、自动驾驶 |

---

### 📰 行业媒体（4 个）

| 信息源 | RSS 地址 | 更新频率 | 说明 |
|--------|---------|---------|------|
| **The Batch** | https://www.deeplearning.ai/the-batch/rss | 周刊 | Andrew Ng 主编，AI 周报 |
| **MIT Tech Review AI** | https://www.technologyreview.com/topic/artificial-intelligence/feed | 每日更新 | 麻省理工科技评论 |
| **Stanford HAI** | https://hai.stanford.edu/news/rss | 每周 1-2 篇 | 以人为本的 AI 研究 |
| **Berkeley AI** | https://bair.berkeley.edu/blog/feed.xml | 每周 1-2 篇 | 伯克利 AI 研究博客 |

---

### 👤 个人博客（专家观点）（3 个）

| 信息源 | RSS 地址 | 更新频率 | 说明 |
|--------|---------|---------|------|
| **Sam Altman** | https://blog.samaltman.com/posts.atom | 不定期 | OpenAI CEO，行业洞察 |
| **Lenny Rachitsky** | https://lennysan.substack.com/feed | 每周 1-2 篇 | 产品管理、AI 产品实践 |
| **Andrej Karpathy** | https://karpathy.github.io/feed.xml | 不定期 | AI 技术博客、LLM 教程 |

---

## 👤 个人博客详细介绍

### 1. Sam Altman (OpenAI CEO)

**博客**: https://blog.samaltman.com  
**RSS**: https://blog.samaltman.com/posts.atom  
**更新频率**: 不定期（重要节点发布）

**内容特点**:
- 📌 OpenAI 战略方向
- 💡 行业深度思考
- 🌍 AGI 未来展望
- 🎯 创业建议

**近期文章**:
- 反思 ChatGPT 发布两周年
- 被解雇事件的反思与感恩
- AGI 进展与未来展望

---

### 2. Lenny Rachitsky (产品专家)

**博客**: https://lennysan.substack.com  
**RSS**: https://lennysan.substack.com/feed  
**更新频率**: 每周 1-2 篇

**内容特点**:
- 📊 产品管理最佳实践
- 🤖 AI 产品案例分析
- 📈 增长策略
- 💼 职业发展建议

**背景**:
- 前 Airbnb PM
- 现专注产品通讯
- 订阅用户超 100 万

---

### 3. Andrej Karpathy (AI 研究员)

**博客**: https://karpathy.github.io  
**RSS**: https://karpathy.github.io/feed.xml  
**更新频率**: 不定期

**内容特点**:
- 🎓 AI 技术教程（LLM、神经网络）
- 💻 开源项目（micrograd, microgpt）
- 🔬 研究分享
- 📚 教育资源

**近期文章**:
- microgpt (2026-02-12) - 200 行 Python 实现 GPT 训练和推理
- Deep Neural Nets: 33 years ago and 33 years from now (2022)
- A from-scratch tour of Bitcoin in Python (2021)

**背景**:
- 前 OpenAI 创始成员
- 前 Tesla AI 总监
- 现创办 Eureka Labs（AI 教育）
- CS231n 创始人（斯坦福深度学习课程）

---

## 📈 信息源优先级

### 第一梯队（必关注）
1. ✅ **OpenAI** - 产品发布、技术突破
2. ✅ **Anthropic** - Claude 更新、AI 安全
3. ✅ **Google AI** - Gemini、Google AI 动态
4. ✅ **NVIDIA** - GPU、AI 硬件、深度学习框架
5. ✅ **MIT Tech Review AI** - 第三方深度分析

### 第二梯队（重要）
6. ✅ **Meta AI** - Llama、开源模型
7. ✅ **Microsoft AI** - Copilot、企业应用
8. ✅ **Sam Altman** - 行业洞察
9. ✅ **The Batch** - 每周简报

### 第三梯队（补充）
10. ✅ **DeepMind** - 前沿研究
11. ✅ **Stanford HAI** - 学术研究
12. ✅ **Berkeley AI** - 学术研究
13. ✅ **Lenny Rachitsky** - 产品视角
14. ✅ **Andrej Karpathy** - 技术教育

---

## 🔧 配置说明

### RSS 源配置

在 `scripts/ai-news-daily.py` 中配置：

```python
RSS_FEEDS = {
    # 公司官方博客
    "OpenAI": "https://openai.com/news/rss",
    "Anthropic": "https://www.anthropic.com/news/rss",
    # ... 其他源
}
```

### 抓取策略

- **每个源最多抓取**: 5 条最新动态
- **时间范围**: 最近 7 天
- **过滤规则**: 自动过滤旧内容

---

## 📊 预期输出

### 每日动态数量

- **工作日**: 10-20 条
- **周末**: 5-10 条
- **平均**: 8-15 条/天

### 内容分布

- **公司动态**: 40-50%
- **行业媒体**: 30-40%
- **专家观点**: 10-20%

---

## 💡 使用建议

### 快速浏览
1. 先看 **AI 中文摘要**（150-250 字）
2. 感兴趣再看 **中文翻译**（300-500 字）
3. 需要细节点击 **阅读原文**

### 深度学习
1. 关注 **Sam Altman** 的行业洞察
2. 学习 **Andrej Karpathy** 的技术讲座
3. 参考 **Lenny** 的产品实践

---

## 📁 相关文件

- **脚本**: `scripts/ai-news-daily.py`
- **输出**: `ai-news/AI-NEWS-DAILY-YYYY-MM-DD.md`
- **配置文档**: `AI-NEWS-FINAL-SETUP.md`
- **信息源清单**: 本文档

---

## 🔗 快速访问

### 公司博客
- [OpenAI News](https://openai.com/news)
- [Anthropic News](https://www.anthropic.com/news)
- [Google AI Blog](https://blog.google/technology/ai)
- [DeepMind Blog](https://deepmind.google/discover/blog)
- [Meta AI Blog](https://ai.meta.com/blog)
- [Microsoft AI Blog](https://blogs.microsoft.com/ai)

### 行业媒体
- [The Batch](https://www.deeplearning.ai/the-batch)
- [MIT Tech Review AI](https://www.technologyreview.com/topic/artificial-intelligence)
- [Stanford HAI](https://hai.stanford.edu)
- [Berkeley AI](https://bair.berkeley.edu)

### 个人博客
- [Sam Altman](https://blog.samaltman.com)
- [Lenny Rachitsky](https://lennysan.substack.com)
- [Andrej Karpathy](https://karpathy.ai)
- [Karpathy YouTube](https://www.youtube.com/@AndrejKarpathy)

---

*创建时间：2026-04-09 13:15*  
*最后更新：2026-04-09 13:15*
