/* Only the contents list collapses; every article remains readable without JS. */
(() => {
  const toc = document.querySelector('.guide-toc');
  if (!toc) return;
  const wide = window.matchMedia('(min-width: 761px)');
  const adapt = () => { toc.open = wide.matches; };
  adapt();
  wide.addEventListener('change', adapt);
})();
