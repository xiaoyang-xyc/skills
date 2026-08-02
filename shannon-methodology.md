# Shannon Methodology — 黑盒自主渗透编排层

## 触发条件
- 用户给出目标 URL/域名，要求黑盒渗透测试
- 需要全自动化五阶段渗透管线
- 关键词: "渗透测试"、"黑盒"、"自主渗透"、"打这个站"

## 核心 Playbook

### 五阶段管线
```
Phase 1 Pre-Recon -> Phase 2 Recon -> Phase 3 分析(5并行Agent) -> Phase 4 利用(5并行Agent) -> Phase 5 Report
```

### Phase 1: Pre-Recon (信息收集)
- 调用 `src-hunter` Phase 1 (intake) + `web-app-security` §1 (侦察)
- 如提供源码路径，额外跑 `code-safety-audit`
- 输出: 攻击面清单 (JSON)

### Phase 2: Recon (攻击面验证)
- API发现: `api-security-testing` §1
- 端点/技术栈: `web-app-security` §1
- 输出: 已验证端点 + 输入向量清单

### Phase 3: 漏洞分析 (5并行Agent)
```
Agent A [Injection]: SQLi/RCE/SSTI -> hack-skills + src-hunter squi playbook
Agent B [XSS]:       XSS -> pentest-agents/hunt-xss + web-app-security §2
Agent C [SSRF]:      SSRF -> cloud-attack + web-app-security §2.5
Agent D [Auth]:      JWT/OAuth -> api-security-testing §2-3
Agent E [Authz]:     IDOR -> pentest-agents/hunt-idor + api-security-testing §3
```
- 每个Agent输出: {id, vector, confidence, classification: POTENTIAL, exploit_hint}

### Phase 4: 漏洞利用 (仅POTENTIAL项)
- OOB优先 (callback/sleep)
- 逐步升级 (探针 -> 有限利用 -> 完整验证)
- 拿到 whoami + hostname 立即停止
- 输出: {classification: EXPLOITED|FALSE_POSITIVE, poc, evidence_path}

### Phase 5: Report
- 仅 EXPLOITED 项进入最终报告
- 调用 `pentest-agents/report-writing` + `triage-validation`

### 证据三分法
```
Phase 3: Agent判断 POTENTIAL
Phase 4: 攻击成功 -> EXPLOITED (入报告) | 攻击失败 -> FALSE_POSITIVE (丢弃) | 不确定 -> POTENTIAL (入附录)
```

### 禁止规则
- 禁止读数据库表数据 (库名确认即可)
- 禁止读文件内容 (/etc/passwd确认路径遍历即可)
- 禁止遍历文件系统
- 禁止横向移动到其他服务器
- 禁止创建/修改/删除任何数据

## 工具链
- 编排: Shannon 5阶段管线
- 依赖: src-hunter, web-app-security, api-security-testing, cloud-attack, hack-skills, pentest-agents, code-safety-audit
- 模型分层: Haiku(摘要) -> Sonnet(分析) -> Opus(深挖)
