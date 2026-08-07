# Confluence HTML+ 노드 카탈로그

`updateConfluencePage`·`createConfluencePage`에 `contentFormat:html`로 넘길 때 쓰는
노드 모음. Confluence는 CSS class가 아니라 **`data-type` 속성**으로 특수 노드를
구분한다. 여기 있는 형태만 쓰면 렌더링이 어긋나지 않는다.

## 기본 블록

| 용도 | HTML |
|------|------|
| 제목 | `<h1>~<h6>` |
| 문단 | `<p>텍스트</p>` |
| 링크 | `<a href="URL">텍스트</a>` |
| 목록 | `<ul><li>..</li></ul>` · `<ol><li>..</li></ol>` |
| 코드 | `<pre><code class="language-python">..</code></pre>` |

## 표

```html
<table data-layout="default"><tbody>
<tr><th><p>헤더1</p></th><th><p>헤더2</p></th></tr>
<tr><td><p>셀1</p></td><td><p>셀2</p></td></tr>
</tbody></table>
```

- `data-layout`: `default`(본문 폭) · `center` · `wide` · `full-width`.
- 셀 내용은 `<p>`로 감싼다. 셀 안에 제목·패널·목록·미디어는 가능하나 **중첩 표는 불가**.

## 패널 (강조 박스)

```html
<div data-type="panel-info"><p>안내</p></div>
```

`data-type` 값: `panel-info` · `panel-warning` · `panel-note` · `panel-success` · `panel-error`.
패널 안에 **표·펼치기·인용·다른 패널은 넣지 못한다**(단순 문단·목록만).

## 상태 뱃지 (인라인)

```html
<span data-type="status" data-color="green">완료</span>
```

`data-color`: `green` · `red` · `yellow` · `blue` · `neutral` · `purple`.

## 펼치기 (expand)

```html
<details><summary>📂 제목</summary><p>펼친 내용</p></details>
```

- **제목 앞에 `📂 `를 붙인다** (하우스 규약) — 접힌 상태에선 제목 한 줄만 보이므로,
  아이콘이 있어야 "펼쳐볼 게 더 있다"가 눈에 들어온다. 예: `📂 [참고] PoC 상세 기록`.
  - 새로 만드는 펼치기에 적용. 이미 `📂`가 있는 제목에 덧붙이지 않는다.
  - 기존 페이지의 펼치기 제목을 부분수정 중에 바꾸지 않는다 → [`safe-edit.md`].
- 표 셀 안에 넣을 때만 `<details data-type="nested-expand">`.
- **펼치기 안에 표는 넣을 수 있으나, 펼치기를 다시 펼치기로 중첩하지 않는다.**

## 기타 인라인

| 용도 | HTML |
|------|------|
| 날짜 | `<time datetime="YYYY-MM-DD">라벨</time>` |
| 멘션 | `<span data-type="mention" data-user-id="ACCOUNT_ID">@이름</span>` |
| 인라인 카드 | `<a href="URL" data-card-appearance="inline">텍스트</a>` |

## 미디어 (첨부 이미지·파일) — Part B 산출물

브라우저 업로드→게시 후 페이지가 갖게 되는 형태. **이 노드는 손으로 새로 만들지
않는다** — 실제 첨부가 없으면 `UNKNOWN_MEDIA_ID`로 이미지가 사라진다. 반드시 게시된
본문에서 `data-id`를 회수해(→ `scripts/media_figures.py extract`) 그대로 되쓴다.

```html
<figure data-type="media-single" data-layout="center" data-width="760" data-width-type="pixel">
  <div data-type="media" data-media-type="file"
       data-id="UUID" data-collection="contentId-<pageid>"
       data-width="1280" data-height="720">파일명.svg</div>
</figure>
```

- **불변(절대 변경 금지)**: `data-id` · `data-collection`. 실제 첨부를 가리킨다.
- **조정 가능**: `data-layout`(center/wide/full-width) · `data-width`(표시 폭 px) · figure 순서 · 주변 텍스트.
- 여러 파일을 나열하면 각 `media-single`이 세로로 1장씩 쌓인다.

## CSS·JavaScript 반입 한계 (실측)

보낸 HTML은 그대로 저장되지 않고 **ADF 노드로 변환**된다. 그래서 ADF에 대응 표현이 있는
속성만 살아남고, 나머지는 **하드 거부**(요청 전체 실패) 또는 **조용한 소멸** 둘 중 하나다.
스타일시트·스크립트로 꾸미려는 시도는 전부 실패한다.

| 시도 | 결과 | 실제 저장 형태 |
|---|---|---|
| 인라인 `style="color:#RRGGBB"` | ✅ 생존 | `color: rgb(r,g,b)` (textColor 마크) |
| `<p style="text-align:center">` | ✅ 생존 | 문단 정렬 마크 |
| 표 셀 `style="background-color:.."` · `data-background=".."` | ✅ 생존 | 둘 다 `data-highlight-colour`로 통일 |
| 인라인 `style="background-color:.."` | ⚠ 생존하나 **쓰지 말 것** | 배경색과 **동일한 글자색**이 함께 설정돼 글자가 안 보인다 |
| `style="font-size:.."`·`border`·`padding` 등 | ❌ 조용히 소멸 | style만 제거되고 텍스트는 남음 |
| `<div style="..">` 래퍼 | ❌ 조용히 소멸 | div째로 사라지고 내부 블록만 남음 |
| `<style>` 블록 | ❌ 조용히 소멸 | 흔적 없음 |
| `<script>` 블록 | ❌ 조용히 소멸 | 흔적 없음 |
| `class="..."` (코드블록 `language-*` 제외) | 🚫 하드 거부 | `Unsupported attribute 'class'` — **본문 미갱신** |
| `onclick` 등 이벤트 핸들러 | 🚫 하드 거부 | 동일 |
| `<iframe src="..">` | 🔄 변환 | embed 스마트링크 카드(`data-card-appearance="embed"`). `width`·`height`는 하드 거부 |

두 실패 모드의 대처가 다르다.

- **하드 거부** — 에러로 즉시 드러나지만 **하나라도 섞이면 본문이 전혀 갱신되지 않는다**.
  로컬 HTML·md를 옮길 때 `class`·이벤트 핸들러 잔여를 **보내기 전에** 제거한다.
- **조용한 소멸** — 응답은 성공(`version` +1)인데 의도한 표현만 없다. 그래서 스타일을
  넣었으면 재조회 검증(→ [`authoring.md`] Part A 3단계)을 건너뛰지 않는다.

시각 표현이 필요하면 **패널·상태 칩·표 셀 배경·레이아웃 같은 네이티브 노드**로 만들고,
그걸로 안 되는 도식은 **SVG·PNG로 만들어 첨부**한다(→ [`authoring.md`] Part B).

## 금지·주의

- 본문을 `<html>`·`<head>`·`<body>`로 감싸지 않는다.
- CSS class·`<style>`·`<script>`·이벤트 핸들러로 꾸미지 않는다 → §CSS·JavaScript 반입 한계.
- 스토리지 XML(`<ac:structured-macro>`)을 쓰지 않는다 — HTML+ `data-*`로만.
- 특수문자는 엔티티로: `&amp;` `&lt;` `&gt;` `&#39;`(') `&#34;`(").
- ADF 중첩 규칙: task/decision 항목·제목·캡션은 인라인 전용, 목록 항목 안에
  제목·표·패널·펼치기 불가, 패널 안에 표·펼치기·인용·패널 불가.
