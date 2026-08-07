# 부분수정 · 동기화 (safe-edit)

기존 페이지에서 **일부만** 고치되 사람이 만든 펼치기·도식·표·임베드를 소실 없이
보존하는 경로, 그리고 로컬 .md를 SoT로 라이브 페이지에 **반복 반영**하는 동기화 루프.

## ⚠ 적용 범위 — 첨부는 페이지에 매인다 (가장 먼저 읽을 것)

이 절차의 보장은 **첨부(도식·SVG·이미지)가 그 페이지에 물려 있을 때** 성립한다.
**타 페이지의 `data-id`를 그대로 옮겨 붙이는 것은 언제나 실패한다** — 첨부가 따라오지
않기 때문이다.

- `createConfluencePage`로 타 페이지의 `<figure data-id=...>`를 그대로 넣으면,
  Confluence가 이를 **새 페이지 자신의 첨부**로 재해석하고 첨부가 없어
  `data-id="UNKNOWN_MEDIA_ID"`로 **이미지 전멸**(텍스트·표·펼치기는 남음).

**그렇다고 복제가 불가능한 것은 아니다.** 막히는 것은 "id를 그대로 옮기는 것"뿐이며,
**대상 페이지에 도식을 먼저 올려 그 페이지 자신의 첨부를 만든 뒤 id만 갈아끼우면**
텍스트·표·펼치기·도식이 전부 살아서 복제된다 → 아래 §페이지 간 복제. 대안으로
Confluence UI **"페이지 복사(Copy)"**(첨부까지 복제) 후 in-place 부분수정도 유효하다.

## 결론 (먼저)

`updateConfluencePage`는 **부분 패치 API가 아니다 — 페이지 전체 본문을 새 버전으로
덮어쓴다.** 따라서 "일부만 수정"은 **읽기 → 해당 부분만 교체 → 전체 재게시**로
구현하며, **손대지 않은 영역(펼치기·도식·표)을 원형 그대로 보존**하는 것이 전부다.

핵심 안전장치 = **읽기·쓰기를 둘 다 `html` 포맷으로** 한다. MCP 스키마가 "HTML is
round-trip safe"를 보증하며, 펼치기는 `<details>`, 도식은 `<figure>`로 충실히 보존된다.

```
[1] getConfluencePage(contentFormat="html")   → 본문 전체를 HTML로 읽기
[2] 로컬에서 지정된 문단/문장만 교체 (나머지 0글자 변경)
[3] updateConfluencePage(contentFormat="html") → 수정된 전체 본문 재게시 (버전 +1)
```

## 절차 (순서 엄수)

### 1. 읽기 — 반드시 html 포맷
- `getConfluencePage`, `contentFormat="html"` 고정. tiny link 끝 토큰을 `pageId`에
  그대로 넣어도 됨.
- 반환 `body`에서 보존 대상 식별:
  - 펼치기 = `<details ...><summary>제목</summary> ... </details>`
  - 도식·이미지 = `<figure data-type="media-single"><div data-media-type="file" data-id="...">파일명</div></figure>`
  - 임베드 = `<div data-type="embed-card">`, iframe 등

### 2. 부분 교체 — 경계 침범 금지
- 고칠 **문단/문장만** 좁게 지정해 교체. `<details>`·`<figure>` 블록은 **글자 하나
  안 건드린다.**
- ⚠ **함정**: `<details>` 바로 인접한 문단을 고칠 때 경계를 넘으면 펼치기가 깨진다.
  수정 범위를 `<details>` 시작 태그 직전까지로 명확히 끊을 것.
- ⚠ 도식 `data-id`는 첨부 참조다. MCP로 **첨부 업로드는 불가**하지만, 기존 참조 XML을
  보존하면 연결은 그대로 유지된다 → 참조를 삭제·변형하지 말 것.

### 3. 쓰기 — 읽기와 동일 포맷
- `updateConfluencePage`, `contentFormat="html"` (읽기와 반드시 통일).
- ❌ 포맷 혼용 금지: 읽기 html → 쓰기 markdown 하면 변환 손실로 펼치기·표 깨짐.
- 버전 번호는 자동 +1.

