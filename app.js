/* 🐿️ 다람쥐 뽀모도로 — 프로토타입 로직
 * 요구사항 명세서(docs/다람쥐_뽀모도로_요구사항명세서.md) 기반
 * - 집중 시간 5~60분(기본 25), 도토리 5분당 1개
 * - 성공 시 100% / 포기(화면 이탈 포함) 시 50% 지급
 * - 도토리로 꾸미기 아이템·친구 영입(친구는 도감 수집 전용)
 * - 결제 요소 없음, 상태는 localStorage에 저장
 */

const ACORN_PER_MINUTES = 5; // 5분당 도토리 1개

// ---- 카탈로그 ----
const ITEMS = [
  // 모자
  { id: 'hat_acorn', slot: 'hat', name: '도토리 모자', emoji: '🌰', price: 10 },
  { id: 'hat_maple', slot: 'hat', name: '단풍잎 모자', emoji: '🍁', price: 15 },
  { id: 'hat_chestnut', slot: 'hat', name: '밤송이 모자', emoji: '🌟', price: 20 },
  // 목도리
  { id: 'scarf_red', slot: 'scarf', name: '빨간 목도리', emoji: '🧣', price: 12 },
  { id: 'scarf_check', slot: 'scarf', name: '체크 목도리', emoji: '🟫', price: 18 },
  // 반지
  { id: 'ring_acorn', slot: 'ring', name: '도토리 반지', emoji: '💍', price: 15 },
  { id: 'ring_star', slot: 'ring', name: '별 반지', emoji: '⭐', price: 25 },
  // 하늘 배경
  { id: 'sky_clear', slot: 'skyBg', name: '맑은 하늘', emoji: '☀️', price: 25, css: 'linear-gradient(#9fd8ff, #e9f7ff)' },
  { id: 'sky_sunset', slot: 'skyBg', name: '노을 하늘', emoji: '🌇', price: 35, css: 'linear-gradient(#ffb88c, #ffe6c7)' },
  // 바닥 배경
  { id: 'floor_grass', slot: 'floorBg', name: '잔디밭', emoji: '🌱', price: 25, css: 'linear-gradient(#9bd17a, #7cc05a)' },
  { id: 'floor_leaf', slot: 'floorBg', name: '낙엽밭', emoji: '🍂', price: 35, css: 'linear-gradient(#e0a96d, #c9853f)' },
];

const SQUIRRELS = [
  { id: 'sq_basic', name: '기본 다람쥐', emoji: '🐿️', price: 0 },
  { id: 'sq_baby', name: '아기 다람쥐', emoji: '🐿️', price: 50 },
  { id: 'sq_stripe', name: '줄무늬 다람쥐', emoji: '🐿️', price: 100 },
  { id: 'sq_white', name: '흰 다람쥐', emoji: '🐿️', price: 200 },
];

// 기본(무료) 배경
const DEFAULT_SKY = 'linear-gradient(#bfe7ff, #e9f7ff)';
const DEFAULT_FLOOR = 'linear-gradient(#9bd17a, #7cc05a)';

// ---- 상태 ----
const SAVE_KEY = 'daramzi_pomodoro_v1';
const defaultState = () => ({
  acorns: 0,
  defaultMinutes: 25,
  ownedItems: [],
  equipped: { hat: null, scarf: null, ring: null, skyBg: null, floorBg: null },
  ownedSquirrels: ['sq_basic'],
});

let state = loadState();

function loadState() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (raw) return Object.assign(defaultState(), JSON.parse(raw));
  } catch (e) { /* noop */ }
  return defaultState();
}
function saveState() {
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(state)); } catch (e) { /* noop */ }
}

// ---- 타이머 세션 ----
let session = null; // { totalSec, leftSec, intervalId, droppedAcorns }

const $ = (id) => document.getElementById(id);

