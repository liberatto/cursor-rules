# 작성 · 파일 업로드 (authoring)

새 페이지를 짓거나 기존 페이지 본문을 **전면 교체**하고, 콘텐츠에 로컬 파일이 필요하면
그 파일을 올려 임베드하는 경로. `updateConfluencePage`는 본문 전체를 새 버전으로
덮어쓰므로, 남길 게 있는 부분수정이라면 여기가 아니라 [`safe-edit.md`]로 간다.

> 역할 분담: **글 = MCP**(HTML을 정밀 제어), **파일 반입 = 브라우저**(첨부 생성은
> 브라우저에서만 가능). 둘을 섞지 말고 순서대로 쓴다.

## Part A — 글쓰기 (기본)

1. **대상 확정** — `getConfluencePage(cloudId, pageId, contentFormat:"html")`로 현재
   본문·spaceKey·`contentId-<pageid>`를 확인한다. tiny link(`/wiki/x/XXXX`)만 있으면
   page_id 디코딩(base64url little-endian, 길이 부족 시 끝에 `A` 패딩). 새 페이지면
   `spaceId`·`parentId` 준비.
   - 검증: 응답에 기대한 페이지 제목·space가 나오는가.
2. **본문 작성** — HTML을 조립해 `updateConfluencePage`(기존) 또는
   `createConfluencePage`(신규)에 `contentFormat:"html"`로 전송. 표·패널·상태·펼치기·
   코드·미디어 노드 문법은 → [`html-nodes.md`]. 노드가 많거나 특수문자·UUID가 섞이면
   손으로 쓰지 말고 **`scripts/md2confluence.py`로 body를 생성**한다 — 원고 .md를 받아
   하우스 규약(패널 승격·`📂 ` 펼치기·표 900px·media 파일명)을 적용한 HTML을 만들고,
   원고의 불릿·`<br>` 개수를 대조하는 **손실 게이트**를 게시 전에 통과시킨다.
   ```
   python scripts/md2confluence.py <원고.md> -o body.html \
          --page-id <대상 페이지id> --file-ids <fileids.json>
   ```
   `--page-id`는 media `collection`에 쓰이므로 **대상 페이지의 id**여야 한다(다른 페이지
   값을 넣으면 남의 첨부를 가리켜 이미지가 전멸한다). `--file-ids`는 5단계에서 회수한
   `{파일명: fileId}` 매핑이며 **원고 옆에 둔다**(스킬은 범용 절차만 — 예:
   `reports/ao-agent/figures/fileids-<pageid>.json`).
   - **펼치기 지시가 붙은 절** — 로컬 원고에 `> Confluence 펼치기(Expand) 수록` 류의
     지시가 달린 절은 그 절을 통째로 `<details>`로 감싸고, `<summary>`는 **절 제목 앞에
     `📂 `를 붙여** 만든다(예: `📂 [참고] PoC 상세 기록`). 지시 줄 자체는 작성 지침이므로
     본문에 싣지 않는다 → [`html-nodes.md`] §펼치기.
   - ⚠ **CSS·JS를 실어 보내지 않는다** — `class`·이벤트 핸들러가 하나라도 섞이면 요청
     전체가 거부돼 본문이 아예 갱신되지 않는다. 로컬 HTML을 옮길 때 먼저 걷어낸다
     → [`html-nodes.md`] §CSS·JavaScript 반입 한계.
   - 검증: 응답의 `version.number`가 올랐는가(신규는 id 발급).
3. **렌더링 확인** — `getConfluencePage(...html)` 재조회로 노드 보존 확인, 또는 보기
   페이지 스크린샷으로 실제 렌더링을 눈으로 확인. **성공 응답이 표현 보존을 뜻하지
   않는다** — `<style>`·`font-size` 등은 에러 없이 소멸하므로 재조회를 생략하지 않는다.

## Part B — 파일 업로드·임베드 (콘텐츠에 로컬 파일이 필요할 때만)

### 왜 브라우저를 거치는가

**MCP는 Confluence 첨부를 만들지 못한다.** `<div data-type="media">`만 본문에 써넣어도
실체 첨부가 없으면 `UNKNOWN_MEDIA_ID`로 이미지가 전멸한다. 첨부라는 실체는 편집기에
파일을 올려야만 생긴다 — 그래서 로그인된 브라우저를 한 번 거친다. 브라우저의 역할은
**첨부 생성**까지고, 배치·크기 같은 레이아웃은 다시 Part A(MCP)로 정밀하게 잡는다.

