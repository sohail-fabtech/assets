// Edge Pulse feedback animations. Durations/easings follow the motion spec; all return promises.
import { ease, tween, lerp, wait } from './tween.js';

const T = (el, s) => (el.style.transform = s);

// button press: 80ms down (outQuad) → 120ms release (outBack)
export async function press(el) {
  await tween(80, ease.outQuad, v => T(el, `translateY(${3 * v}px) scale(${lerp(1, .94, v)})`));
  await tween(120, ease.outBack, v => T(el, `translateY(${3 - 3 * v}px) scale(${lerp(.94, 1, v)})`));
  el.style.transform = '';
}

// appear: 0.85 → 1.05 → 1 (280ms)
export async function popIn(el) {
  el.style.opacity = 0;
  await tween(180, ease.outBack, v => { el.style.opacity = Math.min(1, v * 1.6); T(el, `scale(${lerp(.85, 1.05, v)})`); });
  await tween(100, ease.outQuad, v => T(el, `scale(${lerp(1.05, 1, v)})`));
  el.style.transform = '';
}

// staggered entrance for grids/lists (mode tiles, badges)
export const stagger = (els, gap = 60) => Promise.all([...els].map((el, i) => (el.style.opacity = 0, wait(i * gap).then(() => popIn(el)))));

// HUD value bump: 1 → 1.08 → 1 in 100ms
export async function bump(el) {
  await tween(40, ease.outQuad, v => T(el, `scale(${lerp(1, 1.08, v)})`));
  await tween(60, ease.outBack, v => T(el, `scale(${lerp(1.08, 1, v)})`));
}

// rolling number for score/shards (tabular nums keep width stable)
export const countTo = (el, from, to, ms = 450) =>
  tween(ms, ease.outCubic, v => (el.textContent = Math.round(lerp(from, to, v)).toLocaleString()));

// locked tap: short horizontal wiggle, 250ms
export const wiggle = el => tween(250, ease.outQuad, v => T(el, `translateX(${Math.sin(v * Math.PI * 5) * 6 * (1 - v)}px)`));

// stamp: slam down 1.6 → 0.95 → 1 (240ms) + dust burst
export async function stampDown(el, fx) {
  el.style.opacity = 1;
  await tween(140, ease.outCubic, v => T(el, `scale(${lerp(1.6, .95, v)}) rotate(${lerp(-18, -6, v)}deg)`));
  fx?.burst(el, 14, ['#ff9ee8', '#fff']);
  await tween(100, ease.outBack, v => T(el, `scale(${lerp(.95, 1, v)}) rotate(-6deg)`));
}

// unlock reward (badge, cosmetic): anticipation → pop with spin → sparkle
export async function unlock(el, fx) {
  await tween(20, ease.outQuad, v => T(el, `scale(${lerp(1, .9, v)})`));
  await tween(220, ease.outBack, v => { T(el, `scale(${lerp(.9, 1.1, v)}) rotate(${lerp(-20, 0, v)}deg)`); el.style.filter = `brightness(${lerp(1, 1.6, v)})`; });
  fx?.burst(el, 18, ['#fff3b0', '#ffc21f', '#fff']);
  await tween(120, ease.outQuad, v => { T(el, `scale(${lerp(1.1, 1, v)})`); el.style.filter = `brightness(${lerp(1.6, 1, v)})`; });
}

// ribbon unfurl: scaleX 0 → 1.05 → 1 (300ms)
export async function unfurl(el) {
  el.style.opacity = 1;
  await tween(200, ease.outBack, v => T(el, `scaleX(${lerp(0, 1.05, v)}) scaleY(${lerp(.6, 1, v)})`));
  await tween(100, ease.outQuad, v => T(el, `scaleX(${lerp(1.05, 1, v)})`));
}

// panel: 300ms open, 250ms close (inOutCubic)
export const panelOpen = el => tween(300, ease.inOutCubic, v => { el.style.opacity = v; T(el, `translateY(${lerp(24, 0, v)}px) scale(${lerp(.92, 1, v)})`); });
export const panelClose = el => tween(250, ease.inOutCubic, v => { el.style.opacity = 1 - v; T(el, `scale(${lerp(1, .95, v)})`); });

