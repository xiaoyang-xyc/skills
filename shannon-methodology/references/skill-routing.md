# Shannon Agent → 现有 Skill 路由表

> 本文件是编排层的路由索引。Shannon 的 5 个分析 Agent 不包含漏洞技术细节——所有 Payload、工具、方法都在已有的 Skill 中。

## Phase 3 Agent 路由

| Shannon Agent | 漏洞类型 | 首选 Skill | 具体章节/文件 |
|---|---|---|---|
| **Agent A: Injection** | SQL注入 | `hack-skills` + `src-hunter` | src-hunter: `references/playbooks/sqli.md` |
| | 命令注入 | `src-hunter` | `references/playbooks/rce.md` |
| | SSTI | `web-app-security` | §4 XXE/SSTI |
| | NoSQL/LDAP | `api-security-testing` | §4 Injection |
| **Agent B: XSS** | 反射/存储/DOM | `pentest-agents/hunt-xss` | SKILL.md 全文 |
| | mXSS | `web-app-security` | §2 XSS |
| | 原型污染→XSS | `web-app-security` | §8 原型污染 |
| **Agent C: SSRF** | SSRF基础 | `web-app-security` | §6 SSRF |
| | 云Metadata | `cloud-attack` | §1 SSRF→Metadata |
| | Gopher/协议走私 | `cloud-attack` | §2 协议利用 |
| | URL跳转链 | `src-hunter` | `references/playbooks/ssrf.md` |
| **Agent D: Auth** | JWT攻击 | `api-security-testing` | §2 Authentication |
| | 暴力破解/限流 | `api-security-testing` | §5 Rate Limit |
| | OAuth/SAML | `pentest-agents/hunt-oauth` | SKILL.md 全文 |
| | MFA绕过 | `api-security-testing` | §2 Authentication |
| **Agent E: Authz** | IDOR | `pentest-agents/hunt-idor` | SKILL.md 全文 |
| | Mass Assignment | `api-security-testing` | §7 Mass Assign |
| | 路径遍历 | `web-app-security` | §7 路径遍历 |
| | 权限提升 | `pentest-agents/hunt-business-logic` | SKILL.md 全文 |

## Phase 1/2/5 路由

| Shannon Phase | 功能 | 首选 Skill |
|---|---|---|
| Phase 1 信息收集 | 端口/子域/技术栈 | `src-hunter` (recon phase) + `web-app-security` §1 |
| Phase 1 源码审计 | SAST/密钥/OWASP | `code-safety-audit` |
| Phase 2 端点验证 | API文档/存活检测 | `api-security-testing` §1 + `pentest-agents/recon-methodology` |
| Phase 5 报告撰写 | 模板/格式 | `pentest-agents/report-writing` |
| Phase 5 去重复核 | 严重性/证据 | `pentest-agents/triage-validation` |

## Agent 输出标准

所有 Phase 3 Agent 统一输出格式：

```json
{
  "agent": "injection|xss|ssrf|auth|authz",
  "findings": [{
    "id": "TYPE-NNN",
    "endpoint": "完整URL+参数",
    "vector": "漏洞类型(如SQLi-BooleanBlind)",
    "probe_used": "触发探针Payload",
    "confidence": "high|medium|low",
    "classification": "POTENTIAL",
    "routing_to": "Phase 4 验证方法的简短提示"
  }]
}
```

Phase 4 验证后附加：
```json
{
  "classification": "EXPLOITED|FALSE_POSITIVE",
  "poc": "可复现的命令/脚本",
  "evidence_path": "截图/日志文件路径",
  "severity": "critical|high|medium|low"
}
```