### 파일 형식 — SVG 우선 (기본 규칙)

같은 도식이 `.svg`와 `.png`로 함께 있으면 **SVG를 올리고 임베드한다.** 도식은 SVG로
먼저 만드는 것이 이 저장소의 작업 순서라, PNG는 파생본이고 **갱신이 밀려 stale하기
쉽다**(실측: SVG를 고친 뒤 PNG를 다시 뽑지 않아 이틀 묵은 PNG가 남아 있었음).

- 이미 게시된 페이지를 갱신할 때는 **현재 본문이 인용 중인 형식을 먼저 확인**한다 —
  첨부에 두 형식이 다 있어도 본문 media가 가리키는 건 하나뿐이다(5단계 매핑 참조).
- PNG가 필요하면(뷰어 호환·발표 삽입) SVG에서 **그때 다시 렌더**한다:
  `rsvg-convert -w 1280 -h 720 in.svg -o out.png` — 원본을 손대지 않고 파생본만 갱신.
- 파생 PNG를 새로 뽑았으면 **원본 SVG와 함께 갱신**해 두 형식이 어긋나지 않게 한다.

### 함정 (먼저 읽을 것)

- **경로 제약** — 브라우저 `file_upload`는 세션 접근 경로만 받는다(작업 디렉토리·
  `outputs/`·연결 폴더). 그 밖 경로 거부. 1회 호출 합계 **10MB 미만** — 많으면 여러 번에
  나눠 올린다(순서·완결은 아래 별도 함정 참조).
- **대량 업로드는 순서·완결을 보장하지 않는다** ⚠ — 편집기가 파일을 **비동기로 삽입**해,
  여러 장을 올리면 **삽입 순서가 뒤섞이거나 일부가 게시 전 누락**될 수 있다(실측: 30장
  업로드에서 순서 뒤섞임 + 1장 드롭). 대응 셋 — ① 파일명에 **0-패딩 순번 접두사**
  (`01-`·`02-`…, 두 자리로 맞춰야 사전식 정렬이 맞다)를 붙여 올리고, 재구성 때 **paths
  순서가 아니라 파일명으로 정렬**(`media_figures.py extract --sort-name`) ② 업로드 후
  **모든 이미지가 편집기에 렌더될 때까지 대기**한 뒤 게시 ③ 게시 후 **회수 미디어 수 ==
  기대 N** 대조(`--expect N`), 부족하면 누락분(파일명으로 식별)만 재업로드.
- **툴바 버튼을 클릭하지 않는다** — "이미지 추가" 버튼을 누르면 네이티브 파일 피커가
  떠서 자동화가 막힌다. 대신 DOM에 숨은 `button[type="file"]`을 `find`로 찾아
  `file_upload`의 ref로 파일을 직접 주입한다.
- **삽입 지점 = 현재 커서, 새로 연 편집기는 문서 맨 앞** ⚠ — 파일은 **현재 선택 위치**에
  삽입되는데, edit-v2를 새로 열면 커서가 **문서 시작**에 있다. 그대로 올리면 새 미디어가
  **보존해야 할 상단 텍스트 앞에 쌓이고**, 게시하면 라이브에서 그 텍스트가 슬라이드 아래로
  밀려 **"앞부분 텍스트가 사라진 것처럼" 보인다**(실측: 세미나 슬라이드 교체 때 상단
  개요·목차 테이블이 슬라이드 밑으로 밀려 사용자가 유실로 오인). 대응 — **업로드 전 본문
  맨 끝 블록을 클릭**해 커서를 끝에 두고 올리면 최소한 보존 텍스트 **뒤**에 쌓인다(장 간
  순서는 어차피 6단계 재구성이 파일명으로 잡음).
  - 이 한 줄을 건너뛰면 실제로 밟는다(실측 '26.8.6: 완성된 페이지에 도식 1장을 갱신하며
    커서 이동을 생략해 **최상단에 잉여 도식이 삽입**됨). 뒤이어 본문을 6단계로 재구성한다면
    잉여는 자연히 사라지지만, **재구성 없이 잉여만 걷어내는 경우**는 위치를 믿지 말고
    id로 식별한다 → §완성된 페이지에서 도식 몇 장만 교체할 때.
