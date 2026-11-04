import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { sha256 } from './rom.mjs';

export async function verifyAuraV3(root, sourceHash) {
  const json = async path => JSON.parse(await readFile(resolve(root, path), 'utf8'));
  const hex = async path => Buffer.from((await readFile(resolve(root, path), 'utf8')).replace(/\s/g, ''), 'hex');
  const m = await json('patches/auras-c2-v3/manifest.json');
  assert.equal(m.source.sha256, sourceHash);
  assert.equal(sha256(await readFile(resolve(root, m.patch.path))), m.patch.sha256);
  assert.equal(sha256(await hex(m.code.assemblyHex)), m.code.assembled_sha256);
  const tiles = await hex(m.tiles.hex), maps = await hex(m.maps.hex), target = await hex(m.flame.indexedHex);
  assert.equal(tiles.length, 64 * 32);
  assert.equal(sha256(tiles), m.tiles.sha256);
  assert.equal(sha256(maps), m.maps.sha256);
  assert.equal(target.length, 80 * 128);
  assert.equal(m.maps.pointers.length, 384);
  const entries = new Map(m.maps.storage.map(entry => [entry.address.toLowerCase(), entry]));
  const logical = tile => {
    assert(tile >= 0x513 && tile < 0x554 && tile !== 0x540, 'Un sprite del aura pisa el tile de desplazamiento o sale del atlas');
    return tile - 0x513 - (tile > 0x540 ? 1 : 0);
  };
  for (const pointer of m.maps.pointers) {
    const entry = entries.get(pointer.toLowerCase());
    assert(entry, pointer);
    const count = maps.readUInt16BE(entry.offset), rendered = Buffer.alloc(80 * 128);
    assert.equal(entry.bytes, 2 + count * 6);
    assert(count > 0 && count <= 46);
    for (let i = count - 1; i >= 0; i--) {
      const at = entry.offset + 2 + i * 6, attr = maps.readUInt16BE(at), packed = maps[at + 4], size = maps[at + 5];
      let x = ((packed & 15) << 8) | maps[at + 2], y = ((packed >> 4) << 8) | maps[at + 3];
      if (x & 0x800) x -= 0x1000;
      if (y & 0x800) y -= 0x1000;
      const w = ((size >> 2) & 3) + 1, h = (size & 3) + 1, first = attr & 0x7ff;
      const firstLogical = logical(first);
      for (let t = 0; t < w * h; t++) logical(first + t);
      if (firstLogical >= m.flame.tiles) continue;
      for (let py = 0; py < h * 8; py++) for (let px = 0; px < w * 8; px++) {
        const sx = attr & 0x800 ? w * 8 - 1 - px : px, sy = attr & 0x1000 ? h * 8 - 1 - py : py;
        const tile = logical(first + (sx >> 3) * h + (sy >> 3));
        const byte = tiles[tile * 32 + (sy & 7) * 4 + ((sx & 7) >> 1)], value = (byte >> (sx & 1 ? 0 : 4)) & 15;
        const dx = x + 40 + px, dy = y + 120 + py;
        assert(dx >= 0 && dx < 80 && dy >= 0 && dy < 128);
        if (value) rendered[dy * 80 + dx] = value;
      }
    }
    assert.deepEqual(rendered, target, `El mapa ${pointer} cambia el contorno o introduce huecos`);
  }
  const v = await json('evidence/auras-c2-v3/validation.json'), q = await json('evidence/auras-c2-v3/runtime-qa.json');
  assert.equal(v.target_sha256, m.target.sha256);
  assert.equal(q.sha256, m.target.sha256);
  assert.equal(q.capacity.over_limit_frames, 0);
  assert.equal(v.characters.length, 11);
  assert.deepEqual(v.characters.filter(item => item.lightning).map(item => item.character_id), [1, 5]);
  assert(v.graphics_budgets.every(item => item.sprites <= 80 && item.scanline <= 20 && item.pixels <= 320));
  for (const item of v.characters) {
    assert(item.exit_completed && item.movement_after_release && item.scratch_magic_stable);
    assert.equal(sha256(await readFile(resolve(root, 'assets/media/auras-c2-v3', item.video))), item.sha256);
  }
}
