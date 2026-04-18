# gstack - Garry Tan 的 AI 工程团队系统

**整理时间**: 2026-04-13  
**项目地址**: https://github.com/garrytan/gstack  
**发布者**: Garry Tan (YC President & CEO)  
**状态**: ✅ 已开源 (MIT License)

---

## 📊 项目概览

| 指标 | 数据 |
|------|------|
| **Stars** | 71,300+ |
| **Forks** | 10,000+ |
| **许可证** | MIT (免费开源) |
| **发布时间** | 2026 年初 |
| **语言** | TypeScript |

---

## 🎯 gstack 解决了什么问题？

### 核心问题

**一个人如何像 20 个人的团队一样高效开发？**

Garry Tan 的答案：
> "2026 年，我 60 天内生产了 60 万行代码（35% 是测试），每天 1-2 万行，还是兼职做 YC 全职工作的同时。"

**关键差异**: 工具链（Tooling）

---

### gstack 的核心价值

把 **Claude Code** 变成一个**虚拟工程团队**：

| 角色 | 技能命令 | 功能 |
|------|----------|------|
| 🧑‍💼 **CEO** | `/plan-ceo-review` | 重新思考问题，找到 10 倍产品 |
| 👨‍💻 **工程师** | `/plan-eng-review` | 锁定架构、数据流、边界情况 |
| 🎨 **设计师** | `/plan-design-review` | 设计评审，AI Slop 检测 |
| 🔍 **审查员** | `/review` | 找出生产级 bug |
| 🧪 **QA** | `/qa` | 真实浏览器测试 |
| 🔒 **安全官** | `/cso` | OWASP + STRIDE 审计 |
| 🚀 **发布工程师** | `/ship` | 自动 PR、测试、部署 |

---

## 🛠️ 23 个核心技能工具

### 📋 规划阶段

| 技能 | 说明 |
|------|------|
| **/office-hours** | YC Office Hours 风格，6 个强制问题重新定义产品 |
| **/plan-ceo-review** | CEO 视角，4 种模式（扩展/选择性扩展/保持/缩减） |
| **/plan-eng-review** | 工程师视角，ASCII 图、状态机、测试矩阵 |
| **/plan-design-review** | 设计师视角，0-10 分评分，AI Slop 检测 |
| **/plan-devex-review** | 开发者体验评审，20-45 个强制问题 |

---

### 🎨 设计阶段

| 技能 | 说明 |
|------|------|
| **/design-consultation** | 从零构建完整设计系统 |
| **/design-shotgun** | 生成 4-6 个 AI 原型变体，对比选择 |
| **/design-html** | 将原型转为可生产 HTML（30KB，零依赖） |
| **/design-review** | 设计审计 + 自动修复 |

---

### 🔍 审查阶段

| 技能 | 说明 |
|------|------|
| **/review** | 员工级代码审查，自动修复简单问题 |
| **/investigate** | 系统性根因调试（Iron Law: 不调查不修复） |
| **/devex-review** | 真实开发者体验审计，截图 + 计时 |
| **/cso** | 首席安全官，OWASP Top 10 + STRIDE 威胁模型 |

---

### 🧪 测试阶段

| 技能 | 说明 |
|------|------|
| **/qa** | 真实浏览器测试，发现并修复 bug |
| **/qa-only** | 仅报告 bug，不修改代码 |
| **/benchmark** | 性能基准测试（Core Web Vitals） |

---

### 🚀 发布阶段

| 技能 | 说明 |
|------|------|
| **/ship** | 同步、测试、推送、开 PR |
| **/land-and-deploy** | 合并、等待 CI、部署、验证 |
| **/canary** | 部署后监控（控制台错误、性能回归） |
| **/document-release** | 自动更新文档匹配新代码 |

---

### 🔄 反思阶段

| 技能 | 说明 |
|------|------|
| **/retro** | 每周工程回顾，按人分解、测试健康度趋势 |
| **/learn** | 从错误中学习，建立知识库 |

---

### 🔧 工具类