- **브라우저 스토리지에 백업을 못 남긴다** ⚠ — `sessionStorage`·`localStorage`는 확장
  정책에 막혀 쓸 수 없다(실측: `setItem` 후 `getItem`이 `null`/길이 0, 키에 따라
  `[BLOCKED: Sensitive key]`). 페이지를 이동하면 `window.__…`에 담아둔 원본 ADF도 함께
  사라지므로, **백업을 전제로 한 절차를 짜지 말 것**. 대신 ⑴ 편집이 필요하면 **탭을
  옮기지 않고** 같은 탭에서 끝내거나 ⑵ 이동 후 **라이브를 다시 조회**해 id·구조로 대상을
  식별한다(Confluence는 이전 버전을 히스토리에 보관하므로 원본은 언제든 되읽을 수 있다).
- **게시~재구성 사이 라이브는 깨져 보인다** ⚠ — 4단계 게시본은 순서가 뒤섞이고(위 삽입지점
  문제까지 겹치면 보존 텍스트가 밀려 있다) 폭도 작다. **4→6단계를 끊지 말고 연속 수행**해
  깨진 상태의 노출을 최소화하고, **사용자가 지켜보는·공유된 페이지**면 시작 전에 "중간에
  순서가 뒤섞여 보이다 마지막에 정렬된다"고 **미리 알린다**(안 그러면 유실로 오인해 놀란다).
- **덮어쓰기 순서** — 본문을 MCP로 먼저 덮으면 안 된다. **업로드→게시가 먼저**, 그다음
  게시된 본문에서 회수한 `data-id`를 인용해 재구성한다.
- **기본 폭이 작다** — 업로드 직후 figure는 `data-width="250"`. 슬라이드처럼 크게
  보이려면 재구성 때 폭을 키운다(예 760~960).

### 절차

0. **사전조건** — 사용자가 Chrome에 Confluence 로그인, 파일이 세션 접근 경로 안.
   브라우저 도구가 deferred면 한 번에 로드:
   `ToolSearch "select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__find,mcp__claude-in-chrome__file_upload"`
1. **편집기 열기** — `tabs_context_mcp{createIfEmpty:true}`로 새 탭 → `navigate`
   `https://<site>/wiki/spaces/<KEY>/pages/edit-v2/<id>`. → 검증: 스크린샷에 편집 화면.
2. **file input 확보 + 커서를 본문 끝에** — `find "file input for uploading images or
   attachments"` → ref. 이어서 **보존할 텍스트가 있으면 본문 맨 끝 블록을 `computer`
   left_click**해 커서를 끝에 둔다(새 미디어가 그 텍스트 앞에 삽입되는 사고 방지 — 함정 참조).
3. **업로드** — `file_upload{paths:[0-패딩 순번 접두사로 정렬된 절대경로…], ref, tabId}`.
   많으면 10MB 단위로 여러 콜. ⚠ **삽입 순서·완결은 보장되지 않는다**(비동기) — 순서는
   파일명 접두사로 나중에 잡고, 완결은 개수로 확인한다(함정 참조). → 검증: "Uploaded N
   file(s)" 응답 + **게시 전** 편집기에 N개가 모두 렌더됐는지 육안 확인.
4. **게시** — "업데이트/게시" 버튼 클릭 → `wait` 2~3초. → 검증: 탭 URL이 `edit-v2`를
   벗어나 보기 URL로 전환.
