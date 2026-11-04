import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyIps, sha256, updateGenesisChecksum } from './lib/rom.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
async function main() {
  const args = process.argv.slice(2).filter(arg => arg !== '--');
  if (args.includes('--help')) { console.log('pnpm build:auras --rom ruta/a/original.bin'); return; }
  if (args.length !== 2 || args[0] !== '--rom') throw new Error('Usa pnpm build:auras --rom ruta/a/original.bin');
  const manifest = JSON.parse(await readFile(resolve(root, 'patches/auras-c2-v1/manifest.json'), 'utf8'));
  const source = await readFile(resolve(args[1]));
  if (source.length !== manifest.source.bytes || sha256(source) !== manifest.source.sha256) throw new Error('La ROM japonesa original no coincide con el SHA-256 admitido.');
  const patch = await readFile(resolve(root, manifest.patch.path));
  if (sha256(patch) !== manifest.patch.sha256) throw new Error('El parche C2 no coincide con su manifiesto.');
  const rom = updateGenesisChecksum(applyIps(source, patch));
  if (rom.length !== manifest.target.bytes || sha256(rom) !== manifest.target.sha256) throw new Error('El resultado no coincide con el prototipo grabado.');
  const output = resolve(root, 'dist', manifest.target.filename);
  await mkdir(dirname(output), { recursive: true });
  await writeFile(output, rom);
  console.log(`Prototipo C2 verificado: ${output}\nSHA-256: ${sha256(rom)}`);
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
