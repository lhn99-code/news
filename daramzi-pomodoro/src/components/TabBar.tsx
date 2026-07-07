export type TabKey = 'timer' | 'shop' | 'collection' | 'rank';

const TABS: { key: TabKey; label: string }[] = [
  { key: 'timer', label: '⏱️ 집중' },
  { key: 'shop', label: '🛍️ 상점' },
  { key: 'collection', label: '📖 도감' },
  { key: 'rank', label: '🏆 랭킹' },
];

interface Props {
  tab: TabKey;
  onTab: (t: TabKey) => void;
}

export function TabBar({ tab, onTab }: Props) {
  return (
    <nav className="tabbar">
      {TABS.map((t) => (
        <button
          key={t.key}
          className={`tab${tab === t.key ? ' active' : ''}`}
          onClick={() => onTab(t.key)}
        >
          {t.label}
        </button>
      ))}
    </nav>
  );
}
