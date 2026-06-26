#!/usr/bin/env python3
"""
Замінює seller-sec на блок 5 навігаційних плашок.
  python3 patch_nav_cards.py --check
  python3 patch_nav_cards.py
"""
import sys

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r', encoding='utf-8') as f:
    original = f.read()

content = original
changes = []

# ── 1. Замінюємо seller-sec ──────────────────────────────────────────────────
OLD = '''<div class="seller-sec">
  <h2>🌾 Ти продаєш?</h2>
  <p>1 фото + 1 відео на місяць безкоштовно.<br>Реєстрація через Google за 30 секунд.</p>
  <a href="#launch" class="btn-seller">🌾 ЗАПИСАТИСЬ У ПЕРШИЙ СПИСОК →</a>
</div>'''

NEW = '''<!-- НАВ ПЛАШКИ -->
<div class="nav-cards-sec">
  <div class="nav-cards-label">Досліджуй Базар Толока</div>
  <div class="nav-cards-grid">

    <a href="/partners" class="nav-card nav-card-amber">
      <div class="nc-icon">🤝</div>
      <div class="nc-content">
        <div class="nc-title">Партнерам та блогерам</div>
        <div class="nc-desc">Увійди в проект, стань акредитованим партнером або навчальним експертом платформи</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

    <a href="/panas" class="nav-card nav-card-green">
      <div class="nc-icon">🎓</div>
      <div class="nc-content">
        <div class="nc-title">Навчання продавців</div>
        <div class="nc-desc">Панас відповідає — покрокові пояснення як продавати, отримувати 5 зірок і уникати помилок</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

    <a href="/blog" class="nav-card">
      <div class="nc-icon">📝</div>
      <div class="nc-content">
        <div class="nc-title">Блог</div>
        <div class="nc-desc">Аналітика ринку, поради для продавців, новини платформи та порівняння з конкурентами</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

    <a href="/about" class="nav-card">
      <div class="nc-icon">🇺🇦</div>
      <div class="nc-content">
        <div class="nc-title">Про нас</div>
        <div class="nc-desc">Місія, цінності, команда і юридичний статус — хто стоїть за Базар Толока</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

    <a href="/upgrade" class="nav-card nav-card-wide">
      <div class="nc-icon">💎</div>
      <div class="nc-content">
        <div class="nc-title">Тарифи та підписка</div>
        <div class="nc-desc">Господар, Майстер, Крамар, Купець — порівняй плани і обери свій. Перший місяць безкоштовно.</div>
      </div>
      <div class="nc-arrow">→</div>
    </a>

  </div>
</div>'''

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    changes.append('✅ seller-sec замінено на 5 навігаційних плашок')
elif 'nav-cards-sec' in content:
    changes.append('⏭️  nav-cards вже є')
else:
    changes.append('❌ seller-sec не знайдено')

# ── 2. CSS ───────────────────────────────────────────────────────────────────
if '.nav-cards-sec' not in content:
    css = '''
/* Навігаційні плашки */
.nav-cards-sec{margin:0 5% 48px}
.nav-cards-label{font-size:11px;font-weight:700;letter-spacing:2px;color:var(--green);text-transform:uppercase;text-align:center;margin-bottom:20px}
.nav-cards-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.nav-card{display:flex;align-items:center;gap:16px;background:var(--clay2);border:1px solid var(--border);border-radius:18px;padding:20px 22px;transition:all .2s;cursor:pointer}
.nav-card:hover{border-color:rgba(245,230,200,.18);transform:translateY(-2px)}
.nav-card-amber{border-color:var(--aborder)}
.nav-card-amber:hover{background:rgba(232,160,48,.05);border-color:var(--amber)}
.nav-card-green{border-color:var(--gborder)}
.nav-card-green:hover{background:rgba(46,204,142,.05);border-color:var(--green)}
.nav-card-wide{grid-column:1/-1}
.nc-icon{font-size:28px;flex-shrink:0;width:44px;text-align:center}
.nc-content{flex:1}
.nc-title{font-family:'Unbounded',sans-serif;font-size:14px;font-weight:700;color:var(--cream);margin-bottom:5px;line-height:1.3}
.nav-card-amber .nc-title{color:var(--amber)}
.nav-card-green .nc-title{color:var(--green)}
.nc-desc{font-size:12px;color:var(--cream3);line-height:1.6}
.nc-arrow{font-size:18px;color:var(--cream4);flex-shrink:0;transition:transform .2s}
.nav-card:hover .nc-arrow{transform:translateX(4px);color:var(--amber)}
:root[data-theme="light"] .nav-card{background:#EFD9B0}
@media(max-width:600px){
  .nav-cards-grid{grid-template-columns:1fr}
  .nav-card-wide{grid-column:auto}
}'''
    content = content.replace('</style>', css + '\n</style>', 1)
    changes.append('✅ CSS додано')
else:
    changes.append('⏭️  CSS вже є')

# ── Звіт ─────────────────────────────────────────────────────────────────────
print('\n{}Патч: навігаційні плашки'.format('[DRY-RUN] ' if DRY_RUN else ''))
print('Файл: {}  ({} рядків)\n'.format(PATH, original.count('\n')+1))
for c in changes:
    print(' ', c)

if DRY_RUN:
    print('\n→ Dry-run: НЕ змінено.')
    sys.exit(0)

if content == original:
    print('\n→ Змін немає.')
    sys.exit(0)

with open(PATH+'.bak5','w',encoding='utf-8') as f:
    f.write(original)
with open(PATH,'w',encoding='utf-8') as f:
    f.write(content)
print('\n  Готово. Рядків: {}'.format(content.count('\n')+1))
