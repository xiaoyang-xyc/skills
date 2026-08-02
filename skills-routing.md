# 技能路由表

> 渗透测试技能库路由索引 | 按攻击面自动分发
> 来源: ~/.kimi-code/memory/tools/skills/

---

## 技能架构（三层）

```
Layer 1: 编排层（选一个）
  pentest-skills → 统一入口，自动路由到 shannon / cve-yu2 / src-hunter

Layer 2: 战术层（按攻击面自动加载）
  web-app-security  api-security-testing  cloud-attack  red-team-ai
  hack-skills       pentest-agents        web-pentest-sample

Layer 3: 工具层
  code-safety-audit  smart-web-scraper
```

---

## 遇到什么攻击面 -> 调用什么技能

### 编排层选择（三选一）

| 任务场景 | 技能 | 核心要点 |
|---------|------|----------|
| 给 URL/域名，黑盒渗透，拿 Shell/数据 | `shannon-methodology` | 5阶段管线 + 5+5 Agent并行 + No Exploit No Report |
| 给源码/仓库，白盒审计，找 CVE 级漏洞 | `cve-yu2` | Source->Sink追踪 + 反幻觉 + P0-P3评分 + WooYun 88,636案例 |
| Bug Bounty / SRC 众测挖洞 | `src-hunter` | 5阶段checkpoint + 19 playbooks + 2,887 H1真实案例 |

### 战术层路由

| 攻击面 | 技能 | 核心要点 |
|--------|------|----------|
| REST / Swagger / GraphQL API | `api-security-testing` | Discovery -> Auth -> IDOR -> Injection -> RateLimit, OWASP API Top 10 |
| Web 应用 (XSS/CSRF/SQLi/XXE) | `web-app-security` | 三柱法 Recon->Offense->Defense, 28 SSRF参数, 反序列化指纹 |
| 云平台 (AWS/阿里云/Azure/GCP/K8s) | `cloud-attack` | SSRF->Metadata->凭证窃取->横向移动->持久化, 11种IP编码绕过 |
| AI 红队 / C2 / AD域 / 后渗透 | `red-team-ai` | AI辅助侦察, C2隐蔽通道, AD Kerberoasting/DCSync, 8种免杀 |
| SQL注入 / WAF绕过 (深度) | `hack-skills` | 263 WAF绕过变体, 按DB类型区分playbook, Ghost Bits字符集攻击 |
| 渗透工具链 (Burp式CLI) | `web-pentest-sample` | 12个CLI工具, 6阶段测试, SQLite项目数据库, OWASP 50+用例 |
| 渗透Agent自动化框架 | `pentest-agents` | 50 agents + 26 commands + 19 CLI tools, 5阶段hunt管线 |
| 代码安全自动扫描 | `code-safety-audit` | 3层扫描: 依赖CVE + 密钥泄露(Shannon熵) + OWASP反模式 |
| Web 爬虫 / OSINT 信息收集 | `smart-web-scraper` | Playwright隐身模式绕过Cloudflare, 动态渲染抓取 |

### 按漏洞类型速查

| 漏洞类型 | 首选技能 | 备选 |
|---------|---------|------|
| SQL 注入 | `web-app-security` §2.3 | `hack-skills` sqli |
| XSS | `web-app-security` §2.1 | `hack-skills` xss |
| IDOR / BOLA | `api-security-testing` §3 | `hack-skills` idor |
| JWT 攻击 | `api-security-testing` §2 | `hack-skills` jwt-oauth |
| SSRF | `cloud-attack` §1-2 + `web-app-security` §2.5 | `hack-skills` ssrf |
| XXE | `web-app-security` §2.4 | `hack-skills` xxe |
| 命令注入 / RCE | `web-app-security` §2 + `red-team-ai` §2 | `hack-skills` cmdi |
| 反序列化 | `web-app-security` §2.6 | `hack-skills` deserialization |
| SSTI | `api-security-testing` §4.3 | `hack-skills` ssti |
| Mass Assignment | `api-security-testing` §7 | - |
| GraphQL 攻击 | `api-security-testing` §6 | `hack-skills` graphql |
| 原型污染 | `web-app-security` §2.7 | `hack-skills` prototype-pollution |
| 竞态条件 | `web-app-security` §3.2 | `hack-skills` race-condition |
| CSRF | `web-app-security` §2.2 | - |
| 请求走私 | `web-app-security` §3.1 | `hack-skills` request-smuggling |
| 云 Metadata 窃取 | `cloud-attack` §1 | - |
| K8s 容器逃逸 | `cloud-attack` §5 | `hack-skills` container-escape |
| AD 域攻击 | `red-team-ai` §4 | `hack-skills` ad-kerberos |
| 免杀 / C2 | `red-team-ai` §3 | `hack-skills` windows-av-evasion |

### 按技术栈速查

| 技术栈 | 检查项 | 路由 |
|--------|--------|------|
| Spring Boot | /actuator, SpEL注入 | `red-team-ai` §2.2, `web-app-security` |
| Shiro | rememberMe=deleteMe, ysoserial | `red-team-ai` §2.2 |
| Fastjson | @type, JNDI注入 | `red-team-ai` §2.2 |
| Ruoyi | /common/upload, 文件上传CVE | `red-team-ai` §2.2 |
| ThinkPHP | 指纹+版本, 5.x RCE | `red-team-ai` §2.2 |
| WordPress | /wp-admin, SQLi插件 | `web-app-security` |
| GraphQL | 内省查询, Batching爆破 | `api-security-testing` §6 |
| OAuth/OIDC | redirect_uri绕过, token窃取 | `api-security-testing` §2, `hack-skills` oauth |
| JWT | alg:none, RS256->HS256, kid注入 | `api-security-testing` §2.2 |
| Docker/K8s | Socket挂载, 特权容器 | `cloud-attack` §5 |

---

## 技能文件索引

| 技能名 | 文件 | 行数 |
|--------|------|------|
| shannon-methodology | `shannon-methodology.md` | 编排层 |
| cve-yu2 | `cve-yu2.md` | 编排层 |
| src-hunter | `src-hunter.md` | 编排层 |
| api-security-testing | `api-security-testing.md` | 战术层 |
| web-app-security | `web-app-security.md` | 战术层 |
| cloud-attack | `cloud-attack.md` | 战术层 |
| red-team-ai | `red-team-ai.md` | 战术层 |
| hack-skills | `hack-skills.md` | 战术层 |
| pentest-agents | `pentest-agents.md` | 战术层 |
| web-pentest-sample | `web-pentest-sample.md` | 战术层 |
| code-safety-audit | `code-safety-audit.md` | 工具层 |
| smart-web-scraper | `smart-web-scraper.md` | 工具层 |

---

> 原始技能库: `~/.kimi-code/memory/tools/skills/`
> 生成日期: 2026-07-21