## 방법 B — ADF 부분 치환 (단어·문장 몇 곳만 고칠 때)

위 절차(방법 A)는 본문 전체를 읽어 고치고 전체를 다시 보낸다. **긴 문서에서 단어 몇
개만 고칠 때는 본문 왕복 비용이 과하고**, 옮겨 적는 과정에서 오타가 섞일 위험도 있다.
이때는 로그인된 브라우저에서 **ADF의 text 노드만 직접 치환**하고 되돌려 보낸다.

- 본문이 대화로 들어오지 않는다(비용·전사 위험 0). 매크로·펼치기·media id는 손대지
  않으므로 **구조 보존이 구조적으로 보장**된다.
- 조건 = 사용자가 Chrome에 Confluence 로그인. 브라우저 `javascript_tool` 사용.

```js
const id='<pageid>';
const j = await (await fetch(`/wiki/api/v2/pages/${id}?body-format=atlas_doc_format`,
                 {headers:{Accept:'application/json'}})).json();
const d = JSON.parse(j.body.atlas_doc_format.value);
let n0=0; const done=[];
(function w(n){ if(!n||typeof n!=='object')return;
  if(n.type==='text'&&n.text){ n0++;
    /* 여기서 조건에 맞는 노드만 치환하고 done.push(라벨) */
  }
  (n.content||[]).forEach(w);})(d);
if(done.length!==<기대건수>) throw new Error('치환 '+JSON.stringify(done));  // ← 게이트
const res = await fetch(`/wiki/api/v2/pages/${id}`,{method:'PUT',
  headers:{'Content-Type':'application/json',Accept:'application/json','X-Atlassian-Token':'no-check'},
  body: JSON.stringify({id, status:'current', title:j.title,
    body:{representation:'atlas_doc_format', value:JSON.stringify(d)},
    version:{number:j.version.number+1, message:'<변경 요약>'}})});
JSON.stringify({http:res.status, 치환:done, 새버전:(await res.json()).version?.number});
```

### 지켜야 할 3가지

1. **치환 건수 게이트를 PUT 앞에 둔다** — 기대 건수와 다르면 `throw`로 중단. PUT 전에
   던지므로 페이지는 그대로다. (실측: 이 게이트가 잘못된 매칭 1회를 막았다.)
2. **볼드·링크는 별도 text 노드다** ⚠ — `**AO Agent**를 확산` 은 ADF에서
   `[{text:"…자율 수행하는 "},{text:"AO Agent",marks:[strong]},{text:"를 확산"}]` 로
   쪼개진다. **볼드 경계를 걸친 문자열은 절대 매칭되지 않는다.** 먼저 후보 노드를
   조회해 실제 `text`·`marks`를 확인하고, 같은 문자열이 여러 곳(표 셀 등)에 있으면
   **노드 순번(n0)과 marks로 대상 1개만 특정**한다.
3. **새 서식은 못 넣는다** — text 치환이라 없던 볼드·링크를 만들 수 없다. 서식이 바뀌면
   방법 A로 간다. 반대로 라벨 텍스트 교체(`한 줄 정의`→`AO Agent란`)는 볼드 노드의
   text만 바꾸는 것이므로 가능.

### 게시 후 구조 지문 검증

본문을 대화로 끌어오지 않고 **숫자만** 받아 생성본과 대조한다(SKILL.md 게이트 ②).

```js
const j = await (await fetch('/wiki/api/v2/pages/<id>?body-format=atlas_doc_format',
                 {headers:{Accept:'application/json'}})).json();
const d = JSON.parse(j.body.atlas_doc_format.value);
const c={}; let text=''; const media=[]; const seg=[]; let cur={h:'(선두)',len:0};
(function w(n){ if(!n||typeof n!=='object')return; if(n.type)c[n.type]=(c[n.type]||0)+1;
  if(n.type==='media'&&n.attrs)media.push(n.attrs.id);
  if(n.type==='text'&&n.text)text+=n.text; (n.content||[]).forEach(w);})(d);
for(const n of d.content){ const t=JSON.stringify(n).match(/"text":"([^"]*)"/g)||[];
  if(n.type==='heading'){seg.push([cur.h,cur.len]); cur={h:'h',len:0};} }
JSON.stringify({version:j.version.number, textLen:text.length, mediaIds:media, ...c});
```

