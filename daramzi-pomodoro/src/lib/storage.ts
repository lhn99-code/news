// 앱인토스 Storage 래퍼.
// 토스 웹뷰 안에서는 SDK의 Storage(영구 저장 + 서버 동기화 기반)를 사용하고,
// 일반 브라우저(rsbuild dev 미리보기 등)에서는 localStorage로 자동 폴백해요.
//
// 요구사항: "로컬 + 서버 동기화" — 실제 서버 동기화는 토스 로그인(Phase 2)과 함께
// SDK Storage가 처리합니다. 여기서는 그 접근을 단일 인터페이스로 감쌉니다.
import { Storage } from '@apps-in-toss/web-framework';

export async function getItem(key: string): Promise<string | null> {
  try {
    const v = await Storage.getItem(key);
    return v ?? null;
  } catch {
    try {
      return globalThis.localStorage?.getItem(key) ?? null;
    } catch {
      return null;
    }
  }
}

export async function setItem(key: string, value: string): Promise<void> {
  try {
    await Storage.setItem(key, value);
  } catch {
    try {
      globalThis.localStorage?.setItem(key, value);
    } catch {
      /* noop */
    }
  }
}
