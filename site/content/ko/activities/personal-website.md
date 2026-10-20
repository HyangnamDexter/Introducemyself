---
title: "개인 소개 웹사이트 구축"
description: "Hugo 테마로 나를 소개하는 사이트를 만들고, push만으로 자동 배포되도록 구성한 개인 활동입니다."
---

## 기간과 진행 상태 {#period}

- **기간**: 2026년 10월 ~ 현재
- **상태**: 진행 중 (2026년 10월 31일 제출 예정)

## 활동 목적 {#purpose}

나를 소개하는 공개 웹사이트를 만들고, `main` 브랜치에 push만 하면 자동으로 빌드·배포되는 구조를 직접 구성해 보는 것이 목표입니다.

## 내 역할 {#role}

**개인 활동**입니다. 테마 선택, 배포 설정, 콘텐츠 작성, 접근성·반응형 점검을 모두 직접 수행했습니다.

## 수행 과정과 선택 이유 {#process}

1. **테마 선택**: Hugo Themes에서 **CareerCanvas**를 골랐습니다. 데모 버전 속 남성의 이미지가 너무 매력적이어서 이 테마를 선택했습니다.
2. **배포 구성**: 테마 ZIP을 내려받아 수업에서 제공한 준비 스크립트를 실행하고, GitHub Actions로 GitHub Pages에 배포되도록 저장소를 연결했습니다.
3. **빌드 실패 해결**: 첫 배포가 Hugo 빌드 단계에서 실패했습니다. 테마가 Tailwind CSS(PostCSS) 설정 파일을 요구하는데 ZIP에 없었던 것이 원인이었고, `package.json`·`postcss.config.js`·`tailwind.config.js`를 추가해 해결했습니다.
4. **한국어·접근성 개선**: 테마 원본은 그대로 두고 `site/layouts/`에서 필요한 템플릿만 덮어썼습니다. 원본과 내가 고친 부분을 구분해서 관리하기 위해서입니다. 문서 언어(`lang="ko"`), 메뉴 앵커, 아이콘 링크 이름, 키보드 초점 표시, 애니메이션 멈춤 버튼을 고쳤습니다.

## 산출물과 결과 {#result}

- **공개 사이트**: <https://hyangnamdexter.github.io/Introducemyself/>. 지금 보고 있는 이 사이트입니다.
- **저장소**: <https://github.com/HyangnamDexter/Introducemyself>. 설정·템플릿·콘텐츠와 커밋 이력이 있습니다.
- **자동 배포 기록**: <https://github.com/HyangnamDexter/Introducemyself/actions>. push할 때마다 빌드·배포가 성공하는지 확인했습니다.
- **빌드 실패를 고친 커밋**: [6ccbc03](https://github.com/HyangnamDexter/Introducemyself/commit/6ccbc03bdae8f270ccac3e0f3f132c80e531a7dc). 이 커밋 이후 Actions 빌드가 성공하고 사이트가 열리는 것을 확인했습니다.

## 배운 점과 한계, 다음 개선 방향 {#learned}

**배운 점**: 테마 ZIP만으로는 빌드에 필요한 설정이 빠져 있을 수 있다는 것을 알게 되었습니다. Actions 로그에서 실패한 단계를 찾고 같은 버전의 Hugo로 로컬에서 재현하면 원인을 빠르게 좁힐 수 있었습니다.

**한계**: 템플릿 수정의 많은 부분을 AI(Claude Code)의 도움을 받아 진행해서, Hugo 템플릿 문법을 아직 혼자서 모두 다루지는 못합니다. 또 Windows에서는 Node 권한 문제 때문에 로컬 빌드에 우회 방법이 필요합니다.

**다음 개선 방향**: Hugo 템플릿 문법을 공부해 다음 활동 페이지는 직접 추가하겠습니다. 연구실의 Intent Caching 연구가 정리되면 이 사이트에 두 번째 활동으로 기록하겠습니다.
