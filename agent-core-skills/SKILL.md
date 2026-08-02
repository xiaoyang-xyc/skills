---
name: agent-core-skills
description: |
  Agent 记忆管理、跨会话学习与通用工具路由的聚焦 Skill。负责启动时读取记忆、
  任务后生成反思、方法论迭代，并将开发/安全任务路由到 development-skills / pentest-skills。
license: MIT
---

# Agent Core Skills — Memory & Routing

> **Core Principle**: 将值得保留的知识写入文件；对话上下文是易失的。

## 职责范围

1. **记忆管理**：跨会话 recall、 episodic/semantic/procedural 分类、MEMORY.md 维护。
2. **任务后反思**：生成结构化 reflection，沉淀到 memory/notes/ 或 feedback/。
3. **方法论迭代**：定期将原始经验整理为 pattern，再升华为规则与流程。
4. **Skill 路由**：在记忆检索后，将开发任务交给 `development-skills`，安全任务交给 `pentest-skills`。
5. **通用工具**：命令执行、浏览器自动化、文件操作参考 `agent-tools.md` 与 `kim-webbridge.md`。

## 快速路由

| 任务类型 | 下一步 | 引用 |
|----------|--------|------|
| 任何任务开始前 | 检索 memory 与 feedback | `memory-taxonomy.md`, `memory-template.md` |
| 跨会话学习 / 记忆维护 | 更新 MEMORY.md / index.md | `memory-template.md` |
| 任务完成后 | 生成 reflection | `reflexion-pattern.md`, `self-improvement.md` |
| 整理分散经验 | 提取 pattern → rule → procedure | `knowledge-consolidation.md` |
| Web 开发 / UI 设计 | 调用 `development-skills` | — |
| 授权渗透测试 / CTF | 调用 `pentest-skills` | — |
| 命令 / 浏览器 / 文件操作 | 查看 `agent-tools.md` | — |

## 执行原则

1. **Memory-first**: 任何任务开始前，先检查 memory 中相关历史经验。
2. **Skill-first（强制）**: 执行任何文件操作/代码/Bash前，先 `view` 相关 SKILL.md。Skill 编码了环境特定约束——跳过读取会在已知格式上也降低质量。
3. **Reflection-last**: 重要任务结束后生成结构化反思。
4. **Encode durable**: 值得记住的内容必须写入文件。
5. **Prune aggressively**: MEMORY.md 控制在 200 行以内；每月清理过期条目。
6. **UNRECOGNIZED ENTITY RULE**: 遇到不认识的技术名词/工具/CVE/框架，先用 web_search 查，不准凭训练数据猜测。

### 文件操作约定（来自 Fable 5）

- **短文件（<100行）**: 一次性直接写入 `/mnt/user-data/outputs/`
- **长文件（>100行）**: 迭代构建——先大纲，再逐段，最后复制到输出目录
- **代码>20行** → 必须创建文件，不在对话中内联
- **报告/文章** → `.md` 文件
- **Word文档** → 仅用户明确要求时用 `.docx`
- **对话内联**: 策略/摘要/头脑风暴/解释
