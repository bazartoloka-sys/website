#!/usr/bin/env python3
"""
apply_light_theme_panas.py — Adds light theme + toggle to panas.html.

Usage:
    cd /home/boot/website
    python3 apply_light_theme_panas.py            # apply changes
    python3 apply_light_theme_panas.py --check    # dry-run

Idempotent. Uses localStorage key 'bazar-theme' — same as other pages,
so theme choice carries across the whole site.
"""
import re
import os
import sys

TARGET = 'panas.html'


# ======================== CSS BLOCK ========================
LIGHT_CSS = r'''
/* ============ LIGHT THEME (panas-specific) ============ */
:root[data-theme="light"]{
  --clay:#F5E6C8;
  --clay2:#EFD9B0;
  --clay3:#E6C898;
  --border:rgba(26,15,8,.12);
  --amber:#B8700C;
  --amber2:#D89020;
  --green:#1FA670;
  --cream:#2A1810;
  --cream2:#5A3318;
  --cream3:#735030;
  --cream4:#8B6440;
  --red:#C0392B;
  --blue:#2670A8;
}
:root[data-theme="light"] body{background:linear-gradient(180deg,#F5E6C8 0%,#EBD5A8 100%);background-attachment:fixed}
:root[data-theme="light"] nav{background:rgba(245,230,200,.94)!important;border-bottom-color:var(--border)}
:root[data-theme="light"] .ncta{background:var(--amber);color:#fff!important;box-shadow:0 4px 12px rgba(184,112,12,.32)}

/* Carousel wrap & gradient overlays — must use light clay too */
:root[data-theme="light"] .carousel-wrap{background:var(--clay)}
:root[data-theme="light"] .carousel-wrap::before{background:linear-gradient(to bottom,#F5E6C8 0%,transparent 100%)!important}
:root[data-theme="light"] .carousel-wrap::after{background:linear-gradient(to top,#F5E6C8 0%,transparent 100%)!important}

/* Carousel buttons (prev/next) — invert dark rgba bg */
:root[data-theme="light"] .carousel-btn{background:rgba(245,230,200,.88)!important;border-color:rgba(26,15,8,.20);color:var(--amber);box-shadow:0 4px 12px rgba(26,15,8,.12)}
:root[data-theme="light"] .carousel-btn:hover{background:var(--amber)!important;color:#fff;border-color:var(--amber)}

/* Slide counter */
:root[data-theme="light"] .slide-counter{background:rgba(245,230,200,.85)!important;border-color:rgba(26,15,8,.12);color:var(--amber)}

/* Carousel dots */
:root[data-theme="light"] .cdot{background:rgba(26,15,8,.20)}
:root[data-theme="light"] .cdot.active{background:var(--amber)}

/* Tabs */
:root[data-theme="light"] .tabs{background:var(--clay2);border-color:rgba(26,15,8,.10)}
:root[data-theme="light"] .tab{color:var(--cream2)}
:root[data-theme="light"] .tab.active{background:var(--amber);color:#fff}

/* QA cards */
:root[data-theme="light"] .qa-card{background:var(--clay2);border-color:rgba(26,15,8,.10);box-shadow:0 2px 8px rgba(26,15,8,.05)}
:root[data-theme="light"] .qa-card:hover{box-shadow:0 8px 24px rgba(26,15,8,.15)}
:root[data-theme="light"] .qa-q-icon{background:rgba(184,112,12,.14);border-color:rgba(184,112,12,.30)}
:root[data-theme="light"] .qa-answer{border-top-color:rgba(26,15,8,.10)}
:root[data-theme="light"] .qa-answer-inner{background:rgba(31,166,112,.08);border-left-color:var(--green)}

/* CTA button */
:root[data-theme="light"] .cta-btn{background:var(--amber);color:#fff!important;box-shadow:0 4px 12px rgba(184,112,12,.28)}
:root[data-theme="light"] .cta-btn:hover{background:var(--amber2);box-shadow:0 8px 24px rgba(184,112,12,.40)}

/* Carousel image shadow — softer on light bg */
:root[data-theme="light"] .carousel-slide img{filter:drop-shadow(0 20px 50px rgba(26,15,8,.20))}

/* Footer */
:root[data-theme="light"] footer{border-top-color:rgba(26,15,8,.10)}

/* Theme toggle button (inline in nav) */
.theme-toggle{background:transparent;border:1px solid var(--border);color:var(--cream3);width:36px;height:36px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;margin-right:10px;transition:background .2s,border-color .2s,transform .15s;flex-shrink:0;padding:0;font-family:inherit}
.theme-toggle:hover{background:rgba(232,160,48,.10);border-color:var(--amber);transform:scale(1.08)}
:root[data-theme="light"] .theme-toggle{border-color:rgba(26,15,8,.20);color:var(--cream2)}
:root[data-theme="light"] .theme-toggle:hover{background:rgba(184,112,12,.10);border-color:var(--amber)}
.nav-right{display:flex;align-items:center;gap:0}

/* Body transition for smooth switching */
body{transition:background-color .4s ease,color .4s ease}
/* ====================================== */
'''


