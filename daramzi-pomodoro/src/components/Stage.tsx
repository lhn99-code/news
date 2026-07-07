import { CSSProperties } from 'react';
import { DEFAULT_FLOOR, DEFAULT_SKY, ITEMS, Slot } from '../data/catalog';

interface Props {
  equipped: Record<Slot, string | null>;
  working: boolean;
}

function eq(equipped: Record<Slot, string | null>, slot: Slot) {
  const id = equipped[slot];
  return ITEMS.find((i) => i.id === id) ?? null;
}

// 3D 다람쥐 이미지 (임시 URL). 실제 배포 시 프로젝트에 에셋을 번들해 교체하세요.
const SQUIRREL_SRC =
  'https://mcp-tools-z-image-turbo.hf.space/--replicas/sjbqs/gradio_api/file=/tmp/gradio/8620c4c82eae7ede33c69eea9ccd1fc701c177f73b25a1e1be75d764c31be791/image.webp';

export function Stage({ equipped, working }: Props) {
  const sky = eq(equipped, 'skyBg');
  const floor = eq(equipped, 'floorBg');
  const hat = eq(equipped, 'hat');
  const scarf = eq(equipped, 'scarf');
  const ring = eq(equipped, 'ring');

  const skyStyle: CSSProperties = { background: sky?.css ?? DEFAULT_SKY };
  const floorStyle: CSSProperties = { background: floor?.css ?? DEFAULT_FLOOR };

  return (
    <section className="stage">
      <div className="sky" style={skyStyle} />
      <div className="floor" style={floorStyle} />
      <div className="pines">🌲🌲🌲🌲🌲🌲</div>
      <div className="tree">🌳</div>
      <div className="squirrel-wrap">
        {hat && <div className="deco hat">{hat.emoji}</div>}
        <img
          className={`squirrel${working ? ' working' : ''}`}
          src={SQUIRREL_SRC}
          alt="다람쥐"
          onError={(e) => {
            const el = e.currentTarget;
            el.onerror = null;
            const div = document.createElement('div');
            div.className = `squirrel${working ? ' working' : ''}`;
            div.textContent = '🐿️';
            el.replaceWith(div);
          }}
        />
        {scarf && <div className="deco scarf">{scarf.emoji}</div>}
        {ring && <div className="deco ring">{ring.emoji}</div>}
      </div>
      {working && (
        <div className="falling">
          <span className="acorn-drop d1">🌰</span>
          <span className="acorn-drop d2">🌰</span>
          <span className="acorn-drop d3">🌰</span>
        </div>
      )}
    </section>
  );
}
