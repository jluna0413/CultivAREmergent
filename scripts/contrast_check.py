from playwright.sync_api import sync_playwright
import math

# WCAG contrast calculation utilities

def luminance(rgb):
    # rgb = (r,g,b) each 0-255
    def s(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * s(r) + 0.7152 * s(g) + 0.0722 * s(b)


def hex_to_rgb(hex_str):
    hex_str = hex_str.strip()
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def contrast_ratio(fg, bg):
    L1 = luminance(fg)
    L2 = luminance(bg)
    lighter = max(L1, L2)
    darker = min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)


def parse_css_color(css_color):
    css_color = css_color.strip()
    if css_color.startswith('rgb'):
        nums = css_color[css_color.find('(')+1:css_color.find(')')].split(',')
        return tuple(int(float(n.strip())) for n in nums[:3])
    if css_color.startswith('#'):
        return hex_to_rgb(css_color)
    # fallback: try to evaluate common color names via a small map
    named = {
        'white': (255,255,255),
        'black': (0,0,0),
        'transparent': (255,255,255)
    }
    return named.get(css_color.lower(), (0,0,0))


PAGES = [
    ('/marketing/', 'marketing'),
    ('/marketing/blog', 'blog')
]

SELECTORS = [
    ('.section-header h2', 'Section header H2'),
    ('.cta-content h2', 'CTA H2'),
    ('.cta-feature', 'CTA feature text'),
    ('.newsletter-text h3', 'Newsletter H3')
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    results = []

    for path, name in PAGES:
        url = f'http://127.0.0.1:5000{path}'
        page.goto(url, wait_until='networkidle')
        for theme in ('light','dark'):
            if theme == 'dark':
                page.evaluate("() => document.documentElement.setAttribute('data-theme','dark')")
            else:
                page.evaluate("() => document.documentElement.removeAttribute('data-theme')")
            page.wait_for_timeout(200)
            for sel, label in SELECTORS:
                handle = page.query_selector(sel)
                if not handle:
                    results.append((name, theme, label, 'MISSING', None))
                    continue
                fg = page.evaluate("(el) => getComputedStyle(el).color", handle)
                # find background color by walking up until non-transparent
                bg = page.evaluate("(el)=>{let cur=el; while(cur){let c=getComputedStyle(cur).backgroundColor; if(c && c!=='rgba(0, 0, 0, 0)' && c!=='transparent') return c; cur=cur.parentElement;} return getComputedStyle(document.documentElement).backgroundColor}", handle)
                fg_rgb = parse_css_color(fg)
                bg_rgb = parse_css_color(bg)
                ratio = contrast_ratio(fg_rgb, bg_rgb)
                results.append((name, theme, label, f'{ratio:.2f}', (fg, bg)))

    browser.close()

    # print formatted
    print('Page | Theme | Element | Contrast | (fg, bg)')
    print('----|-------|---------|----------|--------')
    for r in results:
        print(' | '.join([str(x) if x is not None else '' for x in r]))
