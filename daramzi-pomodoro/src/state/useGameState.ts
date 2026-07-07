import { useCallback, useEffect, useRef, useState } from 'react';
import { getItem, setItem } from '../lib/storage';
import {
  ACORN_PER_MINUTES,
  AD_DAILY_CAP,
  AD_REWARD,
  Item,
  Slot,
  Squirrel,
  streakBonus,
} from '../data/catalog';

const SAVE_KEY = 'daramzi_state_v1';

export interface GameState {
  acorns: number;
  defaultMinutes: number;
  ownedItems: string[];
  equipped: Record<Slot, string | null>;
  ownedSquirrels: string[];
  streakDays: number;
  lastSessionDate: string | null; // 'YYYY-MM-DD' (streak 판정)
  totalFocusMin: number;
  adsToday: number;
  adsDate: string | null; // 광고 일일 카운트 기준 날짜
}

function defaultState(): GameState {
  return {
    acorns: 0,
    defaultMinutes: 25,
    ownedItems: [],
    equipped: { hat: null, scarf: null, ring: null, skyBg: null, floorBg: null },
    ownedSquirrels: ['sq_basic'],
    streakDays: 0,
    lastSessionDate: null,
    totalFocusMin: 0,
    adsToday: 0,
    adsDate: null,
  };
}

function todayStr(): string {
  const d = new Date();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
}

function daysBetween(a: string, b: string): number {
  const da = new Date(a + 'T00:00:00').getTime();
  const db = new Date(b + 'T00:00:00').getTime();
  return Math.round((db - da) / 86400000);
}

export interface SessionResult {
  earned: number;
  base: number;
  bonus: number;
  completed: boolean;
}

export function useGameState() {
  const [state, setState] = useState<GameState>(defaultState);
  const [loaded, setLoaded] = useState(false);
  const stateRef = useRef(state);
  stateRef.current = state;

  // 최초 로드
  useEffect(() => {
    (async () => {
      const raw = await getItem(SAVE_KEY);
      if (raw) {
        try {
          setState({ ...defaultState(), ...JSON.parse(raw) });
        } catch {
          /* keep default */
        }
      }
      setLoaded(true);
    })();
  }, []);

  // 변경 시 저장
  useEffect(() => {
    if (!loaded) return;
    setItem(SAVE_KEY, JSON.stringify(state));
  }, [state, loaded]);

  const update = useCallback((patch: Partial<GameState>) => {
    setState((s) => ({ ...s, ...patch }));
  }, []);

  const setDefaultMinutes = useCallback((minutes: number) => {
    setState((s) => ({ ...s, defaultMinutes: minutes }));
  }, []);

  /** streak 갱신: 하루 첫 완료면 연속일 증가/초기화 */
  const bumpStreak = useCallback((s: GameState): Partial<GameState> => {
    const today = todayStr();
    if (s.lastSessionDate === today) return {}; // 오늘 이미 반영됨
    if (s.lastSessionDate == null) return { streakDays: 1, lastSessionDate: today };
    const gap = daysBetween(s.lastSessionDate, today);
    const streakDays = gap === 1 ? s.streakDays + 1 : 1; // 어제=연속, 그 외=초기화
    return { streakDays, lastSessionDate: today };
  }, []);

  /**
   * 집중 세션 종료 처리.
   * @param elapsedSec 실제 집중한 초
   * @param completed  true=완료(100%+보너스), false=중도 종료(50%)
   */
  const finishSession = useCallback(
    (elapsedSec: number, completed: boolean): SessionResult => {
      const s = stateRef.current;
      const accrued = Math.floor(elapsedSec / (ACORN_PER_MINUTES * 60));
      let streakPatch: Partial<GameState> = {};
      let base: number;
      let bonus = 0;

      if (completed) {
        streakPatch = bumpStreak(s);
        base = accrued;
        bonus = streakBonus(streakPatch.streakDays ?? s.streakDays);
      } else {
        base = Math.floor(accrued / 2);
      }
      const earned = base + bonus;

      setState((prev) => ({
        ...prev,
        ...streakPatch,
        acorns: prev.acorns + earned,
        totalFocusMin: prev.totalFocusMin + Math.round(elapsedSec / 60),
      }));

      return { earned, base, bonus, completed };
    },
    [bumpStreak]
  );

  const buyItem = useCallback((item: Item): boolean => {
    const s = stateRef.current;
    if (s.acorns < item.price || s.ownedItems.includes(item.id)) return false;
    setState((prev) => ({
      ...prev,
      acorns: prev.acorns - item.price,
      ownedItems: [...prev.ownedItems, item.id],
      equipped: { ...prev.equipped, [item.slot]: item.id },
    }));
    return true;
  }, []);

  const toggleEquip = useCallback((item: Item) => {
    setState((prev) => {
      const on = prev.equipped[item.slot] === item.id;
      return { ...prev, equipped: { ...prev.equipped, [item.slot]: on ? null : item.id } };
    });
  }, []);

  const adoptSquirrel = useCallback((sq: Squirrel): boolean => {
    const s = stateRef.current;
    if (s.acorns < sq.price || s.ownedSquirrels.includes(sq.id)) return false;
    setState((prev) => ({
      ...prev,
      acorns: prev.acorns - sq.price,
      ownedSquirrels: [...prev.ownedSquirrels, sq.id],
    }));
    return true;
  }, []);

  const adsLeftToday = useCallback((): number => {
    const s = stateRef.current;
    const used = s.adsDate === todayStr() ? s.adsToday : 0;
    return Math.max(0, AD_DAILY_CAP - used);
  }, []);

  /** 광고 보상 지급 (일일 상한 체크). 성공 시 지급 개수 반환, 상한 초과면 0 */
  const grantAdReward = useCallback((): number => {
    const today = todayStr();
    const s = stateRef.current;
    const used = s.adsDate === today ? s.adsToday : 0;
    if (used >= AD_DAILY_CAP) return 0;
    setState((prev) => ({
      ...prev,
      acorns: prev.acorns + AD_REWARD,
      adsToday: used + 1,
      adsDate: today,
    }));
    return AD_REWARD;
  }, []);

  const reset = useCallback(() => setState(defaultState()), []);

  return {
    state,
    loaded,
    update,
    setDefaultMinutes,
    finishSession,
    buyItem,
    toggleEquip,
    adoptSquirrel,
    adsLeftToday,
    grantAdReward,
    reset,
  };
}

export type GameStore = ReturnType<typeof useGameState>;
