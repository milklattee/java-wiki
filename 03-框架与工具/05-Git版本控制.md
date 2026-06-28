# Git 版本控制

## 基本工作流

```
工作区 → git add → 暂存区 → git commit → 本地仓库 → git push → 远程仓库
```

## 常用命令速查

```bash
# 配置
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# 基本操作
git init                                # 初始化仓库
git clone <url>                         # 克隆远程仓库
git status                              # 查看状态
git add <file>                          # 添加文件到暂存区
git commit -m "message"                 # 提交
git push origin main                    # 推送到远程
git pull origin main                    # 拉取远程更新

# 分支
git branch                              # 查看分支
git branch feature-x                    # 创建分支
git switch feature-x                    # 切换分支 (Git 2.23+)
git merge feature-x                     # 合并分支
git branch -d feature-x                 # 删除分支

# 历史
git log --oneline --graph --all         # 可视化历史
git diff                                # 查看未暂存更改
git diff --staged                       # 查看已暂存更改
```

## 撤销操作

| 场景 | 命令 |
|------|------|
| 撤销工作区修改 | `git restore <file>` |
| 取消暂存 | `git restore --staged <file>` |
| 修改最近 commit 消息 | `git commit --amend -m "new msg"` |
| 回退到某版本（保留修改）| `git reset --soft HEAD~1` |
| 回退到某版本（丢弃修改）| `git reset --hard HEAD~1` |

## 常见工作流

### Git Flow

```
main ────●────────●──────●─
           \      /      /
develop ──●──●──●──●──●
             \    \/
feature/a ───●
```

- `main` — 生产就绪代码
- `develop` — 集成分支
- `feature/*` — 功能开发
- `release/*` — 发布准备
- `hotfix/*` — 紧急修复

### GitHub Flow（推荐个人项目）

1. 从 `main` 创建 feature 分支
2. 开发 + 提交
3. 创建 Pull Request
4. 代码审查后合并到 `main`