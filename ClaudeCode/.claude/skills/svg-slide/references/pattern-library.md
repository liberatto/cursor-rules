# 인포그래픽 패턴 라이브러리 (컴포넌트 템플릿)

> **목적**: `SKILL.md §2 도식 유형` 다음 단계에서, 정한 **관계·의도에 맞는 패턴을 골라 시작 골격으로 복사**해 쓰는 재사용 템플릿 모음(18종).
> **시각 인덱스**: 18종을 한눈에 훑으려면 같은 폴더의 `../assets/pattern-gallery.html`을 브라우저로 연다(라이트/다크 대응 갤러리).
> **성격**: 이들은 **컴포넌트(삽입 figure)** — 그 자체로 완결 슬라이드가 아니라, 16:9 캔버스(`assets/boilerplate.svg`) 안에 1~3개를 배치하는 조각. `scripts/check.py`는 **컴포넌트를 담은 최종 슬라이드**에 돌린다(컴포넌트 단독은 16:9·액센트 바 규칙 대상이 아님).
> **색**: 5색 팔레트 하드코딩 — 블루 `#4D73BF`·그린 `#3E9B6B`·앰버 `#E0952F`·코럴 `#C85C5C`·바이올렛 `#6B5FCB` + 중립 그레이. 한 슬라이드 안에서 과용하지 말고 강조 1~2색으로.

---

## 0. 사용 절차

1. `SKILL.md §1` 설계 4단계로 **메시지·정보·관계**를 먼저 확정한다.
2. 아래 **§1 선택 매트릭스**에서 그 관계·의도에 맞는 패턴을 고른다. (맞는 게 없으면 박스형을 직접 구성 — §2 유형 매핑)
3. 해당 패턴의 SVG 스니펫을 복사해 **캔버스 좌표에 맞게 배치·리사이즈**하고, **더미 텍스트·수치를 실제 값으로 교체**한다.
4. 여러 패턴을 조합할 땐 **색·폰트 위계를 한 슬라이드 기준으로 통일**(SKILL.md §5).
5. 최종 슬라이드에 `scripts/check.py`를 돌려 0건 확인 후 마감.

> ⚠ 스니펫의 `viewBox`는 대개 `0 0 384 188`(컴포넌트 기준). 슬라이드에 넣을 땐 `<g transform="translate(x y) scale(s)">`로 감싸 배치하거나 좌표를 슬라이드 스케일로 다시 잡는다. 텍스트는 배치 후 **본문 15px 이상**(SKILL.md 폰트 하한)인지 재확인.

---

## 1. 선택 매트릭스 — 관계·의도 → 패턴

| 강조할 관계·의도 | 패턴 | 카테고리 |
| --- | --- | --- |
| 순서·단계 흐름 | **프로세스 스텝** | 흐름·시간 |
| 일정·마일스톤 | **타임라인 · 로드맵** | 흐름·시간 |
| 반복·순환 루프 | **순환 사이클** | 흐름·시간 |
| 단계별 감소·전환 | **퍼널** | 흐름·시간 |
| 계층·소속 | **계층 트리** | 구조·관계 |
| 시스템 레이어 | **레이어드 아키텍처** | 구조·관계 |
| 중심-주변 연결 | **네트워크 · 연결** | 구조·관계 |
| 2축 포지셔닝 | **2×2 매트릭스** | 구조·관계 |
| 개선 전후 대비 | **Before / After** | 비교·구성 |
| 양·규모·추이 비교 | **막대 차트** | 비교·구성 |
| 전체 구성비 (≤5) | **도넛 구성비** | 비교·구성 |
| 교집합·시너지 | **벤 다이어그램** | 비교·구성 |
| 핵심 수치 나열 | **KPI 스탯 타일** | 숫자·지표 |
| 단일 달성률·진행 | **도넛 게이지** | 숫자·지표 |
| 항목별 진척률 | **진행 막대** | 숫자·지표 |
| 수량·비율 감각 | **아이소타입 (픽토그래프)** | 숫자·지표 |
| 메시지 3~4개 강조 | **콜아웃 하이라이트** | 강조 |
| 단 하나의 숫자 | **대형 스테이트먼트** | 강조 |

