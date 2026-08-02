---
name: self-improvement
description: |
  一个用于 AI Agent 自我学习与持续改进的 Skill。每次完成渗透测试、代码审计、CTF 挑战或其他安全任务后，
  主动复盘方法论、工具链与绕过技巧，将可复用的经验沉淀到 `skills/final-pentest/SKILL.md` 中，
  形成不断进化的个人知识库。
category: meta-learning
tags:
  - self-improvement
  - lessons-learned
  - playbook
  - knowledge-management
user-invocable: true
---

# Self-Improvement — 自我学习与知识沉淀

## 触发时机

当用户说出以下任意意图时，激活本 Skill：

- “总结/复盘这次测试”
- “把经验加到最终渗透 Skill”
- “完善我的渗透知识库”
- “记录教训/技巧/TTP”
- “自我学习/持续改进”

## 核心流程

### 1. 复盘最近一次任务

读取当前会话上下文、MEMORY.md、操作日志以及最终交付物，回答以下问题：

- **目标环境**：目标系统、技术栈、防护设施（WAF、CDN、EDR、RASP 等）。
- **信息收集**：哪些渠道/工具最有效？哪些漏掉了？
- **漏洞发现**：每个漏洞的发现路径、验证方式、可利用性、风险等级。
- **绕过技巧**：WAF/参数校验/过滤器的绕过手法，哪些成功、哪些失败。
- **工具表现**：AutoRedTeam、ScareAISec、SQLMap、Burp 插件等是否达到预期？
- **失误与卡点**：哪些步骤低效？哪些误判？哪些依赖外部条件？
- **输出质量**：报告、PoC、CVE/CNVD 材料是否完整、合规、可复现？

### 2. 提取可复用知识

将复盘结果抽象为以下类型：

| 类型 | 示例 |
|---|---|
| 通用方法论 | 信息收集顺序、最小权限验证原则、无害化 PoC 设计 |
| 目标指纹 | 某 CMS 的默认路径、某 WAF 的拦截特征、某框架的已知弱点 |
| 绕过 Payload | 针对特定 WAF 的编码/分块/JSON 包裹绕过 |
| 工具配置 | AutoRedTeam/ScareAISec 的模型选择、Base URL、提示词模板 |
| 报告模板 | 风险描述、影响范围、修复建议、CVE 提交材料格式 |

### 3. 更新最终渗透 Skill

将提取的知识追加或整合到 `skills/final-pentest/SKILL.md` 的对应章节：

- `methodology/` — 流程与原则
- `targets/` — 目标指纹与历史案例
- `bypasses/` — WAF/过滤绕过技巧
- `tools/` — 工具配置与最佳实践
- `reporting/` — 报告与提交材料模板
- `lessons/` — 按时间排序的教训日志

更新时遵循：

- **不重复**：已有知识点只补充差异与验证细节。
- **可验证**：每个技巧注明测试目标、成功/失败状态、限制条件。
- **可追溯**：标注发现日期与对应任务/会话。

### 4. 更新 MEMORY.md 与索引

- 在 `MEMORY.md` 中追加“本次改进点”。
- 若新增 Skill 或修改关键结构，更新 `skills/SKILL_INDEX.md`。

### 5. 备份到服务器

服务器可访问时，将以下文件同步到 `/opt/skills-backup/` 或用户指定的备份目录：

- `MEMORY.md`
- `skills/` 目录
- 操作日志与关键脚本

## 输出格式

每次激活后输出：

1. 复盘摘要（3-5 条要点）。
2. 已沉淀到 `final-pentest` 的知识点列表。
3. 待验证/待补充项（如需后续测试确认）。
4. 备份状态。
