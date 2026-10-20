"""Run axe-core 4.10.2 (WCAG 2 A/AA rules) on the live pages in dark and light mode.

Usage: python tools/a11y_check.py > docs/verification/axe_result.json
"""
import sys, json, urllib.request
from playwright.sync_api import sync_playwright

BASE = "https://hyangnamdexter.github.io/Introducemyself/"
PAGES = [BASE, BASE + "activities/personal-website/"]
AXE = urllib.request.urlopen("https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js").read().decode()

out = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for mode in ["dark", "light"]:
        for url in PAGES:
            for run in range(2 if url == BASE else 1):
                ctx = b.new_context(viewport={"width": 1440, "height": 900})
                page = ctx.new_page()
                if mode == "light":
                    page.add_init_script("localStorage.setItem('darkMode','false')")
                # start paused so text is in its final state (no typewriter / fades)
                page.add_init_script("localStorage.setItem('motionPaused','true')")
                page.goto(url, wait_until="networkidle"); page.wait_for_timeout(1500)
                page.add_script_tag(content=AXE)
                r = page.evaluate("""async () => {
                  const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa']}});
                  return {violations: r.violations.map(v => ({id: v.id, impact: v.impact, n: v.nodes.length,
                            nodes: v.nodes.slice(0,6).map(n => [n.target.join(' '), (n.any[0]||{}).message || n.failureSummary.slice(0,140)])})),
                          passes: r.passes.length, incomplete: r.incomplete.map(v => v.id)};
                }""")
                r.update(mode=mode, url=url.replace(BASE, "/"),
                         primary=page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim()"))
                out.append(r); ctx.close()
    b.close()
print(json.dumps(out, ensure_ascii=False, indent=1))
