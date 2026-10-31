// Edge Pulse motion core. All gameplay motion goes through these curves — never linear.
export const ease = {
  inQuad: t => t * t,
  outQuad: t => t * (2 - t),
  outCubic: t => 1 - (1 - t) ** 3,
  inOutCubic: t => t < .5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2,
  outBack: t => { const s = 1.4; return 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2; }, // ~8% overshoot
  fall: t => t < .6 ? .6 * (t / .6) ** 2 : .6 + .4 * (1 - (1 - (t - .6) / .4) ** 2), // inQuad 60% → outQuad
};
// tween(ms, ease, v => apply(v)) — v goes 0→1; resolves when done so steps can be chained with await
// globalThis.SLOW stretches time for debugging only (1 = real speed)
const k = () => globalThis.SLOW || 1;
export const tween = (ms, e, fn) => new Promise(done => {
  ms *= k();
  const t0 = performance.now();
  const step = now => { const t = Math.min(1, (now - t0) / ms); fn(e(t)); t < 1 ? requestAnimationFrame(step) : done(); };
  requestAnimationFrame(step);
});
export const lerp = (a, b, v) => a + (b - a) * v;
export const wait = ms => new Promise(r => setTimeout(r, ms * k()));
