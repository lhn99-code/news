import { GameStore } from '../state/useGameState';
import { ITEMS, Item, SHOP_GROUPS } from '../data/catalog';

interface Props {
  store: GameStore;
  toast: (m: string) => void;
}

export function ShopScreen({ store, toast }: Props) {
  const { state, buyItem, toggleEquip } = store;

  const renderButton = (item: Item) => {
    const owned = state.ownedItems.includes(item.id);
    const equipped = state.equipped[item.slot] === item.id;
    if (!owned) {
      return (
        <button
          className="item-btn buy"
          disabled={state.acorns < item.price}
          onClick={() => {
            if (buyItem(item)) toast(`${item.name} 구매 완료!`);
          }}
        >
          🌰 {item.price}
        </button>
      );
    }
    if (equipped) {
      return (
        <button className="item-btn equipped" onClick={() => toggleEquip(item)}>
          장착중
        </button>
      );
    }
    return (
      <button className="item-btn equip" onClick={() => toggleEquip(item)}>
        장착
      </button>
    );
  };

  return (
    <section className="panel sheet">
      <h2>🛍️ 꾸미기 상점</h2>
      <p className="hint">도토리로 아이템을 사고, 눌러서 장착/해제해요.</p>
      {SHOP_GROUPS.map((g) => (
        <div className="shop-group" key={g.slot}>
          <h3>{g.label}</h3>
          {ITEMS.filter((i) => i.slot === g.slot).map((item) => {
            const owned = state.ownedItems.includes(item.id);
            return (
              <div className="item-row" key={item.id}>
                <div className="item-emoji">{item.emoji}</div>
                <div className="item-info">
                  <div className="item-name">{item.name}</div>
                  <div className="item-price">{owned ? '보유중' : `🌰 ${item.price}`}</div>
                </div>
                {renderButton(item)}
              </div>
            );
          })}
        </div>
      ))}
    </section>
  );
}
