#!/usr/bin/env python3
"""
apply_light_theme.py — Adds light theme + toggle to Bazar Toloka HTML pages.

Usage:
    cd /home/boot/website
    python3 apply_light_theme.py            # apply changes
    python3 apply_light_theme.py --check    # dry-run, just report what would change
    python3 apply_light_theme.py --revert   # ❌ NOT IMPLEMENTED — use `git restore .` instead

Idempotent: if a file already has the light theme block, it is skipped.
Skipped intentionally: panas.html (has different palette).
"""
import re
import os
import sys

# Pages with standard nav (toggle goes into nav)
PAGES_WITH_NAV = [
    'index.html', 'blog.html', 'compare.html', 'jobs.html', 'upgrade.html',
    'article-001.html', 'article-template.html',
    'offer.html', 'privacy.html', 'support.html', 'terms.html',
]
# Pages without nav (floating toggle in corner)
PAGES_NO_NAV = ['success.html', 'fail.html']
# Pages to skip entirely
SKIPPED = ['panas.html']


# ======================== CSS BLOCK ========================
LIGHT_CSS = r'''
/* ============ LIGHT THEME ============ */
:root[data-theme="light"]{
  --clay:#F5E6C8;
  --clay2:#EFD9B0;
  --clay3:#E6C898;
  --green:#1FA670;
  --amber:#B8700C;
  --cream:#2A1810;
  --cream2:#5A3318;
  --cream3:#735030;
  --cream4:#8B6440;
  --border:rgba(26,15,8,.12);
  --gborder:rgba(31,166,112,.32);
  --aborder:rgba(184,112,12,.32);
}
:root[data-theme="light"] body{background:linear-gradient(180deg,#F5E6C8 0%,#EBD5A8 100%);background-attachment:fixed}
:root[data-theme="light"] .nav{background:rgba(245,230,200,.94)!important;border-bottom-color:var(--aborder)}
:root[data-theme="light"] .panas-c{border:3px solid #1A0F08;box-shadow:0 10px 28px rgba(26,15,8,.28),0 2px 6px rgba(26,15,8,.15),inset 0 -3px 10px rgba(26,15,8,.12);background:#EFD9B0}
:root[data-theme="light"] .vc,
:root[data-theme="light"] .pc,
:root[data-theme="light"] .tcard,
:root[data-theme="light"] .feat-card,
:root[data-theme="light"] .stat-box,
:root[data-theme="light"] .rcard,
:root[data-theme="light"] .istat,
:root[data-theme="light"] .ai-b,
:root[data-theme="light"] .video-block,
:root[data-theme="light"] .invest-sec,
:root[data-theme="light"] .seller-sec,
:root[data-theme="light"] .ai-sec,
:root[data-theme="light"] .card,
:root[data-theme="light"] .job-card,
:root[data-theme="light"] .compare-card,
:root[data-theme="light"] .article-card,
:root[data-theme="light"] .blog-card,
:root[data-theme="light"] .tariff-card,
:root[data-theme="light"] .upgrade-card{box-shadow:0 4px 14px rgba(26,15,8,.08),0 1px 3px rgba(26,15,8,.05)}
:root[data-theme="light"] .float-chip{background:rgba(245,230,200,.96);color:var(--cream);border-color:rgba(26,15,8,.12);box-shadow:0 4px 10px rgba(26,15,8,.10)}
:root[data-theme="light"] .phone{box-shadow:0 30px 60px rgba(26,15,8,.25),0 0 0 1px rgba(26,15,8,.10)}
:root[data-theme="light"] .ncta{box-shadow:0 4px 12px rgba(31,166,112,.30)}
:root[data-theme="light"] .btn-play,
:root[data-theme="light"] .cta-primary{box-shadow:0 5px 16px rgba(31,166,112,.32)}
:root[data-theme="light"] .notify-btn,
:root[data-theme="light"] .btn-invest{box-shadow:0 4px 12px rgba(184,112,12,.32)}
:root[data-theme="light"] .notify-input,
:root[data-theme="light"] .field input,
:root[data-theme="light"] .field textarea,
:root[data-theme="light"] .field select,
:root[data-theme="light"] input[type=text],
:root[data-theme="light"] input[type=email],
:root[data-theme="light"] textarea,
:root[data-theme="light"] select{background:#FAF0D8;border-color:rgba(26,15,8,.15);color:var(--cream)}
:root[data-theme="light"] .notify-input::placeholder,
:root[data-theme="light"] .field input::placeholder,
:root[data-theme="light"] .field textarea::placeholder,
:root[data-theme="light"] input::placeholder,
:root[data-theme="light"] textarea::placeholder{color:var(--cream3)}
:root[data-theme="light"] .pill{background:#EFD9B0;border-color:rgba(26,15,8,.10);color:var(--cream2)}
:root[data-theme="light"] .div{background:rgba(26,15,8,.10)}
:root[data-theme="light"] footer{border-top-color:rgba(26,15,8,.10)}
:root[data-theme="light"] .sbadge{background:rgba(31,166,112,.12);border-color:var(--gborder)}
:root[data-theme="light"] .notify-chip,
:root[data-theme="light"] .invest-chip{background:rgba(184,112,12,.12);border-color:rgba(184,112,12,.25)}
:root[data-theme="light"] .feat-glow,
:root[data-theme="light"] .vc::before{opacity:.10}
:root[data-theme="light"] .phone-screen{color:#F5E6C8}
:root[data-theme="light"] .ai-search{background:rgba(46,204,142,.10);border-color:rgba(46,204,142,.25)}
:root[data-theme="light"] .ai-text{color:#B89060}
:root[data-theme="light"] .rating-card{background:rgba(245,230,200,.06);border-color:rgba(245,230,200,.10)}
:root[data-theme="light"] .rating-name{color:#F5E6C8}
:root[data-theme="light"] .shield-chip{background:rgba(46,204,142,.10);border-color:rgba(46,204,142,.18);color:#2ECC8E}
:root[data-theme="light"] .feat-card{background:var(--clay2);border-color:rgba(26,15,8,.08)}
:root[data-theme="light"] .feat-tag{background:rgba(26,15,8,.05);border-color:rgba(26,15,8,.10);color:var(--cream3)}
:root[data-theme="light"] .feat-number{color:var(--cream3)}

/* Theme toggle button (inline in nav) */
.theme-toggle{background:transparent;border:1px solid var(--aborder);color:var(--cream2);width:36px;height:36px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;margin-right:10px;transition:background .2s,border-color .2s,transform .15s;flex-shrink:0;padding:0;font-family:inherit}
.theme-toggle:hover{background:rgba(232,160,48,.10);border-color:var(--amber);transform:scale(1.08)}
:root[data-theme="light"] .theme-toggle:hover{background:rgba(184,112,12,.10);border-color:var(--amber)}
.nav-right{display:flex;align-items:center;gap:0}

/* Theme toggle button (floating, for pages without nav) */
.theme-toggle-fab{position:fixed;bottom:20px;right:20px;background:var(--clay2);border:1px solid var(--aborder);color:var(--cream);width:48px;height:48px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;z-index:1000;box-shadow:0 6px 20px rgba(0,0,0,.30);transition:transform .15s,box-shadow .15s;padding:0;font-family:inherit}
.theme-toggle-fab:hover{transform:scale(1.08);box-shadow:0 8px 26px rgba(0,0,0,.40)}
:root[data-theme="light"] .theme-toggle-fab{background:#EFD9B0;color:var(--cream);box-shadow:0 6px 20px rgba(26,15,8,.18)}
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


def patch_html(content: str, has_nav: bool, filename: str) -> tuple[str, list[str], bool]:
    """Apply patches. Returns (new_content, log_list, was_changed)."""
    log = []

    if ':root[data-theme="light"]' in content:
        log.append(f'  ⏭  {filename}: already patched, skipping')
        return content, log, False

    if ':root{' not in content:
        log.append(f'  ✗  {filename}: no :root block found, skipping')
        return content, log, False

    # 1) Inject light theme CSS BEFORE :root
    content = content.replace(':root{', LIGHT_CSS + '\n:root{', 1)

    # 2) Add transition on body
    body_pattern = re.compile(r"(body\s*\{[^}]*background\s*:\s*var\(--clay\)[^}]*)\}", re.DOTALL)
    m = body_pattern.search(content)
    if m and 'transition:' not in m.group(0):
        content = content[:m.end()-1] + ';transition:background-color .4s ease,color .4s ease}' + content[m.end():]

    # 3) Toggle button
    button_placed = False
    if has_nav:
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
            button_placed = True
        else:
            log.append(f'  ⚠  {filename}: no <a> found inside nav, using floating button instead')

    if not button_placed:
        fab = '<button class="theme-toggle-fab" id="themeToggle" aria-label="Перемкнути тему" title="Перемкнути тему">🌙</button>\n'
        content = content.replace('</body>', fab + '</body>', 1)

    # 4) JS before </body>
    content = content.replace('</body>', THEME_JS + '\n</body>', 1)

    log.append(f'  ✓  {filename}: patched')
    return content, log, True


def main():
    check_only = '--check' in sys.argv or '-n' in sys.argv

    # Verify we're in the right directory
    if not os.path.exists('index.html'):
        print('❌  Run this script from the website root directory (where index.html lives).')
        print('    Example:  cd /home/boot/website && python3 apply_light_theme.py')
        sys.exit(1)

    all_pages = sorted(set(PAGES_WITH_NAV + PAGES_NO_NAV))

    print(f'{"DRY-RUN " if check_only else ""}Patching {len(all_pages)} pages')
    print(f'Skipping: {SKIPPED}')
    print()

    total_changed = 0
    total_skipped = 0
    total_missing = 0

    for page in all_pages:
        if not os.path.exists(page):
            print(f'  ?  {page}: file not found, skipping')
            total_missing += 1
            continue

        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()

        has_nav = page in PAGES_WITH_NAV
        new_content, log, changed = patch_html(content, has_nav, page)

        for line in log:
            print(line)

        if changed:
            total_changed += 1
            if not check_only:
                with open(page, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        else:
            total_skipped += 1

    print()
    if check_only:
        print(f'DRY-RUN complete: {total_changed} would be patched, {total_skipped} skipped, {total_missing} missing.')
        print('Run without --check to apply.')
    else:
        print(f'Done: {total_changed} patched, {total_skipped} skipped, {total_missing} missing.')
        print()
        print('Next steps:')
        print('  git diff --stat        # should show ONLY additions, no deletions')
        print('  git add -u             # only modified tracked files')
        print('  git commit -m "Add light theme + toggle across all pages"')
        print('  git push origin main')


if __name__ == '__main__':
    main()
