import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import assert from 'node:assert/strict';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const expected = Buffer.from((await readFile(process.argv[3] ? resolve(process.argv[3]) : resolve(root, 'src/gameplay/v1/controls.hex'), 'utf8')).replace(/\s/g, ''), 'hex');
const actual = await readFile(process.argv[2]);
assert.deepEqual(actual, expected, 'La fuente ensamblada ha cambiado respecto al parche revisado.');
console.log(`Ensamblado verificado: ${actual.length} bytes idénticos a la versión revisada.`);
