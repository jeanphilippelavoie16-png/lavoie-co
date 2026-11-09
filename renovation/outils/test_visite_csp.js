// Test : rend la visite sous une CSP proche de celle des artifacts publiés (fetch bloqué, pas de WebAssembly) et compte les modèles 3D chargés.
// node renovation/outils/test_visite_csp.js renovation/<projet>/3d/visite.html capture.png  (Playwright requis)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1180, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.text().slice(0, 160)); });
  const csp = "default-src 'none'; script-src 'unsafe-inline' https://cdn.jsdelivr.net; img-src data: blob:; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; connect-src 'none'";
  const html = `<!doctype html><html><head><meta charset=utf8><meta http-equiv="Content-Security-Policy" content="${csp}"></head><body>` + fs.readFileSync(process.argv[2], 'utf8') + '</body></html>';
  await p.setContent(html, { waitUntil: 'load', timeout: 120000 });
  await p.waitForFunction(() => window.VISITE_PRETE, null, { timeout: 180000 }).catch(() => errs.push('PAS PRÊTE'));
  await p.waitForTimeout(5000);
  const n = await p.evaluate(() => { let k = 0; scene.traverse(o => { if (o.isMesh && o.parent && o.parent.parent && o.parent.parent.type === 'Group' && o.geometry && o.geometry.attributes.position.count > 200) k++; }); return k; }).catch(e => 'erreur ' + e.message);
  await p.evaluate(() => { choisirMode('visite'); joueur.x = 400; joueur.y = 135; joueur.cap = 205 * Math.PI / 180; masquerAstuce(); }).catch(() => {});
  await p.waitForTimeout(1500); await p.screenshot({ path: process.argv[3] || 'csp.png' });
  console.log('meshes lourds', n); console.log('errs', JSON.stringify([...new Set(errs)].slice(0, 6)));
  await b.close();
})();
