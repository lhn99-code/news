# 🐿️ 다람쥐 뽀모도로 (Apps in Toss)

집중 타이머(뽀모도로)에 다람쥐 육성·수집을 결합한 앱인토스 미니앱.
`@apps-in-toss/web-framework`(React + Granite) 기반으로, 요구사항 명세서 v2의 MVP를 구현했습니다.

> 이 프로젝트는 목업(`../mockup_v2.html`)의 로직을 실제 앱인토스 코드로 옮긴 것입니다.
> 요구사항 원본: `../docs/다람쥐_뽀모도로_요구사항명세서_v2.md`

## 구현된 MVP 기능

- **집중 타이머**: 5~60분(기본 25분), 진행/종료, 화면 이탈 시 종료 처리(FR-T7)
- **도토리**: 5분당 1개 적립, 완료 100% + **연속(streak) 보너스**, 중도 종료 50%
- **연속 보너스**: 3·7·14일 마일스톤 (상단 🔥 pill 표시)
- **꾸미기 상점**: 모자·목도리·반지·하늘·바닥 배경 구매/장착/해제
- **다람쥐 도감**: 수집 전용(능력치 효과 없음), 미보유 실루엣
- **리워드 광고**: 도토리 추가 보상(일 5회 제한) — *SDK 연동은 아래 참고*
- **랭킹·공유(Phase 2)**: 토스 로그인 전제, 현재는 미리보기 UI
- **저장**: `Storage`(로컬+서버 동기화) 래퍼, 브라우저에선 localStorage 폴백

## 폴더 구조

```
src/
  App.tsx                 앱 셸(상단바/무대/탭/토스트)
  index.tsx / index.css   진입점 · 토스풍 스타일
  data/catalog.ts         아이템·다람쥐·상수·보너스 규칙
  state/useGameState.ts   Storage 기반 게임 상태·로직
  lib/storage.ts          Storage 래퍼(+localStorage 폴백)
  lib/rewardedAd.ts       리워드 광고 추상화(SDK 연동 지점)
  components/             Stage · TabBar · Toast
  screens/                Timer · Shop · Collection · Rank
granite.config.ts         앱 이름/브랜드/권한 설정
```

## 실행

```bash
# 의존성 설치 (yarn 권장, npm도 가능)
yarn install        # 또는: npm install

# 로컬 개발 (브라우저 미리보기)
yarn dev            # granite dev → http://localhost:3000

# 프로덕션 번들
yarn build
```

## 실기기(토스) 테스트 & 출시

1. `granite build`로 앱 번들 생성
2. [앱인토스 콘솔](https://developers-apps-in-toss.toss.im/prepare/console-workspace.html)에 앱 등록 후 **번들 업로드**
3. **'테스트하기'** → QR 코드 → **토스 앱으로 스캔**하면 실제 화면 확인 (테스트 1회 이상 필수)
4. `ait deploy`(또는 콘솔 업로드) → **검토 요청** → 심사 → 출시

## 남은 연동 작업 (TODO)

- **리워드 광고**: `src/lib/rewardedAd.ts`의 시뮬레이션을 실제 SDK로 교체
  (`GoogleAdMob.showAppsInTossAdMob`, 콘솔에서 `adGroupId` 발급, `granite.config.ts` 권한 설정)
- **토스 로그인 / 랭킹 / 공유 (Phase 2)**: `appLogin()`으로 사용자 식별 후 서버 랭킹,
  `share({ message })`로 공유 (`src/screens/RankScreen.tsx` 주석 참고)
- **3D 다람쥐 에셋**: `src/components/Stage.tsx`의 임시 이미지 URL을 번들 에셋으로 교체
- **앱 아이콘**: `granite.config.ts`의 `brand.icon`을 실제 아이콘 URL로 교체

## 참고

- 앱인토스 개발자센터: https://developers-apps-in-toss.toss.im/
- 공식 예제: https://github.com/toss/apps-in-toss-examples
