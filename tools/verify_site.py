"""Live-site checks used for the report's verification table.

Usage (from the repository root):
    pip install playwright
    python tools/verify_site.py docs/verification

Uses the locally installed Google Chrome (channel="chrome"), so no browser
download is needed. Writes screenshots (fig*.png) and verify_log.json.
"""
import json, sys, datetime, pathlib
from playwright.sync_api import sync_playwright

BASE = "https://hyangnamdexter.github.io/Introducemyself/"
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs/verification")
OUT.mkdir(parents=True, exist_ok=True)
KST = datetime.timezone(datetime.timedelta(hours=9))
log = {}

def now():
    return datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")

def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth > window.innerWidth")

def errors_collector(page, bucket):
    page.on("console", lambda m: bucket.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: bucket.append(str(e)))
    page.on("requestfailed", lambda r: bucket.append("REQFAIL " + r.url))
    page.on("response", lambda r: bucket.append(f"HTTP{r.status} {r.url}") if r.status >= 400 else None)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    log["browser"] = "Chrome " + browser.version

    # ---- 1440 desktop
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page(); errs = []; errors_collector(page, errs)
    page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(3500)
    log["t1440_time"] = now()
    page.screenshot(path=str(OUT / "fig1_home_1440.png"))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0, 0)"); page.wait_for_timeout(300)
    page.screenshot(path=str(OUT / "fig2_home_1440_full.png"), full_page=True)
    css = page.evaluate("""[...document.styleSheets].map(s=>s.href).filter(Boolean)""")
    log["d1440"] = {"overflow": overflow(page), "stylesheets": css,
                    "bodyFont": page.evaluate("getComputedStyle(document.body).fontFamily"),
                    "navVisible": page.is_visible("nav .hidden.lg\\:flex")}
    # menu click -> anchor + back
    page.click("nav .lg\\:flex >> text=활동"); page.wait_for_timeout(600)
    top = page.evaluate("document.getElementById('experience').getBoundingClientRect().top")
    log["menu_activity"] = {"url": page.url, "sectionTop": top}
    page.click("nav .lg\\:flex >> text=연락처"); page.wait_for_timeout(600)
    url2 = page.url
    page.go_back(); page.wait_for_timeout(600)
    log["back"] = {"after_contact": url2, "after_back": page.url,
                   "experienceTop": page.evaluate("document.getElementById('experience').getBoundingClientRect().top")}
    # icons and images
    log["images"] = page.evaluate("[...document.images].map(i=>[i.getAttribute('src'), i.naturalWidth>0, i.getAttribute('alt')])")
    log["fa_loaded"] = page.evaluate("document.fonts.check('900 16px \"Font Awesome 6 Free\"')")
    # motion toggle
    page.click("nav .lg\\:flex .motion-toggle"); page.wait_for_timeout(300)
    log["motion"] = page.evaluate("""({pressed: document.querySelector('.motion-toggle').getAttribute('aria-pressed'),
        paused: gsap.globalTimeline.paused(), tagline: document.querySelector('.typewriter').textContent})""")
    page.click("nav .lg\\:flex .motion-toggle")
    # about modal via keyboard
    page.focus("#aboutModalBtn"); page.keyboard.press("Enter"); page.wait_for_timeout(300)
    log["modal_open_focus"] = page.evaluate("document.activeElement.id")
    page.keyboard.press("Tab"); page.keyboard.press("Tab")
    log["modal_tab_inside"] = page.evaluate("document.getElementById('aboutModal').contains(document.activeElement)")
    page.keyboard.press("Escape"); page.wait_for_timeout(300)
    log["modal_after_escape"] = {"hidden": page.evaluate("document.getElementById('aboutModal').classList.contains('hidden')"),
                                 "focus": page.evaluate("document.activeElement.id")}
    log["errors_1440"] = errs
    ctx.close()

    # ---- keyboard from top of page
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(3000)
    seq = []
    for i in range(14):
        page.keyboard.press("Tab")
        seq.append(page.evaluate("""(()=>{const e=document.activeElement;const cs=getComputedStyle(e);
            return [(e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,20), cs.outlineStyle, cs.outlineWidth]})()"""))
    log["tab_sequence"] = seq
    page.screenshot(path=str(OUT / "fig5_keyboard_focus_1440.png"))
    # Tab to "소개" and press Enter
    page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(2000)
    for i in range(10):
        page.keyboard.press("Tab")
        if page.evaluate("document.activeElement.innerText.trim()") == "소개":
            break
    page.keyboard.press("Enter"); page.wait_for_timeout(500)
    log["enter_about"] = page.url
    ctx.close()

    # ---- 768 tablet
    ctx = browser.new_context(viewport={"width": 768, "height": 1024})
    page = ctx.new_page(); page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(3500)
    page.screenshot(path=str(OUT / "fig6_home_768.png"))
    log["t768"] = {"overflow": overflow(page), "time": now()}
    ctx.close()

    # ---- 390 mobile
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    page = ctx.new_page(); errs = []; errors_collector(page, errs)
    page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(3500)
    log["t390_time"] = now()
    page.screenshot(path=str(OUT / "fig3_home_390.png"))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0, 0)"); page.wait_for_timeout(300)
    page.screenshot(path=str(OUT / "fig4_home_390_full.png"), full_page=True)
    log["m390"] = {"overflow": overflow(page)}
    page.tap("#menu-btn"); page.wait_for_timeout(300)
    log["m390"]["menu_expanded"] = page.get_attribute("#menu-btn", "aria-expanded")
    page.screenshot(path=str(OUT / "fig7_menu_open_390.png"))
    sizes = page.evaluate("[...document.querySelectorAll('#mobile-menu a, nav button')].filter(e=>e.offsetParent).map(e=>{const r=e.getBoundingClientRect();return [(e.innerText||e.getAttribute('aria-label')).trim().slice(0,12), Math.round(r.width), Math.round(r.height)]})")
    log["m390"]["targets"] = sizes
    page.tap("#mobile-menu >> text=활동"); page.wait_for_timeout(600)
    log["m390"]["after_tap"] = {"url": page.url,
        "menuHidden": page.evaluate("document.getElementById('mobile-menu').classList.contains('hidden')"),
        "sectionTop": page.evaluate("document.getElementById('experience').getBoundingClientRect().top")}
    log["errors_390"] = errs
    ctx.close()

    # ---- resize 1440 -> 390 -> 1440 without reload
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page(); page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(2500)
    page.set_viewport_size({"width": 390, "height": 844}); page.wait_for_timeout(500)
    page.click("#menu-btn"); page.wait_for_timeout(200)
    page.set_viewport_size({"width": 1440, "height": 900}); page.wait_for_timeout(500)
    log["resize"] = {"desktopMenuVisible": page.is_visible("nav .hidden.lg\\:flex"),
                     "mobileMenuVisible": page.is_visible("#mobile-menu"),
                     "heroVisible": page.is_visible("h1"), "overflow": overflow(page)}
    ctx.close()

    # ---- 200% zoom equivalent: 1440 window at 200% = 720 CSS px
    ctx = browser.new_context(viewport={"width": 720, "height": 450}, device_scale_factor=2)
    page = ctx.new_page(); page.goto(BASE, wait_until="networkidle"); page.wait_for_timeout(3000)
    page.click("#menu-btn"); page.wait_for_timeout(200)
    page.click("#mobile-menu >> text=소개"); page.wait_for_timeout(500)
    log["zoom200"] = {"overflow": overflow(page), "url": page.url}
    page.screenshot(path=str(OUT / "fig8_zoom200.png"))
    ctx.close()

    # ---- direct URL + reload
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page(); errs = []; errors_collector(page, errs)
    r = page.goto(BASE + "activities/personal-website/", wait_until="networkidle")
    log["direct_activity"] = {"status": r.status, "h1": page.inner_text("h1"),
                              "h2": page.eval_on_selector_all("article h2", "e=>e.map(x=>x.innerText)")}
    page.reload(wait_until="networkidle")
    log["reload_activity"] = page.inner_text("h1")
    page.screenshot(path=str(OUT / "fig9_activity_1440.png"), full_page=True)
    page.click("text=활동 목록으로 돌아가기"); page.wait_for_timeout(800)
    log["back_link"] = page.url
    page = ctx.new_page()
    r = page.goto(BASE + "#experience", wait_until="networkidle"); page.wait_for_timeout(1200)
    log["direct_anchor"] = {"status": r.status, "top": page.evaluate("document.getElementById('experience').getBoundingClientRect().top")}
    page.reload(wait_until="networkidle"); page.wait_for_timeout(1200)
    log["reload_anchor_top"] = page.evaluate("document.getElementById('experience').getBoundingClientRect().top")
    r = page.goto(BASE + "no-such-page/")
    log["404"] = {"status": r.status, "h1": page.inner_text("h1") if page.query_selector("h1") else None}
    log["errors_direct"] = [e for e in errs if "no-such-page" not in e]
    ctx.close()
    browser.close()

log["finished"] = now()
(OUT / "verify_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(log, ensure_ascii=False, indent=1))