- **박스형·화살표가 기본** — 위 패턴 중 딱 맞는 게 없으면 억지로 끼우지 말고 `SKILL.md §2`대로 박스+화살표로 직접 구성한다.
- **한 장 한 메시지** — 한 슬라이드에 패턴 1~2개. 세 개 이상 욱여넣으면 분할(§1.3).

---

## 2. 패턴 카탈로그

### 1. 숫자 · 지표

#### KPI 스탯 타일  `지표`

- **언제**: 핵심 수치 3~4개를 아이콘 배지와 함께 병렬 배치. 요약 슬라이드 상단에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="KPI 스탯 타일 예시">
            <!-- tile 1 -->
            <rect x="4" y="16" width="118" height="156" rx="14" fill="#EEF3FC"/>
            <circle cx="63" cy="56" r="20" fill="#4D73BF"/>
            <path d="M55 56l6 6 12-13" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="63" y="112" font-size="30" font-weight="800" fill="#23375F" text-anchor="middle">128</text>
            <text x="63" y="140" font-size="13" fill="#5A6472" text-anchor="middle">완료 건수</text>
            <!-- tile 2 -->
            <rect x="133" y="16" width="118" height="156" rx="14" fill="#E7F4EC"/>
            <circle cx="192" cy="56" r="20" fill="#3E9B6B"/>
            <path d="M192 45v22M181 56h22" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>
            <text x="192" y="112" font-size="30" font-weight="800" fill="#1F5F3E" text-anchor="middle">+24%</text>
            <text x="192" y="140" font-size="13" fill="#5A6472" text-anchor="middle">전년 대비</text>
            <!-- tile 3 -->
            <rect x="262" y="16" width="118" height="156" rx="14" fill="#FBF1DE"/>
            <circle cx="321" cy="56" r="20" fill="#E0952F"/>
            <circle cx="321" cy="56" r="9" fill="none" stroke="#fff" stroke-width="3"/>
            <path d="M321 51v6l4 3" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="321" y="112" font-size="30" font-weight="800" fill="#8A5A12" text-anchor="middle">3.2s</text>
            <text x="321" y="140" font-size="13" fill="#5A6472" text-anchor="middle">평균 응답</text>
          </svg>
```

#### 도넛 게이지  `비율`

- **언제**: 단일 비율·달성률을 원형 링으로. 목표 대비 진행을 직관적으로.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="도넛 게이지 예시">
            <circle cx="98" cy="94" r="60" fill="none" stroke="#E9EDF4" stroke-width="20"/>
            <circle cx="98" cy="94" r="60" fill="none" stroke="#4D73BF" stroke-width="20" stroke-linecap="round"
                    stroke-dasharray="271.4 105.4" transform="rotate(-90 98 94)"/>
            <text x="98" y="88" font-size="34" font-weight="800" fill="#23375F" text-anchor="middle">72%</text>
            <text x="98" y="112" font-size="12.5" fill="#7B8594" text-anchor="middle">달성</text>
            <text x="210" y="70" font-size="17" font-weight="700" fill="#1a1a1a">목표 달성률</text>
            <rect x="210" y="86" width="30" height="10" rx="5" fill="#4D73BF"/>
            <text x="248" y="95" font-size="13" fill="#5A6472">달성 72%</text>
            <rect x="210" y="106" width="30" height="10" rx="5" fill="#E9EDF4"/>
            <text x="248" y="115" font-size="13" fill="#5A6472">잔여 28%</text>
            <text x="210" y="142" font-size="12.5" fill="#9AA3AE">목표 대비 진행 상황</text>
          </svg>
```

#### 진행 막대  `지표`

