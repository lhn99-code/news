import { useEffect, useRef, useState } from 'react';
import { GameStore } from '../state/useGameState';
import { ACORN_PER_MINUTES } from '../data/catalog';
import { requestRewardedAd } from '../lib/rewardedAd';

interface Props {
  store: GameStore;
  toast: (m: string) => void;
  onWorkingChange: (working: boolean) => void;
}

function fmt(sec: number) {
  sec = Math.max(Math.round(sec), 0);
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

export function TimerScreen({ store, toast, onWorkingChange }: Props) {
  const { state, setDefaultMinutes, finishSession, grantAdReward, adsLeftToday } = store;
  const [minutes, setMinutes] = useState(state.defaultMinutes);
  const [running, setRunning] = useState(false);
  const [leftSec, setLeftSec] = useState(minutes * 60);
  const totalRef = useRef(minutes * 60);
  const leftRef = useRef(leftSec);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  leftRef.current = leftSec;

  // 슬라이더 조작 (대기 중일 때만)
  useEffect(() => {
    if (!running) setLeftSec(minutes * 60);
  }, [minutes, running]);

  const stop = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = null;
  };

  const start = () => {
    totalRef.current = minutes * 60;
    setLeftSec(minutes * 60);
    setRunning(true);
    onWorkingChange(true);
    stop();
    timerRef.current = setInterval(() => {
      setLeftSec((prev) => {
        const next = prev - 1;
        if (next <= 0) {
          stop();
          endSession(true);
          return 0;
        }
        return next;
      });
    }, 1000);
  };

  const endSession = (completed: boolean) => {
    stop();
    const elapsed = totalRef.current - Math.max(leftRef.current, 0);
    setRunning(false);
    onWorkingChange(false);
    const r = finishSession(elapsed, completed);
    if (completed) {
      toast(`집중 성공! 🌰 ${r.base}${r.bonus ? ` + 연속보너스 ${r.bonus}` : ''} = ${r.earned}개`);
    } else {
      toast(`종료했어요. 절반인 🌰 ${r.earned}개`);
    }
  };

  // 화면 이탈 = 종료 (FR-T7)
  useEffect(() => {
    const onHidden = () => {
      if (document.hidden && timerRef.current) {
        const elapsed = totalRef.current - Math.max(leftRef.current, 0);
        stop();
        setRunning(false);
        onWorkingChange(false);
        const r = finishSession(elapsed, false);
        toast(`화면을 벗어나 종료됐어요. 절반인 🌰 ${r.earned}개`);
      }
    };
    document.addEventListener('visibilitychange', onHidden);
    return () => document.removeEventListener('visibilitychange', onHidden);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => stop, []);

  const onWatchAd = async () => {
    if (adsLeftToday() <= 0) {
      toast('오늘 광고 보상은 모두 받았어요');
      return;
    }
    const { rewarded } = await requestRewardedAd();
    if (!rewarded) return;
    const got = grantAdReward();
    if (got > 0) toast(`📺 광고 시청 완료! 🌰 +${got}`);
  };

  const elapsed = totalRef.current - leftSec;
  const sessionAcorns = Math.floor(elapsed / (ACORN_PER_MINUTES * 60));
  const progress = Math.min((elapsed / totalRef.current) * 100, 100);

  if (running) {
    return (
      <section className="panel">
        <p className="hint">집중 중이에요. 화면을 벗어나면 종료로 처리돼요!</p>
        <div className="time-display countdown">{fmt(leftSec)}</div>
        <div className="progress">
          <div className="progress-bar" style={{ width: `${progress}%` }} />
        </div>
        <p className="session-acorns">
          이번 집중 도토리: <strong>{sessionAcorns}</strong> 🌰
        </p>
        <button className="btn ghost" onClick={() => endSession(false)}>
          종료하기 (절반만 획득)
        </button>
      </section>
    );
  }

  return (
    <section className="panel">
      <p className="hint">
        집중할 시간을 정하고 시작해요.
        <br />
        집중하는 동안 다람쥐가 도토리를 모아요.
      </p>
      <div className="time-display">
        {minutes}
        <small>분</small>
      </div>
      <input
        type="range"
        min={5}
        max={60}
        step={5}
        value={minutes}
        onChange={(e) => {
          const m = Number(e.target.value);
          setMinutes(m);
          setDefaultMinutes(m);
        }}
      />
      <div className="slider-bounds">
        <span>5분</span>
        <span>60분</span>
      </div>
      <button className="btn primary" onClick={start}>
        집중 시작 🌰
      </button>
      <button className="btn ad" onClick={onWatchAd}>
        📺 광고 보고 도토리 +3 (오늘 {adsLeftToday()}회 남음)
      </button>
    </section>
  );
}
