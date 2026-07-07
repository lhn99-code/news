import { GameStore } from '../state/useGameState';
import { SQUIRRELS } from '../data/catalog';

interface Props {
  store: GameStore;
  toast: (m: string) => void;
}

export function CollectionScreen({ store, toast }: Props) {
  const { state, adoptSquirrel } = store;
  return (
    <section className="panel sheet">
      <h2>📖 다람쥐 도감</h2>
      <p className="hint">도토리를 모아 다람쥐를 수집하세요. (능력치 효과 없는 수집 전용!)</p>
      <div className="friends-grid">
        {SQUIRRELS.map((sq) => {
          const owned = state.ownedSquirrels.includes(sq.id);
          return (
            <div className={`friend-card${owned ? '' : ' locked'}`} key={sq.id}>
              <div className="friend-emoji">🐿️</div>
              <div className="friend-name">{owned ? sq.name : '???'}</div>
              <div className="friend-status">{owned ? '수집 완료 ✅' : `🌰 ${sq.price}`}</div>
              {!owned && (
                <button
                  className="item-btn buy"
                  disabled={state.acorns < sq.price}
                  onClick={() => {
                    if (adoptSquirrel(sq)) toast(`${sq.name}를 도감에 추가! 📖`);
                  }}
                >
                  데려오기
                </button>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