function init() {
  // 슬라이더
  const slider = $('minuteSlider');
  slider.value = state.defaultMinutes;
  $('minutesLabel').textContent = state.defaultMinutes;
  slider.addEventListener('input', () => {
    $('minutesLabel').textContent = slider.value;
    state.defaultMinutes = Number(slider.value);
    saveState();
  });

  $('startBtn').addEventListener('click', startFocus);
  $('giveUpBtn').addEventListener('click', () => endFocus('abandon'));

  // 탭 전환
  document.querySelectorAll('.tab').forEach((tab) => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  // 화면 이탈 = 포기 (집중 중일 때만)
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && session) {
      endFocus('abandon', true);
    }
  });

  renderAll();
}

// ---- 집중 시작/종료 ----
function startFocus() {
  const minutes = Number($('minuteSlider').value);
  session = {
    totalSec: minutes * 60,
    leftSec: minutes * 60,
    droppedAcorns: 0,
    intervalId: null,
  };
  $('setupView').classList.add('hidden');
  $('focusView').classList.remove('hidden');
  $('squirrel').classList.add('working');
  tick(); // 즉시 1회 갱신
  session.intervalId = setInterval(tick, 1000);
}

function tick() {
  if (!session) return;
  session.leftSec -= 1;

  const elapsedSec = session.totalSec - session.leftSec;
  const accrued = Math.floor(elapsedSec / (ACORN_PER_MINUTES * 60)); // 적립된 도토리

  // 새 도토리가 적립되면 떨어지는 연출
  while (session.droppedAcorns < accrued) {
    session.droppedAcorns += 1;
    dropAcorn();
  }

  // 화면 갱신
  $('countdown').textContent = fmt(Math.max(session.leftSec, 0));
  $('sessionAcorns').textContent = accrued;
  $('progressBar').style.width = `${(elapsedSec / session.totalSec) * 100}%`;
  $('treeAcorns').textContent = '🌰'.repeat(Math.min(accrued, 8));

  if (session.leftSec <= 0) endFocus('complete');
}

function endFocus(reason, dueToHidden = false) {
  if (!session) return;
  clearInterval(session.intervalId);

  const elapsedSec = session.totalSec - Math.max(session.leftSec, 0);
  const accrued = Math.floor(elapsedSec / (ACORN_PER_MINUTES * 60));
  let earned;
  if (reason === 'complete') {
    earned = accrued; // 100%
  } else {
    earned = Math.floor(accrued / 2); // 포기 50%
  }

  state.acorns += earned;
  saveState();
  session = null;

  // UI 복귀
  $('focusView').classList.add('hidden');
  $('setupView').classList.remove('hidden');
  $('squirrel').classList.remove('working');
  $('treeAcorns').textContent = '';
  $('progressBar').style.width = '0%';
  renderAll();

  if (reason === 'complete') {
    toast(`집중 성공! 🌰 ${earned}개 획득`);
  } else if (dueToHidden) {
    toast(`화면을 벗어나 포기 처리됐어요. 절반인 🌰 ${earned}개만 획득`);
  } else {
    toast(`포기했어요. 절반인 🌰 ${earned}개 획득`);
  }
}

// ---- 연출 ----
function dropAcorn() {
  const layer = $('fallingLayer');
  const el = document.createElement('div');
  el.className = 'acorn-drop';
  el.textContent = '🌰';
  el.style.left = `${30 + Math.random() * 20}%`;
  el.style.top = '60px';
  layer.appendChild(el);
  setTimeout(() => el.remove(), 1100);
}

// ---- 렌더링 ----
function renderAll() {
  $('acornBalance').textContent = `🌰 ${state.acorns}`;
  renderStage();
  renderShop();
  renderFriends();
}

function renderStage() {
  const sky = equippedItem('skyBg');
  const floor = equippedItem('floorBg');
  $('sky').style.background = sky ? sky.css : DEFAULT_SKY;
  $('floor').style.background = floor ? floor.css : DEFAULT_FLOOR;
  $('decoHat').textContent = textOf(equippedItem('hat'));
  $('decoScarf').textContent = textOf(equippedItem('scarf'));
  $('decoRing').textContent = textOf(equippedItem('ring'));
}