# ======================== THEME JS ========================
THEME_JS = '''
<script>
/* ============ THEME SWITCHER ============ */
(function(){
  const KEY = 'bazar-theme';
  const root = document.documentElement;
  const btn = document.getElementById('themeToggle');
  if(!btn) return;
  function apply(theme){
    if(theme === 'light'){
      root.setAttribute('data-theme', 'light');
      btn.textContent = '☀️';
      btn.title = 'Темна тема';
    } else {
      root.removeAttribute('data-theme');
      btn.textContent = '🌙';
      btn.title = 'Світла тема';
    }
  }
  const saved = localStorage.getItem(KEY) || 'dark';
  apply(saved);
  btn.addEventListener('click', () => {
    const current = root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    const next = current === 'light' ? 'dark' : 'light';
    localStorage.setItem(KEY, next);
    apply(next);
  });
})();
</script>
'''


def main():
    check_only = '--check' in sys.argv or '-n' in sys.argv

    if not os.path.exists(TARGET):
        print(f'❌  {TARGET} not found in current directory.')
        print(f'    Run from website root, e.g.:  cd /home/boot/website && python3 apply_light_theme_panas.py')
        sys.exit(1)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    if ':root[data-theme="light"]' in content:
        print(f'⏭  {TARGET}: already patched, nothing to do.')
        sys.exit(0)

    if ':root{' not in content:
        print(f'✗  {TARGET}: no :root block found, skipping.')
        sys.exit(1)

    # 1) Inject light CSS before :root
    content = content.replace(':root{', LIGHT_CSS + '\n:root{', 1)

    # 2) Wrap last <a> in nav + add toggle button
    nav_a_pattern = re.compile(
        r'(\s*)(<a\s[^>]+>[^<]*</a>)\s*(</nav>)',
        re.DOTALL
    )
    m = nav_a_pattern.search(content)
    if m:
        indent, last_link, close = m.group(1), m.group(2), m.group(3)
        replacement = (
            f'{indent}<div class="nav-right">'
            f'<button class="theme-toggle" id="themeToggle" aria-label="Перемкнути тему" title="Перемкнути тему">🌙</button>'
            f'{last_link}'
            f'</div>{indent}{close}'
        )
        content = content[:m.start()] + replacement + content[m.end():]
        button_in_nav = True
    else:
        # Fallback: floating button
        content = content.replace('</body>', '<button class="theme-toggle" id="themeToggle" style="position:fixed;bottom:20px;right:20px;z-index:1000" aria-label="Перемкнути тему">🌙</button>\n</body>', 1)
        button_in_nav = False

    # 3) JS before </body>
    content = content.replace('</body>', THEME_JS + '\n</body>', 1)

    if check_only:
        print(f'DRY-RUN: {TARGET} would be patched.')
        print(f'  ✓ Light theme CSS would be injected')
        print(f'  ✓ Toggle button would be {"placed in nav" if button_in_nav else "added as floating FAB"}')
        print(f'  ✓ Theme switcher JS would be added')
        print()
        print('Run without --check to apply.')
    else:
        with open(TARGET, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓  {TARGET}: patched.')
        print()
        print('Next steps:')
        print('  git diff --stat panas.html')
        print('  git add panas.html')
        print('  git commit -m "Add light theme support to panas.html"')
        print('  git push origin main')


if __name__ == '__main__':
    main()
