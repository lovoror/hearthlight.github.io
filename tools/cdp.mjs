// A tiny Chrome DevTools Protocol driver, so the game's own in-page test harnesses
// (tools/langshots.js, tools/sagatest.js, tools/partybots.js …) can be driven from
// the command line with no dependencies at all — Node's built-in fetch and
// WebSocket are enough.
//
//   start Chrome once, headless, with a debugging port:
//     chrome --headless=new --remote-debugging-port=9222 --window-size=1280,720 \
//            --lang=zh-CN http://localhost:8765/?debug=1
//   then:
//     node tools/cdp.mjs eval "1+1"
//     node tools/cdp.mjs eval "(await import('/tools/langshots.js?'+Date.now())).start('zh')"
//     node tools/cdp.mjs poll "window.__ls" 240000
//
const PORT = Number(process.env.CDP_PORT || 9222);
const HOST = '127.0.0.1:' + PORT;
const { writeFile } = await import('node:fs/promises');

async function findPage() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch(`http://${HOST}/json/list`)).json();
      const pages = list.filter((t) => t.type === 'page' && t.webSocketDebuggerUrl);
      const game = pages.find((t) => /^https?:/.test(t.url)) || pages[0];
      if (game) return game;
    } catch (e) { /* Chrome not up yet */ }
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error(`no Chrome page on ${HOST} — is it running with --remote-debugging-port=${PORT}?`);
}

function connect(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const waiting = new Map();
  const ready = new Promise((res, rej) => { ws.onopen = res; ws.onerror = () => rej(new Error('cdp socket failed')); });
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    const p = waiting.get(m.id);
    if (p) { waiting.delete(m.id); p.try(m); }
  };
  ws.onclose = () => { for (const p of waiting.values()) p.fail(new Error('cdp socket closed')); waiting.clear(); };
  // A request whose reply never arrives (a reload destroys the execution context
  // mid-evaluate) must fail loudly instead of hanging the whole run.
  const send = (method, params, timeoutMs = 30000) => new Promise((res, rej) => {
    const i = ++id;
    const to = setTimeout(() => { waiting.delete(i); rej(new Error(`cdp ${method} timed out`)); }, timeoutMs);
    const settle = (fn, v) => { clearTimeout(to); fn(v); };
    waiting.set(i, { try: (m) => settle(res, m), fail: (e) => settle(rej, e) });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  return { ws, ready, send };
}

async function evaluate(cdp, expression) {
  const r = await cdp.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true, userGesture: true });
  const x = r.result || {};
  if (x.exceptionDetails) {
    const d = x.exceptionDetails;
    throw new Error((d.exception && (d.exception.description || d.exception.value)) || d.text || 'evaluate failed');
  }
  return x.result ? x.result.value : undefined;
}

const show = (v) => (typeof v === 'string' ? v : JSON.stringify(v));

async function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const page = await findPage();
  const cdp = connect(page.webSocketDebuggerUrl);
  await cdp.ready;
  try {
    if (cmd === 'tabs') {
      const list = await (await fetch(`http://${HOST}/json/list`)).json();
      for (const t of list) console.log(t.type, t.url);
      return;
    }
    if (cmd === 'url') { console.log(page.url); return; }
    // Page.navigate / Page.reload answer before the execution context dies, so
    // they are safe where `eval "location.reload()"` would hang forever.
    if (cmd === 'navigate') { await cdp.send('Page.navigate', { url: rest[0] }); console.log('navigating to ' + rest[0]); return; }
    if (cmd === 'reload') { await cdp.send('Page.reload', { ignoreCache: false }); console.log('reloading ' + page.url); return; }
    if (cmd === 'eval') { console.log(show(await evaluate(cdp, rest.join(' ')))); return; }
    if (cmd === 'shot') {
      await cdp.send('Page.enable', {});
      const r = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false }, 60000);
      const data = (r.result || r).data;
      if (!data) throw new Error('no screenshot data back from Chrome');
      const file = rest[0] || 'shot.png';
      await writeFile(file, Buffer.from(data, 'base64'));
      console.log('wrote ' + file);
      return;
    }
    if (cmd === 'poll') {
      const expr = rest[0];
      const timeout = Number(rest[1] || 120000);
      const every = Number(rest[2] || 5000);
      const until = Date.now() + timeout;
      for (;;) {
        let v;
        try { v = await evaluate(cdp, expr); } catch (e) { v = 'eval-error ' + e.message; }
        console.log(show(v));
        const s = typeof v === 'string' ? v : '';
        if (/^(done|err)\b/.test(s) || (s && !/^(run|wait|undefined)$/.test(s) && /done|err/.test(s))) return;
        if (Date.now() > until) { console.log('[timeout]'); return; }
        await new Promise((r) => setTimeout(r, every));
      }
    }
    console.error('usage: node tools/cdp.mjs eval <expr> | poll <expr> [timeoutMs] [everyMs] | shot <file.png> | navigate <url> | reload | tabs | url');
    process.exitCode = 2;
  } finally {
    cdp.ws.close();
  }
}

main().catch((e) => { console.error(String(e && e.message || e)); process.exitCode = 1; });
