# API Security Testing — API 安全测试

## 触发条件
- 目标暴露 REST API / Swagger文档 / GraphQL端点
- 关键词: "API测试"、"Swagger"、"OpenAPI"、"GraphQL"、"JWT攻击"、"IDOR"、"BOLA"、"Mass Assignment"
- 检测到 API 接口需要专项测试

## 核心 Playbook

### §1 API 发现
**Swagger/OpenAPI路径字典**:
```
/swagger.json, /api-docs, /openapi.json, /v2/swagger.json, /v3/api-docs,
/swagger-ui.html, /redoc, /doc.html, /knife4j, /swagger-resources
```
**自动发现**: `ffuf -u https://api.target.com/FUZZ -w swagger_paths.txt`
**Google Dork**: `site:target.com intitle:"Swagger UI"`

### §2 认证攻击
**JWT攻击清单 (9项)**:
- alg:none (6种变体: none/None/NONE/nOnE)
- RS256->HS256 密钥混淆
- 弱密钥爆破 (Top 15: secret/password/key/123456...)
- kid路径穿越 (../../etc/passwd)
- kid SQL注入
- jwk自签名注入
- 空签名 / 过期token重用 / refresh token无限刷新

**检测工具**: `jwt_tool.py <token> --exploit` / `hashcat -m 16500`
**API Key模式识别**: AWS(AKIA+), Google(AIzaSy+), Stripe(sk_live_/sk_test_), GitHub(ghp_/gho_), OpenAI(sk-)

### §3 IDOR/BOLA 攻击
**8种核心测试方法**:
1. 数字ID交换 `/user/123 -> /user/124`
2. UUID枚举 (从邀请邮件泄露)
3. 数组包裹 `{"id":111} -> {"id":[111]}`
4. JSON嵌套 `{"id":{"id":111}}`
5. 参数污染 `?user_id=legit&user_id=victim`
6. 通配符 `{"user_id":"*"}`
7. HTTP方法交换 (PUT有保护, DELETE无)
8. 旧API版本 `/v1/` 无权限控制

**影响分级**: 读PII->Medium / 写他人数据->High / 管理员端点->Critical / 账号接管->Critical

### §4 API 注入
**NoSQL注入**: `{"username": {"$ne": null}, "password": {"$ne": null}}`
**SSTI检测**: `{{7*7}}->49?(Jinja2) / ${7*7}->49?(Freemarker) / {{=7*7}}(Django) / #{7*7}(Pug) / <%=7*7%>(ERB)`

### §5 限流绕过
IP轮换 (X-Forwarded-For) / 请求批处理 / 空格变体 / 参数顺序变化 / User-Agent轮换 / API版本降级

### §6 GraphQL 攻击
- 内省查询: `{ __schema { types { name fields { name type { name } } } } }`
- Batching爆破 / Alias IDOR / node() IDOR / 深度递归DoS / 指令注入(@skip @include)
- 工具: InQL(Burp), GraphQLmap, clairvoyance, graphw00f

### §7 Mass Assignment
**检测**: 添加敏感字段 `{"name":"John","role":"admin","isAdmin":true}`
**常见敏感参数**: role, isAdmin, balance, credits, organization_id, email_verified

## 工具链
- JWT: jwt_tool.py, hashcat -m 16500
- API发现: ffuf + swagger_paths.txt
- GraphQL: InQL, GraphQLmap, clairvoyance, graphql-cop, graphw00f
- 参考: OWASP API Top 10 2025, 《Secure APIs》Manning 2025
