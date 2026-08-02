---
name: smart-web-scraper
description: "基于 Playwright 智能爬取网页内容，提供简单模式和隐身模式应对不同反爬强度，输出网页标题、文本内容和截图。当用户需要抓取动态网页、绕过 Cloudflare 等反爬机制，或提到爬虫、网页截图、JavaScript 渲染时触发。"
version: 1.2.0
---

# Playwright 网页爬取工具

基于 Playwright 的网页爬取 Skill，内置反爬虫保护机制。根据目标网站反爬强度选择对应方案。

## 使用场景

| 目标网站 | 反爬级别 | 推荐方案 | 脚本 |
|---------|---------|---------|------|
| 普通静态网站 | 低 | Fetch 工具 | 无需脚本 |
| 动态渲染网站 | 中 | Playwright 简单模式 | `scripts/playwright-simple.js` |
| Cloudflare 等保护网站 | 高 | Playwright 隐身模式 | `scripts/playwright-stealth.js` |

## 前置准备

```bash
cd ~/.kimi-code/memory/tools/skills/smart-web-scraper
npm install
npx playwright install chromium
```

## 快速使用

### 简单模式（动态渲染，无反爬）

```bash
node scripts/playwright-simple.js "https://example.com"
```

输出 JSON：标题、URL、正文内容、meta 描述、耗时。

### 隐身模式（反爬保护）

```bash
node scripts/playwright-stealth.js "https://example.com"
```

输出 JSON：标题、URL、HTML 长度、内容预览、Cloudflare 检测状态、截图路径、可选 HTML 文件。

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `HEADLESS` | 是否无头模式 | `true` |
| `WAIT_TIME` | 等待加载时间（毫秒） | 简单模式 3000，隐身模式 5000 |
| `SCREENSHOT_PATH` | 截图保存路径 | 隐身模式自动生成 |
| `SAVE_HTML` | 是否保存 HTML | `false` |
| `USER_AGENT` | 自定义 User-Agent | 隐身模式使用 iPhone UA |

示例：

```bash
HEADLESS=false WAIT_TIME=10000 SAVE_HTML=true node scripts/playwright-stealth.js "https://example.com"
```

## 反爬要点

- 隐藏 `navigator.webdriver`
- 使用真实设备 User-Agent（默认 iPhone）
- 模拟真实视口和语言环境
- 随机等待时间让页面完成渲染
- 检测到 Cloudflare 挑战时自动额外等待 10 秒

## 故障排除

- **403 Forbidden / Cloudflare 验证**：切换到隐身模式，增加 `WAIT_TIME`，必要时使用 `HEADLESS=false`。
- **空白页面**：增加等待时间，或使用 `waitUntil: 'networkidle'`。
- **需要登录**：先手动获取 Cookie 或通过浏览器登录后复用状态。
