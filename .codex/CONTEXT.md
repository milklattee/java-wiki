# Project: Java 学习知识库

## What this is
一个将 Markdown 笔记渲染为单页 Wiki 的知识库管理系统。借鉴了 Karpathy's rendergit 的扁平化浏览理念。用户在 Obsidian 中编辑 .md 笔记，Flask 服务器将其渲染为带侧边栏导航、搜索、Human/LLM 双视图的单页应用。

GitHub: `git@github.com:milklattee/java-wiki.git` (SSH only — 443 端口被墙)

## Tech stack
- Server: Python Flask (wiki_server.py, port 5000)
- Template: Jinja2 (templates/wiki.html — 暗色 Catppuccin Mocha 主题)
- Markdown: Python-Markdown (extensions: fenced_code, tables, toc, codehilite, nl2br)
- Code highlighting: Pygments
- Editor: Obsidian (.obsidian/ vault 配置就绪)

## Directory structure
```
Java学习知识库/
├── 01-Java基础/            数据类型、运算符、控制流程、数组、面向对象
├── 02-Java进阶/            集合、泛型、异常、IO、多线程、JVM、Stream & 函数式接口
├── 03-框架与工具/          Spring、SpringBoot、MyBatis、Maven、Git
├── wiki_server.py          Flask Wiki 服务器
├── templates/wiki.html     Jinja2 暗色主题模板（单文件，内联 CSS/JS）
├── .codex/CONTEXT.md       Codex 项目上下文（本文件）
├── README.md               GitHub 仓库说明
└── .obsidian/              Obsidian vault 配置
```

## Server
```bash
cd "D:\studyspace\Java学习知识库"
python wiki_server.py 5000
# → http://127.0.0.1:5000
```
停止: `Ctrl+C` 或 `Get-Process python | Stop-Process`
添加新 .md 后无需重启，刷新浏览器即生效。

## Critical rules — must follow

### 1. Markdown 前导空格问题
`apply_patch` 创建的 .md 文件每行会自动加一个前导空格，导致 `# 标题` 变成 ` # 标题`，Python-Markdown 无法识别为标题/代码块/列表。
每次用 apply_patch 创建 .md 后，必须执行去前导空格脚本：
```python
import pathlib
root = pathlib.Path('D:/studyspace/Java学习知识库')
for md in root.rglob('*.md'):
     if '.obsidian' not in str(md) and '.codex' not in str(md) and '.git' not in str(md):
         text = md.read_text('utf-8')
         fixed = '\n'.join(line[1:] if line.startswith(' ') and not line.startswith('  ') else line for line in text.splitlines())
         if fixed != text:
             md.write_text(fixed, 'utf-8')
```
代码缩进（两个空格以上）不受影响，只去掉行首单空格。

### 2. 模板修改注意事项
- `templates/wiki.html` 是单文件，内联 CSS 和 JS
- Jinja2 树形结构使用 `__files__` 作为叶子节点键名（不是空字符串 `''`）
- 模板条件判断用 `key != '__files__'` 过滤文件列表
- 修改模板后必须用 Python 读回验证中文未损坏

### 3. 编码问题
- 所有 .md 和 .html 文件使用 UTF-8（无 BOM）
- PowerShell 的 `@""@` heredoc 会损坏中文字符，禁止在 shell 中直接写中文模板内容
- 中文内容一律通过 apply_patch 或 Python 写入
- `Set-Content -Encoding UTF8` 会在文件头加 BOM，改用 Python `write_text(encoding='utf-8')`

### 4. Git workflow
```bash
cd "D:\studyspace\Java学习知识库"
git add -A
git commit -m "描述变更"
git push origin main
```
远程使用 SSH（`git@github.com:milklattee/java-wiki.git`），HTTPS 443 不通。

### 5. 忽略目录
wiki_server.py 的 `IGNORED_DIRS` = {".git", ".obsidian", "__pycache__", "templates", "static", ".agents", ".codex"}

## Behaviors established in conversation
- 用户提问 "补充 XX 内容" → 创建新 .md，内容全面有深度（速查表 + 实战代码 + 陷阱），用 apply_patch 创建后自动去前导空格，然后重启服务器
- 用户报告显示问题 → 先排查编码（中文损坏？前导空格？），再排查服务器端逻辑
- 修改模板后 → 重启 Flask 服务器生效
- 每次对话结束前 → 推送到 GitHub