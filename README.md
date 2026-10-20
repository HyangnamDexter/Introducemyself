# Introducemyself: 개인 소개 웹사이트

Hugo 테마 **CareerCanvas**로 만든 개인 소개(포트폴리오) 사이트입니다. `main` 브랜치에 push하면 GitHub Actions가 자동으로 빌드하고 GitHub Pages에 배포합니다.

- 공개 사이트: <https://hyangnamdexter.github.io/Introducemyself/>
- 저장소: <https://github.com/HyangnamDexter/Introducemyself>
- 배포 기록(Actions): <https://github.com/HyangnamDexter/Introducemyself/actions>

## 목차

1. [폴더 구조](#폴더-구조)
2. [필요한 도구와 버전](#필요한-도구와-버전)
3. [로컬에서 설치·빌드·미리보기](#로컬에서-설치빌드미리보기)
4. [내용 수정 위치](#내용-수정-위치)
5. [수정 후 재배포와 확인 방법](#수정-후-재배포와-확인-방법)
6. [공개 사이트 자동 점검](#공개-사이트-자동-점검)
7. [출처와 이용 조건](#출처와-이용-조건)

## 폴더 구조

| 경로 | 역할 |
|---|---|
| `site/` | **실제로 빌드되는 Hugo 사이트**. 수정은 거의 모두 여기서 합니다. |
| `site/hugo.toml` | 사이트 설정: 이름·소개·지역·이메일·링크·메뉴 |
| `site/pages.json` | 준비 스크립트가 만든 배포용 설정(baseURL, 테마 이름, 보안 설정) |
| `site/content/ko/` | 섹션별 본문(자기소개, 역량, 활동, 기술, 연락처, 활동 상세 페이지) |
| `site/static/images/` | 프로필 사진 등 이미지 |
| `site/i18n/ko.toml` | 테마 화면 문구의 한국어 번역 |
| `site/layouts/` | 테마 템플릿을 덮어쓰는 사이트 전용 수정본(접근성·경로·메뉴 개선) |
| `site/assets/css/site.css`, `site/assets/js/motion-control.js` | 사이트 전용 스타일(초점 표시 등)과 애니메이션 멈춤 기능 |
| `site/themes/template/` | CareerCanvas 테마 원본(수정하지 않음) |
| `site/package.json`, `site/package-lock.json` | Tailwind CSS·PostCSS 빌드 도구 버전 |
| `site/postcss.config.js`, `site/tailwind.config.js` | 테마 CSS(Tailwind) 빌드 설정 |
| `.github/workflows/hugo-pages.yml` | GitHub Actions 배포 워크플로 |
| `tools/verify_site.py`, `tools/a11y_check.py` | 공개 사이트 자동 점검 스크립트 |
| `docs/verification/` | 점검 결과(화면 캡처, 로그, 접근성 검사 결과) |
| `.github/pages_build.py` | 워크플로가 실행하는 의존성 설치·빌드 스크립트(수업 제공) |
| 저장소 루트의 `assets/`, `layouts/`, `theme.toml`, `LICENSE` 등 | 내려받은 테마 ZIP 원본(준비 스크립트 입력, 테마 라이선스 보존) |

## 필요한 도구와 버전

| 도구 | 버전 | 용도 |
|---|---|---|
| Hugo **extended** | 0.167.0 | 사이트 빌드 (워크플로에 고정) |
| Node.js / npm | Node 24 (npm 포함) | Tailwind CSS·PostCSS 실행 |
| Git | 최신 | 커밋·push |
| Python | 3.9 이상 (워크플로는 3.12) | `.github/pages_build.py` 실행 시 |

Hugo는 <https://github.com/gohugoio/hugo/releases/tag/v0.167.0> 에서 `hugo_extended_0.167.0_<OS>` 파일을 받아 `hugo` 실행 파일을 PATH에 둡니다. 설치 확인:

```bash
hugo version
node --version
```

## 로컬에서 설치·빌드·미리보기

모든 명령은 저장소의 `site/` 폴더에서 실행합니다.

```bash
cd site
npm ci
```

미리보기 서버(수정하면 자동 새로고침, <http://localhost:1313/Introducemyself/>):

```bash
hugo server --config hugo.toml,pages.json --theme template --themesDir themes
```

배포와 같은 방식의 빌드(결과는 저장소 루트의 `public/`):

```bash
hugo --gc --minify --config hugo.toml,pages.json --theme template --themesDir themes --destination ../public
```

> **Windows 주의**: Hugo가 Tailwind를 실행할 때 Node 권한 검사에서 드라이브 문자의 대소문자가 다르면 `ERR_ACCESS_DENIED`로 실패합니다. `cmd`에서 경로를 소문자 드라이브로 이동한 뒤 실행하면 됩니다. 예: `cd /d c:\users\<사용자>\desktop\careercanvas-main\site`. GitHub Actions(Linux)에서는 이 문제가 없습니다.

## 내용 수정 위치

| 바꾸고 싶은 것 | 파일 |
|---|---|
| 이름, 상단 소개, 지역, 이메일, GitHub 링크 | `site/hugo.toml`의 `[params]`, `[languages.ko.params]` |
| 상단 메뉴 이름·순서 | `site/hugo.toml`의 `[menus]` |
| 자기소개·관심 분야·학습 목표 | `site/content/ko/about.md` |
| 역량(관심 분야별 카드) | `site/content/ko/skills.md` |
| 활동 타임라인 | `site/content/ko/experience.md` |
| 대표 활동 상세 페이지 | `site/content/ko/activities/` 아래 `.md` 파일 |
| 기술 아이콘 목록 | `site/content/ko/technical.md` |
| 연락처 안내 문구 | `site/content/ko/contact.md` |
| 프로필 사진 | `site/static/images/` 에 파일을 넣고 `hugo.toml`의 `profile_image` 수정 (앞에 `/` 없이 `images/파일명`) |

## 수정 후 재배포와 확인 방법

1. 위 파일을 수정하고 로컬 미리보기로 확인합니다.
2. 커밋하고 `main`에 push합니다.

   ```bash
   git add <수정한 파일>
   git commit -m "변경 내용을 설명하는 메시지"
   git push origin main
   ```

3. 저장소의 **Actions** 탭에서 `Deploy Hugo to GitHub Pages` 실행이 자동으로 시작되는지 확인합니다. `build`와 `deploy` 작업이 모두 초록색 체크가 되면 성공입니다.
4. 1~2분 뒤 공개 사이트를 새로고침(캐시 무시: `Ctrl+F5`)해서 변경 내용이 반영됐는지 확인합니다.

처음 한 번은 저장소 **Settings → Pages → Build and deployment → Source**를 `GitHub Actions`로 설정해야 합니다.

## 공개 사이트 자동 점검

배포 후 공개 사이트를 실제 브라우저로 점검하는 스크립트입니다. 설치된 Google Chrome을 사용하므로 브라우저를 따로 내려받지 않습니다. 저장소 루트에서 실행합니다.

```bash
pip install playwright
python tools/verify_site.py docs/verification
python tools/a11y_check.py > docs/verification/axe_result.json
```

- `verify_site.py`: 폭 1440·768·390px 화면, 모바일 메뉴, 메뉴 앵커와 뒤로 가기, 직접 URL 접근과 새로고침, 키보드(Tab·Enter·Escape), 소개 팝업 초점, 애니메이션 멈춤, 200% 확대에 해당하는 폭, 404 페이지, 콘솔·네트워크 오류를 확인하고 화면을 `docs/verification/fig*.png`로 저장합니다. 결과는 `verify_log.json`에 남습니다.
- `a11y_check.py`: axe-core 4.10.2로 다크·라이트 모드에서 WCAG 2 A/AA 규칙을 검사합니다.

## 출처와 이용 조건

| 자료 | 사용 위치 | 구분 | 출처 | 이용 조건 |
|---|---|---|---|---|
| CareerCanvas 테마 | `site/themes/template/`, 루트의 테마 파일, `site/layouts/`의 수정본 | 외부 자료 | <https://github.com/felipecordero/careercanvas> | MIT License, © 2024 Felipe Cordero (`LICENSE`, 사이트 푸터에 표기) |
| Tailwind/PostCSS 설정 형식 | `site/postcss.config.js`, `site/tailwind.config.js`, `site/package.json` | 외부 자료 참고 | <https://github.com/felipecordero/felipecordero.github.io> | MIT License |
| Hugo | 빌드 도구 | 외부 도구 | <https://gohugo.io> | Apache License 2.0 |
| Tailwind CSS, PostCSS, Autoprefixer | CSS 빌드 | 외부 도구 | npm | MIT License |
| Font Awesome Free 6.4.0 | 아이콘(cdnjs) | 외부 자료 | <https://fontawesome.com> | Icons CC BY 4.0, Fonts SIL OFL 1.1, Code MIT |
| Devicon v2.16.0 SVG (Python, Git, GitHub, Hugo) | `site/static/images/icons/` (저장소에 포함) | 외부 자료 | <https://devicon.dev> | MIT License |
| GSAP 3.13.0 | 애니메이션(cdnjs) | 외부 자료 | <https://gsap.com> | GSAP Standard License (무료 사용) |
| Montserrat, Nunito Sans | 웹폰트(Google Fonts) | 외부 자료 | <https://fonts.google.com> | SIL Open Font License 1.1 |
| 준비 스크립트 | `prepare_github_pages.py`, `.github/pages_build.py`, 워크플로 | 수업 제공 | 초급프로젝트 수업 | 수업 자료 |
| 사이트 전용 템플릿 수정, `site.css`, `motion-control.js`, `i18n/ko.toml`, 이 README | `site/layouts/`, `site/assets/`, `site/i18n/` | 직접 작성 (AI 도움) | Claude Code(Anthropic)로 작성한 뒤 직접 검토·빌드·브라우저 확인 | 본 저장소 |
| 소개·활동 글 | `site/content/ko/` | 직접 작성 | 본인 | 본인 저작물 |