- **언제**: 여러 항목의 진척률을 나란히. 과제·단계별 상태 비교에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="진행 막대 예시">
            <g font-size="13.5" fill="#3A4658">
              <text x="4" y="42">기획</text>
              <text x="4" y="86">설계</text>
              <text x="4" y="130">개발</text>
              <text x="4" y="174">검증</text>
            </g>
            <g>
              <rect x="70" y="30" width="250" height="14" rx="7" fill="#EEF1F6"/>
              <rect x="70" y="30" width="250" height="14" rx="7" fill="#3E9B6B"/>
              <rect x="70" y="74" width="250" height="14" rx="7" fill="#EEF1F6"/>
              <rect x="70" y="74" width="220" height="14" rx="7" fill="#4D73BF"/>
              <rect x="70" y="118" width="250" height="14" rx="7" fill="#EEF1F6"/>
              <rect x="70" y="118" width="145" height="14" rx="7" fill="#4D73BF"/>
              <rect x="70" y="162" width="250" height="14" rx="7" fill="#EEF1F6"/>
              <rect x="70" y="162" width="60" height="14" rx="7" fill="#E0952F"/>
            </g>
            <g font-size="13" font-weight="700" fill="#3A4658" text-anchor="end" font-variant-numeric="tabular-nums">
              <text x="380" y="42">100%</text>
              <text x="380" y="86">88%</text>
              <text x="380" y="130">58%</text>
              <text x="380" y="174">24%</text>
            </g>
          </svg>
```

#### 아이소타입 (픽토그래프)  `비율`

- **언제**: 수량·비율을 아이콘 개수로. 숫자보다 감각적으로 와닿음.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="아이소타입 픽토그래프 예시">
            <defs>
              <g id="person">
                <circle cx="0" cy="-9" r="7"/>
                <path d="M-12 14a12 12 0 0 1 24 0z"/>
              </g>
            </defs>
            <text x="4" y="30" font-size="15" font-weight="700" fill="#1a1a1a">참여율 &#160;<tspan fill="#4D73BF">7 / 10</tspan></text>
            <g transform="translate(30 68)">
              <use href="#person" x="0"   fill="#4D73BF"/>
              <use href="#person" x="60"  fill="#4D73BF"/>
              <use href="#person" x="120" fill="#4D73BF"/>
              <use href="#person" x="180" fill="#4D73BF"/>
              <use href="#person" x="240" fill="#4D73BF"/>
              <use href="#person" x="0"   y="58" fill="#4D73BF"/>
              <use href="#person" x="60"  y="58" fill="#4D73BF"/>
              <use href="#person" x="120" y="58" fill="#D3DAE5"/>
              <use href="#person" x="180" y="58" fill="#D3DAE5"/>
              <use href="#person" x="240" y="58" fill="#D3DAE5"/>
            </g>
            <text x="24" y="176" font-size="12.5" fill="#9AA3AE">아이콘 1개 = 대상 10%</text>
          </svg>
```

### 2. 흐름 · 시간

#### 프로세스 스텝  `흐름`