| 技能 | 说明 |
|------|------|
| **/browse** | 真实 Chromium 浏览器，~100ms/命令 |
| **/connect-chrome** | 连接你的 Chrome 浏览器 |
| **/setup-browser-cookie** | 配置浏览器 Cookie |
| **/pair-agent** | 多 Agent 协调器，共享浏览器 |

---

## 🏗️ 架构设计

### 核心流程

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

**每个阶段都有专门的技能**，环环相扣：
- `/office-hours` 写的设计文档 → `/plan-ceo-review` 读取
- `/plan-eng-review` 写的测试计划 → `/qa` 使用
- `/review` 发现的 bug → `/ship` 验证修复
- **没有遗漏，因为每一步都知道前一步做了什么**

---

### 技术栈

| 组件 | 技术 |
|------|------|
| **基础平台** | Claude Code (Anthropic) |
| **脚本语言** | TypeScript |
| **运行时** | Bun v1.0+ / Node.js |
| **浏览器** | Chromium (通过 MCP) |
| **安装位置** | `~/.claude/skills/gstack/` |

---

## 📦 安装方式

### 快速安装（30 秒）

```bash
# 克隆到 Claude Skills 目录
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack

# 运行安装脚本
cd ~/.claude/skills/gstack && ./setup
```

### 团队安装

```bash
# 全局安装（自动更新）
cd ~/.claude/skills/gstack && ./setup --team

# 在当前项目启用
cd <your-repo>
~/.claude/skills/gstack/bin/gstack-team-init required
git add .claude/ CLAUDE.md && git commit -m "require gstack for AI-assisted work"
```

---

## 💬 使用示例

### 场景 1: 从想法到上线

```
你：我想做一个日历每日简报应用

你：/office-hours
Claude: [问 6 个强制问题，重新定义产品]
你：多个 Google 日历，信息过时，位置错误...
Claude: 你实际需要的不是简报应用，而是"个人首席助理 AI"
       [提出 3 种实现方案，建议从最小可行产品开始]

你：/plan-ceo-review
[重新思考范围，输出 10 部分评审]

你：/plan-eng-review
[ASCII 数据流图、状态机、测试矩阵]

你：批准计划，退出规划模式

[Claude 自动编写 2400 行代码，11 个文件，8 分钟]

你：/review
[自动修复 2 个问题，询问 1 个竞态条件]

你：/qa https://staging.myapp.com
[打开真实浏览器，测试流程，发现并修复 bug]

你：/ship
测试：42 → 51 (+9 个新测试)
PR: github.com/you/app/pull/42
```

**8 个命令，端到端完成**。这不是 Copilot，这是一个团队。

---

### 场景 2: 安全审计

```
你：/cso

[运行 OWASP Top 10 + STRIDE 威胁模型]
[零噪音：17 个误报排除，8/10+ 置信度门槛]
[每个发现包含具体利用场景]

输出：
🔴 高危：XSS 漏洞（利用场景：攻击者可注入...）
🟡 中危：缺少 CSRF 保护
🟢 低危：信息泄露风险
```

---

### 场景 3: 每周回顾

```
你：/retro

生成本周回顾：
- 提交数：362
- 新增代码：140,751 行
- 测试覆盖率：35% → 42%
- 发现问题：23 个，修复：21 个
- 连续 shipping 天数：14 天
```

---

## 🔗 与 OpenClaw 集成

gstack 支持 **8 个 AI 编码 Agent**：

| Agent | 安装标志 |
|-------|---------|
| **Claude Code** | 默认 |
| **OpenAI Codex CLI** | `--host codex` |
| **OpenCode** | `--host opencode` |
| **Cursor** | `--host cursor` |
| **Factory Droid** | `--host factory` |
| **Slate** | `--host slate` |
| **Kiro** | `--host kiro` |
| **OpenClaw** | 自动检测 |

---

### OpenClaw 配置

在你的 `AGENTS.md` 中添加：