- 대조 항목 = `heading`·`table`·`tableRow`·`expand`·`media`·`panel`·`blockquote`·`rule`
  카운트 + 미디어 id 목록 + 텍스트 길이. 전부 같으면 통과.
- **알려진 정상 차이 2가지** — ⑴ 펼치기 제목은 ADF에서 `attrs.title`이라 text 길이에
  안 잡힌다(생성본 HTML의 `<summary>` 글자 수만큼 짧게 나옴) ⑵ media div 안 파일명도
  text 노드가 아니다. 이 둘을 뺀 뒤에도 차이가 남으면 실제 유실이다.
- 더 좁히려면 **절(heading) 단위 텍스트 길이**를 뽑아 생성본과 1:1 대조한다 — 어느
  절에서 몇 글자가 어긋났는지까지 특정된다.

## 페이지 간 복제 — 같은 원고를 다른 페이지에도 게시할 때

같은 본문을 **여러 페이지에 올려야 할 때**(예: 기존 게시본 + 신규 공식 보고 페이지)
로컬 원고를 두 번 변환해 두 번 전송하면 본문이 대화를 두 번 통과한다. 본문이 수십 KB면
이 비용이 지배적이다. **이미 라이브에 있는 정상 본문을 브라우저 안에서 복사·치환하면
본문은 대화를 한 번도 통과하지 않는다.**

1. **대상 페이지에 도식을 먼저 업로드** — [`authoring.md`] Part B로 편집기에 도식 전량을
   올리고 게시한다. 이 단계가 있어야 대상 페이지 자신의 첨부가 생긴다.
2. **대상 페이지의 파일명 ↔ fileId 매핑 회수** — `child/attachment?limit=50&expand=extensions`
   로 한 번에 받는다(편집기가 만든 media div에는 파일명이 없어 본문 파싱으로는 매핑 불가).
3. **원본 페이지의 ADF를 조회해 치환** — media 노드를 **본문 등장 순서대로** 새 fileId로
   바꾸고 `attrs.collection`을 `contentId-<대상 페이지 id>`로 바꾼다. 등장 순서는 원고에서
   확인한다(`grep -n` 순서 = ADF media 순서).
4. **함께 반영할 텍스트 변경분이 있으면 같은 패스에서 치환**하고, PUT 전에 게이트를 건다.
5. **PUT** — §방법 B의 PUT 형태 그대로.

```js
// 3~4단계 예시. 게이트가 통과해야만 PUT으로 넘어간다.
const adf = JSON.parse(JSON.stringify(window.__src.adf));       // 원본 페이지 ADF
const NEW = ["<fileId-1>", "…", "<fileId-N>"];                  // 본문 등장 순서
let mi = 0;
(function w(n){ if(n.type==='media'){ n.attrs.id = NEW[mi++];
  n.attrs.collection = 'contentId-<대상 페이지 id>'; } (n.content||[]).forEach(w); })(adf);
const SUBS = [["<옛 문장>","<새 문장>"]];                        // 같이 고칠 텍스트
const hit = SUBS.map(()=>0);
(function w(n){ if(n.type==='text'){ SUBS.forEach((s,i)=>{
  if(n.text===s[0]){ n.text=s[1]; hit[i]++; } }); } (n.content||[]).forEach(w); })(adf);
({mediaReplaced: mi, substitutions: hit, ok: mi===NEW.length && hit.every(h=>h===1)})
```

