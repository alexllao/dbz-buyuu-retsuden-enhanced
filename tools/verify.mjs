import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, resolve, relative, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { sha256 } from './lib/rom.mjs';
import { verifyAuraV3 } from './lib/verify-aura-v3.mjs';
import { verifyAuraV4 } from './lib/verify-aura-v4.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const json = async path => JSON.parse(await readFile(resolve(root, path), 'utf8'));
const intro62 = await json('patches/review-v6-2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, intro62.patch.path))), intro62.patch.sha256);
const intro62Evidence = await json('evidence/intro-v2/combined-validation.json');
assert.equal(intro62Evidence.targetSha256, intro62.target.sha256);
assert(Object.values(intro62Evidence.checks).every(value => value === true));
const asm62 = await json('research/disassembly-es/mapa-mod-v6-2.json');
assert.equal(asm62.sha256, intro62.target.sha256);
const manifest = await json('patches/gameplay-v1/manifest.json');
for (const patch of Object.values(manifest.patches)) assert.equal(sha256(await readFile(resolve(root, patch.path))), patch.sha256, patch.path);
const hex = (await readFile(resolve(root, 'src/gameplay/v1/controls.hex'), 'utf8')).replace(/\s/g, '');
assert.match(hex, /^(?:[0-9a-f]{2})+$/);
const code = Buffer.from(hex, 'hex');
assert.equal(code.length, manifest.assembly.bytes);
assert.equal(sha256(code), manifest.assembly.sha256);
const graphics = await json('project/graphics.json');
const images = graphics.categories.flatMap(category => category.items);
assert.equal(images.length, 71);
assert.equal(images.length, graphics.imageCount);
assert.equal(new Set(images.map(item => item.path)).size, images.length);
for (const item of images) {
  assert(!item.path.includes('..') && !item.path.includes('\\'));
  assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256, item.path);
}
const decisions = await json('project/decisions.json');
assert.equal(decisions.presentation.selected, 'G');
assert.equal(decisions.presentation.modCredit.text, '- 2026 ALEX LLAO');
assert.equal(decisions.presentation.modCredit.usePseudonym, false);
assert.equal(decisions.preservePreviousVersions, true);
assert.deepEqual(decisions.auras.lightningAllowedOnly, []);
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
const aura = await json('patches/auras-c2-v1/manifest.json');
assert.equal(aura.source.sha256, manifest.source.sha256);
assert.equal(sha256(await readFile(resolve(root, aura.patch.path))), aura.patch.sha256);
const readHex = async path => Buffer.from((await readFile(resolve(root, path), 'utf8')).replace(/\s/g, ''), 'hex');
assert.equal(sha256(await readHex(aura.code.assemblyHex)), aura.code.assembled_sha256);
assert.equal((await readHex(aura.tiles.hex)).length, 45 * 32);
const auraMaps = await readHex(aura.maps.hex);
assert.equal(aura.maps.addresses.length, 16);
for (const address of aura.maps.addresses) {
  const offset = Number(address) - Number(aura.maps.base);
  const count = auraMaps.readUInt16BE(offset);
  assert(count > 0 && count <= 34);
  for (let i = 0; i < count; i++) {
    const at = offset + 2 + i * 6;
    const tile = auraMaps.readUInt16BE(at) & 0x7ff;
    const size = auraMaps[at + 5];
    const tiles = (((size >> 2) & 3) + 1) * ((size & 3) + 1);
    assert(tile >= 0x513 && tile + tiles <= 0x540, 'Aura fuera del espacio de VRAM reservado');
  }
}
const auraValidation = await json('evidence/auras-c2-v1/validation.json');
assert.equal(auraValidation.target_sha256, aura.target.sha256);
assert.equal(auraValidation.characters.length, 11);
assert.deepEqual(auraValidation.characters.filter(item => item.lightning).map(item => item.character_id), [1, 5]);
for (const item of auraValidation.characters) {
  assert(item.exit_completed && item.movement_after_release && item.scratch_magic_stable);
  assert.equal(sha256(await readFile(resolve(root, 'assets/media/auras-c2-v1', item.video))), item.sha256);
}
const auraQa = await json('evidence/auras-c2-v1/runtime-qa.json');
assert.equal(auraQa.prototype_sha256, aura.target.sha256);
assert.equal(auraQa.frames_with_aura_when_both_phase_zero.length, 0);
assert.equal(auraQa.native118_11f_match_all_frames, true);
const aura2 = await json('patches/auras-c2-v2/manifest.json');
assert.equal(aura2.source.sha256, manifest.source.sha256);
assert.equal(sha256(await readFile(resolve(root, aura2.patch.path))), aura2.patch.sha256);
assert.equal(sha256(await readHex(aura2.code.assemblyHex)), aura2.code.assembled_sha256);
const tiles2 = await readHex(aura2.tiles.hex);
assert.equal(tiles2.length, 45 * 32);
assert.equal(sha256(tiles2), aura2.tiles.sha256);
const maps2 = await readHex(aura2.maps.hex);
assert.equal(sha256(maps2), aura2.maps.sha256);
assert.equal(aura2.maps.storage.length, 128);
for (const entry of aura2.maps.storage) {
  const count = maps2.readUInt16BE(entry.offset);
  assert(count > 0 && count <= 50);
  assert.equal(entry.bytes, 2 + count * 6);
  for (let i = 0; i < count; i++) {
    const at = entry.offset + 2 + i * 6;
    const tile = maps2.readUInt16BE(at) & 0x7ff, size = maps2[at + 5];
    assert(tile >= 0x513 && tile + (((size >> 2) & 3) + 1) * ((size & 3) + 1) <= 0x540);
  }
}
const validation2 = await json('evidence/auras-c2-v2/validation.json');
assert.equal(validation2.target_sha256, aura2.target.sha256);
assert.deepEqual(validation2.flame_sizes.c2_v2, [80, 128]);
assert.equal(validation2.characters.length, 11);
assert.deepEqual(validation2.characters.filter(item => item.lightning).map(item => item.character_id), [1, 5]);
for (const item of validation2.characters) {
  assert(item.exit_completed && item.movement_after_release && item.scratch_magic_stable);
  assert.equal(sha256(await readFile(resolve(root, 'assets/media/auras-c2-v2', item.video))), item.sha256);
}
assert.equal(validation2.graphics_budgets.length, 11);
assert(validation2.graphics_budgets.every(item => item.sprites <= 80 && item.scanline <= 20 && item.pixels <= 320));
const qa2 = await json('evidence/auras-c2-v2/runtime-qa.json');
assert.equal(qa2.sha256, aura2.target.sha256);
assert.equal(qa2.tested.natural_collisions, 6);
assert.equal(qa2.tested.residual_sprites_when_both_phases_zero, 0);
assert(qa2.capacity.tested_max_sprites_per_frame <= 80);
assert(qa2.capacity.tested_max_scanline_sprites <= 20);
assert(qa2.capacity.tested_max_scanline_width_pixels <= 320);
await verifyAuraV3(root, manifest.source.sha256);
await verifyAuraV4(root, manifest.source.sha256);
const noRays = await json('patches/auras-c2-v3-no-rays/manifest.json');
assert.equal(noRays.source.sha256, manifest.source.sha256);
assert.equal(sha256(await readFile(resolve(root, noRays.patch.path))), noRays.patch.sha256);
assert.deepEqual(noRays.lightningCharacterIds, []);
const noRaysTable = await readHex(noRays.mapTable.hex);
assert.equal(noRaysTable.length, 384 * 4);
const v3 = await json('patches/auras-c2-v3/manifest.json');
const v3maps = await readHex(v3.maps.hex);
for (let i = 0; i < 384; i++) {
  const plain = i - (i % 8 >= 4 ? 4 : 0);
  assert.equal(noRaysTable.readUInt32BE(i * 4), Number(v3.maps.pointers[plain]));
  const entry = v3.maps.storage.find(e => Number(e.address) === noRaysTable.readUInt32BE(i * 4));
  assert(entry);
  const count = v3maps.readUInt16BE(entry.offset);
  for (let j = 0; j < count; j++) {
    const tile = v3maps.readUInt16BE(entry.offset + 2 + j * 6) & 0x7ff;
    assert(tile < 0x54b || tile > 0x550, 'Un mapa alcanzable conserva rayos');
  }
}

