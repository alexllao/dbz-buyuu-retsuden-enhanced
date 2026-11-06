import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyIps, sha256, updateGenesisChecksum } from './lib/rom.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
async function main() {
  const args = process.argv.slice(2).filter(x => x !== '--');
  let input, version = 'v6.6';
  for (let i = 0; i < args.length; i += 2) {
    if (!args[i + 1] || !['--rom', '--version'].includes(args[i])) throw new Error('Usa pnpm build:review --rom ruta/a/original.bin [--version v1.0|responsive-v3|responsive-v2|responsive-v1|hud-hits-v3|hud-hits-v2|hud-hits-v1|side-advantage-v1|stun-break-v2|hud-stun-v1|combos-v5-native-stun|combos-v4-natural|combos-v3|combos-v2|combos-v1|v6.6|v6.5|v6.4|v6.3|v6.2|v6.1|v6|v5.2]');
    if (args[i] === '--rom') input = args[i + 1]; else version = args[i + 1];
  }
  const versions = { 'gravity-g1': 'gravity-g1', 'v1.0': 'release-v1-0-build-20261106-124607', 'v1.0-build-20261106-105411': 'release-v1-0-build-20261106-105411', 'gohan-hits-v1': 'release-v1-0-build-20261106-124607', 'v1.0-build-20261106-103002': 'release-v1-0-build-20261106-103002', 'piccolo-hits-v1': 'release-v1-0-build-20261106-105411', 'v1.0-build-20261106-100534': 'release-v1-0', 'ki-startup-v1': 'release-v1-0-build-20261106-103002', 'responsive-v3': 'release-v1-0', 'responsive-v2': 'responsive-v2', 'responsive-v1': 'responsive-v1', 'hud-hits-v3': 'hud-hits-v3', 'hud-hits-v2': 'hud-hits-v2', 'hud-hits-v1': 'hud-hits-v1', 'side-advantage-v1': 'side-advantage-v1', 'stun-break-v2': 'stun-break-v2', 'hud-stun-v1': 'hud-stun-v1', 'combos-v5-native-stun': 'combos-v5-native-stun', 'combos-v4-natural': 'combos-v4-natural', 'combos-v3': 'combos-v3', 'combos-v2': 'combos-v2', 'combos-v1': 'combos-v1', 'v6.6': 'review-v6-6', 'v6.5': 'review-v6-5', 'v6.4': 'review-v6-4', 'v6.3': 'review-v6-3', 'v6.2': 'review-v6-2', 'v6.1': 'review-v6-1', 'v6': 'review-v3', 'v5.2': 'review-v2' };
  if (!input || !Object.hasOwn(versions, version)) throw new Error('Indica --rom y una versiÃ³n admitida: v6.6, v6.5, v6.4, v6.3, v6.2, v6.1, v6, v5.2, combos-v1, combos-v2, combos-v3, combos-v4-natural, combos-v5-native-stun, hud-stun-v1, stun-break-v2, side-advantage-v1, hud-hits-v1, hud-hits-v2, hud-hits-v3, responsive-v1, responsive-v2 o v1.0.');
  const folder = versions[version];
  const manifest = JSON.parse(await readFile(resolve(root, `patches/${folder}/manifest.json`), 'utf8'));
  const source = await readFile(resolve(input));
  if (source.length !== manifest.source.bytes || sha256(source) !== manifest.source.sha256) throw new Error('La ROM original no coincide con la base japonesa admitida.');
  const patch = await readFile(resolve(root, manifest.patch.path));
  if (sha256(patch) !== manifest.patch.sha256) throw new Error('El parche no coincide con el manifiesto.');
  const rom = updateGenesisChecksum(applyIps(source, patch));
  if (rom.length !== manifest.target.bytes || sha256(rom) !== manifest.target.sha256) throw new Error('El resultado no coincide con la ROM de revisiÃ³n.');
  await mkdir(resolve(root, 'dist'), { recursive: true });
  const destination = resolve(root, 'dist', manifest.target.filename);
  await writeFile(destination, rom);
  console.log(`ROM de revisiÃ³n verificada: ${destination}\nSHA-256: ${sha256(rom)}`);
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