- **언제**: 순서 있는 단계를 화살표로 연결. 방법론·파이프라인 설명에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="프로세스 스텝 예시">
            <g>
              <rect x="6" y="52" width="78" height="72" rx="12" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.6"/>
              <rect x="106" y="52" width="78" height="72" rx="12" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.6"/>
              <rect x="206" y="52" width="78" height="72" rx="12" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.6"/>
              <rect x="306" y="52" width="72" height="72" rx="12" fill="#4D73BF"/>
            </g>
            <g text-anchor="middle">
              <text x="45"  y="82" font-size="20" font-weight="800" fill="#4D73BF">1</text>
              <text x="45"  y="106" font-size="12.5" fill="#3A4658">수집</text>
              <text x="145" y="82" font-size="20" font-weight="800" fill="#4D73BF">2</text>
              <text x="145" y="106" font-size="12.5" fill="#3A4658">분석</text>
              <text x="245" y="82" font-size="20" font-weight="800" fill="#4D73BF">3</text>
              <text x="245" y="106" font-size="12.5" fill="#3A4658">검증</text>
              <text x="342" y="82" font-size="20" font-weight="800" fill="#fff">4</text>
              <text x="342" y="106" font-size="12.5" fill="#DCE7FA">배포</text>
            </g>
            <g fill="#A6B4C8">
              <path d="M88 88l14 0m0 0l-5-4m5 4l-5 4" stroke="#A6B4C8" stroke-width="2" fill="none" stroke-linecap="round"/>
              <path d="M188 88l14 0m0 0l-5-4m5 4l-5 4" stroke="#A6B4C8" stroke-width="2" fill="none" stroke-linecap="round"/>
              <path d="M288 88l14 0m0 0l-5-4m5 4l-5 4" stroke="#A6B4C8" stroke-width="2" fill="none" stroke-linecap="round"/>
            </g>
          </svg>
```

#### 타임라인 · 로드맵  `시간`

- **언제**: 마일스톤을 시간축에. 완료·진행·예정을 채움으로 구분.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="타임라인 로드맵 예시">
            <line x1="20" y1="94" x2="364" y2="94" stroke="#D3DAE5" stroke-width="3"/>
            <line x1="20" y1="94" x2="210" y2="94" stroke="#4D73BF" stroke-width="3"/>
            <g>
              <circle cx="40" cy="94" r="9" fill="#4D73BF"/>
              <circle cx="135" cy="94" r="9" fill="#4D73BF"/>
              <circle cx="230" cy="94" r="9" fill="#fff" stroke="#4D73BF" stroke-width="3"/>
              <circle cx="325" cy="94" r="9" fill="#fff" stroke="#C3CCDA" stroke-width="3"/>
            </g>
            <g font-size="13" font-weight="700" fill="#23375F" text-anchor="middle">
              <text x="40" y="58">1분기</text>
              <text x="135" y="58">2분기</text>
              <text x="230" y="140">3분기</text>
              <text x="325" y="140">4분기</text>
            </g>
            <g font-size="11.5" fill="#7B8594" text-anchor="middle">
              <text x="40" y="42">기획 완료</text>
              <text x="135" y="42">PoC</text>
              <text x="230" y="156">상용화</text>
              <text x="325" y="156">확산</text>
            </g>
          </svg>
```

#### 순환 사이클  `반복`

- **언제**: 끝이 처음으로 돌아가는 루프. 운영 사이클·반복 개선에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="순환 사이클 예시">
            <g fill="none" stroke="#B9C6DC" stroke-width="2">
              <path d="M150 40a54 54 0 0 1 46 26" marker-end="url(#ah)"/>
              <path d="M204 90a54 54 0 0 1 -30 50" marker-end="url(#ah)"/>
              <path d="M164 148a54 54 0 0 1 -56 -12" marker-end="url(#ah)"/>
              <path d="M96 122a54 54 0 0 1 20 -74" marker-end="url(#ah)"/>
            </g>
            <defs>
              <marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
                <path d="M0 0l6 4l-6 4z" fill="#8FA1BD"/>
              </marker>
            </defs>
            <g>
              <circle cx="150" cy="38" r="24" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.6"/>
              <circle cx="212" cy="94" r="24" fill="#E7F4EC" stroke="#3E9B6B" stroke-width="1.6"/>
              <circle cx="150" cy="150" r="24" fill="#FBF1DE" stroke="#E0952F" stroke-width="1.6"/>
              <circle cx="88" cy="94" r="24" fill="#F3EEFB" stroke="#6B5FCB" stroke-width="1.6"/>
            </g>
            <g font-size="12.5" font-weight="700" text-anchor="middle" fill="#2b3440">
              <text x="150" y="42">계획</text>
              <text x="212" y="98">실행</text>
              <text x="150" y="154">점검</text>
              <text x="88" y="98">개선</text>
            </g>
            <text x="300" y="90" font-size="15" font-weight="700" fill="#1a1a1a">PDCA</text>
            <text x="300" y="110" font-size="12.5" fill="#7B8594">반복 개선 루프</text>
          </svg>
