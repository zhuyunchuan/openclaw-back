# GBrain - Garry Tan 的 AI 记忆管理系统

**整理时间**: 2026-04-13  
**项目地址**: https://github.com/garrytan/gbrain  
**发布者**: Garry Tan (YC President & CEO)  
**发布时间**: 2026-04-10  
**许可证**: MIT (免费开源)

---

## 📊 项目概览

| 指标 | 数据 |
|------|------|
| **Stars** | 1,000+ (4 天) |
| **Forks** | 136 |
| **Contributors** | 2 |
| **许可证** | MIT |
| **状态** | ✅ 刚发布，活跃开发中 |

---

## 🎯 GBrain 解决了什么问题？

### 核心问题

**你的 AI Agent 很聪明，但它不了解你的生活。**

> "如果你希望你的 OpenClaw 或 Hermes Agent 能够完美地完全回忆所有 10,000+ 个 Markdown 文件，GBrain 在这里提供帮助。"

---

### GBrain 的核心价值

**让 AI Agent 拥有长期记忆**，越用越聪明：

```
会议、邮件、推文、日历事件、语音通话、原创想法...
    ↓
全部流入可搜索的知识库
    ↓
Agent 每次回答前读取，每次对话后写入
    ↓
Agent 每天都变得更聪明
```

---

## 🏗️ 核心架构

### 三层记忆系统

```
┌─────────────────────────────────────────────────────────┐
│                    你的 AI Agent                         │
│  (OpenClaw / Hermes / Claude Code / 任何持久 Agent)       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   GBrain 检索层                           │
│  • 混合搜索（向量 + 关键词 + RRF）                        │
│  • 实体检测（人物/公司/概念/想法）                         │
│  • 自动反向链接                                           │
│  • 37 种检索操作                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   大脑仓库 (Brain Repo)                   │
│  • Git 管理的 Markdown 文件                              │
│  • PGLite 本地数据库（2 秒启动，无需服务器）                │
│  • 可选 Supabase 云端（Pro $25/月）                       │
│  • 人类可随时编辑                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 数据流向

```
信号到达（会议/邮件/推文/链接）
    ↓
Agent 检测实体（人物、公司、想法）
    ↓
READ: 先检查大脑（gbrain search / gbrain get）
    ↓
Respond: 用完整上下文回答
    ↓
WRITE: 更新大脑页面写入新信息
    ↓
Sync: gbrain 索引变更供下次查询

每个循环都增加知识 → 知识复合增长
```

---

## 🛠️ 核心功能

### 1. 混合搜索（Hybrid Search）

| 搜索类型 | 说明 | 是否需要 API Key |
|---------|------|-----------------|
| **关键词搜索** | 传统全文检索 | ❌ 不需要 |
| **向量搜索** | 语义相似度匹配 | ✅ OpenAI |
| **RRF 融合** | 混合排序，最佳结果 | ✅ Anthropic（可选） |

**37 种检索操作**：
- `gbrain search` - 混合搜索
- `gbrain query` - 自然语言查询
- `gbrain get` - 获取特定实体页面
- `gbrain traverse_graph` - 遍历知识图谱
- `gbrain brief` - 生成实体简报

---

### 2. 实体系统（Entity System）

**自动检测并创建页面**：

| 实体类型 | 说明 | 示例 |
|---------|------|------|
| **People** | 人物档案 | Pedro, Diana, Jordan |
| **Companies** | 公司档案 | Coinbase, Instacart |
| **Concepts** | 概念/想法 | " shame and founder performance" |
| **Meetings** | 会议记录 | 2026-04-10 与 Jordan 的会议 |
| **Media** | 媒体/链接 | 文章、视频、播客 |

**页面结构**：
```markdown
# Pedro Domingos

## Compiled Truth（顶部）
- 机器学习教授
- 2023 年在 SF 见过
- 对具身智能感兴趣

## Timeline（底部，追加式）
- 2026-04-10: 在 YC 晚宴上讨论具身智能
- 2023-06-15: 第一次见面，讨论 AutoGluon
```

---

### 3. 自动集成（Integrations）

**数据自动流入大脑**：

| 集成 | 功能 | 依赖 |
|------|------|------|
| **Email-to-Brain** | Gmail → 实体页面 | Credential Gateway |
| **Calendar-to-Brain** | Google Calendar → 可搜索页面 | Credential Gateway |
| **X-to-Brain** | Twitter → 时间线 + 提及 + 删除 | 无 |
| **Voice-to-Brain** | 电话通话 → 转录 + 实体检测 | ngrok + Twilio |
| **Meeting Sync** | Circleback 转录 → 带参会者的页面 | 无 |
| **Public Tunnel** | 固定 URL 用于 MCP + 语音 | ngrok Hobby $8/月 |

---

### 4. 语音集成（Voice Integration）

**最强演示**：

```
拨打一个电话号码 → AI 接听
    ↓
