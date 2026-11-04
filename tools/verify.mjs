import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, resolve, relative, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { sha256 } from './lib/rom.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const json = async path => JSON.parse(await readFile(resolve(root, path), 'utf8'));
const manifest = await json('patches/gameplay-v1/manifest.json');
for (const patch of Object.values(manifest.patches)) assert.equal(sha256(await readFile(resolve(root, patch.path))), patch.sha256, patch.path);
const hex = (await readFile(resolve(root, 'src/gameplay/v1/controls.hex'), 'utf8')).replace(/\s/g, '');
assert.match(hex, /^(?:[0-9a-f]{2})+$/);
const code = Buffer.from(hex, 'hex');
assert.equal(code.length, manifest.assembly.bytes);
assert.equal(sha256(code), manifest.assembly.sha256);
const graphics = await json('project/graphics.json');
const images = graphics.categories.flatMap(category => category.items);
assert.equal(images.length, 67);
assert.equal(images.length, graphics.imageCount);
assert.equal(new Set(images.map(item => item.path)).size, images.length);
for (const item of images) {
  assert(!item.path.includes('..') && !item.path.includes('\\'));
  assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256, item.path);
}
const decisions = await json('project/decisions.json');
assert.equal(decisions.presentation.selected, 'B');
assert.equal(decisions.preservePreviousVersions, true);
assert.deepEqual(decisions.auras.lightningAllowedOnly, ['Gohan', 'Cell']);
await stat(resolve(root, decisions.presentation.image));
await stat(resolve(root, decisions.auras.image));
const matrix = await json('evidence/gameplay-v1/character-matrix.json');
assert.equal(matrix.length, 22);
assert.equal(new Set(matrix.map(item => `${item.mode}:${item.character_id}`)).size, 22);
assert(matrix.every(item => item.passed && Object.values(item.checks).every(Boolean)));
const summary = await json('evidence/gameplay-v1/summary.json');
assert.equal(summary.romSha256, manifest.targets.gameplay.sha256);
assert.equal(summary.damageMatchesOriginal, true);
assert.equal(summary.queuedHitInterruptions, 15);
async function walk(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (['.git', 'node_modules', '.build', 'build-local', 'dist'].includes(entry.name)) continue;
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else files.push(path);
  }
  return files;
}
const files = await walk(root);
for (const path of files.filter(path => extname(path) === '.md')) {
  const text = await readFile(path, 'utf8');
  for (const match of text.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)) {
    const link = match[1].split('#')[0];
    if (!link || /^(https?:|mailto:)/.test(link)) continue;
    await stat(resolve(dirname(path), decodeURIComponent(link)));
  }
}
let tracked = [];
try { tracked = execFileSync('git', ['ls-files', '-z'], { cwd: root, encoding: 'utf8' }).split('\0').filter(Boolean); }
catch { /* An exported source archive may have no .git metadata. */ }
for (const path of tracked) {
  assert(!/\.(bin|smd|gen|zip|dll|exe|state|srm)$/i.test(path), `Archivo generado/base inesperado en Git: ${path}`);
}
console.log(`Verificado: ${images.length} imágenes, decisión B, ${matrix.length} combinaciones históricas, parches, código y enlaces locales (${files.length} archivos).`);