```

#### 퍼널  `전환`

- **언제**: 단계마다 줄어드는 전환. 유입→구매, 지원자→합격에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="퍼널 예시">
            <g>
              <path d="M40 26h304l-30 34H70z" fill="#4D73BF"/>
              <path d="M74 66h236l-30 34H104z" fill="#5D82C6"/>
              <path d="M108 106h168l-30 34H138z" fill="#7E9BD4"/>
              <path d="M142 146h100l-22 26H164z" fill="#A6BCE2"/>
            </g>
            <g fill="#fff" font-weight="700" text-anchor="middle">
              <text x="192" y="49" font-size="14">방문 12,400</text>
              <text x="192" y="89" font-size="14">가입 4,200</text>
              <text x="192" y="129" font-size="13">활성 1,850</text>
              <text x="192" y="166" font-size="12.5">구매 620</text>
            </g>
          </svg>
```

### 3. 구조 · 관계

#### 계층 트리  `계층`

- **언제**: 소속·상하 관계를 분기선으로. 조직도·분류 체계에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="계층 트리 예시">
            <g fill="none" stroke="#C3CCDA" stroke-width="1.8">
              <path d="M192 56v14M192 70H80v16M192 70h112v16M192 70v16"/>
            </g>
            <rect x="132" y="22" width="120" height="34" rx="9" fill="#4D73BF"/>
            <text x="192" y="44" font-size="13.5" font-weight="700" fill="#fff" text-anchor="middle">본부</text>
            <g>
              <rect x="26" y="86" width="108" height="60" rx="9" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.4"/>
              <rect x="138" y="86" width="108" height="60" rx="9" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.4"/>
              <rect x="250" y="86" width="108" height="60" rx="9" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.4"/>
            </g>
            <g text-anchor="middle" font-weight="700" fill="#23375F" font-size="13">
              <text x="80" y="112">A 담당</text>
              <text x="192" y="112">B 담당</text>
              <text x="304" y="112">C 담당</text>
            </g>
            <g text-anchor="middle" fill="#7B8594" font-size="11.5">
              <text x="80" y="132">3팀</text>
              <text x="192" y="132">4팀</text>
              <text x="304" y="132">2팀</text>
            </g>
          </svg>
```

#### 레이어드 아키텍처  `구조`

- **언제**: 시스템 계층을 위아래 띠로. 기술 스택·아키텍처 설명에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="레이어드 아키텍처 예시">
            <g>
              <rect x="20" y="20" width="344" height="34" rx="8" fill="#EEF3FC" stroke="#4D73BF" stroke-width="1.4"/>
              <rect x="20" y="60" width="344" height="34" rx="8" fill="#E7F4EC" stroke="#3E9B6B" stroke-width="1.4"/>
              <rect x="20" y="100" width="344" height="34" rx="8" fill="#FBF1DE" stroke="#E0952F" stroke-width="1.4"/>
              <rect x="20" y="140" width="344" height="34" rx="8" fill="#F3EEFB" stroke="#6B5FCB" stroke-width="1.4"/>
            </g>
            <g font-size="13.5" font-weight="700">
              <text x="38" y="42" fill="#23375F">Presentation · UI</text>
              <text x="38" y="82" fill="#1F5F3E">Application · API</text>
              <text x="38" y="122" fill="#8A5A12">Domain · Logic</text>
              <text x="38" y="162" fill="#3E357F">Data · Storage</text>
            </g>
            <g font-size="11.5" fill="#7B8594" text-anchor="end">
              <text x="348" y="42">React</text>
              <text x="348" y="82">FastAPI</text>
              <text x="348" y="122">Service</text>
              <text x="348" y="162">DB · S3</text>
            </g>
          </svg>
```

