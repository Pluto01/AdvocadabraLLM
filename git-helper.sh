#!/bin/bash

# Git Workflow Helper Script for AdvocadabraLLM
# Usage: ./git-helper.sh <command> [args]

set -e

MAIN_BRANCH="main"
DEV_BRANCH="development"

show_help() {
    echo "Git Workflow Helper for AdvocadabraLLM"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  start-feature <name>     Create and switch to a new feature branch"
    echo "  start-bugfix <name>      Create and switch to a new bugfix branch"
    echo "  sync-dev                 Sync development branch with remote"
    echo "  finish-branch            Merge current branch to development and clean up"
    echo "  status                   Show enhanced Git status"
    echo "  clean-branches           Remove merged local branches"
    echo "  setup-hooks             Install Git hooks for commit validation"
    echo ""
    echo "Examples:"
    echo "  $0 start-feature document-analysis"
    echo "  $0 start-bugfix login-error"
    echo "  $0 sync-dev"
    echo "  $0 status"
}

start_feature() {
    local feature_name="$1"
    if [ -z "$feature_name" ]; then
        echo "Error: Feature name is required"
        echo "Usage: $0 start-feature <feature-name>"
        exit 1
    fi
    
    echo "🚀 Starting new feature: $feature_name"
    
    # Switch to development and pull latest
    git checkout $DEV_BRANCH
    git pull origin $DEV_BRANCH
    
    # Create feature branch
    git checkout -b "feature/$feature_name"
    
    echo "✅ Created and switched to feature/$feature_name"
    echo "📝 Don't forget to push your branch: git push -u origin feature/$feature_name"
}

start_bugfix() {
    local bugfix_name="$1"
    if [ -z "$bugfix_name" ]; then
        echo "Error: Bugfix name is required"
        echo "Usage: $0 start-bugfix <bugfix-name>"
        exit 1
    fi
    
    echo "🐛 Starting new bugfix: $bugfix_name"
    
    # Switch to development and pull latest
    git checkout $DEV_BRANCH
    git pull origin $DEV_BRANCH
    
    # Create bugfix branch
    git checkout -b "bugfix/$bugfix_name"
    
    echo "✅ Created and switched to bugfix/$bugfix_name"
    echo "📝 Don't forget to push your branch: git push -u origin bugfix/$bugfix_name"
}

sync_dev() {
    echo "🔄 Syncing development branch..."
    
    # Store current branch
    current_branch=$(git branch --show-current)
    
    # Switch to development and pull
    git checkout $DEV_BRANCH
    git pull origin $DEV_BRANCH
    
    # Switch back to original branch if it wasn't development
    if [ "$current_branch" != "$DEV_BRANCH" ]; then
        git checkout "$current_branch"
        echo "📝 Consider merging development into your current branch:"
        echo "   git merge $DEV_BRANCH"
    fi
    
    echo "✅ Development branch synced"
}

enhanced_status() {
    echo "📊 Enhanced Git Status"
    echo "===================="
    
    # Current branch info
    current_branch=$(git branch --show-current)
    echo "Current branch: $current_branch"
    
    # Show commits ahead/behind
    if git rev-parse --verify origin/$current_branch >/dev/null 2>&1; then
        ahead=$(git rev-list --count origin/$current_branch..$current_branch)
        behind=$(git rev-list --count $current_branch..origin/$current_branch)
        echo "Ahead: $ahead commits | Behind: $behind commits"
    else
        echo "Branch not pushed to remote yet"
    fi
    
    echo ""
    
    # Regular git status
    git status
    
    echo ""
    echo "📝 Recent commits:"
    git log --oneline -5
}

clean_branches() {
    echo "🧹 Cleaning merged branches..."
    
    # Switch to development
    git checkout $DEV_BRANCH
    
    # Delete merged branches (except main and development)
    git branch --merged | grep -v "\* $DEV_BRANCH" | grep -v "$MAIN_BRANCH" | xargs -n 1 git branch -d
    
    echo "✅ Cleaned up merged branches"
}

setup_hooks() {
    echo "⚙️  Setting up Git hooks..."
    
    # Create hooks directory if it doesn't exist
    mkdir -p .git/hooks
    
    # Create commit-msg hook for conventional commits validation
    cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash

# Conventional Commits validation
commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Commit messages must follow Conventional Commits format:"
    echo "  <type>[optional scope]: <description>"
    echo ""
    echo "Examples:"
    echo "  feat: add user authentication"
    echo "  fix: resolve login error"
    echo "  docs: update API documentation"
    echo ""
    exit 1
fi
EOF

    chmod +x .git/hooks/commit-msg
    
    echo "✅ Git hooks installed"
}

# Main script logic
case "$1" in
    start-feature)
        start_feature "$2"
        ;;
    start-bugfix)
        start_bugfix "$2"
        ;;
    sync-dev)
        sync_dev
        ;;
    status)
        enhanced_status
        ;;
    clean-branches)
        clean_branches
        ;;
    setup-hooks)
        setup_hooks
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