```markdown
## Coding Tasks

当spawn Claude Code 会话进行编码工作时，使用 gstack 技能：

- 安全审计："Load gstack. Run /cso"
- 代码审查："Load gstack. Run /review"
- QA 测试："Load gstack. Run /qa https://..."
- 构建功能："Load gstack. Run /autoplan → implement → /ship"
- 规划："Load gstack. Run /office-hours then /autoplan"
```

---

## 🎯 适合你吗？

### ✅ 适合的场景

如果你：

1. **使用 AI 编程工具**（Claude Code、Codex 等）
2. **想要系统化工作流**（不是随机对话）
3. **需要生产级质量**（测试、审查、安全）
4. **一个人开发**（需要虚拟团队）
5. **创始人/技术负责人**（想要快速迭代）

---

### ❌ 可能不适合

如果你：

1. **偶尔用 AI**（不需要复杂流程）
2. **已有成熟团队**（流程已固定）
3. **不想学习新工具**（有学习曲线）
4. **只用 AI 做简单任务**（杀鸡用牛刀）

---

## 📊 与 AI 记忆系统的关系

### gstack **不是**记忆管理系统

**gstack 解决的是工程流程问题**，不是记忆存储问题：

| 维度 | gstack | AI 记忆系统（如 Mem0） |
|------|--------|----------------------|
| **核心功能** | 工程流程自动化 | 跨会话记忆存储 |
| **持久化** | 项目文件（CLAUDE.md） | Vector DB |
| **检索** | 文件读取 | 语义搜索 |
| **适用场景** | 代码开发 | 对话历史、用户偏好 |

---

### 但 gstack **包含**记忆元素

1. **CLAUDE.md** - 项目级记忆
   - 编码标准
   - 架构决策
   - 偏好设置

2. **Auto Memory** - 自动学习
   - 构建命令
   - 调试经验
   - 跨会话知识

3. **/retro** - 团队记忆
   - 每周回顾
   - 经验教训
   - 改进建议

---

## 🎯 我的建议

### 是否适合你？

**值得尝试**，原因：

1. **已验证的效果**
   - Garry Tan 本人每天使用
   - 60 天 60 万行代码（35% 测试）
   - 71k+ stars 社区认可

2. **与现有工具兼容**
   - 基于 Claude Code
   - 支持 8 个 Agent
   - 可与 Get 笔记并存

3. **开源免费**
   - MIT License
   - 无订阅费
   - 社区持续贡献

4. **系统化方法**
   - 不是零散工具
   - 完整工程流程
   - 可学习可复制

---

### 建议的尝试方式

**第 1 周**：
```bash
# 安装
git clone --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup

# 试用 3 个核心技能
/office-hours   # 规划新产品
/review         # 审查现有代码
/qa             # 测试网页
```

**第 2-4 周**：
- 深度使用 `/ship` 自动化发布
- 尝试 `/cso` 做安全审计
- 每周运行 `/retro` 回顾

**评估标准**：
- 是否提高了效率？
- 是否减少了 bug？
- 是否愿意继续使用？

---

## 📚 相关资源

### 官方资源

- **GitHub**: https://github.com/garrytan/gstack
- **Garry Tan Twitter**: https://twitter.com/garrytan
- **文档**: https://github.com/garrytan/gstack/tree/main/docs

### 类似项目对比

| 项目 | 定位 | 差异 |
|------|------|------|
| **gstack** | 工程流程自动化 | 完整团队模拟 |
| **Mem0** | AI 记忆层 | 专注记忆存储 |
| **LangChain** | AI 应用框架 | 更底层，需自建 |
| **Cursor** | AI 优先 IDE | 编辑器集成 |

---

## 🔮 未来展望

### gstack 可能的演进方向

1. **记忆系统集成**
   - 可能与 Mem0 等合作
   - 增加跨项目记忆
   - 个性化学习

2. **更多 Agent 支持**
   - 目前 8 个，可能扩展到 15+
   - 统一技能接口

3. **企业功能**
   - 团队协作
   - 审计日志
   - 合规性检查

---

*最后更新：2026-04-13*  
*参考资料：https://github.com/garrytan/gstack*
