import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const ROOT = path.resolve(import.meta.dirname, '..');
const wf = JSON.parse(fs.readFileSync(path.join(ROOT, 'IMPORT_ME_n8n_workflow_GC_MAIN_01.json'), 'utf8'));
const htmlFixture = fs.readFileSync(
  '/Users/satvikjain/.gemini/antigravity/brain/feb6fd6e-069d-4d7f-85c1-2617e5e8b536/scratch/live_page1.html',
  'utf8'
);

// 1. B12 Layout checks
const stickies = wf.nodes.filter(n => n.type === 'n8n-nodes-base.stickyNote').sort((a, b) => a.position[0] - b.position[0]);
const others = wf.nodes.filter(n => n.type !== 'n8n-nodes-base.stickyNote');
for (let i = 0; i < stickies.length - 1; i++) {
  const gap = stickies[i + 1].position[0] - (stickies[i].position[0] + stickies[i].parameters.width);
  assert.ok(gap >= 160, `Gap too small between ${stickies[i].name} and ${stickies[i + 1].name}: ${gap}`);
}
for (const n of others) {
  const [nx, ny] = n.position;
  const inside = stickies.find(s =>
    nx >= s.position[0] &&
    nx + 100 <= s.position[0] + s.parameters.width &&
    ny >= s.position[1] + 120 &&
    ny + 80 <= s.position[1] + s.parameters.height
  );
  assert.ok(inside, `Node ${n.name} at (${nx},${ny}) is outside sticky boxes`);
}
for (const [srcName, conns] of Object.entries(wf.connections)) {
  const src = wf.nodes.find(n => n.name === srcName);
  for (const branch of (conns.main || [])) {
    for (const edge of branch) {
      const dst = wf.nodes.find(n => n.name === edge.node);
      assert.ok(dst.position[0] > src.position[0], `Link ${srcName} -> ${edge.node} is not left-to-right`);
    }
  }
}
console.log(`PASS 1/4: B12 layout (${stickies.length} boxes, ${others.length} nodes).`);

// Helper to run Code node inside strict node:vm (no URLSearchParams/URL/Buffer/require)
function runVm(jsCode, $, $input) {
  const sb = { $, $input, helpers: {} };
  vm.createContext(sb);
  return vm.runInContext(`(async () => { ${jsCode} })()`, sb);
}

const configNode = wf.nodes.find(n => n.name === 'Config');
const registryNode = wf.nodes.find(n => n.name === 'Portal Registry');
const parseNode = wf.nodes.find(n => n.name === 'Parse Portal Jobs');
const requiredCols = wf.nodes.find(n => n.name === 'Ensure Data table').parameters.columns.column.map(c => c.name);

function evalConfig(triggerJson) {
  const cfg = {};
  for (const a of configNode.parameters.assignments.assignments) {
    if (typeof a.value === 'string' && a.value.startsWith('={{')) {
      const sb = { $json: triggerJson };
      vm.createContext(sb);
      cfg[a.name] = vm.runInContext(a.value.slice(3, -2).trim(), sb);
    } else {
      cfg[a.name] = a.value;
    }
  }
  return cfg;
}

// 2. Schedule Trigger path (Run Search never executed)
const cfgSched = evalConfig({ timestamp: '2026-11-11T00:00:00Z' });
assert.equal(cfgSched.override_query, false);
assert.equal(cfgSched.override_location, false);
const portalsOut = await runVm(registryNode.parameters.jsCode, (name) => {
  if (name === 'Run Search') throw new Error("Node 'Run Search' hasn't been executed");
  return { first: () => ({ json: cfgSched }) };
}, { all: () => [] });
assert.equal(portalsOut.length, 1);
assert.equal(
  portalsOut[0].json.request_url,
  'https://www.google.com/about/careers/applications/jobs/results?q=%22Product%20Manager%22&location=India&hl=en-GB'
);
const parsedSched = await runVm(
  parseNode.parameters.jsCode,
  (name) => ({ all: () => (name === 'Portal Registry' ? portalsOut : [{ json: cfgSched }]) }),
  { all: () => [{ json: { body: htmlFixture } }] }
);
assert.equal(parsedSched.length, 19);
for (const col of requiredCols) assert.ok(col in parsedSched[0].json, `Missing column ${col}`);
console.log('PASS 2/4: Schedule Trigger end-to-end in strict node:vm (19 rows, 35 cols).');

// 3. Fault-isolation test: 1 healthy portal + 2 failing portals -> still returns 19 healthy jobs
const mixedPortals = [
  portalsOut[0],
  { json: { portal_id: 'broken_http', company: 'BrokenCorp', parser_type: 'json_path', request_url: 'https://x/1' } },
  { json: { portal_id: 'bad_json', company: 'BadJsonCorp', parser_type: 'json_path', request_url: 'https://x/2' } },
];
const mixedResponses = [
  { json: { body: htmlFixture } },
  { json: { error: { message: '503 Service Unavailable' } } },
  { json: { body: '<html>Not JSON</html>' } },
];
const parsedMixed = await runVm(
  parseNode.parameters.jsCode,
  () => ({ all: () => mixedPortals }),
  { all: () => mixedResponses }
);
assert.equal(parsedMixed.length, 19, 'Healthy portal jobs must survive when other portals fail');
console.log('PASS 3/4: Fault isolation (1 healthy + 2 failed portals -> 19 jobs saved).');

// 4. Fail-closed test: ALL portals fail -> throws error instead of silent empty success
await assert.rejects(
  () => runVm(
    parseNode.parameters.jsCode,
    () => ({ all: () => [mixedPortals[1]] }),
    { all: () => [mixedResponses[1]] }
  ),
  /All portals failed/
);
console.log('PASS 4/4: Fail-closed when all portals fail.');

