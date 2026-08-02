# Smart Web Scraper — 智能网页爬取 (OSINT/侦察)

## 触发条件
- OSINT阶段需要抓取目标网页内容
- 需要绕过反爬保护 (Cloudflare等)
- 关键词: "网页爬虫"、"绕过Cloudflare"、"动态渲染"、"网页截图"、"JS渲染抓取"

## 核心 Playbook

### 方案选择
| 目标网站 | 反爬级别 | 方案 | 脚本 |
|---------|---------|------|------|
| 普通静态网站 | 低 | Fetch工具 | 无需脚本 |
| 动态渲染网站 | 中 | Playwright简单模式 | `playwright-simple.js` |
| Cloudflare保护网站 | 高 | Playwright隐身模式 | `playwright-stealth.js` |

### 简单模式
```bash
cd ~/.kimi-code/memory/tools/skills/smart-web-scraper
node scripts/playwright-simple.js "https://example.com"
```
输出JSON: {title, url, text, meta_description, duration}

### 隐身模式
```bash
node scripts/playwright-stealth.js "https://example.com"
```
输出JSON: {title, url, html_length, preview, cloudflare_detected, screenshot_path}
反爬要点: 隐藏navigator.webdriver / 真实设备UA(默认iPhone) / 模拟真实视口 / 随机等待 / CF检测额外等待10s

### 环境变量
```
HEADLESS=true/false           # 无头模式
WAIT_TIME=5000                # 等待时间ms
SCREENSHOT_PATH=/path/to.png  # 截图路径
SAVE_HTML=true                # 保存HTML
USER_AGENT="..."              # 自定义UA
```

### 故障排除
- **403/Cloudflare验证**: 切换到隐身模式, 增加WAIT_TIME, 必要时HEADLESS=false
- **空白页面**: 增加等待时间, 使用waitUntil:'networkidle'
- **需要登录**: 先手动获取Cookie, 或复用浏览器状态

## 工具链
- Playwright (Chromium)
- npm + Node.js
- 脚本位置: `~/.kimi-code/memory/tools/skills/smart-web-scraper/scripts/`
- 前置: `npm install` + `npx playwright install chromium`