AI 知道是谁来电，从 3000+ 人物页面拉取完整上下文
    ↓
引用上次会议，像真正了解你世界的人一样回应
    ↓
通话结束 → 结构化大脑页面出现
    （转录 + 实体检测 + 交叉引用）
```

**这不是演示，是生产系统**：
- 真实电话号码运行
- 筛选未知来电
- 每次通话后更聪明
- WebRTC 浏览器零配置
- 25 个生产模式包含

---

### 5. 梦境周期（Dream Cycle）

**Agent 在你睡觉时工作**：

```
夜间运行：
1. 扫描每次对话
2. 丰富缺失的实体
3. 修复断裂的引用
4. 巩固记忆

早上醒来 → 大脑比睡前更聪明
```

---

## 📦 安装与配置

### 快速安装（30 分钟）

```bash
# 1. 克隆并安装
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"
bun install && bun link

# 2. 验证
gbrain --version

# 3. 初始化大脑（2 秒，无需服务器）
gbrain init

# 4. 导入现有 Markdown
gbrain import ~/notes/ --no-embed

# 5. 生成向量嵌入
gbrain embed --stale

# 6. 测试查询
gbrain query "这些文档中有什么主题？"
```

---

### API Keys 配置

| Key | 用途 | 是否必需 |
|-----|------|---------|
| **OpenAI API Key** | 向量嵌入（text-embedding-3-large） | ✅ 必需（用于向量搜索） |
| **Anthropic API Key** | 多查询扩展 + LLM 分块 | ⚠️ 可选（提升搜索质量） |

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

**没有 API Key 也能用**：
- 无 OpenAI → 关键词搜索仍工作
- 无 Anthropic → 搜索工作但跳过查询扩展

---

### 数据库选项

| 模式 | 说明 | 成本 |
|------|------|------|
| **PGLite（默认）** | 本地嵌入式 Postgres，无需服务器 | 免费 |
| **Supabase** | 托管 Postgres + pgvector | $25/月（Pro 8GB） |

**升级**：
```bash
gbrain migrate --to supabase
```

---

## 🧠 与 OpenClaw 集成

### GBrain + OpenClaw 记忆层

| 层级 | 存储内容 | 查询方式 |
|------|---------|---------|
| **GBrain** | 世界知识（人物/公司/会议/想法/媒体） | `gbrain search`, `gbrain query`, `gbrain get` |
| **Agent Memory** | 偏好/决策/操作配置 | `memory_search` |
| **Session Context** | 当前对话 | 自动 |

**推荐**：三层都检查
- GBrain → 世界事实
- Memory → Agent 配置
- Session → 即时上下文

---

### 安装到 OpenClaw

```bash
# 通过 ClawHub 安装技能
clawhub install gbrain

# 或在 AGENTS.md 中添加
当收到消息时：
1. 先运行 gbrain search 检查相关知识
2. 检测实体（人物/公司/想法）
3. 回答前读取大脑
4. 回答后写入新信息
```

---

## 💬 使用示例

### 场景 1: 会议准备

```
你：30 分钟后要和 Jordan 开会，帮我准备

GBrain Agent:
1. gbrain get "Jordan" → 拉取人物档案
2. gbrain search "Jordan meetings" → 历史会议
3. gbrain traverse_graph "Jordan → companies" → 关联公司
4. 生成简报：
   - 上次见面：2026-03-15，讨论 A 轮
   - 共同联系人：Pedro, Diana
   - 开放线程：尽职调查清单
   - 最近动态：公司发布了新功能
```

---

### 场景 2: 社交图谱查询

```
你：我应该邀请谁参加晚宴，既认识 Pedro 又认识 Diana？

GBrain Agent:
1. gbrain get "Pedro" → 获取社交连接
2. gbrain get "Diana" → 获取社交连接
3. 交叉引用 3000+ 人物页面
4. 返回结果：
   - John（和两人都参加过 YC 晚宴）
   - Sarah（共同投资了某公司）
   - Mike（三人都在某董事会）
