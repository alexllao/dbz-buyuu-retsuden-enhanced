import test from 'node:test';
import assert from 'node:assert/strict';
import { applyIps, updateGenesisChecksum } from '../tools/lib/rom.mjs';

const ips = records => Buffer.concat([Buffer.from('PATCH'), ...records, Buffer.from('EOF')]);
test('aplica registros literales y RLE sin modificar la entrada', () => {
  const base = Buffer.from([1, 2, 3, 4]);
  const literal = Buffer.from([0, 0, 1, 0, 2, 8, 9]);
  const rle = Buffer.from([0, 0, 4, 0, 0, 0, 3, 7]);
  assert.deepEqual(applyIps(base, ips([literal, rle])), Buffer.from([1, 8, 9, 4, 7, 7, 7]));
  assert.deepEqual(base, Buffer.from([1, 2, 3, 4]));
});
test('acepta el tamaño final opcional de IPS', () => {
  assert.deepEqual(applyIps(Buffer.from([1, 2, 3]), Buffer.concat([ips([]), Buffer.from([0, 0, 2])])), Buffer.from([1, 2]));
  const expandedThenTruncated = Buffer.concat([ips([Buffer.from([0, 0, 10, 0, 1, 99])]), Buffer.from([0, 0, 2])]);
  assert.deepEqual(applyIps(Buffer.from([1, 2, 3]), expandedThenTruncated), Buffer.from([1, 2]));
});
test('rechaza cabeceras, registros truncados, RLE vacío y datos tras EOF', () => {
  for (const patch of [Buffer.from('WRONGEOF'), Buffer.from('PATCH'), Buffer.concat([Buffer.from('PATCH'), Buffer.from([0, 0, 1, 0, 2, 7])]), ips([Buffer.from([0, 0, 0, 0, 0, 0, 0, 1])]), Buffer.from('PATCHEOFextra')]) assert.throws(() => applyIps(Buffer.alloc(4), patch));
});
test('limita expansiones de salida', () => {
  assert.throws(() => applyIps(Buffer.alloc(4), ips([Buffer.from([0, 0, 10, 0, 1, 255])]), { maxSize: 8 }));
});
test('el checksum suma las palabras del cuerpo y no incluye la cabecera', () => {
  const rom = Buffer.alloc(0x206);
  rom.writeUInt16BE(0xffff, 0x200);
  rom.writeUInt16BE(2, 0x202);
  rom.writeUInt16BE(3, 0x204);
  rom.writeUInt16BE(123, 0x18e);
  const result = updateGenesisChecksum(rom);
  assert.equal(result.readUInt16BE(0x18e), 4);
  assert.equal(rom.readUInt16BE(0x18e), 123);
  assert.throws(() => updateGenesisChecksum(Buffer.alloc(3)));
  assert.throws(() => updateGenesisChecksum(Buffer.alloc(0x201)));
});
