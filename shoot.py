import sys, json
from playwright.sync_api import sync_playwright
cases = [('ok',5101),('bad',5102),('custom',5103),('empty',5104)]
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for name, port in cases:
        for label, w, h in [('desktop',1280,900),('mobile',390,844)]:
            ctx = b.new_context(viewport={'width':w,'height':h}, device_scale_factor=1 if label=='desktop' else 2)
            pg = ctx.new_page(); logs=[]
            pg.on('console', lambda m, logs=logs: logs.append(f'{m.type}: {m.text}') if m.type in ('error','warning') else None)
            pg.on('pageerror', lambda e, logs=logs: logs.append(f'pageerror: {e}'))
            pg.goto(f'http://localhost:{port}/', wait_until='networkidle')
            # scroll through to trigger reveals, then back
            pg.evaluate("""async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){window.scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,120));}window.scrollTo({top:0,behavior:'instant'});}""")
            pg.wait_for_timeout(2500)
            st = pg.evaluate("""()=>({state:document.getElementById('chartWrap').dataset.state,
              counters:[...document.querySelectorAll('.stat-number')].map(e=>e.textContent),
              hidden:[...document.querySelectorAll('.fade-in-up')].filter(e=>getComputedStyle(e).opacity<0.99).length,
              overflowX: document.documentElement.scrollWidth > innerWidth})""")
            fn = f'shots/{label}.png' if name=='ok' else f'shots/{name}-{label}.png'
            full_h = pg.evaluate('document.documentElement.scrollHeight')
            pg.set_viewport_size({'width': w, 'height': full_h}); pg.wait_for_timeout(1200)
            pg.screenshot(path=fn)
            out[f'{name}-{label}'] = dict(st, logs=logs)
            ctx.close()
    # reduced motion + no-JS checks
    ctx = b.new_context(viewport={'width':1280,'height':900}, reduced_motion='reduce'); pg=ctx.new_page()
    pg.goto('http://localhost:5101/', wait_until='networkidle'); pg.wait_for_timeout(500)
    out['reduced'] = pg.evaluate("()=>({counters:[...document.querySelectorAll('.stat-number')].map(e=>e.textContent), hidden:[...document.querySelectorAll('.fade-in-up')].filter(e=>getComputedStyle(e).opacity<0.99).length, state:document.getElementById('chartWrap').dataset.state})")
    ctx.close()
    ctx = b.new_context(viewport={'width':1280,'height':900}, java_script_enabled=False); pg=ctx.new_page()
    pg.goto('http://localhost:5101/'); pg.wait_for_timeout(1500)
    out['nojs'] = pg.evaluate("()=>1") if False else None
    pg.screenshot(path='shots/nojs-desktop.png', full_page=True); ctx.close()
    b.close()
print(json.dumps(out, indent=1, ensure_ascii=False))
