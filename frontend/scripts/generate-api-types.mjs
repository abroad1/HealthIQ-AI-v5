/**
 * Regenerates OpenAPI snapshot (from the FastAPI app) and TypeScript types.
 * Run from repo: npm run generate-types (cwd: frontend/)
 *
 * Requires: Python 3 on PATH with backend dependencies installed (from backend/).
 */
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';
import { mkdirSync, existsSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..', '..');
const backendRoot = join(repoRoot, 'backend');
const outJson = join(__dirname, 'openapi-snapshot.json');
const generatedDir = join(__dirname, '..', 'app', 'types', 'generated');
const outTs = join(generatedDir, 'openapi.d.ts');

mkdirSync(generatedDir, { recursive: true });
mkdirSync(dirname(outJson), { recursive: true });

const py = [
  'import json, pathlib, os, sys',
  `os.chdir(r'${backendRoot.replace(/\\/g, '\\\\')}')`,
  'from app.main import app',
  `pathlib.Path(r'${outJson.replace(/\\/g, '\\\\')}').write_text(` +
    'json.dumps(app.openapi(), indent=2), encoding="utf-8")',
].join('\n');

const r = spawnSync('python', ['-c', py], {
  encoding: 'utf-8',
  stdio: ['inherit', 'inherit', 'pipe'],
});
if (r.status !== 0) {
  console.error(r.stderr || 'Python failed to write OpenAPI snapshot.');
  process.exit(1);
}

if (!existsSync(outJson)) {
  console.error('Expected snapshot missing:', outJson);
  process.exit(1);
}

const o = spawnSync(
  'npx',
  ['--yes', 'openapi-typescript@7.4.4', outJson, '-o', outTs],
  { encoding: 'utf-8', stdio: 'inherit', cwd: join(__dirname, '..') }
);
if (o.status !== 0) {
  process.exit(1);
}
console.log('Wrote', outJson, 'and', outTs);
