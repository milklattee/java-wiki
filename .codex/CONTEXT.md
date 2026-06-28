 # Project: Java 学习知识库
 
 ## What this is
 一个 Java 学习知识库管理系统，将 markdown 笔记渲染为单页 wiki 浏览界面。借鉴了 Karpathy 的 rendergit 体系（单页渲染、侧边栏导航、Human/LLM 双视图）。
 
 ## Tech stack
 - **Server**: Python Flask (wiki_server.py)
 - **Template**: Jinja2 (templates/wiki.html)
 - **Markdown rendering**: Python-Markdown (extensions: fenced_code, tables, toc, codehilite, nl2br)
 - **Syntax highlighting**: Pygments
 - **Editor**: Obsidian (.obsidian/ vault 配置，兼容双向链接)
 
 ## Key files
 | File | Purpose |
 |------|---------|
 | `wiki_server.py` | Flask 主程序，扫描 .md 文件，渲染 wiki 页面 |
 | `templates/wiki.html` | Jinja2 模板：侧边栏目录树 + 内容区 + 搜索 + 双视图 |
 | `.codex/CONTEXT.md` | 项目上下文记忆（本文件） |
 
 ## Directory structure
 ```
 Java学习知识库/
 ├── 01-Java基础/       # 数据类型、运算符、控制流程、数组、OOP
 ├── 02-Java进阶/       # 集合、泛型、异常、IO、多线程、JVM
 ├── 03-框架与工具/     # Spring、SpringBoot、MyBatis、Maven、Git
 ├── wiki_server.py     # Flask 服务器
 ├── templates/         # Jinja2 模板
 └── .obsidian/         # Obsidian vault 配置
 ```
 
 ## Server commands
 ```bash
 # Start dev server
 cd "D:\studyspace\Java学习知识库"
 python wiki_server.py 5000
 # → http://127.0.0.1:5000
 
 # Stop
 # Ctrl+C or kill python process
 ```
 
 ## Common workflows
 
 ### Adding new knowledge documents
 1. 在对应分类目录下创建 `.md` 文件（可用 Obsidian 或直接创建）
 2. 文件名格式: `序号-标题.md`（如 `06-继承与多态.md`）
 3. **重要**: markdown 标题 `#` 必须从行首开始，不要有前导空格
 4. 刷新浏览器即可看到新文档
 
 ### Adding a new category
 1. 在根目录创建新文件夹（如 `04-设计模式/`）
 2. 在其中创建 `.md` 文件
 3. 服务器重启后自动识别新目录
 
 ## Important notes for Codex
 - 所有 `.md` 文件中的 `#` 标题行必须以行首开始（不能有前导空格），否则 markdown 渲染失败
 - 模板文件 `wiki.html` 中使用了 Jinja2 `__files__` 作为树形结构的叶子节点键名
 - 忽略目录列表: .git, .obsidian, __pycache__, templates, static, .agents, .codex
 - 页面底部有 Human/LLM 双视图切换按钮
