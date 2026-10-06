(() => {
  const root = document.documentElement;
  const seed = 1;
  const speed = 0.77;
  const amount = 1.0;
  const direction = 1;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const blobs = [
    {
      x: 65.34,
      y: 44.62,
      stops: "rgba(52, 52, 50, 1) 0%, rgba(52, 52, 50, 0.844) 8.53%, rgba(52, 52, 50, 0.5) 17.05%, rgba(52, 52, 50, 0.156) 25.58%, rgba(52, 52, 50, 0) 34.1%"
    },
    {
      x: 28.07,
      y: 74.48,
      stops: "rgba(18, 18, 17, 1) 0%, rgba(18, 18, 17, 0.844) 11.15%, rgba(18, 18, 17, 0.5) 22.3%, rgba(18, 18, 17, 0.156) 33.45%, rgba(18, 18, 17, 0) 44.6%"
    },
    {
      x: 52.42,
      y: 19.94,
      stops: "rgba(52, 52, 50, 1) 0%, rgba(52, 52, 50, 0.844) 14.13%, rgba(52, 52, 50, 0.5) 28.25%, rgba(52, 52, 50, 0.156) 42.38%, rgba(52, 52, 50, 0) 56.5%"
    },
    {
      x: 80.31,
      y: 84.47,
      stops: "rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.844) 17.27%, rgba(0, 0, 0, 0.5) 34.55%, rgba(0, 0, 0, 0.156) 51.82%, rgba(0, 0, 0, 0) 69.1%"
    }
  ].map((blob, index) => ({
    ...blob,
    phaseX: hashToPhase(seed, index * 2),
    phaseY: hashToPhase(seed, index * 2 + 1)
  }));

  function hashToPhase(value, offset) {
    let hash = (value + Math.imul(offset + 1, 0x9e3779b9)) >>> 0;
    hash ^= hash >>> 16;
    hash = Math.imul(hash, 0x21f0aaad);
    hash ^= hash >>> 15;
    hash = Math.imul(hash, 0x735a2d97);
    hash ^= hash >>> 15;
    return (hash >>> 0) / 0x100000000 * Math.PI * 2;
  }

  function render(elapsedSeconds) {
    const ph = elapsedSeconds * speed;
    const amt = amount;
    const dir = direction;
    const spin = ph * dir;
    const layers = blobs.map((blob) => {
      const x = blob.x + (Math.sin(ph * 0.55 + blob.phaseX) - Math.sin(blob.phaseX)) * 14 * amt;
      const y = blob.y + (Math.sin(ph * 0.43 + blob.phaseY) - Math.sin(blob.phaseY)) * 14 * amt;
      return `radial-gradient(circle at ${x}% ${y}%, ${blob.stops})`;
    });

    root.style.setProperty("--bloom-field-image", layers.join(", "));
    root.style.setProperty("--bloom-field-spin", `${spin}rad`);
  }

  if (reducedMotion.matches) {
    return;
  }

  let startTime;
  function animate(timestamp) {
    if (startTime === undefined) {
      startTime = timestamp;
    }
    render((timestamp - startTime) / 1000);
    window.requestAnimationFrame(animate);
  }

  window.requestAnimationFrame(animate);
})();
