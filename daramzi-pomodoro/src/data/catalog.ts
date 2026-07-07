// 다람쥐 뽀모도로 콘텐츠 카탈로그 (요구사항 명세서 9.1 가격표 기준)

export const ACORN_PER_MINUTES = 5; // 5분당 도토리 1개
export const AD_DAILY_CAP = 5; // 리워드 광고 일일 시청 상한
export const AD_REWARD = 3; // 광고 1회 보상 도토리
export const STREAK_MILESTONES = [3, 7, 14]; // 연속 보너스 마일스톤(일)

export type Slot = 'hat' | 'scarf' | 'ring' | 'skyBg' | 'floorBg';

export interface Item {
  id: string;
  slot: Slot;
  name: string;
  emoji: string;
  price: number;
  /** 배경 아이템일 때 무대에 적용할 CSS 그라데이션 */
  css?: string;
}

export interface Squirrel {
  id: string;
  name: string;
  price: number; // 도감 영입 비용 (능력치 효과 없음)
}

export const ITEMS: Item[] = [
  { id: 'hat_acorn', slot: 'hat', name: '도토리 모자', emoji: '🌰', price: 10 },
  { id: 'hat_maple', slot: 'hat', name: '단풍잎 모자', emoji: '🍁', price: 15 },
  { id: 'hat_chestnut', slot: 'hat', name: '밤송이 모자', emoji: '🌟', price: 20 },
  { id: 'scarf_red', slot: 'scarf', name: '빨간 목도리', emoji: '🧣', price: 12 },
  { id: 'scarf_check', slot: 'scarf', name: '체크 목도리', emoji: '🟫', price: 18 },
  { id: 'ring_acorn', slot: 'ring', name: '도토리 반지', emoji: '💍', price: 15 },
  { id: 'ring_star', slot: 'ring', name: '별 반지', emoji: '⭐', price: 25 },
  { id: 'sky_clear', slot: 'skyBg', name: '맑은 하늘', emoji: '☀️', price: 25, css: 'linear-gradient(180deg,#9fd8ff 0%,#e3f4ff 100%)' },
  { id: 'sky_sunset', slot: 'skyBg', name: '노을 하늘', emoji: '🌇', price: 35, css: 'linear-gradient(180deg,#ffb88c 0%,#ffe6cc 100%)' },
  { id: 'floor_grass', slot: 'floorBg', name: '잔디밭', emoji: '🌱', price: 25, css: 'linear-gradient(180deg,#a7dd86 0%,#8ccb64 100%)' },
  { id: 'floor_leaf', slot: 'floorBg', name: '낙엽밭', emoji: '🍂', price: 35, css: 'linear-gradient(180deg,#e9b878 0%,#d49a52 100%)' },
];

export const SQUIRRELS: Squirrel[] = [
  { id: 'sq_basic', name: '기본 다람쥐', price: 0 },
  { id: 'sq_baby', name: '아기 다람쥐', price: 50 },
  { id: 'sq_stripe', name: '줄무늬 다람쥐', price: 100 },
  { id: 'sq_white', name: '흰 다람쥐', price: 200 },
];

export const DEFAULT_SKY = 'linear-gradient(180deg,#d6efff 0%,#eaf7ff 55%,#fef6ec 100%)';
export const DEFAULT_FLOOR = 'linear-gradient(180deg,#a7dd86 0%,#8ccb64 100%)';

export const SHOP_GROUPS: { slot: Slot; label: string }[] = [
  { slot: 'hat', label: '🎩 모자' },
  { slot: 'scarf', label: '🧣 목도리' },
  { slot: 'ring', label: '💍 반지' },
  { slot: 'skyBg', label: '🌤️ 하늘 배경' },
  { slot: 'floorBg', label: '🌳 바닥 배경' },
];

/** 연속 일수에 따른 보너스 도토리 */
export function streakBonus(days: number): number {
  if (days >= 14) return 5;
  if (days >= 7) return 3;
  if (days >= 3) return 1;
  return 0;
}

/** 다음 마일스톤까지 남은 일수 계산에 쓰는 목표 일수 */
export function nextMilestone(days: number): number {
  for (const m of STREAK_MILESTONES) if (days < m) return m;
  return days + 1;
}
