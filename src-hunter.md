# SRC Hunter — Bug Bounty / SRC 漏洞挖掘

## 触发条件
- Bug Bounty / SRC众测 / HackerOne平台挖洞
- 关键词: "src挖洞"、"漏洞赏金"、"bug bounty"、"众测"、"SRC"、"怎么测某个目标"
- 用户给出 URL/API/APK 让你测试

## 核心 Playbook (5阶段 + 强制Checkpoint)

### Phase 1: Intake (接单)
MUST输出四项 (缺一不进Phase 2):
- [ ] In-scope: 可测域名/IP/endpoint
- [ ] Out-of-scope: 禁测项
- [ ] 规则: payout tier / disclosure / safe-harbor / 测试header
- [ ] 时间盒: 6h / 单日 / HVV / 月度

### Phase 2: Recon (被动侦察，禁止主动发包)
资产来源 >= 3种:
- CT日志 (crt.sh/Censys)
- Wayback/CommonCrawl 历史快照
- GitHub dorks (org:target + password|api_key|SECRET|.env)
- FOFA/Shodan favicon hash
- SecurityTrails/DNS历史
- ASN/IP段 (bgp.he.net)

### Phase 3: Enum (主动探测)
输出: 活资产矩阵 `域 -> 端口 -> 服务 -> 指纹 -> JS endpoint`
- 命中国产OA指纹 -> 读 fingerprints + default-credentials-cn
- 银行/支付资产 -> 读 industry/banking-finance.md
- 运营商资产 -> 读 industry/telecom-isp.md

### Phase 4: Hunt (漏洞探测)
每个候选目标按信号选playbook (19个playbook):

| 入口信号 | Playbook |
|---------|---------|
| Actuator/Swagger/默认端口/弱密码 | unauth-access |
| .git/.svn/.env/heapdump | info-disclosure |
| 用户态ID可遍历 | arbitrary-x-authz |
| 密码重置/支付/验证码/订单 | logic-flaws |
| OAuth/SAML/JWT | oauth-saml-jwt |
| REST API/BOLA/Mass Assignment | api-rest |
| 任何用户输入进DB | squi |
| 反序列化/SSTI/XXE/框架RCE | rce |
| URL入参/缓存/Host注入 | ssrf-cache-host |
| 文件路径入参 | path-traversal |
| 上传点+解析漏洞 | file-upload |
| 用户输入回显到HTML/JS | xss |
| GraphQL endpoint | graphql |
| 并发/TOCTOU | race-conditions |
| APK/IPA/移动端 | mobile |
| LLM agent/prompt入口 | llm-prompt-injection |
| 已拿shell/凭据/内网 | intranet-postexp |

强制流程: Read playbook -> 按参数频率表挑入口 -> 按payload库探测 -> WAF拦则读bypass-toolkit -> 命中立即保存证据

### Phase 5: Report
- 读 compliance.md 核对合规红线
- 三段式输出: 标题(<=80字) + 重现步骤(curl/HTTP包/截图) + CVSS 4.0 + 修复建议

### 反幻觉约束
- 不准凭记忆出payload -> 必须先Read对应playbook
- 不准编造案例编号 -> 必须先Read h1-reports文件
- 无证据不下结论 -> 无HTTP包/截图只写"待验证"
- 出scope立即停 -> 回到Phase 1重核

## 工具链
- 子域名: subfinder, amass, crt.sh
- 存活检测: httpx, httprobe
- 目录爆破: ffuf, gobuster, dirsearch
- 漏洞扫描: nuclei
- MCP集成: mcp__jshook__search_tools/activate_tools
- 数据: 305 payloads, 263 WAF bypass变体, 2,887 H1案例, 88,636 WooYun案例