```

---

### 场景 3: 想法检索

```
你：我说过关于"羞耻感和创始人表现"的关系吗？

GBrain Agent:
1. gbrain query "shame founder performance"
2. 搜索你的思考，不是互联网
3. 返回结果：
   - 2025-11-03: 原创想法 - "羞耻感驱动 vs 愿景驱动"
   - 2026-02-14: 会议记录 - 与心理学教授讨论
   - 2026-03-20: 阅读笔记 - 某篇相关论文
```

---

### 场景 4: 语音通话

```
来电显示：Pedro Domingos

AI 接听：
"嗨 Pedro！最近怎么样？上次在 YC 晚宴后你说要发
具身智能的论文，进展如何？"

[通话 15 分钟，讨论合作机会]

通话结束 → 自动生成页面：

# Pedro Domingos - Call 2026-04-13

## 转录
[完整对话转录]

## 检测实体
- 具身智能论文（新建页面）
- 合作机会（新建页面）
- 某大学（链接到现有页面）

## 后续行动
- [ ] 发送论文草稿
- [ ] 安排与 Diana 的三方会议
```

---

## 📊 真实部署数据

Garry Tan 的生产环境（1 周）：

| 指标 | 数量 |
|------|------|
| **Markdown 文件** | 10,000+ |
| **人物页面** | 3,000+ |
| **日历数据** | 13 年 |
| **会议转录** | 280+ |
| **原创想法** | 300+ |
| **公司页面** | 500+ |
| **概念页面** | 1,000+ |

---

##  与 gstack 的对比

| 维度 | gstack | gbrain |
|------|--------|--------|
| **定位** | 工程流程自动化 | AI 记忆管理 |
| **核心功能** | 23 个编码技能 | 37 个检索操作 |
| **数据存储** | CLAUDE.md（项目级） | Brain Repo（终身记忆） |
| **适用场景** | 代码开发 | 知识管理 + 社交图谱 |
| **数据库** | 无需 | PGLite / Supabase |
| **集成** | GitHub/浏览器 | Gmail/Calendar/Twitter/Voice |
| **依赖模型** | Claude Opus | GPT-5.4 / Claude Opus 4.6 |

---

### 两者关系

**互补，不是替代**：

```
gstack → 帮你写代码（工程团队）
gbrain → 帮你记住一切（长期记忆）

最佳实践：两者都用
- gstack 负责 Build
- gbrain 负责 Remember
```

---

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| **运行时** | Bun |
| **数据库** | PGLite（嵌入式 Postgres）+ pgvector |
| **搜索** | 混合搜索（向量 + 关键词 + RRF） |
| **嵌入** | OpenAI text-embedding-3-large |
| **LLM** | Claude Opus 4.6 / GPT-5.4 Thinking |
| **MCP** | 30 个工具（stdio） |
| **部署** | 本地 / Supabase / Railway |

---

## 📋 推荐配置

### 定时任务（Cron Schedule）

```bash
# 每 15 分钟：实时同步
*/15 * * * * gbrain sync --repo ~/brain && gbrain embed --stale

# 每天：自动更新检查
0 9 * * * gbrain check-update --json

# 每晚：梦境周期
0 2 * * * gbrain dream-cycle

