# Code Safety Audit — 代码安全自动扫描

## 触发条件
- 给源码路径，需要快速自动化安全扫描
- 关键词: "安全扫描"、"漏洞检测"、"依赖审计"、"密钥泄露"、"OWASP"、"npm audit"、"pip-audit"
- 任何涉及源码的安全审计前，先跑此工具

## 核心 Playbook: 三层扫描

### 1. 依赖漏洞扫描 (deps)
自动检测项目类型:
- Node.js: `package.json` + `package-lock.json` -> `npm audit`
- Python: `requirements.txt` / `pyproject.toml` / `Pipfile` -> `pip-audit`

### 2. 密钥泄露检测 (secrets)
**正则匹配** (覆盖常见格式):
```
AWS: AKIA + 16chars | GitHub: ghp_/github_pat_
Slack: xoxb-/xoxp- | Stripe: sk_live_/pk_live_
私钥: -----BEGIN PRIVATE KEY----- | JWT: eyJ...
URL内嵌凭据: https://user:pass@host
```

**Shannon熵值分析**: 对字符串常量计算信息熵，阈值 > 4.5 且长度 >= 20 (发现非标准格式密钥)

### 3. OWASP模式检测 (owasp)
| OWASP | 检测模式 |
|-------|---------|
| A02 密码学失败 | 弱哈希 (MD5/SHA1), 弱加密 (DES/RC4) |
| A03 注入 | SQL注入 (f-string/字符串拼接), 命令注入 (os.system/eval/exec), XSS (innerHTML/dangerouslySetInnerHTML/v-html) |
| A04 不安全设计 | 路径遍历 |
| A05 安全配置错误 | Debug模式, CORS通配符, 绑定0.0.0.0 |
| A08 完整性失败 | 不安全反序列化 (pickle/yaml.load/marshal/unserialize) |
| A10 SSRF | 用户输入直接用于HTTP请求 |

支持语言: Python, JavaScript/TypeScript, Java, PHP, Ruby, Go

### 使用方法
```bash
python3 scripts/security_scan.py .                    # 全扫
python3 scripts/security_scan.py --mode deps .        # 仅依赖
python3 scripts/security_scan.py --mode secrets .     # 仅密钥
python3 scripts/security_scan.py --mode owasp .       # 仅OWASP
python3 scripts/security_scan.py --severity high .    # 仅高危+
python3 scripts/security_scan.py --format json --output report.json .
```

### 退出码
- `0`: 无发现
- `1`: 有发现 (至少一个安全问题)
- `2`: 扫描器自身错误

## 工具链
- Python 3.7+ (仅标准库, 无外部依赖)
- npm (Node.js项目依赖扫描, 可选)
- pip-audit (Python项目依赖扫描, 可选)
- 脚本位置: `~/.kimi-code/memory/tools/skills/code-safety-audit/scripts/security_scan.py`