#### 네트워크 · 연결  `관계`

- **언제**: 중심 노드와 주변의 연결. 통합 허브·에이전트 구성도에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="네트워크 연결 예시">
            <g stroke="#C3CCDA" stroke-width="1.8">
              <line x1="192" y1="94" x2="70" y2="44"/>
              <line x1="192" y1="94" x2="70" y2="146"/>
              <line x1="192" y1="94" x2="320" y2="44"/>
              <line x1="192" y1="94" x2="330" y2="100"/>
              <line x1="192" y1="94" x2="300" y2="150"/>
            </g>
            <circle cx="192" cy="94" r="34" fill="#4D73BF"/>
            <text x="192" y="90" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">Core</text>
            <text x="192" y="106" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">Agent</text>
            <g>
              <circle cx="70" cy="44" r="20" fill="#E7F4EC" stroke="#3E9B6B" stroke-width="1.4"/>
              <circle cx="70" cy="146" r="20" fill="#E7F4EC" stroke="#3E9B6B" stroke-width="1.4"/>
              <circle cx="320" cy="44" r="20" fill="#FBF1DE" stroke="#E0952F" stroke-width="1.4"/>
              <circle cx="332" cy="100" r="20" fill="#FBF1DE" stroke="#E0952F" stroke-width="1.4"/>
              <circle cx="300" cy="150" r="20" fill="#F3EEFB" stroke="#6B5FCB" stroke-width="1.4"/>
            </g>
            <g font-size="11" font-weight="700" text-anchor="middle" fill="#2b3440">
              <text x="70" y="48">DB</text>
              <text x="70" y="150">API</text>
              <text x="320" y="48">LLM</text>
              <text x="332" y="104">Tool</text>
              <text x="300" y="154">RAG</text>
            </g>
          </svg>
```

#### 2×2 매트릭스  `위치`

- **언제**: 두 기준으로 사분면에 배치. 우선순위·포지셔닝 분석에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="2x2 매트릭스 예시">
            <rect x="70" y="18" width="290" height="150" rx="8" fill="#F7F9FC"/>
            <line x1="215" y1="18" x2="215" y2="168" stroke="#D3DAE5" stroke-width="1.4"/>
            <line x1="70" y1="93" x2="360" y2="93" stroke="#D3DAE5" stroke-width="1.4"/>
            <g fill="none" stroke="#9AA9C0" stroke-width="1.6">
              <path d="M70 168 L70 10" marker-end="url(#ah2)"/>
              <path d="M62 168 L368 168" marker-end="url(#ah2)"/>
            </g>
            <defs><marker id="ah2" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0 0l6 4l-6 4z" fill="#9AA9C0"/></marker></defs>
            <circle cx="285" cy="55" r="15" fill="#3E9B6B" opacity=".85"/>
            <circle cx="150" cy="128" r="11" fill="#C85C5C" opacity=".8"/>
            <circle cx="165" cy="55" r="9" fill="#4D73BF" opacity=".8"/>
            <circle cx="300" cy="120" r="10" fill="#E0952F" opacity=".8"/>
            <text x="47" y="24" font-size="11" fill="#7B8594" text-anchor="end">높음</text>
            <text x="47" y="166" font-size="11" fill="#7B8594" text-anchor="end">낮음</text>
            <text x="285" y="90" font-size="11.5" font-weight="700" fill="#1F5F3E" text-anchor="middle">우선</text>
          </svg>
```

### 4. 비교 · 구성

#### Before / After  `대비`

