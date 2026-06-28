# Java 学习知识库

一个将 Markdown 笔记渲染为单页 Wiki 的知识库管理系统，借鉴了 [Karpathy's rendergit](https://github.com/karpathy/rendergit) 的扁平化浏览理念。

## 快速开始

```bash
pip install flask markdown pygments
python wiki_server.py 5000
# 浏览器打开 → http://127.0.0.1:5000
```

## 功能

| 功能 | 说明 |
|------|------|
| **单页 Wiki 浏览** | 所有笔记渲染在同一页面，Ctrl+F 全局搜索 |
| **侧边栏目录树** | 按文件夹/文件层级导航，点击跳转 |
| **双视图模式** | 👤 人类视图（Markdown 渲染 + 代码高亮） ↔ 🤖 LLM 视图（CXML 格式，一键复制给 AI） |
| **客户端搜索** | `Ctrl+K` 聚焦搜索框，实时过滤匹配文件 |
| **暗色主题** | Catppuccin Mocha 配色，护眼适合长时间阅读 |
| **Obsidian 兼容** | `.obsidian/` 配置已就绪，可用 Obsidian 编辑笔记 |

## 目录结构

```
Java学习知识库/
├── 01-Java基础/          数据类型、运算符、控制流程、数组、面向对象
├── 02-Java进阶/          集合、泛型、异常、IO、多线程、JVM、Stream & 函数式接口
├── 03-框架与工具/        Spring、SpringBoot、MyBatis、Maven、Git
├── wiki_server.py        Flask Wiki 服务器
├── templates/wiki.html   Jinja2 模板（侧边栏 + 内容 + 搜索 + 双视图）
└── .codex/CONTEXT.md     Codex 项目上下文
```

## 添加新笔记

1. 在对应分类目录下创建 `.md` 文件（命名: `序号-标题.md`）
2. Markdown 标题 `#` 需从行首开始（不要有前导空格）
3. 刷新浏览器即可看到新文档（无需重启服务器）

## 技术栈

- **Server**: Python Flask
- **Template**: Jinja2
- **Markdown**: Python-Markdown (fenced_code, tables, toc, codehilite, nl2br)
- **Syntax Highlighting**: Pygments
- **Editor**: Obsidian