5. **data-id 회수** — `getConfluencePage(...html)` 결과를
   `scripts/media_figures.py extract --sort-name --expect N`에 물려 **파일명 순**으로
   정렬된 `(data-id, collection, name)`을 뽑는다(문서 순서는 뒤섞였을 수 있어 신뢰 금지).
   stderr의 **개수 == 기대 N**·**중복 파일명 경고**를 확인 — 부족·중복이면 4로 돌아가
   누락분만 재업로드 후 다시 회수한다. 각 파일은 `<figure data-type="media-single">…
   <div data-type="media" data-id="UUID" data-collection="contentId-<pageid>">name</div>
   </figure>` 형태.
   - ⚠ **media div가 비어 있으면 extract로 매핑 불가** — 편집기가 아니라 API로 만들어진
     media 노드는 **파일명 텍스트가 없다**(`<div data-type="media" …></div>`). 이때는
     첨부 REST로 파일명 ↔ fileId를 직접 받는다. 이게 매핑의 **정답 소스**다:
     ```
     GET /wiki/rest/api/content/<pageid>/child/attachment?limit=50&expand=extensions
     GET /wiki/rest/api/content/<pageid>/child/attachment?filename=<파일명>&expand=extensions
         → results[].title (파일명) · results[].extensions.fileId (= media data-id)
     ```
     브라우저 탭에서 이 URL로 이동해 `get_page_text`로 JSON을 읽으면 된다(로그인 세션
     필요). `filename=` 필터를 쓰면 응답이 1건이라 대화 비용이 작다.
   - ⚠ **같은 파일명 재업로드 = fileId 재발급** — 편집기가 "기존 첨부를 대체합니다"로
     받아주지만, **첨부 id(`att…`)는 유지되고 fileId(media data-id)는 새로 발급된다**
     (실측 '26.8.5: `att888078761` 유지, fileId `1d278e36…`→`f81761d1…`).
     **본문 media id를 손으로 교체해야 하는지는 경로에 따라 갈린다** — 단정하지 말고
     게시 후 라이브 ADF의 실제 id를 보고 판단한다:
     - **MCP로 본문을 다시 쓰는 경우** → 내가 써넣는 id가 곧 본문 id이므로 **새 fileId를
       직접 넣어야 한다**(옛 id를 그대로 쓰면 끊긴다).
     - **편집기에서 업로드·게시하는 경우** → Confluence가 **본문의 기존 media 노드 id를
       자동으로 새 fileId로 갱신**한다(실측 '26.8.6: 갱신 대상이 이미 새 id였고 교체
       불필요). 이때 손댈 것은 **새로 끼어든 잉여 노드뿐**(아래 §도식 1장만 교체).
   - **재구성 시 media div 안에 파일명을 넣는다**(`media_figures.py build`가 그렇게
     만든다). 파일명이 있어야 다음 회차에 `extract`가 동작하고 `verify-parity.py`의
     도식 인벤토리 대조도 성립한다.
6. **본문 재구성 (Part A로 복귀)** — 텍스트(제목·표·패널)와 figure를 원하는 순서·폭으로
   조립해 `updateConfluencePage`. figure 조립은 `scripts/media_figures.py build --width <px>`로
   생성. `data-id`·`data-collection`은 절대 바꾸지 않는다(왕복 안전). 바꿔도 되는 것 =
   `data-width`·`data-layout`·순서·주변 텍스트.
   - 원고 .md 전체를 다시 조립하는 경우라면 `md2confluence.py`가 figure까지 만들어 주므로
     `build`를 따로 부르지 않아도 된다(두 스크립트가 같은 `FIG` 템플릿을 공유한다).
     그 밖의 변환기를 쓰더라도 **figure 조립만은 `build`의 템플릿을 쓴다** — 손으로 쓰면
     UUID·속성이 훼손된다. 스크립트를 모듈로 import해 `media_figures.FIG.format(...)`을
     호출해도 된다.
   - ⚠ **media div를 빈 채로 내보내면 다음 회차가 비싸진다** — 파일명이 없으면 `extract`가
     매핑을 못 해 매번 첨부 REST로 우회해야 하고, `verify-parity.py`의 도식 인벤토리
     대조도 통째로 실패한다(실측 '26.8.6: 자체 변환기가 파일명을 빠뜨려 fileId를 REST로
     받아옴 / '26.8.8: 같은 산출물에서 도식 7종이 전부 "라이브에 없음"으로 잡힘).
     변환기를 새로 쓰더라도 `<div data-type="media" …>` **안에 파일명 텍스트를 반드시
     넣을 것**.
7. **검증** — SKILL.md §검증 3게이트. 이미지 로드는 보기 페이지에서 프로그램으로 전수
   확인한다(스크린샷은 화면에 보이는 것만 잡는다). ⚠ **단순 셀렉터 한 방은 실패한다** —
   실측 3가지 함정을 모두 피한 형태가 아래다:
   - `main img`로는 **0건**이 잡힌다(보기 페이지 DOM이 그 구조가 아님) → `document`
     전체에서 `img`를 받아 **표시 폭으로 도식만 거른다**.
   - 도식은 **지연 로드**라 스크롤 없이는 뷰포트 근처 몇 장만 잡힌다(실측: 7장 중 4장).
   - 스크롤러가 **window가 아니다** — `window.scrollBy`·`document.body.scrollHeight`는
     먹지 않는다. 내부 스크롤 div를 찾아 그것을 굴린다(실측 `scrollHeight` 11757).
   - dedupe를 `src`로 하면 **SVG가 data URI라 앞부분이 전부 같아** 1건으로 뭉개진다
     → **요소 자체를 `Set`에 담는다**.
   ```js
   const els = new Set();
   const collect = () => [...document.querySelectorAll('img')]
     .filter(i => i.getBoundingClientRect().width > 300).forEach(i => els.add(i));
   const sc = [...document.querySelectorAll('div')]
     .filter(d => d.scrollHeight > d.clientHeight + 500 && d.clientHeight > 300)
     .sort((a,b) => b.scrollHeight - a.scrollHeight)[0];        // 실제 스크롤 컨테이너
   collect();
   if (sc) { for (let y=0; y<sc.scrollHeight; y+=500) { sc.scrollTop=y;
     await new Promise(r=>setTimeout(r,400)); collect(); } sc.scrollTop=0; }
   const v=[...els].map(i=>({ok:i.complete&&i.naturalWidth>0,
     nat:`${i.naturalWidth}x${i.naturalHeight}`, disp:Math.round(i.getBoundingClientRect().width)}));
   ({seen:v.length, allLoaded:v.every(x=>x.ok), widths:[...new Set(v.map(x=>x.disp))]})
   ```
   기대 = `seen` == 도식 N · `ok` 전부 true · 표시 폭이 지정 폭과 일치.
   - 그래도 N에 못 미치면 **라이브 ADF로 대신 확인한다**(게이트 ②) — media 노드 개수와
     `attrs.collection`이 `contentId-<이 페이지>`인지 보면 첨부 연결은 확정된다. 렌더는
     핵심 도식 1~2장만 스크린샷으로 눈확인하면 충분하다.

## 완성된 페이지에서 도식 몇 장만 교체할 때 (짧은 경로)

이미 정상 게시된 페이지의 도식 파일만 갱신하는 경우다. 위 6단계 "본문 재구성"을 다시
돌릴 필요가 없다 — 편집기 업로드가 본문 기존 media를 자동 갱신하므로, **끼어든 잉여
노드만 걷어내면 끝난다**.

1. 편집기(`edit-v2`)를 열고 **바뀐 파일만** 업로드 → 게시.
2. 라이브 ADF를 조회해 media 노드를 세고, **잉여 노드를 새 fileId로 식별**한다. 첨부
   REST(`child/attachment?filename=…&expand=extensions`)로 그 파일의 **현재 fileId**를
   받은 뒤, 본문 media 배열에서 그 id가 **두 번** 나오면 한쪽이 잉여다.
   - 잉여는 **삽입 위치로 찾지 않는다** — 커서가 문서 맨 앞이면 최상단에, 끝이면 최하단에
     생겨 위치가 일정하지 않다. **정상 위치의 노드는 이미 새 id로 자동 갱신돼 있으므로,
     문서 구조상 있어서는 안 되는 자리(예: 첫 블록이 mediaSingle)의 것을 지운다.**
3. 잉여 `mediaSingle`을 제거하고 ADF를 PUT([`safe-edit.md`] §방법 B의 PUT 형태).
   - 게이트 = 제거 후 **media 개수 == 원래 N**, **첫 블록 타입이 원래대로**(패널·헤딩 등),
     그리고 구조 지문(heading·table·expand·listItem) 불변.

> 실측('26.8.6) — 이 경로로 도식 1장 갱신에 걸린 라이브 편집은 편집기 게시 1회 + PUT
> 1회였다. 본문은 대화를 통과하지 않았다.

## 새 페이지에 파일이 필요할 때

`createConfluencePage`로 만든 새 페이지에 이미지가 들어가야 하면: **① 빈/텍스트 본문으로
페이지를 먼저 만들고 → ② 그 페이지 편집기에 Part B로 업로드 → ③ Part A로 재구성**한다.
빈 페이지 없이 곧장 media 노드를 써넣으면 첨부가 없어 `UNKNOWN_MEDIA_ID`가 된다.

- **올릴 본문이 이미 다른 페이지에 라이브로 있으면** ③을 Part A로 하지 말고
  [`safe-edit.md`] §페이지 간 복제로 간다 — 라이브 ADF를 브라우저 안에서 복사·치환하므로
  본문이 대화를 통과하지 않는다. 본문이 수십 KB일 때 차이가 크다.
- ⚠ **본문 HTML을 셸로 출력해 옮기려 하지 말 것** — 수십 KB는 도구 출력 한도에 걸려
  잘린다(실측 '26.8.6: 41KB가 잘려 나가 경로를 바꿔야 했다). 크기를 먼저 재고(`wc -c`),
  10KB를 넘으면 복제 경로나 §방법 B를 택한다.
