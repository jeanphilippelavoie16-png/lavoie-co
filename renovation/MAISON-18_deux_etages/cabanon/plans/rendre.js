#!/usr/bin/env node
// Rend les feuilles du cabanon avec Edge sans fenêtre : png/A1..A6.png et PLANS_cabanon.pdf.
//   python plans_cabanon.py && node rendre.js
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { pathToFileURL } = require('url');

const ICI = __dirname;
const EDGE = ['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'].find(p => fs.existsSync(p));
if (!EDGE) { console.error('ni Edge ni Chrome'); process.exit(3); }

const dormir = ms => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

function edge(args, sortie) {
  const profil = fs.mkdtempSync(path.join(os.tmpdir(), 'rendu-cabanon-'));
  if (fs.existsSync(sortie)) fs.unlinkSync(sortie);
  try {
    execFileSync(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars',
      '--no-default-browser-check', `--user-data-dir=${profil}`, ...args], { stdio: 'ignore', timeout: 120000 });
  } catch (e) { /* le lanceur peut sortir en erreur alors que le rendu se fait */ }
  let ok = false;
  for (let t = 0; t < 80 && !ok; t++) {
    if (fs.existsSync(sortie) && fs.statSync(sortie).size > 0) {
      const a = fs.statSync(sortie).size; dormir(400);
      ok = fs.statSync(sortie).size === a;
    } else dormir(500);
  }
  try { fs.rmSync(profil, { recursive: true, force: true }); } catch (e) {}
  if (!ok) { console.error('rien produit : ' + sortie); process.exit(4); }
  console.log(sortie);
}

fs.mkdirSync(path.join(ICI, 'png'), { recursive: true });
const seules = process.argv.slice(2);
for (const f of fs.readdirSync(path.join(ICI, 'svg')).filter(f => f.endsWith('.svg')).sort()) {
  if (seules.length && !seules.includes(path.basename(f, '.svg'))) continue;
  edge(['--force-device-scale-factor=1.5', '--window-size=1632,1056',
    `--screenshot=${path.join(ICI, 'png', f.replace('.svg', '.png'))}`,
    pathToFileURL(path.join(ICI, 'svg', f)).href], path.join(ICI, 'png', f.replace('.svg', '.png')));
}
if (!seules.length) {
  edge(['--no-pdf-header-footer', `--print-to-pdf=${path.join(ICI, 'PLANS_cabanon.pdf')}`,
    pathToFileURL(path.join(ICI, 'plans.html')).href], path.join(ICI, 'PLANS_cabanon.pdf'));
}
