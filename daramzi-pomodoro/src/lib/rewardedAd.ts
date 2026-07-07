// 리워드 광고 추상화.
//
// ⚠️ 실제 광고 SDK 연동은 "실기기 테스트 단계"에서 마무리해야 해요.
// 앱인토스 예제(with-rewarded-ad)는 네이티브 프레임워크의 GoogleAdMob API를 사용합니다:
//
//   import { GoogleAdMob } from '@apps-in-toss/framework';
//   GoogleAdMob.loadAppsInTossAdMob({ options: { adGroupId }, onEvent, onError });
//   GoogleAdMob.showAppsInTossAdMob({ options: { adGroupId },
//     onEvent: (e) => { if (e.type === 'userEarnedReward') onRewarded(); ... } });
//
// 콘솔에서 발급받은 adGroupId와 권한(granite.config.ts permissions)을 설정한 뒤
// 아래 requestRewardedAd 내부를 실제 SDK 호출로 교체하세요.
//
// 지금은 개발/미리보기에서 흐름을 검증할 수 있도록, 광고 시청을 즉시 성공 처리하는
// 시뮬레이션으로 동작합니다.

export interface RewardResult {
  rewarded: boolean;
}

export async function requestRewardedAd(): Promise<RewardResult> {
  // TODO(device-test): GoogleAdMob.showAppsInTossAdMob(...) 로 교체
  await new Promise((r) => setTimeout(r, 300));
  return { rewarded: true };
}

/** 실제 광고 SDK가 이 환경에서 지원되는지 여부 (지금은 항상 시뮬레이션) */
export function isRewardedAdSupported(): boolean {
  return false;
}
