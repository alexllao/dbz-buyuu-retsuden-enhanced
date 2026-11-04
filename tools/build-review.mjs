import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyIps, sha256, updateGenesisChecksum } from './lib/rom.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
async function main() {
  const args = process.argv.slice(2).filter(x => x !== '--');
  if (args.length !== 2 || args[0] !== '--rom') throw new Error('Usa pnpm build:review --rom ruta/a/original.bin');
  const manifest = JSON.parse(await readFile(resolve(root, 'patches/review-v2/manifest.json'), 'utf8'));
  const source = await readFile(resolve(args[1]));
  if (source.length !== manifest.source.bytes || sha256(source) !== manifest.source.sha256) throw new Error('La ROM original no coincide con la base japonesa admitida.');
  const patch = await readFile(resolve(root, manifest.patch.path));
  if (sha256(patch) !== manifest.patch.sha256) throw new Error('El parche no coincide con el manifiesto.');
  const rom = updateGenesisChecksum(applyIps(source, patch));
  if (rom.length !== manifest.target.bytes || sha256(rom) !== manifest.target.sha256) throw new Error('El resultado no coincide con la ROM de revisión.');
  await mkdir(resolve(root, 'dist'), { recursive: true });
  const destination = resolve(root, 'dist', manifest.target.filename);
  await writeFile(destination, rom);
  console.log(`ROM de revisión verificada: ${destination}\nSHA-256: ${sha256(rom)}`);
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