const reviewV2 = await json('patches/review-v2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, reviewV2.patch.path))), reviewV2.patch.sha256);
const reviewCode = await readHex(reviewV2.assembly.path);
assert.equal(reviewCode.length, reviewV2.assembly.bytes);
assert.equal(sha256(reviewCode), reviewV2.assembly.sha256);
const reviewMatrix = await json('evidence/gameplay-v2/movement-matrix.json');
assert.equal(reviewMatrix.length, 22);
assert(reviewMatrix.every(item => item.passed && Object.values(item.checks).every(Boolean)));
for (const name of ['final-p1', 'final-p2-turbo']) {
  assert.equal((await json(`evidence/gameplay-v2/${name}.json`)).rom, reviewV2.target.sha256);
}

const reviewV3 = await json('patches/review-v3/manifest.json');
assert.equal(sha256(await readFile(resolve(root, reviewV3.patch.path))), reviewV3.patch.sha256);
for (const entry of Object.values(reviewV3.code)) {
  const bytes = await readHex(entry.path);
  assert.equal(bytes.length, entry.bytes);
  assert.equal(sha256(bytes), entry.sha256);
}
const sideMatrix = await json('evidence/side-switch/matrix.json');
assert.equal(sideMatrix.romSha256, reviewV3.target.sha256);
assert.equal(sideMatrix.jobs, 22);
assert.equal(sideMatrix.cases, 374);
assert(sideMatrix.passed && sideMatrix.failures.length === 0);
assert(sideMatrix.results.every(job => job.cases.every(item => item.passed && Object.values(item.checks).every(Boolean))));
const sideStatic = await json('evidence/side-switch/static-verification.json');
assert.equal(sideStatic.targetSha256, reviewV3.target.sha256);
assert(sideStatic.onlyAllowedRangesChanged && Object.values(sideStatic.preserved).every(item => item.unchanged));

const introReview = await json('patches/review-v6-1/manifest.json');
assert.equal(introReview.baseReviewSha256, reviewV3.target.sha256);
assert.equal(sha256(await readFile(resolve(root, introReview.patch.path))), introReview.patch.sha256);
const introValidation = await json('evidence/intro-v1/validation.json');
assert.equal(introValidation.targetSha256, introReview.target.sha256);
assert(Object.values(introValidation.checks).every(Boolean));
for (const capture of introValidation.captures) {
  assert.equal(sha256(await readFile(resolve(root, capture.path))), capture.sha256);
}

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
console.log(`Verificado: ${images.length} imágenes, decisión G, ${matrix.length} combinaciones históricas, parches, código y enlaces locales (${files.length} archivos).`);