- **게이트** = `media` 교체 수 == 도식 N · 각 텍스트 치환 정확히 1건 · 게시 후 라이브
  ADF의 `attrs.collection`이 **전부 대상 페이지 것**(하나라도 원본 페이지 id가 남으면
  그 도식은 남의 첨부를 가리키는 상태다).
- **전체 폭·표 폭은 승계되지 않을 수 있다** — 폭은 본문 노드 속성(표 `attrs.width`,
  mediaSingle `attrs.width`)과 **페이지 property**(아래)로 나뉜다. 노드 속성은 ADF를
  복사하므로 따라오지만, property는 페이지마다 따로 걸어야 한다.

> 실측('26.8.6) — 41KB 본문을 이 경로로 신규 페이지에 복제. 구조 지문(heading 18·표 15·
> 도식 7·펼치기 5·패널 2·listItem 86)이 로컬 생성본과 완전 일치했고, 본문은 대화를
> 통과하지 않았다.

## 페이지 전체 폭(full-width) 설정

보기 화면 `⋯` 메뉴에 "전체 폭" 토글이 없는 사이트에서는 **content property로만** 걸린다.
새로 만든 페이지는 기본이 고정 폭(본문 760px)이라 900px 도식이 잘려 보인다.

```js
for (const key of ['content-appearance-published','content-appearance-draft']) {
  const g = await fetch(`/wiki/rest/api/content/<id>/property/${key}`, {headers:{Accept:'application/json'}});
  if (g.status === 404) {                       // 미설정 → 생성
    await fetch('/wiki/rest/api/content/<id>/property', {method:'POST',
      headers:{'Content-Type':'application/json'}, body: JSON.stringify({key, value:'full-width'})});
  } else {                                       // 기설정 → 버전 +1로 갱신
    const cur = await g.json();
    await fetch(`/wiki/rest/api/content/<id>/property/${key}`, {method:'PUT',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({key, value:'full-width', version:{number: cur.version.number+1}})});
  }
}
```

- 키 **2개를 모두** 건다(`published`·`draft`). 되돌리기 = 해당 property 삭제.
- 폭 설정은 본문 게시와 별개 단계다 — 복제·전면교체 후 **매번 확인**할 것.

## 검증 (됐다를 확인하는 법 — 눈으로 보지 말고 프로그램으로)

> 개수 세기만으론 부족하다. `1) 부문 요청` 같은 **헤딩 번호·강조 잔재**는 개수가 같아서
> 안 잡힌다. 실측에서 §6·§7의 잔재를 잡아낸 건 **정규화 토큰 diff**였다.

**재게시 후 반드시 다시 읽어**(`getConfluencePage(html)`) 두 축으로 자동 대조:
1. **매크로 인벤토리** — 라이브 `<figure>` 파일명·`<summary>` 펼치기 제목·임베드를
   추출해 수정 전과 **개수·식별자 동일**한지. `data-id="UNKNOWN_MEDIA_ID"`가 하나라도
   보이면 첨부 끊김(= in-place 위반).
2. **본문 토큰 diff** — 굵게/불릿/구분선 등 포맷 마크업과 매크로 식별자를 **양쪽에서
   정규화 제거**한 뒤 토큰 단위 비교. 유사도 **1.0000 / 실질 차이 0건**이어야 통과.

→ 번들 스크립트로 한 방에:
```
python scripts/verify-parity.py <local.md> <live.html>
# live.html = getConfluencePage(html) body를 저장한 파일
# 출력: 매크로 인벤토리 누락 + 본문 유사도(1.0000 목표) + 실질 차이 라인
```
**눈으로 확인하라고 사용자에게 떠넘기지 말 것** — 위 대조를 돌려 0건을 확인한 뒤 보고.

## 안전 운영 원칙
- **대형·중요 페이지**는 수정 전 `body`를 로컬에 백업 저장(롤백 대비).
- 수정 범위가 매크로 인접이면, **"바꾸기 전/후" 해당 부분을 사용자에게 먼저 보여주고
  확정받은 뒤** 재게시 (경계 침범 원천 차단).

## 로컬 .md ↔ 라이브 동기화 루프 (반복 반영 시)

