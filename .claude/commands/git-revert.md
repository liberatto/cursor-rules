Git 커밋을 안전하게 되돌립니다

Usage: `/git-revert $ARGUMENTS`
---
allowed-tools: Bash(git revert:*), Bash(git log:*)
argument-hint: $ARGUMENTS [커밋해시|last]
description: Git 커밋을 안전하게 되돌립니다
---

Git 커밋을 안전하게 되돌립니다.

사용법:
- `/git-revert [커밋해시]` - 지정된 커밋을 revert
- `/git-revert last` - 마지막 커밋을 revert

```bash
if [ "$ARGUMENTS" = "last" ]; then
    COMMIT_HASH=$(git log --oneline -1 --format="%h")
    echo "🔄 마지막 커밋($COMMIT_HASH)을 revert합니다..."
    git revert --no-edit --strategy-option=theirs --no-commit HEAD && git commit -C HEAD
else
    echo "🔄 커밋을 revert합니다..."
    git revert --no-edit --strategy-option=theirs --no-commit $ARGUMENTS && git commit -C $ARGUMENTS
fi
```