// Run ONCE per search, on any linkedin.com page, via javascript_tool.
// Stores the page extractor in localStorage and clears any previous results.
// After this, on each search results page run:
//   await (new Function(localStorage.getItem('tia_fn')))()
// It waits for results to render, saves name / headline / location / query / page
// for every result on the page, and returns a one-line count. Results persist
// across page navigations, so nothing large ever comes back through the tool
// (tool output is truncated at roughly 1,000 characters).
const tiaExtract = async () => {
  const main = () => document.querySelector('main')?.innerText || '';
  for (let k = 0; k < 25 && !/•\s*(1st|2nd|3rd)/.test(main()); k++) await new Promise(r => setTimeout(r, 300));
  await new Promise(r => setTimeout(r, 600));
  const q = new URLSearchParams(location.search);
  const L = main().split('\n').map(s => s.trim()).filter(Boolean);
  const rows = [];
  for (let i = 1; i < L.length - 2; i++) {
    if (/^•\s*(1st|2nd|3rd\+?)$/.test(L[i])) {
      rows.push({ n: L[i - 1], h: L[i + 1], l: L[i + 2], q: q.get('keywords'), p: q.get('page') || '1' });
    }
  }
  const all = JSON.parse(localStorage.getItem('tia_rows') || '[]');
  const seen = new Set(all.map(x => x.q + x.p + x.n));
  localStorage.setItem('tia_rows', JSON.stringify(all.concat(rows.filter(x => !seen.has(x.q + x.p + x.n)))));
  const pages = L.filter(s => /^\d+$/.test(s)).map(Number);
  return `${q.get('keywords')} p${q.get('page') || 1}: ${rows.length} (last page shown ${Math.max(0, ...pages)})`;
};
localStorage.setItem('tia_fn', 'return (' + tiaExtract.toString() + ')()');
localStorage.setItem('tia_rows', '[]');
'tia ready';