# 每周：健康检查
0 9 * * 0 gbrain doctor --json && gbrain embed --stale
```

---

### MCP 配置（Claude Code）

```json
{
  "mcpServers": {
    "gbrain": {
      "command": "gbrain",
      "args": ["serve"]
    }
  }
}
```

**可用工具**：
- `get_page`, `put_page`, `search`, `query`
- `add_link`, `traverse_graph`, `sync_brain`
- `file_upload`, ...（共 30 个）

---

## 🎯 是否适合你？

### ✅ 适合的场景

如果你：

1. **使用 OpenClaw / Hermes / 持久 AI Agent**
   - 需要长期记忆
   - 希望 Agent 了解你的生活

2. **有大量知识需要管理**
   - 会议记录
   - 邮件往来
   - 社交关系
   - 原创想法

3. **需要跨会话连续性**
   - Agent 记住之前的对话
   - 人物/公司背景不丢失
   - 知识复合增长

4. **想要语音集成**
   - AI 接听电话
   - 通话转录 + 实体检测
   - 越用越聪明

---

### ❌ 可能不适合

如果你：

1. **偶尔使用 AI**
   - 不需要长期记忆
   - 每次都是独立任务

2. **已有成熟知识管理系统**
   - Notion/Obsidian 已满足
   - 不想迁移

3. **预算有限**
   - 需要 OpenAI API Key（向量搜索）
   - Supabase 云端 $25/月（可选）

4. **不想维护基础设施**
   - 需要设置 cron 任务
   - 需要管理 API Keys

---

## 💰 成本估算

| 项目 | 免费方案 | 生产方案 |
|------|---------|---------|
| **数据库** | PGLite（本地） | Supabase Pro $25/月 |
| **OpenAI Embedding** | $0（<1000 文件） | ~$10/月（10000 文件） |
| **Anthropic** | $0（可选） | ~$10/月（Haiku） |
| **ngrok** | 动态 URL | Hobby $8/月（固定 URL） |
| **Twilio** | 无语音 | ~$5/月（来电显示） |
| **总计** | **$0/月** | **~$58/月** |

---

## 🚀 我的建议

### 短期（现在）

**值得尝试**，原因：

1. **刚发布，早期采用者优势**
   - 2026-04-10 发布
   - 社区正在形成
   - Garry Tan 亲自维护

2. **与 OpenClaw 深度集成**
   - 你就是 OpenClaw 用户
   - 天然适配
   - 技能已打包

3. **免费起步**
   - PGLite 本地免费
   - 关键词搜索免费
   - 可逐步升级

---

### 建议的尝试方式

**第 1 天**：
```bash
# 安装
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain && bun install && bun link

# 初始化
gbrain init

# 导入现有笔记
gbrain import ~/notes/

# 测试
gbrain query "我的笔记有什么主题？"
```

**第 1 周**：
- 配置 OpenAI API Key
- 设置 Email-to-Brain
- 设置 Calendar-to-Brain
- 每天运行 `gbrain sync`

**第 2-4 周**：
- 设置 Voice-to-Brain（可选）
- 配置梦境周期
- 评估效果

---

### 与 Get 笔记的关系

| 维度 | Get 笔记 | GBrain |
|------|---------|--------|
| **定位** | 知识库 + 语义搜索 | AI Agent 记忆 |
| **使用者** | 人类 + AI | AI Agent 为主 |
| **集成** | API | MCP + CLI |
| **自动流入** | ❌ 手动 | ✅ 邮件/日历/推特/语音 |
| **实体检测** | ❌ | ✅ 自动 |
| **反向链接** | ❌ | ✅ 自动 |

**建议**：
- Get 笔记 → 人类主导的知识库
- GBrain → AI Agent 的长期记忆
- 两者可并存，GBrain 更适合 AI 原生场景

---

## 📚 相关资源

### 官方文档

- **GitHub**: https://github.com/garrytan/gbrain
- **Skillpack**: `docs/GBRAIN_SKILLPACK.md`（最重要的文档）
- **集成指南**: `docs/integrations/README.md`
- **Cron 调度**: `docs/guides/cron-schedule.md`
- **语音集成**: `recipes/twilio-voice-brain.md`

### Garry Tan 推文

- **发布推文**: https://x.com/garrytan/status/2043022208512172263
- **语音演示**: 同上

---

## 🔮 未来展望

### GBrain 可能的演进

1. **更多集成**
   - WhatsApp/Telegram
   - Zoom/Teams 转录
   - Slack/Discord

2. **多模态记忆**
   - 图片识别
   - 视频内容提取
   - 音频嵌入

3. **协作功能**
   - 团队大脑
   - 共享记忆
   - 权限管理

4. **与 gstack 整合**
   - 工程记忆 + 代码流程
   - 完整 AI 原生工作流

---

## 📝 总结

### GBrain 是什么？

**Garry Tan 的 AI Agent 记忆管理系统**，让 AI：
- 记住你的一切（人物/公司/会议/想法）
- 每次对话前读取上下文
- 每次对话后写入新信息
- 每天都变得更聪明

---

### 核心价值

> "没有这个循环的 Agent 从过时的上下文回答。有这个循环的 Agent 每次对话都更聪明。差异每天复合增长。"

---

### 是否适合你？

**✅ 强烈建议尝试**，因为：
- 你是 OpenClaw 用户（天然适配）
- 免费起步（PGLite 本地）
- 刚发布（早期采用者优势）
- Garry Tan 亲自维护（质量保证）

---

*最后更新：2026-04-13*  
*参考资料：https://github.com/garrytan/gbrain*
