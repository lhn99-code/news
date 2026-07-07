import { useCallback, useState } from 'react';
import { useGameState } from './state/useGameState';
import { Stage } from './components/Stage';
import { TabBar, TabKey } from './components/TabBar';
import { Toast } from './components/Toast';
import { TimerScreen } from './screens/TimerScreen';
import { ShopScreen } from './screens/ShopScreen';
import { CollectionScreen } from './screens/CollectionScreen';
import { RankScreen } from './screens/RankScreen';

export default function App() {
  const store = useGameState();
  const [tab, setTab] = useState<TabKey>('timer');
  const [working, setWorking] = useState(false);
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  const toast = useCallback((m: string) => setToastMsg(m), []);

  if (!store.loaded) {
    return <div className="app loading">불러오는 중…</div>;
  }

  const { state } = store;

  return (
    <div className="app">
      <header className="topbar">
        <span className="brand">🐿️ 다람쥐 뽀모도로</span>
        <span className="pills">
          <span className="pill streak">🔥 {state.streakDays}일</span>
          <span className="pill acorn">🌰 {state.acorns}</span>
        </span>
      </header>

      <Stage equipped={state.equipped} working={working} />

      {tab === 'timer' && (
        <TimerScreen store={store} toast={toast} onWorkingChange={setWorking} />
      )}
      {tab === 'shop' && <ShopScreen store={store} toast={toast} />}
      {tab === 'collection' && <CollectionScreen store={store} toast={toast} />}
      {tab === 'rank' && <RankScreen store={store} toast={toast} />}

      <TabBar tab={tab} onTab={setTab} />
      <Toast message={toastMsg} onClear={() => setToastMsg(null)} />
    </div>
  );
}
