import { createHash } from 'node:crypto';

export const sha256 = data => createHash('sha256').update(data).digest('hex');

export function applyIps(input, patch, { maxSize = 32 * 1024 * 1024 } = {}) {
  if (!Buffer.isBuffer(input) || !Buffer.isBuffer(patch)) throw new TypeError('Se esperan buffers.');
  if (patch.subarray(0, 5).toString('ascii') !== 'PATCH') throw new Error('Cabecera IPS inválida.');
  const records = [];
  let cursor = 5;
  let length = input.length;
  const requireBytes = count => {
    if (cursor + count > patch.length) throw new Error('IPS truncado.');
  };
  while (true) {
    requireBytes(3);
    if (patch.subarray(cursor, cursor + 3).toString('ascii') === 'EOF') {
      cursor += 3;
      const trailing = patch.length - cursor;
      if (trailing !== 0 && trailing !== 3) throw new Error('Datos inesperados después de EOF.');
      if (trailing === 3) length = patch.readUIntBE(cursor, 3);
      break;
    }
    requireBytes(5);
    const offset = patch.readUIntBE(cursor, 3);
    const size = patch.readUInt16BE(cursor + 3);
    cursor += 5;
    let data;
    if (size === 0) {
      requireBytes(3);
      const count = patch.readUInt16BE(cursor);
      if (count === 0) throw new Error('Registro RLE vacío.');
      data = Buffer.alloc(count, patch[cursor + 2]);
      cursor += 3;
    } else {
      requireBytes(size);
      data = patch.subarray(cursor, cursor + size);
      cursor += size;
    }
    if (offset + data.length > maxSize) throw new Error('IPS supera el tamaño máximo.');
    length = Math.max(length, offset + data.length);
    records.push({ offset, data });
  }
  if (length > maxSize) throw new Error('Salida IPS demasiado grande.');
  const result = Buffer.alloc(length);
  input.copy(result);
  for (const { offset, data } of records) if (offset < result.length) data.copy(result, offset);
  return result;
}

export function updateGenesisChecksum(input) {
  if (input.length < 0x200 || input.length % 2 !== 0) throw new Error('Tamaño de ROM inválido para el checksum.');
  const result = Buffer.from(input);
  let checksum = 0;
  for (let index = 0x200; index < result.length; index += 2) checksum = (checksum + result.readUInt16BE(index)) & 0xffff;
  result.writeUInt16BE(checksum, 0x18e);
  return result;
}
