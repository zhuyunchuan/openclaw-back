#!/bin/bash
# OpenClaw 配置备份脚本
# 用途：一键备份配置到 GitHub

set -e

WORKSPACE_DIR="/home/admin/.openclaw/workspace"
BACKUP_DIR="/tmp/openclaw-backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🚀 OpenClaw 配置备份脚本"
echo "========================"
echo ""

# 检查是否提供了 GitHub 仓库地址
if [ -z "$1" ]; then
    echo "❌ 用法：$0 <GitHub 仓库地址>"
    echo ""
    echo "示例:"
    echo "  $0 https://github.com/yourusername/openclaw-config.git"
    echo ""
    echo "如果是首次备份，请先在 GitHub 上创建仓库"
    exit 1
fi

REPO_URL="$1"

cd "$WORKSPACE_DIR"

# 检查 git 是否已初始化
if [ ! -d ".git" ]; then
    echo "📦 初始化 git 仓库..."
    git init
fi

# 检查是否有 .gitignore
if [ ! -f ".gitignore" ]; then
    echo "⚠️  .gitignore 不存在，创建中..."
    cat > .gitignore << 'EOF'
# 敏感信息
*.env
.env
*.key
*.secret
*.token
credentials.json
.openclaw/openclaw.json
.openclaw/identity/
.openclaw/devices/
.openclaw/cron/

# 虚拟环境
venv*/
__pycache__/
*.pyc

# 大型文件
*.amr
*.ogg
*.mp3
*.mp4
media/
logs/

# 个人笔记
memory/
MEMORY.md

# 临时文件
*.tmp
*.bak
.DS_Store
EOF
fi

# 添加所有文件
echo "📋 添加文件..."
git add -A

# 查看变更
echo ""
echo "📊 变更概览:"
git status --short

# 提交
echo ""
read -p "输入提交信息 (默认：Backup $(date +%Y-%m-%d)): " COMMIT_MSG
COMMIT_MSG="${COMMIT_MSG:-Backup $(date +%Y-%m-%d)}"

git commit -m "$COMMIT_MSG"

# 检查是否已配置远程仓库
if ! git remote get-url origin &>/dev/null; then
    echo ""
    echo "🔗 配置远程仓库..."
    git remote add origin "$REPO_URL"
else
    echo ""
    echo "ℹ️  远程仓库已配置："
    git remote get-url origin
    read -p "是否更新远程仓库地址？(y/N): " UPDATE_REMOTE
    if [ "$UPDATE_REMOTE" = "y" ] || [ "$UPDATE_REMOTE" = "Y" ]; then
        git remote set-url origin "$REPO_URL"
    fi
fi

# 推送
echo ""
echo "📤 推送到 GitHub..."
git push -u origin master

echo ""
echo "✅ 备份完成！"
echo ""
echo "📍 仓库地址：$REPO_URL"
echo "📅 备份时间：$(date)"
echo ""
echo "💡 提示："
echo "   - 在新服务器上运行：git clone $REPO_URL"
echo "   - 参考 BACKUP-GUIDE.md 进行恢复"
echo ""
