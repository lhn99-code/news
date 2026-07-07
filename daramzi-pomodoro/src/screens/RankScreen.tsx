import { GameStore } from '../state/useGameState';

interface Props {
  store: GameStore;
  toast: (m: string) => void;
}

// Phase 2: 랭킹·친구·공유는 토스 로그인이 전제예요.
// 실제 구현 시 appLogin()으로 사용자 식별 후 서버 랭킹을 연동하세요.
//   import { appLogin } from '@apps-in-toss/framework';
//   const { authorizationCode } = await appLogin();
// 공유는 예제(with-share-link)의 share({ message }) API를 사용합니다.
const MOCK_OTHERS = [
  { name: '도토리왕', min: 520 },
  { name: '밤톨이', min: 330 },
  { name: '다람이', min: 180 },
  { name: '코코', min: 90 },
];

export function RankScreen({ store, toast }: Props) {
  const me = { name: '나', min: store.state.totalFocusMin, me: true };
  const all = [...MOCK_OTHERS.map((o) => ({ ...o, me: false })), me].sort(
    (a, b) => b.min - a.min
  );

  return (
    <section className="panel sheet">
      <h2>
        🏆 랭킹 <span className="phase-tag">Phase 2</span>
      </h2>
      <div className="lock-note">
        🔒 랭킹·친구는 <b>토스 로그인</b>이 필요해요.
        <br />
        아래는 로그인 후 모습 미리보기예요.
      </div>
      {all.map((r, i) => (
        <div className={`rank-row${r.me ? ' me' : ''}`} key={r.name}>
          <div className="rank-no">{i + 1}</div>
          <div className="rank-name">{r.me ? '🐿️ 나' : r.name}</div>
          <div className="rank-min">{r.min}분</div>
        </div>
      ))}
      <button
        className="btn share"
        onClick={() => toast('📤 (Phase 2) 친구에게 공유·초대 — 토스 공유 기능 연동 예정')}
      >
        📤 내 다람쥐·집중 기록 공유하기
      </button>
    </section>
  );
}