function renderShop() {
  const groups = [
    { slot: 'hat', label: '🎩 모자' },
    { slot: 'scarf', label: '🧣 목도리' },
    { slot: 'ring', label: '💍 반지' },
    { slot: 'skyBg', label: '🌤️ 하늘 배경' },
    { slot: 'floorBg', label: '🌳 바닥 배경' },
  ];
  const list = $('shopList');
  list.innerHTML = '';
  groups.forEach((g) => {
    const wrap = document.createElement('div');
    wrap.className = 'shop-group';
    wrap.innerHTML = `<h3>${g.label}</h3>`;
    ITEMS.filter((i) => i.slot === g.slot).forEach((item) => {
      wrap.appendChild(itemRow(item));
    });
    list.appendChild(wrap);
  });
}

function itemRow(item) {
  const owned = state.ownedItems.includes(item.id);
  const equipped = state.equipped[item.slot] === item.id;
  const row = document.createElement('div');
  row.className = 'item-row';

  const btn = document.createElement('button');
  btn.className = 'item-btn';
  if (!owned) {
    btn.classList.add('buy');
    btn.textContent = `🌰 ${item.price}`;
    btn.disabled = state.acorns < item.price;
    btn.onclick = () => buyItem(item);
  } else if (equipped) {
    btn.classList.add('equipped');
    btn.textContent = '장착중';
    btn.onclick = () => toggleEquip(item, false);
  } else {
    btn.classList.add('equip');
    btn.textContent = '장착';
    btn.onclick = () => toggleEquip(item, true);
  }

  row.innerHTML = `
    <div class="item-emoji">${item.emoji}</div>
    <div class="item-info">
      <div class="item-name">${item.name}</div>
      <div class="item-price">${owned ? '보유중' : `🌰 ${item.price}`}</div>
    </div>`;
  row.appendChild(btn);
  return row;
}

function renderFriends() {
  const list = $('friendsList');
  list.innerHTML = '';
  SQUIRRELS.forEach((sq) => {
    const owned = state.ownedSquirrels.includes(sq.id);
    const card = document.createElement('div');
    card.className = 'friend-card' + (owned ? '' : ' locked');
    card.innerHTML = `
      <div class="friend-emoji">${sq.emoji}</div>
      <div class="friend-name">${owned ? sq.name : '???'}</div>
      <div class="friend-status">${owned ? '수집 완료 ✅' : `🌰 ${sq.price}`}</div>`;
    if (!owned) {
      const btn = document.createElement('button');
      btn.className = 'item-btn buy';
      btn.textContent = '데려오기';
      btn.disabled = state.acorns < sq.price;
      btn.onclick = () => adoptSquirrel(sq);
      card.appendChild(btn);
    }
    list.appendChild(card);
  });
}

// ---- 구매/장착 ----
function buyItem(item) {
  if (state.acorns < item.price) return;
  state.acorns -= item.price;
  state.ownedItems.push(item.id);
  state.equipped[item.slot] = item.id; // 사면 바로 장착
  saveState();
  renderAll();
  toast(`${item.name} 구매 완료!`);
}

function toggleEquip(item, on) {
  state.equipped[item.slot] = on ? item.id : null;
  saveState();
  renderAll();
}

function adoptSquirrel(sq) {
  if (state.acorns < sq.price) return;
  state.acorns -= sq.price;
  state.ownedSquirrels.push(sq.id);
  saveState();
  renderAll();
  toast(`${sq.name}를 도감에 추가했어요! 📖`);
}

// ---- 탭 ----
function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t) =>
    t.classList.toggle('active', t.dataset.tab === name)
  );
  $('timerPanel').classList.toggle('hidden', name !== 'timer');
  $('shopPanel').classList.toggle('hidden', name !== 'shop');
  $('friendsPanel').classList.toggle('hidden', name !== 'friends');
}

// ---- 유틸 ----
function equippedItem(slot) {
  const id = state.equipped[slot];
  return ITEMS.find((i) => i.id === id) || null;
}
function textOf(item) { return item ? item.emoji : ''; }
function fmt(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}
let toastTimer = null;
function toast(msg) {
  const el = $('toast');
  el.textContent = msg;
  el.classList.remove('hidden');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add('hidden'), 2600);
}

init();
