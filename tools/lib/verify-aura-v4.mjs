import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { sha256 } from './rom.mjs';

export async function verifyAuraV4(root, sourceHash) {
  const json = async p => JSON.parse(await readFile(resolve(root, p), 'utf8'));
  const hex = async p => Buffer.from((await readFile(resolve(root, p), 'utf8')).replace(/\s/g, ''), 'hex');
  const m = await json('patches/auras-c2-v4/manifest.json');
  assert.equal(m.source.sha256, sourceHash);
  assert.equal(m.target.bytes, 4 * 1024 * 1024);
  assert.deepEqual(m.lightningCharacterIds, []);
  assert.equal(sha256(await readFile(resolve(root, m.patch.path))), m.patch.sha256);
  const code = await hex(m.code.assemblyHex);
  assert.equal(code.length, m.code.bytes);
  assert.equal(sha256(code), m.code.sha256);
  const r = await json(m.resources), memory = Buffer.alloc(0x300000, 255);
  for (const op of r.operations) Buffer.from(op.data, 'hex').copy(memory, op.address);
  assert.equal(r.physical_tiles.length, 113);
  assert.equal(new Set(r.physical_tiles).size, 113);
  assert(!r.physical_tiles.includes(0x540));
  const physical = new Map(r.physical_tiles.map((tile, i) => [tile, i]));
  const tableOffset = Number(m.code.mapTable) - Number(m.code.base);
  for (let i = 0; i < 768; i++) assert.equal(code.readUInt32BE(tableOffset + i * 4), r.map_pointers[i]);
  const decode = address => {
    const size = memory.readUInt16LE(address) + 1, result = []; address += 2;
    while (result.length < size) {
      const flags = memory[address++];
      for (let bit = 0; bit < 8 && result.length < size; bit++) {
        assert(flags & (1 << bit), 'Un recurso generado deja de usar el formato literal esperado');
        result.push(memory[address++]);
      }
    }
    return Buffer.from(result);
  };
  const acceptedTiles = (await hex('src/auras/c2-v3/tiles.hex')).subarray(0, 55 * 32);
  const acceptedPixels = await hex('src/auras/c2-v3/flame-indexed.hex');
  const signed12 = v => v & 0x800 ? v - 4096 : v;
  for (let cid = 0; cid < 11; cid++) {
    const style = r.styles[cid], roles = style.roles;
    const expected = Buffer.from(acceptedTiles);
    for (let i = 0; i < expected.length; i++) expected[i] = ((roles[acceptedTiles[i] >> 4] ?? (acceptedTiles[i] >> 4)) << 4) | (roles[acceptedTiles[i] & 15] ?? (acceptedTiles[i] & 15));
    for (let player = 0; player < 2; player++) {
      const at = (player ? 0x280100 + cid * 12 : 0x280000 + cid * 8);
      const atlas = Buffer.concat(Array.from({ length: player ? 3 : 2 }, (_, i) => decode(memory.readUInt32BE(at + i * 4))));
      assert.deepEqual(atlas, expected, `Atlas de color CID${cid}, P${player + 1}`);
      const context = player * 2 + (style.palette === 'actor' ? 1 : 0);
      const pointers = new Set(r.map_pointers.slice(context * 192, context * 192 + 192));
      for (const pointer of pointers) {
        const pixels = Buffer.alloc(80 * 128), count = memory.readUInt16BE(pointer);
        assert(count > 0 && count <= 48);
        for (let j = count - 1; j >= 0; j--) {
          const q = pointer + 2 + j * 6, attr = memory.readUInt16BE(q), tile = attr & 2047;
          const start = physical.get(tile); assert(start !== undefined);
          if (start >= 110) { assert.equal((attr >> 13) & 3, 3); continue; }
          assert.equal((attr >> 13) & 3, style.palette === 'actor' ? player : 3);
          const x = signed12(((memory[q + 4] & 15) << 8) | memory[q + 2]) + 40;
          const y = signed12(((memory[q + 4] >> 4) << 8) | memory[q + 3]) + 120;
          const w = (((memory[q + 5] >> 2) & 3) + 1) * 8, h = ((memory[q + 5] & 3) + 1) * 8;
          for (let dy = 0; dy < h; dy++) for (let dx = 0; dx < w; dx++) {
            const sx = attr & 0x800 ? w - dx - 1 : dx, sy = attr & 0x1000 ? h - dy - 1 : dy;
            const logical = physical.get(tile + Math.floor(sx / 8) * (h / 8) + Math.floor(sy / 8));
            assert(logical >= player * 55 && logical < player * 55 + 55);
            const byte = atlas[(logical - player * 55) * 32 + (sy % 8) * 4 + Math.floor((sx % 8) / 2)];
            const value = (byte >> (sx % 2 ? 0 : 4)) & 15;
            if (value) { assert(x + dx >= 0 && x + dx < 80 && y + dy >= 0 && y + dy < 128); pixels[(y + dy) * 80 + x + dx] = value; }
          }
        }
        const expectedPixels = Buffer.from(acceptedPixels.map(v => v ? roles[v] : 0));
        assert.deepEqual(pixels, expectedPixels, `Contorno, sin rayos, CID${cid}, P${player + 1}`);
      }
    }
  }
  const mirrorAt = 0x280100 + 11 * 12;
  const mirrorAtlas = Buffer.concat(Array.from({ length: 3 }, (_, i) => decode(memory.readUInt32BE(mirrorAt + i * 4))));
  const mirrorRoles = { 7: 15, 11: 14, 8: 11 };
  const mirrorExpected = Buffer.from(acceptedTiles.map(v => ((mirrorRoles[v >> 4] ?? (v >> 4)) << 4) | (mirrorRoles[v & 15] ?? (v & 15))));
  assert.deepEqual(mirrorAtlas, mirrorExpected, 'Atlas de Recoome P2 alternativo');
  const v = await json('evidence/auras-c2-v4/validation.json');
  assert.equal(v.target_sha256, m.target.sha256);
  assert.equal(v.characters.length, 11);
  for (const entry of v.characters) {
    assert.equal(entry.lightning, false);
    for (const [file, hash] of [[entry.comparison_video, entry.comparison_sha256], [entry.new_only_video, entry.new_only_sha256], [entry.screenshot, entry.screenshot_sha256]]) assert.equal(sha256(await readFile(resolve(root, 'assets/media/ki-colores-v4', file))), hash);
    assert(entry.all_palette_and_atlas_samples_exact && entry.graphics_budgets.sprites <= 80 && entry.graphics_budgets.scanline_sprites <= 20 && entry.graphics_budgets.scanline_pixels <= 320);
  }
  const body = await json('evidence/auras-c2-v4/character-runtime.json');
  assert.equal(body.romSha256, m.target.sha256);
  assert(body.cases.every(c => c.mismatchCount === 0));
  const mixed = await json('evidence/auras-c2-v4/mixed-runtime.json');
  assert.equal(mixed.sha256, m.target.sha256);
  assert(mixed.normal_results.all113atlas_tiles_exact_in_all_samples && mixed.normal_results.max_frame_sprites <= 80 && mixed.normal_results.max_scanline_sprites <= 20 && mixed.normal_results.air_dust_max === 0);
}
