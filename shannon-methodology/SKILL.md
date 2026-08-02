---
name: shannon-methodology
description: Shannon式自主渗透编排层 — 五阶段管线、5+5并行Agent、EXPLOITED/POTENTIAL/FALSE_POSITIVE三分法、"No Exploit No Report"零假阳性。技术细节路由到现有Skill。
user-invocable: true
---

# Shannon Methodology — 渗透测试编排层

> 基于 Keygraph Shannon (34K★, 96.15% XBOW) | 编排层——技术细节由现有 Skill 承载

## 核心价值（本 Skill 独有）

| 能力 | 说明 |
|------|------|
| **五阶段管线** | Pre-Recon → Recon → 分析(5并行) → 利用(5并行) → 报告 |
| **证据三分法** | EXPLOITED / POTENTIAL / FALSE_POSITIVE |
| **No Exploit, No Report** | 打不下来的漏洞不入最终报告 |
| **5+5 Agent Swarm** | 同一类漏洞的分析和利用Agent异步流水线 |
| **模型分层** | Haiku 4.5(摘要) → Sonnet 4.6(分析) → Opus 4.7(深挖) |

---

## §1 五阶段管线总览

```
Phase 1        Phase 2        Phase 3               Phase 4               Phase 5
Pre-Recon  →  Recon      →  漏洞分析(5并行)    →  漏洞利用(5并行)    →  Report
信息收集      攻击面验证      Injection/XSS/        真实攻击验证          去重+PoC
                              SSRF/Auth/Authz       (仅POTENTIAL项)
│              │              │                     │                    │
▼ 路由到       ▼ 路由到       ▼ 路由到              ▼ 路由到             ▼ 路由到
src-hunter    api-security   hack-skills           Playwright/curl       report-writing
web-app-sec   web-app-sec    web-app-security      实际攻击执行          triage-validation
              pentest-agents pentest-agents        验证和分类
                             cloud-attack
                             api-security
```

---

## §2 编排指令模板

### 2.1 完整模式（白盒+黑盒）

```
"对 [目标] 执行 Shannon 五阶段自主渗透测试。

Phase 1 — Pre-Recon:
  → 调用 src-hunter Phase 1 (intake) + web-app-security §1
  → 如果提供源码路径 [path]，额外做: code-safety-audit (依赖+密钥+OWASP)
  输出: 攻击面清单 (JSON)

Phase 2 — Recon:
  → 调用 api-security-testing §1 (API发现)
  → 调用 web-app-security §1 (端点/技术栈)
  → 调用 pentest-agents/recon-methodology
  输出: 已验证端点+输入向量清单 (JSON)

Phase 3 — 漏洞分析(5并行Agent):
  Agent A [Injection]: → hack-skills + src-hunter (SQLi/RCE/SSTI playbook)
  Agent B [XSS]:       → pentest-agents/hunt-xss + web-app-security (XSS)
  Agent C [SSRF]:      → cloud-attack + web-app-security (SSRF)
  Agent D [Auth]:      → api-security-testing §2-3 + pentest-agents/hunt-oauth
  Agent E [Authz]:     → pentest-agents/hunt-idor + api-security-testing §3
  每个Agent输出: {id, vector, confidence, classification: POTENTIAL, exploit_hint}

Phase 4 — 漏洞利用(仅对POTENTIAL项):
  对每个POTENTIAL发现启动验证Agent:
  - OOB优先 (callback/sleep)
  - 逐步升级 (探针→有限利用→完整验证)
  - 拿到 whoami + hostname 立即停止
  输出: {classification: EXPLOITED|FALSE_POSITIVE, poc, evidence_path}

Phase 5 — Report:
  → 调用 pentest-agents/report-writing
  → 调用 pentest-agents/triage-validation (去重+严重性复核)
  → 仅 EXPLOITED 项进入最终报告
  输出: 渗透测试报告 (含可复现PoC)

授权范围: [明确边界]
模式: [完整(yolo) | 保守(confirm)]
"
```

### 2.2 快速模式（跳过 Phase 1）

```
"对 [目标] 执行 Shannon 快速扫描:
 技术栈已知为 [stack]，跳过 Pre-Recon，直接从 Phase 2 开始。
 ...
"
```

### 2.3 纯白盒模式（仅代码审计，不接触线上）

```
"对 [源码路径] 执行 Shannon 白盒审计:
 Phase 1 → code-safety-audit + [pentest-agents/sast-methodology]
 Phase 3 → 仅静态分析，不执行任何网络请求
 Phase 5 → 输出代码审计报告
"
```

---

## §3 证据分类标准（三次判定）