- **언제**: 개선 전후를 정면 대비. 성과·효율 개선을 극적으로.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="Before After 비교 예시">
            <rect x="6" y="24" width="150" height="140" rx="12" fill="#F4F6F9" stroke="#D3DAE5" stroke-width="1.4"/>
            <text x="81" y="52" font-size="12" font-weight="700" fill="#9AA3AE" text-anchor="middle" letter-spacing="1">BEFORE</text>
            <text x="81" y="104" font-size="34" font-weight="800" fill="#7B8594" text-anchor="middle">12일</text>
            <text x="81" y="134" font-size="12.5" fill="#7B8594" text-anchor="middle">수작업 처리</text>
            <rect x="228" y="24" width="150" height="140" rx="12" fill="#E7F4EC" stroke="#3E9B6B" stroke-width="1.6"/>
            <text x="303" y="52" font-size="12" font-weight="700" fill="#3E9B6B" text-anchor="middle" letter-spacing="1">AFTER</text>
            <text x="303" y="104" font-size="34" font-weight="800" fill="#1F5F3E" text-anchor="middle">3일</text>
            <text x="303" y="134" font-size="12.5" fill="#1F5F3E" text-anchor="middle">자동화 후</text>
            <g>
              <circle cx="192" cy="94" r="20" fill="#3E9B6B"/>
              <path d="M184 94h14m0 0l-5-5m5 5l-5 5" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </g>
          </svg>
```

#### 막대 차트  `데이터`

- **언제**: 양·규모를 정확히 비교. 추이·순위를 한눈에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="막대 차트 예시">
            <line x1="34" y1="150" x2="366" y2="150" stroke="#D3DAE5" stroke-width="1.4"/>
            <g>
              <rect x="52" y="96" width="42" height="54" rx="4" fill="#A6BCE2"/>
              <rect x="118" y="72" width="42" height="78" rx="4" fill="#7E9BD4"/>
              <rect x="184" y="54" width="42" height="96" rx="4" fill="#5D82C6"/>
              <rect x="250" y="34" width="42" height="116" rx="4" fill="#4D73BF"/>
              <rect x="316" y="66" width="42" height="84" rx="4" fill="#7E9BD4"/>
            </g>
            <g font-size="11.5" fill="#7B8594" text-anchor="middle">
              <text x="73" y="167">1월</text>
              <text x="139" y="167">2월</text>
              <text x="205" y="167">3월</text>
              <text x="271" y="167">4월</text>
              <text x="337" y="167">5월</text>
            </g>
            <g font-size="12" font-weight="700" fill="#3A4658" text-anchor="middle" font-variant-numeric="tabular-nums">
              <text x="73" y="88">41</text>
              <text x="139" y="64">58</text>
              <text x="205" y="46">72</text>
              <text x="271" y="26">86</text>
              <text x="337" y="58">63</text>
            </g>
          </svg>
```

#### 도넛 구성비  `구성`

- **언제**: 전체를 100%로 쪼갠 비중. 항목 5개 이하일 때 효과적.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="도넛 구성비 예시">
            <g transform="translate(96 94)" stroke="#fff" stroke-width="2">
              <circle r="60" fill="none" stroke="#4D73BF" stroke-width="34" stroke-dasharray="177 200" transform="rotate(-90)"/>
              <circle r="60" fill="none" stroke="#3E9B6B" stroke-width="34" stroke-dasharray="94 283" transform="rotate(80)"/>
              <circle r="60" fill="none" stroke="#E0952F" stroke-width="34" stroke-dasharray="57 320" transform="rotate(170)"/>
              <circle r="60" fill="none" stroke="#D3DAE5" stroke-width="34" stroke-dasharray="49 328" transform="rotate(224)"/>
            </g>
            <text x="96" y="99" font-size="16" font-weight="800" fill="#23375F" text-anchor="middle">100%</text>
            <g font-size="13" fill="#3A4658">
              <rect x="206" y="34" width="12" height="12" rx="3" fill="#4D73BF"/><text x="226" y="44">모바일 47%</text>
              <rect x="206" y="64" width="12" height="12" rx="3" fill="#3E9B6B"/><text x="226" y="74">웹 25%</text>
              <rect x="206" y="94" width="12" height="12" rx="3" fill="#E0952F"/><text x="226" y="104">API 15%</text>
              <rect x="206" y="124" width="12" height="12" rx="3" fill="#D3DAE5"/><text x="226" y="134">기타 13%</text>
            </g>
          </svg>
