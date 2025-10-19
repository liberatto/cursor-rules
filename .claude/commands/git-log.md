Git 커밋 히스토리를 조회합니다

Usage: `/git-log`
---
allowed-tools: Bash(git log:*)
description: Git 커밋 히스토리를 bash 명령어로 조회합니다. bash 출력 결과만 상위 5개를 출력합니다. 
---

```bash
     git log --oneline --graph -20 --date=format:'%Y-%m-%d %H:%M' --format="%h %ad %s"
```

상위 5개의 커밋 내용을 나열합니다. 커밋 내용은 커밋 메시지와 커밋 날짜, 커밋 번호를 포함합니다. 