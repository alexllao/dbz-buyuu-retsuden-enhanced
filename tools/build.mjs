import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyIps, sha256, updateGenesisChecksum } from './lib/rom.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
async function main() {
  const args = process.argv.slice(2).filter(arg => arg !== '--');
  let inputPath = resolve(root, 'roms/original.bin');
  let variant = 'gameplay';
  for (let index = 0; index < args.length; index++) {
    if (args[index] === '--help') {
      console.log('pnpm build [--rom ruta/a/original.bin] [--variant gameplay|colors]');
      return;
    }
    if (!['--rom', '--variant'].includes(args[index]) || !args[index + 1]) throw new Error(`Argumento inválido: ${args[index]}`);
    const key = args[index++];
    if (key === '--rom') inputPath = resolve(args[index]);
    else variant = args[index];
  }
  const manifest = JSON.parse(await readFile(resolve(root, 'patches/gameplay-v1/manifest.json'), 'utf8'));
  if (!Object.hasOwn(manifest.targets, variant)) throw new Error('Variante admitida: gameplay o colors.');
  let rom;
  try { rom = await readFile(inputPath); }
  catch (error) {
    if (error.code === 'ENOENT') throw new Error('No se encuentra la base. Usa --rom con tu copia original japonesa o colócala en roms/original.bin.');
    throw error;
  }
  if (rom.length !== manifest.source.bytes || sha256(rom) !== manifest.source.sha256) throw new Error('La base no coincide con el tamaño y SHA-256 de la ROM japonesa admitida.');
  for (const name of variant === 'colors' ? ['colors', 'gameplay'] : ['gameplay']) {
    const spec = manifest.patches[name];
    const patch = await readFile(resolve(root, spec.path));
    if (sha256(patch) !== spec.sha256) throw new Error(`El parche ${name} no coincide con su manifiesto.`);
    rom = applyIps(rom, patch);
  }
  rom = updateGenesisChecksum(rom);
  const target = manifest.targets[variant];
  const hash = sha256(rom);
  if (hash !== target.sha256) throw new Error('El resultado no coincide con el build revisado; no se ha guardado.');
  const output = resolve(root, 'dist', target.filename);
  if (output === inputPath) throw new Error('La salida no puede sobrescribir la entrada.');
  await mkdir(dirname(output), { recursive: true });
  await writeFile(output, rom);
  await writeFile(`${output}.json`, `${JSON.stringify({ version: manifest.version, variant, bytes: rom.length, sha256: hash, checksum: rom.readUInt16BE(0x18e).toString(16).padStart(4, '0') }, null, 2)}\n`);
  console.log(`ROM verificada: ${output}\nSHA-256: ${hash}`);
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