```

#### 벤 다이어그램  `교집합`

- **언제**: 겹치는 영역이 핵심. 역량 교차·시너지 포인트 강조에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="벤 다이어그램 예시">
            <circle cx="150" cy="94" r="66" fill="#4D73BF" fill-opacity=".38"/>
            <circle cx="234" cy="94" r="66" fill="#3E9B6B" fill-opacity=".38"/>
            <text x="112" y="90" font-size="13.5" font-weight="700" fill="#23375F" text-anchor="middle">데이터</text>
            <text x="112" y="110" font-size="11.5" fill="#3A4658" text-anchor="middle">분석력</text>
            <text x="272" y="90" font-size="13.5" font-weight="700" fill="#1F5F3E" text-anchor="middle">도메인</text>
            <text x="272" y="110" font-size="11.5" fill="#3A4658" text-anchor="middle">지식</text>
            <text x="192" y="92" font-size="12" font-weight="800" fill="#1a1a1a" text-anchor="middle">AI</text>
            <text x="192" y="108" font-size="10.5" fill="#3A4658" text-anchor="middle">인사이트</text>
          </svg>
```

### 5. 강조

#### 콜아웃 하이라이트  `강조`

- **언제**: 핵심 메시지 3~4개를 아이콘 카드로. 성과 요약·결론부에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="콜아웃 하이라이트 예시">
            <g>
              <rect x="6" y="20" width="372" height="46" rx="11" fill="#EEF3FC"/>
              <circle cx="34" cy="43" r="15" fill="#4D73BF"/>
              <path d="M34 35v16M27 43l7 8 8-13" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
              <text x="60" y="40" font-size="13.5" font-weight="700" fill="#1a1a1a">자동 점검 도구 배포</text>
              <text x="60" y="57" font-size="11.5" fill="#5A6472">수작업 대비 처리시간 75% 단축</text>

              <rect x="6" y="72" width="372" height="46" rx="11" fill="#E7F4EC"/>
              <circle cx="34" cy="95" r="15" fill="#3E9B6B"/>
              <path d="M27 95l6 6 10-11" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
              <text x="60" y="92" font-size="13.5" font-weight="700" fill="#1a1a1a">4개 팀 확산 완료</text>
              <text x="60" y="109" font-size="11.5" fill="#5A6472">11개 프로젝트 대상 적용</text>

              <rect x="6" y="124" width="372" height="46" rx="11" fill="#FBF1DE"/>
              <circle cx="34" cy="147" r="15" fill="#E0952F"/>
              <path d="M34 140v10M34 154v1" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
              <text x="60" y="144" font-size="13.5" font-weight="700" fill="#1a1a1a">즉시조치 취약점 선제 검출</text>
              <text x="60" y="161" font-size="11.5" fill="#5A6472">중대 위협 사전 차단</text>
            </g>
          </svg>
```

#### 대형 스테이트먼트  `강조`

- **언제**: 단 하나의 숫자를 크게. 표지·전환·클로징 한 방에.

```svg
<svg font-family="'Pretendard','Apple SD Gothic Neo','Malgun Gothic',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" viewBox="0 0 384 188" role="img" aria-label="대형 스테이트먼트 예시">
            <rect x="6" y="16" width="372" height="156" rx="14" fill="#23375F"/>
            <rect x="6" y="16" width="6" height="156" rx="3" fill="#7CA0E8"/>
            <text x="40" y="92" font-size="62" font-weight="800" fill="#fff">×3.5</text>
            <text x="42" y="128" font-size="15" font-weight="700" fill="#CFE0FF">분석 처리량 향상</text>
            <text x="42" y="150" font-size="12.5" fill="#9DB4DD">에이전트 도입 6개월 기준 · 동일 인력</text>
          </svg>
```
