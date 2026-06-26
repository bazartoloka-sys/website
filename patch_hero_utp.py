#!/usr/bin/env python3
"""
1. Додає УТП чіпи після рядку 579 (hsub)
2. Додає кнопку Блогерам в hero-btns
  python3 patch_hero_utp.py --check
  python3 patch_hero_utp.py
"""
import sys

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

original_lines = lines[:]
changes = []

# ── 1. УТП чіпи — вставляємо після рядку з hsub ─────────────────────────────
hsub_idx = None
for i, l in enumerate(lines):
    if 'class="hsub"' in l and 'справжнє' in l:
        hsub_idx = i
        break

if hsub_idx is None:
    changes.append('❌ hsub не знайдено')
elif 'utp-chips' in ''.join(lines):
    changes.append('⏭️  УТП чіпи вже є')
else:
    utp = '''  <div class="utp-chips">
    <div class="utp-chip"><span>🇺🇦</span> 100% українські дані</div>
    <div class="utp-chip"><span>🤖</span> ШІ-захист 360°</div>
    <div class="utp-chip"><span>🪙</span> 0% комісії для виробника</div>
  </div>
'''
    lines.insert(hsub_idx + 1, utp)
    changes.append(f'✅ УТП чіпи вставлено після рядку {hsub_idx+1}')

# ── 2. Кнопка Блогерам в hero-btns ──────────────────────────────────────────
content = ''.join(lines)

OLD_BTNS = '      <a href="/upgrade" class="btn-upgrade-hero">🌾 ТАРИФИ ДЛЯ ПРОДАВЦІВ →</a>\n    </div>'
NEW_BTNS = '      <a href="/upgrade" class="btn-upgrade-hero">🌾 ТАРИФИ ДЛЯ ПРОДАВЦІВ →</a>\n      <a href="/partners" class="btn-partners-hero">🎬 БЛОГЕРАМ →</a>\n    </div>'

if OLD_BTNS in content:
    content = content.replace(OLD_BTNS, NEW_BTNS, 1)
    changes.append('✅ Кнопка БЛОГЕРАМ додана')
elif 'btn-partners-hero' in content:
    changes.append('⏭️  Кнопка вже є')
else:
    changes.append('❌ hero-btns не знайдено')

# ── 3. CSS ───────────────────────────────────────────────────────────────────
if '.utp-chips' not in content:
    css = '''
/* УТП чіпи */
.utp-chips{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:16px 0 24px}
.utp-chip{display:inline-flex;align-items:center;gap:6px;background:rgba(245,230,200,.06);border:1px solid rgba(245,230,200,.12);border-radius:100px;padding:6px 14px;font-size:12px;font-weight:700;color:var(--cream2);letter-spacing:.3px}
.utp-chip span{font-size:14px}
:root[data-theme="light"] .utp-chip{background:rgba(26,15,8,.05);border-color:rgba(26,15,8,.12)}
/* Кнопка блогерам */
.btn-partners-hero{display:inline-flex;align-items:center;gap:8px;background:transparent;border:1px solid var(--aborder);color:var(--amber);font-family:'Unbounded',sans-serif;font-size:11px;font-weight:700;padding:12px 22px;border-radius:100px;transition:all .2s;letter-spacing:.5px}
.btn-partners-hero:hover{background:rgba(232,160,48,.08);border-color:var(--amber)}'''
    content = content.replace('</style>', css + '\n</style>', 1)
    changes.append('✅ CSS додано')
else:
    changes.append('⏭️  CSS вже є')

# ── Звіт ─────────────────────────────────────────────────────────────────────
print('\n{}Патч: УТП чіпи + кнопка Блогерам'.format('[DRY-RUN] ' if DRY_RUN else ''))
print('Файл: {}  ({} рядків)\n'.format(PATH, len(original_lines)))
for c in changes:
    print(' ', c)

if DRY_RUN:
    print('\n→ Dry-run: НЕ змінено.')
    sys.exit(0)

if content == ''.join(original_lines):
    print('\n→ Змін немає.')
    sys.exit(0)

with open(PATH+'.bak4','w',encoding='utf-8') as f:
    f.writelines(original_lines)
with open(PATH,'w',encoding='utf-8') as f:
    f.write(content)
print('\n  Готово. Рядків: {}'.format(content.count('\n')+1))
