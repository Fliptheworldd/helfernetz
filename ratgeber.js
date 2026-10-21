/* Only the contents list collapses; every article remains readable without JS. */
(() => {
  const toc = document.querySelector('.guide-toc');
  if (!toc) return;
  const wide = window.matchMedia('(min-width: 761px)');
  const adapt = () => { toc.open = wide.matches; };
  adapt();
  wide.addEventListener('change', adapt);
})();

(() => {
  const lexicon = document.querySelector('.lexicon');
  if (!lexicon) return;
  const query = document.getElementById('lexicon-query');
  const clear = document.getElementById('lexicon-clear');
  const filters = [...lexicon.querySelectorAll('[data-category]')].filter(e => e.tagName === 'BUTTON');
  const entries = [...lexicon.querySelectorAll('.lexicon-entry')];
  const sections = [...lexicon.querySelectorAll('.lexicon-section')];
  const normalize = s => s.toLocaleLowerCase('de').replace(/ä/g,'a').replace(/ö/g,'o').replace(/ü/g,'u').replace(/ß/g,'ss').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const index = entries.map(e => normalize(e.dataset.search));
  let category = 'all';
  const update = () => {
    const words = normalize(query.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    entries.forEach((entry,i) => {
      const matches = (category === 'all' || entry.dataset.category.split(' ').includes(category)) && words.every(w => index[i].includes(w));
      entry.hidden = !matches;
      if (matches) count++;
    });
    sections.forEach(section => { section.hidden = ![...section.querySelectorAll('.lexicon-entry')].some(e => !e.hidden); });
    filters.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.category === category)));
    clear.hidden = !query.value;
    lexicon.querySelector('.lexicon-empty').hidden = count !== 0;
    document.getElementById('lexicon-results').textContent = words.length || category !== 'all' ? `${count} ${count === 1 ? 'passender Artikel' : 'passende Artikel'}` : 'Alle 14 Artikel';
  };
  lexicon.querySelector('.lexicon-search').hidden = false;
  lexicon.querySelector('.lexicon-filters').hidden = false;
  query.addEventListener('input',update);
  clear.addEventListener('click',()=>{query.value='';update();query.focus();});
  filters.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.category;update();}));
  document.getElementById('lexicon-reset').addEventListener('click',()=>{category='all';query.value='';update();query.focus();});
})();
