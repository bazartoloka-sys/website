#!/usr/bin/env python3
"""
1. Замінює invest-sec на коротку teaser-плашку → /invest
2. Додає 6-ту nav-card «Інвесторам»
  python3 patch_invest.py --check
  python3 patch_invest.py
"""
import sys, re

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r', encoding='utf-8') as f:
    original = f.read()

content = original
changes = []

# ── 1. Замінюємо весь invest-sec ─────────────────────────────────────────────
pattern = r'<div class="invest-sec" id="invest">.*?</div>\s*</div>\s*</div>'
match = re.search(pattern, content, re.DOTALL)

if match:
    new_invest = '''<div class="invest-teaser" id="invest">
  <div class="invest-teaser-inner">
    <div>
      <div class="it-chip">💰 Інвесторам та партнерам</div>
      <h2 class="it-title">Увійди в проект<br><em>поки ринок вільний</em></h2>
      <p class="it-desc">Будуємо національну інфраструктуру довіри для мільйонів угод між українцями. Відкриті до інвесторів, стратегічних партнерів і медіа.</p>
    </div>
    <div class="it-stats">
      <div class="it-stat"><span>🇺🇦</span><div>Ukraine-first</div></div>
      <div class="it-stat"><span>4</span><div>Платіжних системи</div></div>
      <div class="it-stat"><span>0₴</span><div>Вхід для продавця</div></div>
      <div class="it-stat"><span>🤖</span><div>ШІ-модерація</div></div>
    </div>
    <a href="/invest" class="it-btn">ДЕТАЛЬНІШЕ ТА ЗАЛИШИТИ ЗАЯВКУ →</a>
  </div>
</div>'''
    content = content[:match.start()] + new_invest + content[match.end():]
    changes.append('✅ invest-sec замінено на teaser-плашку')
else:
    changes.append('❌ invest-sec не знайдено')

# ── 2. Додаємо 6-ту nav-card «Інвесторам» перед закриваючим </div> сітки ────
OLD_NAV_END = '''    <a href="/upgrade" class="nav-card nav-card-wide">
      <div class="nc-icon">💎</div>
      <div class="nc-content">
        <div class="nc-title">Тарифи та підписка</div>
        <div class="nc-desc">Господар, Майстер, Крамар, Купець — порівняй плани і обери свій. Перший місяць безкоштовно.</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

  </div>
</div>'''

NEW_NAV_END = '''    <a href="/upgrade" class="nav-card nav-card-wide">
      <div class="nc-icon">💎</div>
      <div class="nc-content">
        <div class="nc-title">Тарифи та підписка</div>
        <div class="nc-desc">Господар, Майстер, Крамар, Купець — порівняй плани і обери свій. Перший місяць безкоштовно.</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

    <a href="/invest" class="nav-card nav-card-wide" style="border-color:var(--aborder)">
      <div class="nc-icon">💰</div>
      <div class="nc-content">
        <div class="nc-title" style="color:var(--amber)">Інвесторам та партнерам</div>
        <div class="nc-desc">Входь у проект поки ринок вільний — інвестори, стратегічні партнери і медіа. Відповідаємо протягом 24 годин.</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

  </div>
</div>'''

if OLD_NAV_END in content:
    content = content.replace(OLD_NAV_END, NEW_NAV_END, 1)
    changes.append('✅ 6-та nav-card «Інвесторам» додана')
elif '/invest' in content:
    changes.append('⏭️  nav-card інвесторам вже є')
else:
    changes.append('❌ nav-cards-grid не знайдено')

# ── 3. CSS для teaser ────────────────────────────────────────────────────────
if '.invest-teaser' not in content:
    css = '''
/* Invest teaser */
.invest-teaser{margin:0 5% 48px;border-radius:24px;border:1px solid var(--aborder);background:var(--clay2);overflow:hidden}
.invest-teaser::before{content:'';display:block;height:4px;background:linear-gradient(90deg,var(--amber),rgba(232,160,48,.2),var(--amber))}
.invest-teaser-inner{padding:32px 28px;display:flex;flex-direction:column;gap:24px}
.it-chip{display:inline-flex;align-items:center;gap:7px;background:rgba(232,160,48,.12);border:1px solid var(--aborder);border-radius:100px;padding:5px 16px;font-size:10px;font-weight:700;color:var(--amber);letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;width:fit-content}
.it-title{font-family:'Unbounded',sans-serif;font-size:clamp(22px,4vw,32px);font-weight:900;line-height:1.1;margin-bottom:10px}
.it-title em{color:var(--amber);font-style:normal}
.it-desc{font-size:14px;color:var(--cream2);line-height:1.7;max-width:560px}
.it-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.it-stat{text-align:center;padding:14px 8px;background:var(--clay3);border-radius:14px;border:1px solid var(--border)}
.it-stat span{font-family:'Unbounded',sans-serif;font-size:22px;font-weight:900;color:var(--amber);display:block;margin-bottom:6px}
.it-stat div{font-size:11px;color:var(--cream3);font-weight:700;line-height:1.3}
.it-btn{display:inline-block;background:var(--amber);color:#1A0800;font-family:'Unbounded',sans-serif;font-size:11px;font-weight:700;padding:14px 28px;border-radius:100px;transition:opacity .2s;text-align:center;width:fit-content}
.it-btn:hover{opacity:.88}
:root[data-theme="light"] .invest-teaser{background:#EFD9B0}
:root[data-theme="light"] .it-stat{background:#E8CFA0}
@media(max-width:600px){.it-stats{grid-template-columns:repeat(2,1fr)}}'''
    content = content.replace('</style>', css + '\n</style>', 1)
    changes.append('✅ CSS teaser додано')
else:
    changes.append('⏭️  CSS вже є')

# ── Звіт ─────────────────────────────────────────────────────────────────────
print('\n{}Патч: invest teaser + 6-та nav-card'.format('[DRY-RUN] ' if DRY_RUN else ''))
print('Файл: {}  ({} рядків)\n'.format(PATH, original.count('\n')+1))
for c in changes:
    print(' ', c)

if DRY_RUN:
    print('\n→ Dry-run: НЕ змінено.')
    sys.exit(0)

if content == original:
    print('\n→ Змін немає.')
    sys.exit(0)

with open(PATH+'.bak6','w',encoding='utf-8') as f:
    f.write(original)
with open(PATH,'w',encoding='utf-8') as f:
    f.write(content)
print('\n  Готово. Рядків: {}'.format(content.count('\n')+1))
