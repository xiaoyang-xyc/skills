# Hack Skills — 深度攻击技能库 (101技能)

## 触发条件
- 需要特定漏洞类型的深度playbook (非通用扫描)
- 关键词: 具体漏洞技术 "SQL注入绕过"、"WAF绕过"、"Ghost Bits"、"XXE OOB"、"SSTI"、"反序列化gadget"
- 遇到WAF拦截需要bypass / 需要按数据库类型定制payload

## 核心 Playbook

### 技能体系 (101技能, 14安全域)
Master Entry -> 6个Category Entry -> 101个Deep Topic Skills

### 6个Category Entry路由

| Category | 覆盖 | 何时进入 |
|----------|------|---------|
| **recon-for-sec** | 资产发现、技术识别 | 刚拿到目标 |
| **api-sec** | REST/GraphQL/移动后端 | 发现API接口 |
| **auth-sec** | 认证/会话/OAuth/JWT/授权 | 登录/Token/对象ID |
| **injection-checking** | XSS/SQLi/SSRF/XXE/SSTI/CMDi/NoSQL | 输入进入解释器 |
| **file-access-vuln** | 上传/下载/LFI/路径控制 | 文件操作 |
| **business-logic-vuln** | 竞态/定价/工作流/状态机 | 业务流程测试 |

### 重点 Deep Topic Skills

**注入类**:
- `sqli-sql-injection`: 475行, DB2/Cassandra/BigQuery/SQLite, WAF绕过矩阵, CTF技巧
- `xss-cross-site-scripting`: 368行, Polyglot payloads, 按WAF厂商bypass, CSP绕过, DOM clobbering
- `ssti-server-side-template-injection`: 340行, 15+引擎, 盲SSTI, Flask PIN计算
- `cmdi-command-injection`: 494行, WAF绕过(wildcards/xor/base64), PHP disable_functions 6路径
- `ssrf-server-side-request-forgery`: 314行, 6平台云metadata, DNS rebinding, Gopher/Redis RCE链
- `nosql-injection`: 341行, 盲提取自动化, 聚合管道注入
- `xxe-xml-external-entity`: 326行, 本地DTD注入(17+路径), 盲XXE, Gopher/FTP OOB
- `deserialization-insecure`: 714行, Java/PHP/Python/Ruby/.NET/Node.js chain
- `ghost-bits-cast-attack`: 400+行, Java char-to-byte窄化WAF绕过 (Black Hat Asia 2026)
- `request-smuggling`: 298行, CL.TE/TE.CL/TE.TE, 8种混淆变体, HTTP/2降级

**权限提升类**:
- `linux-privilege-escalation`: SUID/SGID, kernel exploits, capabilities, cron
- `windows-privilege-escalation`: Token, service, DLL hijack, UAC, Potato
- `container-escape-techniques`: Docker socket, privileged, cgroup, runc
- `active-directory-kerberos-attacks`: Kerberoasting, AS-REP, Golden/Silver Ticket
- `active-directory-certificate-services`: ESC1-ESC8, PKINIT

**其他**:
- `race-condition`: 286行, TOCTOU, HTTP/1.1 last-byte sync, HTTP/2 single-packet
- `prototype-pollution`: Express探测, EJS/Kibana gadget链
- `csrf-cross-site-request-forgery`: 324行, JSON CSRF 3技术, multipart CSRF
- `business-logic-vulnerabilities`: 339行, 支付操纵10攻击, 状态机绕过

### 关键数据规模
- 101个深度技能文件
- 263个WAF/EDR绕过变体
- 按WAF厂商 (Cloudflare/AWS/Akamai/ModSecurity) 分类
- 按数据库类型 (MySQL/PostgreSQL/MSSQL/Oracle/SQLite/Cassandra/BigQuery) 定制

## 工具链
- 安装: `npx skills add yaklang/hack-skills`
- Web: https://skills.hackbenchmark.com (搜索/过滤/复制安装命令)
- 离线ZIP: AES-256加密 (密码hack-skills)