```
Phase 3 分析结果:              Phase 4 验证后:            Phase 5 最终:
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Agent 判断      │  →   │ 实际攻击验证    │  →   │ 入报告判定      │
│                 │      │                 │      │                 │
│ "POTENTIAL"     │      │ 攻击成功        │      │ "EXPLOITED"     │
│ (进入Phase 4)   │      │ → EXPLOITED     │      │ → 入最终报告    │
│                 │      │                 │      │                 │
│                 │      │ 攻击失败        │      │                 │
│                 │      │ → FALSE_POSITIVE │      │ (不出现在报告中)│
│                 │      │                 │      │                 │
│                 │      │ 不确定          │      │                 │
│                 │      │ → POTENTIAL     │      │ → Potential     │
│                 │      │                 │      │   Issues 附录   │
└─────────────────┘      └─────────────────┘      └─────────────────┘

核心原则: Phase 4 之后仍是 POTENTIAL 的 → 不入报告正文，入附录"潜在问题"
           Phase 4 成功 = EXPLOITED → 入报告正文，附完整PoC
           Phase 4 确认为误报 = FALSE_POSITIVE → 丢弃
```

---

## §4 Agent Swarm 编排模式

### 4.1 5+5 并行（标准模式）

```
Phase 3 (5 Agent 并行分析)
  │
  ├── Agent A(Injection)完成 ──→ Agent A'(Injection利用)启动
  ├── Agent B(XSS)完成       ──→ Agent B'(XSS利用)启动
  ├── Agent C(SSRF)完成      ──→ Agent C'(SSRF利用)启动
  ├── Agent D(Auth)完成      ──→ Agent D'(Auth利用)启动
  └── Agent E(Authz)完成     ──→ Agent E'(Authz利用)启动
                                   │
                                   └──→ 全部汇总 → Phase 5 Report

优势: Agent A'在A完成后立即启动，不等B/C/D/E
```

### 4.2 模型分层

| 模型 | 用途 | 调用场景 |
|------|------|---------|
| Haiku 4.5 | Phase 1摘要, Phase 2响应解析, Phase 5去重 | 大量重复性处理 |
| Sonnet 4.6 | Phase 3漏洞分析, Phase 5报告撰写 | 主分析引擎 |
| Opus 4.7 | Phase 4关键漏洞(CRITICAL/HIGH)深度利用 | 仅最难的利用场景 |

---

## §5 停止规则（全局适用）

```
所有 Agent 必须遵守:

□ 拿到 whoami + hostname + 环境信息 → 立即停止，报告成功
□ OOB callback 收到 → 立即停止 (SSRF/RCE 验证完成)
□ SQL注入提取到库名 → 立即停止 (SQLi 验证完成)
□ alert()弹出 → 立即停止 (XSS 验证完成)
□ JWT签名绕过成功 → 立即停止

禁止:
✗ 读取数据库表数据 (库名确认即可)
✗ 读取文件内容 (/etc/passwd 确认路径遍历即可)
✗ 遍历文件系统
✗ 横向移动到其他服务器
✗ 创建/修改/删除任何数据
✗ 使用真实用户凭据进行测试
✗ 窃取Cookie/Token/Session
```

---

## §6 与现有 Skill 的分工

```
shannon-methodology (编排层——本文件)
│
├── Phase 1 技术实现 → src-hunter (recon phase)
│                       web-app-security §1
│
├── Phase 2 技术实现 → api-security-testing §1
│                       pentest-agents/recon-methodology
│
├── Phase 3 技术实现 → hack-skills (SQLi/WAF绕过)
│   Agent A:          src-hunter/playbooks/sqli
│   Agent B:          pentest-agents/hunt-xss
│   Agent C:          cloud-attack
│   Agent D:          api-security-testing §2-3
│   Agent E:          pentest-agents/hunt-idor
│
├── Phase 4 验证执行 → Playwright / curl / 自定义脚本
│                       (由编排层直接控制，不路由到其他Skill)
│
├── Phase 5 技术实现 → pentest-agents/report-writing
│                       pentest-agents/triage-validation
│
└── 代码审计(可选)   → code-safety-audit
                        src-hunter (sast-methodology)
```

**本 Skill 不重复的内容**（直接路由到对应 Skill）：
- 具体 Payload 库 → `hack-skills`, `src-hunter`
- 漏洞攻击技术细节 → `web-app-security`, `api-security-testing`
- 工具使用教程 → `pentest-agents`, `pentest-tools`
- 报告格式模板 → `pentest-agents/report-writing`

**本 Skill 独有且不重复的内容**：
- 五阶段流水线编排逻辑
- 5+5 Agent 并行调度模式
- EXPLOITED/POTENTIAL/FALSE_POSITIVE 三分法
- No Exploit, No Report 执行纪律
- 模型分层策略
- 全局停止规则

---

> **参考**: Keygraph Shannon, XBOW Benchmark, Anthropic Agent SDK | 2026
