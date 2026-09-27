from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for port in (5102, 5103):
        pg = b.new_page(viewport={'width':1280,'height':900})
        pg.goto(f'http://localhost:{port}/', wait_until='networkidle'); pg.wait_for_timeout(4000)
        print(port, pg.evaluate("""()=>{const c=Chart.getChart('activityChart');return {
          fades:[...document.querySelectorAll('.fade-in-up')].map(e=>[e.className, e.getBoundingClientRect().top|0, getComputedStyle(e).opacity]),
          chart: c? {w:c.width,h:c.height, vis:[c.isDatasetVisible(0),c.isDatasetVisible(1)], meta:c.getDatasetMeta(0).data.slice(0,2).map(p=>[p.x|0,p.y|0])}:null}}"""))
        pg.screenshot(path=f'/tmp/dbg{port}.png')
    b.close()
