// Run AFTER the searches, via javascript_tool, then call get_page_text on the same tab.
// Edit the four filter lines first. Write them from this search's ICP (Process step 3b)
// and copy them into the Sourcing Plan's "Filter used" section.
//
// SIGNAL:  the specialty. A headline must contain one of these to be kept.
// ROLE:    the job family. A headline must also contain one of these.
// EXCLUDE: look-alikes that match SIGNAL and ROLE but are the wrong job.
// BROAD:   queries run as last resort. Names found only there are reported separately.
//
// Example (enterprise account executive search):
//   SIGNAL  = /(enterprise|strategic|named accounts|fortune 500|global accounts)/i
//   ROLE    = /(account executive|\bAE\b|sales director|account director)/i
//   EXCLUDE = /(recruit|SDR|BDR|customer success|sales engineer)/i
//   BROAD   = ['account executive', 'B2B sales']
// Example (generative audio ML scientist search):
//   SIGNAL  = /(audio|music|speech|voice|TTS|DSP|sound|MIR)/i
//   ROLE    = /(research|scientist|machine learning|\bML\b|deep learning|diffusion|model|PhD)/i
//   EXCLUDE = /(recruit|sales|designer|product manager)/i
//   BROAD   = ['music generation', 'generative AI']
const SIGNAL = /REPLACE_ME/i;
const ROLE = /REPLACE_ME/i;
const EXCLUDE = /$^/;
const BROAD = [];

const rows = JSON.parse(localStorage.getItem('tia_rows') || '[]');
const people = {};
const perQuery = {};
for (const x of rows) {
  const q = (x.q || '').replace(/"/g, '');
  perQuery[q] = perQuery[q] || { read: 0, pages: new Set(), newKept: 0 };
  perQuery[q].read++;
  perQuery[q].pages.add(x.p);
  if (/^LinkedIn Member$/.test(x.n)) continue;
  people[x.n] = people[x.n] || { h: x.h, l: x.l, q: [] };
  if (!people[x.n].q.includes(q)) people[x.n].q.push(q);
}
const kept = n => SIGNAL.test(people[n].h) && ROLE.test(people[n].h) && !EXCLUDE.test(people[n].h);
const seen = new Set();
for (const x of rows) {
  const q = (x.q || '').replace(/"/g, '');
  if (people[x.n] && kept(x.n) && !seen.has(x.n)) { seen.add(x.n); perQuery[q].newKept++; }
}
const line = (n, v) => `${n} ~ ${v.h.slice(0, 150)} ~ ${v.l.replace(', United States', '')} ~ ${v.q.length}q: ${v.q.join(' / ')}`;
const K = [], KB = [], R = [];
for (const [n, v] of Object.entries(people)) {
  const onlyBroad = v.q.every(q => BROAD.includes(q));
  if (kept(n)) (onlyBroad ? KB : K).push(line(n, v));
  else if (v.q.length >= 2) R.push(line(n, v));
}
const qTable = Object.entries(perQuery)
  .map(([q, s]) => `${q} | pages ${s.pages.size} | read ${s.read} | new kept ${s.newKept}`).join('\n');
document.querySelector('main').innerText =
  `ROWS ${rows.length} | UNIQUE PEOPLE ${Object.keys(people).length} | KEPT ${K.length + KB.length} | RECURRING, NO HEADLINE SIGNAL ${R.length}\n` +
  `=== PER QUERY\n${qTable}\n` +
  `=== KEPT (headline signal)\n${K.join('\n')}\n` +
  `=== KEPT, BROAD QUERIES ONLY\n${KB.join('\n')}\n` +
  `=== RECURRING ACROSS 2+ QUERIES, NO HEADLINE SIGNAL (check profile)\n${R.join('\n')}`;
'report written to page; now run get_page_text';
