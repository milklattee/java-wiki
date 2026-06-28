#!/usr/bin/env python3
#
# Java Knowledge Base Wiki
# Inspired by Karpathy rendergit - flat, searchable, dual-mode knowledge wiki.
#

import os
import html
import pathlib
from typing import Dict, List

from flask import Flask, render_template, jsonify
from markdown import markdown as md_render
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, TextLexer

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
KNOWLEDGE_ROOT = pathlib.Path(__file__).parent.resolve()
IGNORED_DIRS = {".git", ".obsidian", "__pycache__", "templates", "static", ".agents", ".codex"}
MARKDOWN_EXTS = {"fenced_code", "tables", "toc", "codehilite", "nl2br"}

app = Flask(__name__, template_folder=str(KNOWLEDGE_ROOT / "templates"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def bytes_human(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    f = float(n)
    i = 0
    while f >= 1024.0 and i < len(units) - 1:
        f /= 1024.0
        i += 1
    return f"{f:.1f} {units[i]}" if i > 0 else f"{int(f)} {units[i]}"


def slugify(path_str: str) -> str:
    out = []
    for ch in path_str:
        if ch.isalnum() or ch in {"-", "_"}:
            out.append(ch)
        else:
            out.append("-")
    return "".join(out)


def collect_markdown_files(root: pathlib.Path) -> List[Dict]:
    """Recursively collect all .md files with metadata."""
    files = []
    for p in sorted(root.rglob("*.md")):
        rel = str(p.relative_to(root)).replace(os.sep, "/")
        parts = rel.split("/")
        if any(d in IGNORED_DIRS for d in parts[:-1]):
            continue
        size = p.stat().st_size
        anchor = slugify(rel)
        files.append({
            "rel": rel,
            "anchor": anchor,
            "size": size,
            "size_human": bytes_human(size),
            "abs_path": str(p),
        })
    return files


def build_directory_tree(files: List[Dict]) -> Dict:
    """Build a nested directory tree from flat file list."""
    tree = {}
    for f in files:
        parts = f["rel"].split("/")
        node = tree
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            node = node[part]
        filename = parts[-1]
        if "__files__" not in node:
            node["__files__"] = []
        node["__files__"].append(f)
    return tree


def render_markdown_file(filepath: str, filename: str) -> Dict:
    """Render a markdown file into HTML with syntax highlighting."""
    try:
        text = pathlib.Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"html": f'<pre class="error">Error: {html.escape(str(e))}</pre>', "raw": ""}

    try:
        # Strip common leading whitespace so `# Heading` is recognized as a heading
        fixed = "\n".join(line.lstrip(" ") for line in text.splitlines())
        rendered = md_render(fixed, extensions=list(MARKDOWN_EXTS))
    except Exception as e:
        return {"html": f'<pre class="error">Markdown error: {html.escape(str(e))}</pre>', "raw": text}

    return {"html": rendered, "raw": text}


def generate_llm_text(files: List[Dict]) -> str:
    """Generate CXML-style format for LLM consumption."""
    lines = ["<documents>"]
    for idx, f in enumerate(files, 1):
        try:
            text = pathlib.Path(f["abs_path"]).read_text(encoding="utf-8", errors="replace")
        except Exception:
            text = "(read error)"
        lines.append(f'<document index="{idx}">')
        lines.append(f"<source>{f['rel']}</source>")
        lines.append("<document_content>")
        lines.append(text)
        lines.append("</document_content>")
        lines.append("</document>")
    lines.append("</documents>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def wiki_home():
    """Render the full knowledge base in a single-page wiki."""
    all_files = collect_markdown_files(KNOWLEDGE_ROOT)

    rendered_files = []
    for f in all_files:
        content = render_markdown_file(f["abs_path"], f["rel"])
        rendered_files.append({**f, "html": content["html"], "raw": content["raw"]})

    tree = build_directory_tree(rendered_files)
    llm_text = generate_llm_text(rendered_files)

    return render_template(
        "wiki.html",
        files=rendered_files,
        tree=tree,
        llm_text=llm_text,
        total_files=len(rendered_files),
        knowledge_root=str(KNOWLEDGE_ROOT.name),
    )


@app.route("/api/files")
def api_files():
    """API endpoint: list all knowledge files as JSON."""
    files = collect_markdown_files(KNOWLEDGE_ROOT)
    return jsonify(files)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"  Java Knowledge Base Wiki")
    print(f"  http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
