import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('source checkout and Pages artifact both expose every dataset file', () => {
  const names = ['entities', 'cases', 'sources', 'relationships', 'metadata'];
  for (const name of names) {
    assert.doesNotThrow(() => JSON.parse(fs.readFileSync(`public/data/${name}.json`, 'utf8')));
    assert.doesNotThrow(() => JSON.parse(fs.readFileSync(`dist/data/${name}.json`, 'utf8')));
  }
});

test('loader supports GitHub Pages Actions and branch publishing layouts', () => {
  const app = fs.readFileSync('src/app.js', 'utf8');
  assert.match(app, /`data\/\$\{name\}\.json`/);
  assert.match(app, /`public\/data\/\$\{name\}\.json`/);
  assert.match(app, /content-type/);
});
