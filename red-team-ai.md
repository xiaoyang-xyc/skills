# Red Team AI — AI驱动的红队实战

## 触发条件
- 需要AI辅助的红队行动 / C2通信 / 域渗透 / 后渗透
- 关键词: "红队"、"C2"、"域渗透"、"AD攻击"、"免杀"、"后渗透"、"横向移动"、"隐蔽通道"

## 核心 Playbook

### §1 AI 辅助侦察
**智能子域名**: `subfinder -d target.com` + LLM分析模式生成变体
**AI指纹识别**: LLM分析响应头/HTML -> 自动匹配CVE数据库 -> 生成针对性攻击计划
**关键检查清单**:
```
/actuator/health -> Spring Boot
/druid/index.html -> 阿里Druid
rememberMe=deleteMe -> Shiro
/swagger-ui.html -> API文档
.env / .git/HEAD -> 配置/源码泄露
Server头 -> 版本泄露
```

### §2 智能漏洞利用
**框架漏洞速查**:
| 框架 | 检测 | 利用 |
|------|------|------|
| Shiro | rememberMe=deleteMe | ysoserial |
| Fastjson | DNSLog + @type | JNDI注入 |
| Spring Boot | /actuator/env | SpEL注入 |
| Ruoyi | /common/upload | 文件上传CVE |
| ThinkPHP | 指纹+版本 | 5.x RCE |

**漏洞优先级 (按成功率)**:
1. 信息泄露 (20%) / 2. 未授权访问 (18%) / 3. XSS (15%) / 4. SQL注入 (12%) / 5. SSRF (10%) / 6. RCE (8%)

### §3 C2 隐蔽通道
**协议选择**: HTTPS(通用) / DNS Tunnel(高隐蔽) / WebSocket(长连接) / MCP协议(极高,伪装AI API) / ICMP(特殊)

**免杀技术 (8种)**:
ETW Patching / API Unhooking / DLL反射加载 / Process Hollowing / Parent PID Spoofing / Syscall直调 / OLLVM混淆 / memfd_create内存执行

### §4 AD 域攻击
**攻击路径**:
```
初始入口 -> 本地提权 -> 域枚举 -> BloodHound路径分析 ->
Kerberoasting -> AS-REP Roasting -> DCSync -> 域控
```
**关键工具**: SharpHound, Rubeus (kerberoast), mimikatz (DCSync), BloodHound

### §5 后渗透
**持久化**: 计划任务 / WMI事件订阅 / 注册表Run键 / Windows服务 / DLL劫持 / SSH authorized_keys / crontab
**横向移动**: PSRemoting/WinRM / WMI远程执行 / PsExec / RDP / SSH密钥信任链 / 云助手(ECS RunCommand)

### §6 RAG 漏洞挖掘
```
目标代码/文档 -> 嵌入模型 -> 向量数据库 ->
检索相关漏洞模式 -> LLM生成测试用例 -> 自动化验证 -> 报告
```

## 工具链
- AD: BloodHound, SharpHound, Rubeus, mimikatz, impacket
- C2: Cobalt Strike, Sliver, Mythic, Havoc
- 免杀: OLLVM, donut, ScareCrow
- 参考: 《红队实战指南》Omar Santos 2026 / MITRE ATT&CK T1595-T1210-T1078-T1003
