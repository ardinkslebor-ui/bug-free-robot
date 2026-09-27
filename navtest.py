from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width':390,'height':700}, device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:5101/', wait_until='networkidle'); pg.wait_for_timeout(1500)
    pg.click('.navbar-toggler'); pg.wait_for_timeout(600)
    pg.screenshot(path='/tmp/nav.png')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(600)
    print('menu shown after esc:', pg.evaluate("document.getElementById('navbarNav').classList.contains('show')"))
    pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
    pg.goto('http://localhost:5101/'); pg.wait_for_timeout(500); pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
    pg.screenshot(path='/tmp/skip.png', clip={'x':0,'y':0,'width':390,'height':120})
    # legend toggle
    pg.set_viewport_size({'width':1280,'height':900}); pg.wait_for_timeout(2500)
    pg.click('.legend-chip[data-dataset="1"]'); pg.wait_for_timeout(800)
    print('pressed', pg.get_attribute('.legend-chip[data-dataset="1"]','aria-pressed'), 'y1 visible', pg.evaluate("Chart.getChart('activityChart').scales.y1 ? true:false"))
    print('errs', errs)
    b.close()
