// Edge Pulse live bomb FX: burning fuse spark + explosion (flash, shockwave, fireball, sparks, debris, embers, smoke).
// One full-screen canvas; fire and sparks use additive blending so overlapping light blooms like real flame.
import { ease, tween, lerp, wait } from './tween.js';

const rnd = (a, b) => a + Math.random() * (b - a);
const gentle = () => document.body.classList.contains('gentle') || matchMedia('(prefers-reduced-motion: reduce)').matches;

export function blastFX(canvas) {
  const g = canvas.getContext('2d');
  const P = { smoke: [], fire: [], debris: [], sparks: [], rings: [], beams: [], flash: [] };
  const fuses = new Map(); // element → tip fraction [x, y]
  let last = performance.now();

  const fit = () => { canvas.width = innerWidth * devicePixelRatio; canvas.height = innerHeight * devicePixelRatio; };
  fit(); addEventListener('resize', fit);
  const center = el => { const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2, r.width]; };

  function spark(x, y, speed, life, up = true) {
    const a = up ? rnd(-Math.PI * .85, -Math.PI * .15) : rnd(0, Math.PI * 2), s = rnd(speed * .4, speed);
    P.sparks.push({ x, y, px: x, py: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, life, max: life });
  }
  function puff(x, y, r, life, rise = .5, shade = 90) {
    P.smoke.push({ x, y, r, grow: rnd(.35, .6), vx: rnd(-.25, .25), vy: -rnd(rise * .6, rise), life, max: life, shade, a: rnd(.35, .5) });
  }

  function frame(now) {
    const dt = Math.min(48, now - last) / 16.7 / (globalThis.SLOW || 1); last = now;  // SLOW = slow-motion preview
    g.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0); g.clearRect(0, 0, innerWidth, innerHeight);

    // burning fuses: flickering glow + streaking sparks + thin wisps of smoke
    for (const [el, tip] of fuses) {
      if (!el.isConnected) { fuses.delete(el); continue; }
      const r = el.getBoundingClientRect(), x = r.left + r.width * tip[0], y = r.top + r.height * tip[1];
      if (r.bottom < 0 || r.top > innerHeight) continue;
      const n = gentle() ? .4 : 2.2;
      for (let i = 0; i < n * dt; i++) spark(x, y, 3.2, rnd(14, 26));
      if (Math.random() < .08 * dt) puff(x, y - 4, 3, rnd(40, 60), .7, 140);
      const fl = rnd(9, 15), gr = g.createRadialGradient(x, y, 0, x, y, fl * 2.2);
      gr.addColorStop(0, 'rgba(255,255,230,1)'); gr.addColorStop(.25, 'rgba(255,210,80,.9)'); gr.addColorStop(1, 'rgba(255,120,20,0)');
      g.globalCompositeOperation = 'lighter'; g.fillStyle = gr; g.beginPath(); g.arc(x, y, fl * 2.2, 0, 7); g.fill();
      g.globalCompositeOperation = 'source-over';
    }

    // smoke (under everything, normal blending): soft radial puffs that rise, swell and thin out
    P.smoke = P.smoke.filter(p => (p.life -= dt) > 0);
    for (const p of P.smoke) {
      p.x += p.vx * dt; p.y += p.vy * dt; p.r += p.grow * dt; p.vy *= .995;
      const t = p.life / p.max, a = p.a * Math.min(1, t * 1.6) * Math.min(1, (1 - t) * 6 + .2);
      const gr = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
      gr.addColorStop(0, `rgba(${p.shade},${p.shade},${p.shade + 8},${a})`); gr.addColorStop(1, `rgba(${p.shade},${p.shade},${p.shade + 8},0)`);
      g.fillStyle = gr; g.beginPath(); g.arc(p.x, p.y, p.r, 0, 7); g.fill();
    }

    g.globalCompositeOperation = 'lighter';
    // fireball blobs: white-hot core cooling to orange then red as they grow
    P.fire = P.fire.filter(p => (p.life -= dt) > 0);
    for (const p of P.fire) {
      const t = 1 - p.life / p.max; p.x += p.vx * dt; p.y += p.vy * dt; p.vx *= .92; p.vy = p.vy * .92 - .05;
      const r = lerp(p.r0, p.r1, ease.outCubic(t)), a = (1 - t) ** 1.4;
      const gr = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, r);
      gr.addColorStop(0, `rgba(255,250,220,${a})`); gr.addColorStop(.35, `rgba(255,${190 - t * 90 | 0},60,${a * .9})`);
      gr.addColorStop(.75, `rgba(${p.tint},${a * .5})`); gr.addColorStop(1, 'rgba(255,60,0,0)');
      g.fillStyle = gr; g.beginPath(); g.arc(p.x, p.y, r, 0, 7); g.fill();
    }
    // line-bomb beams
    P.beams = P.beams.filter(b => (b.life -= dt) > 0);
    for (const b of P.beams) {
      const t = 1 - b.life / b.max, w = innerWidth * ease.outCubic(Math.min(1, t * 2.2)), h = b.h * (1 - t);
      const gr = g.createLinearGradient(0, b.y - h, 0, b.y + h);
      gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, `rgba(255,250,230,${1 - t})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
      g.fillStyle = gr; g.fillRect(b.x - w, b.y - h, w * 2, h * 2);
    }
    // sparks: streaks drawn from previous to current position, colour by temperature
    P.sparks = P.sparks.filter(p => (p.life -= dt) > 0);
    g.lineCap = 'round';
    for (const p of P.sparks) {
      p.px = p.x; p.py = p.y; p.x += p.vx * dt; p.y += p.vy * dt; p.vy += .12 * dt; p.vx *= .985;
      const t = p.life / p.max;
      g.strokeStyle = t > .6 ? `rgba(255,255,235,${t})` : t > .3 ? `rgba(255,200,70,${t + .2})` : `rgba(255,110,30,${t * 2})`;
      g.lineWidth = 1 + 1.6 * t; g.beginPath(); g.moveTo(p.px - p.vx * 1.5, p.py - p.vy * 1.5); g.lineTo(p.x, p.y); g.stroke();
    }
    g.globalCompositeOperation = 'source-over';

    // debris: chunks of the shell, piece-coloured, tumbling with gravity
    P.debris = P.debris.filter(p => (p.life -= dt) > 0);
    for (const p of P.debris) {
      p.x += p.vx * dt; p.y += p.vy * dt; p.vy += .32 * dt; p.rot += p.vr * dt;
      g.save(); g.translate(p.x, p.y); g.rotate(p.rot); g.globalAlpha = Math.min(1, p.life / 12);
      g.fillStyle = p.c; g.beginPath(); g.moveTo(-p.s, -p.s * .6); g.lineTo(p.s, -p.s * .3); g.lineTo(p.s * .4, p.s); g.lineTo(-p.s * .8, p.s * .5); g.fill();
      g.fillStyle = 'rgba(255,255,255,.45)'; g.fillRect(-p.s * .6, -p.s * .5, p.s * .7, p.s * .25); g.restore();
    }
    g.globalAlpha = 1;
    // shockwave rings + flash
    P.rings = P.rings.filter(p => (p.life -= dt) > 0);
    for (const p of P.rings) {
      const t = 1 - p.life / p.max, r = lerp(p.r0, p.r1, ease.outCubic(t));
      g.strokeStyle = `rgba(255,245,220,${(1 - t) * .8})`; g.lineWidth = lerp(p.w, 1, t); g.beginPath(); g.arc(p.x, p.y, r, 0, 7); g.stroke();
    }
    P.flash = P.flash.filter(p => (p.life -= dt) > 0);
    for (const p of P.flash) {
      const t = 1 - p.life / p.max, gr = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
      gr.addColorStop(0, `rgba(255,255,255,${1 - t})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
      g.fillStyle = gr; g.beginPath(); g.arc(p.x, p.y, p.r, 0, 7); g.fill();
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  return {
    /** Light a fuse on a bomb element; tip = [x, y] fraction of the element box (from bombs.json). */
    fuse(el, tip) { fuses.set(el, tip); },
    unfuse(el) { fuses.delete(el); },

    /** Detonate: anticipation (squash, shake, heat) → explosion → lingering smoke. Resolves when the blast peaks. */
    async blast(el, { color = '#ffa51f', light = '#ffe08a', power = 1, kind = 'round', shakeEl } = {}) {
      const calm = gentle(); fuses.delete(el);
      // 1. anticipation: 140ms swell + jitter + heat flash
      await tween(140, ease.inQuad, v => {
        const j = calm ? 0 : v * 3.5 * power;
        el.style.transform = `translate(${rnd(-j, j)}px,${rnd(-j, j)}px) scale(${lerp(1, 1.14, v)},${lerp(1, .9, v)})`;
        el.style.filter = `brightness(${lerp(1, 1.9, v)}) saturate(${lerp(1, 1.4, v)})`;
      });
      const [x, y, w] = center(el), R = w * .5 * power;
      el.style.opacity = 0; el.style.filter = ''; el.style.transform = '';
      // 2. explosion
      const tint = hexRGB(light), k = calm ? .35 : 1;
      P.flash.push({ x, y, r: R * 2.6, life: 6, max: 6 });
      P.rings.push({ x, y, r0: R * .3, r1: R * 3.2, w: 10 * power, life: 22, max: 22 });
      if (power > 1.2) P.rings.push({ x, y, r0: R * .2, r1: R * 2.2, w: 6, life: 30, max: 30 });
      for (let i = 0; i < 16 * k * power; i++) {
        const a = rnd(0, 7), d = rnd(0, R * .5), s = rnd(1, 4) * power;
        P.fire.push({ x: x + Math.cos(a) * d, y: y + Math.sin(a) * d, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
                      r0: R * rnd(.2, .4), r1: R * rnd(.7, 1.3), life: rnd(22, 34), max: 34, tint });
      }
      for (let i = 0; i < 46 * k * power; i++) spark(x, y, 11 * power, rnd(18, 36), false);
      for (let i = 0; i < 12 * k * power; i++) {
        const a = rnd(0, 7), s = rnd(4, 10) * power;
        P.debris.push({ x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 4, rot: rnd(0, 7), vr: rnd(-.3, .3), s: rnd(4, 8) * Math.sqrt(power), c: i % 3 ? color : light, life: rnd(40, 70) });
      }
      if (kind === 'line') { P.beams.push({ x, y, h: R * .45, life: 22, max: 22 }); }
      if (kind === 'spike') for (let i = 0; i < 8; i++) { const a = i / 8 * 6.28; for (let j = 0; j < 4; j++) spark(x + Math.cos(a) * R * .3, y + Math.sin(a) * R * .3, 13, 30, false); }
      // 3. smoke: starts dark at the core just after the flash, rolls upward and lightens
      setTimeout(() => {
        for (let i = 0; i < 10 * power * (calm ? .5 : 1); i++) {
          const a = rnd(0, 7), d = rnd(0, R * .6);
          puff(x + Math.cos(a) * d, y + Math.sin(a) * d, R * rnd(.25, .45), rnd(70, 100), .9, rnd(60, 95) | 0);
        }
      }, 90);
      // 4. screen shake (skipped in Gentle motion)
      if (shakeEl && !calm) tween(320, ease.outQuad, v => {
        const m = (1 - v) * 7 * power; shakeEl.style.transform = v < 1 ? `translate(${rnd(-m, m)}px,${rnd(-m, m)}px)` : '';
      });
      await wait(120);
    },
  };
}

function hexRGB(h) { const n = parseInt(h.slice(1), 16); return `${n >> 16},${(n >> 8) & 255},${n & 255}`; }
