# Agent Tools（通用 Agent 工具集）

本 Skill 定义一组 AI Agent 在本地/远程环境中执行命令、操作文件、控制浏览器和管理后台进程的通用工具。

## 用途

- 在授权范围内执行系统命令、脚本和工具链
- 自动化浏览器操作、网页截图、前端交互
- 读写和编辑项目文件
- 管理长时间运行的后台任务

## 已安装工具

| 工具 | 作用 | 底层实现 |
|------|------|----------|
| `exec` | 执行 shell 命令 | `child_process.spawn`，支持本地/远程/沙箱 |
| `browser` | 控制浏览器 | Playwright + Chrome DevTools Protocol (CDP) |
| `canvas` | 网页截图/画板操作 | 与 `browser` 共享 Chromium 实例 |
| `read` / `write` / `edit` | 文件操作 | Node.js `fs` 模块 |
| `process` | 后台进程管理 | 基于 `exec` 的 background 模式 |

---

## 1. `exec`：命令执行

### 功能

- 执行本地或远程 shell 命令
- 支持同步/异步执行
- 支持在沙箱或隔离环境中运行
- 返回 stdout / stderr / exit code

### 底层实现

基于 Node.js `child_process.spawn`，根据目标环境选择：

- **本地**：直接 spawn 本机 shell
- **远程**：通过 SSH 在目标主机上 spawn
- **沙箱**：通过容器/虚拟机隔离执行

### 使用规范

1. 优先使用专用工具（如 `read`/`write`）完成文件操作，避免直接用 `cat`、`sed`。
2. 对多步骤命令使用 `&&` 或脚本文件，减少往返。
3. 远程执行前确认目标主机可达、凭据有效。
4. 对可能长时间运行的任务，使用 `process` 工具转为后台。

### 示例

```bash
# 本地执行
exec("node --version")

# 远程执行（已通过 SSH 配置别名）
exec("ssh kali2026 'whoami && uname -a'")

# 多步骤命令
exec("cd /tmp && tar -xzf app.tar.gz && ls -la app")
```

---

## 2. `browser`：浏览器控制

### 功能

- 启动/连接 Chromium 浏览器实例
- 打开网页、点击元素、填写表单
- 执行 JavaScript、拦截网络请求
- 与 `canvas` 配合生成网页截图

### 底层实现

- Playwright 提供跨浏览器自动化 API
- Chrome DevTools Protocol (CDP) 提供底层调试能力
- 与 `canvas` 共享同一个 Chromium 实例

### 使用规范

1. 仅在获得授权的范围内访问目标网站。
2. 对需要登录或敏感信息的站点，使用环境变量或安全凭据管理。
3. 截图/录屏前清理敏感信息。
4. 操作完成后关闭页面或浏览器上下文，释放资源。

### 示例

```javascript
browser.goto("https://example.com")
browser.click("#login")
browser.fill("#username", "admin")
browser.fill("#password", process.env.PASSWORD)
browser.click("#submit")
```

---

## 3. `canvas`：网页截图与画板

### 功能

- 对当前浏览器页面或指定元素截图
- 在网页/截图上绘制标注、框选、箭头
- 生成用于报告或证据链的图片

### 底层实现

- 与 `browser` 共享 Chromium 实例
- 使用 Playwright 的 `page.screenshot()`
- 可选叠加层通过浏览器内 `<canvas>` 或后端图像处理实现

### 使用规范

1. 截图前等待页面关键元素加载完成。
2. 对证据类截图，保留原始图和标注图两个版本。
3. 输出路径使用项目约定的证据目录（如 `evidence/`、`screenshots/`）。

### 示例

```javascript
browser.goto("https://example.com/admin")
canvas.screenshot({ path: "evidence/admin-panel.png", fullPage: true })
canvas.annotate({ path: "evidence/admin-panel-marked.png", boxes: [{x: 100, y: 200, w: 300, h: 50}] })
```

---

## 4. `read` / `write` / `edit`：文件操作

### 功能

| 工具 | 作用 |
|------|------|
| `read` | 读取文本文件内容 |
| `write` | 创建或完全覆盖文件 |
| `edit` | 对现有文件进行精确片段替换 |

### 底层实现

Node.js `fs` 模块：

- `read` → `fs.readFileSync` / `fs.promises.readFile`
- `write` → `fs.writeFileSync` / `fs.promises.writeFile`
- `edit` → 读取后做字符串替换再写回

### 使用规范

1. **优先用 `edit` 做增量修改**，避免 `write` 覆盖导致意外丢失。
2. `write` 仅用于新建文件或明确需要完整替换的场景。
3. 修改前若文件重要，可先 `read` 备份或写入 `.bak`。
4. 不要读取或修改敏感凭据文件（如 `.env`、SSH 私钥、密码库）。

### 示例

```javascript
// 读取
const content = read("src/config.js")

// 增量修改
edit("src/config.js", "const PORT = 3000", "const PORT = 8080")

// 新建文件
write("docs/api.md", "# API 文档\n\n...")
```

---

## 5. `process`：后台进程管理

### 功能

- 启动长时间运行的任务（如服务、扫描、构建、监听）
- 查看后台任务状态与输出
- 停止指定后台任务

### 底层实现

基于 `exec` 的 background 模式：

- 将任务 detach 到后台
- 维护任务 ID、PID、输出日志路径
- 通过信号或 kill 停止任务

### 使用规范

1. 后台任务需给出明确描述，便于后续识别。
2. 任务输出重定向到日志文件，避免阻塞。
3. 任务完成后及时停止，释放系统资源。
4. 对远程后台任务，注意 SSH 连接断开后进程是否存活。

### 示例

```javascript
const taskId = process.start({
  command: "npm run dev",
  description: "启动前端开发服务器",
  logs: "logs/dev-server.log"
})

process.status(taskId)
process.stop(taskId)
```

---

## 安全与授权

1. 所有命令执行、浏览器访问、文件操作必须在用户明确授权范围内。
2. 对外部系统的主动操作（扫描、登录、数据抓取）需获得书面授权。
3. 不得在未经授权的系统上安装、运行或传播恶意软件。
4. 后台任务应记录到操作日志，便于审计。

## 相关文件

- `skills/agent-tools/SKILL.md`：本文件
- `AGENTS.md`：项目级 Agent 技能总览

## 触发规则

当用户请求安装/使用 Agent 通用工具、`exec`、`browser`、`canvas`、文件操作、后台进程管理等相关能力时，先读取本 SKILL.md。