// progress fill to pct (0..1), 600ms outCubic
export const fillTo = (el, from, to) => tween(600, ease.outCubic, v => (el.style.clipPath = `inset(0 ${100 - lerp(from, to, v) * 100}% 0 0 round 99px)`));

// toggle: knob slides via crossfade between on/off art with squash, 180ms
export async function flip(onImg, isOn) {
  const box = onImg.parentElement;
  await Promise.all([
    tween(180, ease.outCubic, v => (onImg.style.opacity = isOn ? v : 1 - v)),
    tween(180, ease.outBack, v => T(box, `scaleX(${1 + Math.sin(v * Math.PI) * .06})`)),
  ]);
}

// life lost: swell + flash (90ms) then shards (handled by fx) — 300ms total
export async function lifeLost(el, fx) {
  await tween(90, ease.outQuad, v => { T(el, `scale(${lerp(1, 1.12, v)})`); el.style.filter = `brightness(${lerp(1, 1.8, v)})`; });
  el.style.opacity = 0;
  await fx?.burst(el, 6, ['#ff7ad9', '#c9a0ff', '#ffffffcc'], true);
}

// stars earned: sequential pops, 150ms apart
export const starsIn = els => Promise.all([...els].map((el, i) => wait(i * 150).then(() => unlock(el))));

// One full-screen canvas for all particles: {x,y,vx,vy,life} + gravity.
export function particles(canvas) {
  const g = canvas.getContext('2d'); let ps = [], running = false;
  const fit = () => { canvas.width = innerWidth * devicePixelRatio; canvas.height = innerHeight * devicePixelRatio; };
  fit(); addEventListener('resize', fit);
  function frame() {
    g.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0); g.clearRect(0, 0, innerWidth, innerHeight);
    ps = ps.filter(p => (p.life -= p.decay) > 0);
    for (const p of ps) {
      p.x += p.vx; p.y += p.vy; p.vy += .3; p.vx *= .98;
      g.globalAlpha = p.life; g.fillStyle = p.c; g.beginPath();
      if (p.shard) { g.moveTo(p.x, p.y - 8); g.lineTo(p.x + 7, p.y + 5); g.lineTo(p.x - 6, p.y + 4); }
      else g.arc(p.x, p.y, 1 + 4 * p.life, 0, 7);
      g.fill();
    }
    running = ps.length > 0; if (running) requestAnimationFrame(frame);
  }
  return {
    burst(el, n, colors, shard = false) {
      const r = el.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
      for (let i = 0; i < n; i++) {
        const a = i / n * 6.28 + Math.random() * .4, s = 3 + Math.random() * 4;
        ps.push({ x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 2, life: 1, decay: shard ? .04 : .03, c: colors[i % colors.length], shard });
      }
      if (!running) { running = true; requestAnimationFrame(frame); }
      return wait(shard ? 320 : 420);
    },
  };
}

// ---- themed control feedback (CSS classes in anim.css, timing from theme tokens) ----
/** Replay a one-shot CSS effect: 'jelly' | 'deny' | 'pop' | 'glow'. */
export function play(el, name) {
  const cls = 'fx-' + name; el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls);
  el.addEventListener('animationend', () => el.classList.remove(cls), { once: true });
}
/** Ripple from the pointer position inside el. */
export function ripple(el, ev) {
  const r = el.getBoundingClientRect(), s = Math.max(r.width, r.height) * 2, d = document.createElement('span');
  d.className = 'ripple'; d.style.cssText = `width:${s}px;height:${s}px;left:${ev.clientX - r.left - s / 2}px;top:${ev.clientY - r.top - s / 2}px`;
  el.style.overflow = 'hidden'; el.appendChild(d); d.addEventListener('animationend', () => d.remove(), { once: true });
}
/** Loading → success: swaps the label for a spinner, then draws a check. */
export async function loadThenSucceed(el, ms = 900) {
  const lbl = el.querySelector('.lbl'), text = lbl.innerHTML;
  lbl.innerHTML = '<span class="spin"></span>';
  await new Promise(r => setTimeout(r, ms));
  lbl.innerHTML = '<svg class="check-draw" width="34" height="34" viewBox="0 0 34 34"><path d="M7 18 L14 25 L27 10" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  play(el, 'pop');
  await new Promise(r => setTimeout(r, 900)); lbl.innerHTML = text;
}