1회 수정이 아니라 **로컬 .md를 계속 고쳐 라이브에 반영**하는 작업이면 SoT를 나눈다:

```
텍스트의 SoT = 로컬 .md          (사용자가 편집)
매크로의 SoT = 라이브 페이지      (도식·펼치기 — UI에서 업로드/큐레이션)
둘을 잇는 열쇠 = 식별자: 도식=파일명 / 펼치기=summary 제목
```

- **베이스라인 1회 정합 (루프 시작 전 필수)**: 로컬 placeholder의 식별자(파일명·펼치기
  제목)를 **라이브 실제 매크로와 1:1로 맞춘다.** 안 맞으면 이후 매칭 실패.
  - 로컬 placeholder 권장형: `> 📂 **펼치기** [원격: 「<정확한 summary 제목>」] — 설명 · 도식: \`파일명.svg\``
  - 제목 매칭 시 **선두 `📂 `는 무시**하고 비교한다. 라이브 제목에는 하우스 규약상
    `📂 `가 붙지만(→ [`html-nodes.md`] §펼치기) 로컬 「」 안에는 아이콘 없는 제목을 쓴다.
    **이미 있는 라이브 제목에 📂를 새로 붙이지 않는다** — 매크로는 불변이 원칙이고,
    제목이 바뀌면 그 자체가 매칭 열쇠를 깨뜨린다. 규약은 **새로 만드는 펼치기**에만 적용.
  - 합성/복제로 만든 라이브엔 원본에서 딸려온 **잉여 블록·헤딩 번호(`1) 2)`)**가 남기
    쉽다 → 베이스라인에서 토큰 diff로 색출해 로컬 기준으로 정리.
- **반영(매 회)**: 라이브를 html로 read → 로컬 텍스트 변경분만 교체 → 재게시. 매크로
  `<figure>`·`<details>` 블록은 **식별자로 찾아 보존**(글자 불변).
- **이동** = 로컬에서 placeholder 줄을 옮김 → 라이브의 해당 매크로 블록 통째 이동.
  **삭제** = placeholder 줄 삭제(또는 `<!-- DELETE -->`) → 라이브 본문에서 참조 제거
  (단 첨부 실파일은 페이지에 잔존 = 화면 미표시).
- **신규/교체 도식** = 그 파일은 [`authoring.md`] Part B로 **브라우저 업로드** 후 참조를
  본문에 넣는다(MCP 단독 불가). 도식 없는 **텍스트 펼치기는 MCP로 생성 가능**.
- **마무리** = `scripts/verify-parity.py`로 매크로·본문 0건 확인 후 보고.
- **프로젝트 바인딩**(라이브 page id·tiny link)은 스킬이 아니라 **해당 .md의 프론트
  매터/SoT 문서**에 둔다(스킬은 범용 절차만).

## MCP 능력·한계 (요약)
| 항목 | 가능 |
|------|:--:|
| 본문 텍스트·표·문단 수정 (html round-trip) | ✅ |
| 펼치기·도식·임베드 보존 | ✅ |
| 첨부파일(이미지/SVG) 신규 업로드 | ❌ (브라우저 우회 → [`authoring.md`] Part B) |
| CSS·JS(`class`·`<style>`·`<script>`) 반입 | ❌ (하드 거부 또는 조용한 소멸 → [`html-nodes.md`] §CSS·JavaScript 반입 한계) |
| 같은 페이지 in-place 도식 보존 | ✅ (첨부가 그 페이지에 있을 때) |
| 타 페이지 `data-id`를 새 페이지에 그대로 인용 | ❌ (첨부 미이관 → `UNKNOWN_MEDIA_ID`) |
| 본문+도식을 다른 페이지로 복제 | ✅ (대상에 도식 선업로드 후 id·collection 치환 → §페이지 간 복제 / UI Copy도 가능) |
| 매크로 복잡 레이아웃 | ⚠ 포맷 통일 시 보존, 혼용 시 깨짐 |
