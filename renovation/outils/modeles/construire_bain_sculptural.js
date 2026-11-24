// Bain autoportant sculptural (pierre de résine mate), 66 x 32 x 23 po, géométrie procédurale three.js r149 -> GLB.
// Coque d'un seul tenant : superellipse décalée vers l'intérieur selon un profil (dx, dy, z) ; fond plat, drain central.
// node construire_bain_sculptural.js sortie.glb
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader'] }); const p = await b.newPage();
  p.on('console', m => console.log('page:', m.text()));
  await p.setContent(`<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three'; import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
const PO = 0.0254, A = 33, B = 16, N = 2.7, SEG = 160;
const lin = c => new THREE.Color(c).convertSRGBToLinear();
const resine = new THREE.MeshStandardMaterial({ name: 'pierre_resine_blanche', color: lin('#f2f0eb'), roughness: 0.42 });
const chrome = new THREE.MeshStandardMaterial({ name: 'noir_mat', color: lin('#1c1c1c'), roughness: 0.45, metalness: 0.6 });
// profil (dx, dy, z) du dessous extérieur jusqu'au fond intérieur
const P = [[2.2,2.2,0],[2.2,2.2,0.8],[1.5,1.5,1.3],[1.0,1.0,3.0],[0.45,0.45,9],[0.12,0.12,15],[0,0,19.5],[0,0,21.9],
  [0.1,0.1,22.55],[0.45,0.45,22.95],[0.95,0.95,23.1],[1.45,1.45,22.95],[1.8,1.8,22.55],[1.95,1.95,21.9],
  [2.3,2.1,19.5],[3.6,2.5,16],[6.0,3.2,12.5],[9.5,4.2,9.2],[13.0,5.4,6.6],[16.0,6.6,4.8],[18.4,7.5,3.9],[20.2,8.1,3.55],[21.5,8.5,3.5]];
function pt(t, a, b) { const c = Math.cos(t), s = Math.sin(t);
  return [a * Math.sign(c) * Math.pow(Math.abs(c), 2 / N), b * Math.sign(s) * Math.pow(Math.abs(s), 2 / N)]; }
// paramètre t réparti selon la longueur d'arc du contour extérieur (points réguliers)
const ts = (() => { const M = 4000, L = [0]; let prev = pt(0, A, B);
  for (let i = 1; i <= M; i++) { const q = pt(i / M * 2 * Math.PI, A, B); L.push(L[i - 1] + Math.hypot(q[0] - prev[0], q[1] - prev[1])); prev = q; }
  const out = []; let j = 0; for (let k = 0; k < SEG; k++) { const target = k / SEG * L[M]; while (L[j] < target) j++; out.push(j / M * 2 * Math.PI); } return out; })();
const pos = [], idx = [];
for (const [dx, dy, z] of P) for (const t of ts) { const [x, y] = pt(t, A - dx, B - dy); pos.push(x * PO, z * PO, y * PO); }
for (let r = 0; r < P.length - 1; r++) for (let k = 0; k < SEG; k++) {
  const a = r * SEG + k, b2 = r * SEG + (k + 1) % SEG, c = (r + 1) * SEG + k, d = (r + 1) * SEG + (k + 1) % SEG;
  idx.push(a, c, b2, b2, c, d); }
// fonds : dessous (z = 0) et fond intérieur
const base = pos.length / 3; pos.push(0, 0, 0);
for (let k = 0; k < SEG; k++) idx.push(base, k, (k + 1) % SEG);
const fond = pos.length / 3, last = (P.length - 1) * SEG; pos.push(0, P[P.length - 1][2] * PO, 0);
for (let k = 0; k < SEG; k++) idx.push(fond, (k + 1) % SEG + last, k + last);
const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx);
g.computeVertexNormals();
const coque = new THREE.Mesh(g, resine); coque.name = 'coque';
const drain = new THREE.Mesh(new THREE.CylinderGeometry(1.3 * PO, 1.3 * PO, 0.12 * PO, 40), chrome); drain.name = 'drain';
drain.position.set(0, 3.56 * PO, 0);
const trop = new THREE.Mesh(new THREE.CylinderGeometry(0.9 * PO, 0.9 * PO, 0.15 * PO, 32), chrome); trop.name = 'trop_plein';
trop.rotation.z = Math.PI / 2; trop.position.set(-(A - 3.2) * PO, 17.5 * PO, 0);
const grp = new THREE.Group(); grp.name = 'bain_sculptural'; grp.add(coque, drain);
const sc = new THREE.Scene(); sc.add(grp);
new GLTFExporter().parse(sc, r => { let s = ''; const u = new Uint8Array(r); for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); window.R = btoa(s); }, e => { window.R = 'ERR' + e; }, { binary: true });
</script>`);
  await p.waitForFunction(() => window.R, null, { timeout: 120000 });
  fs.writeFileSync(out, Buffer.from(await p.evaluate(() => window.R), 'base64')); console.log('ok', fs.statSync(out).size); await b.close();
})();
