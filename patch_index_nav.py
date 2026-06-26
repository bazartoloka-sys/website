#!/usr/bin/env python3
"""
Патч навбару і футеру index.html
Запуск:
  python3 patch_index_nav.py --check   # dry-run
  python3 patch_index_nav.py           # застосувати
"""
import sys
import os

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r') as f:
    original = f.read()

content = original
changes = []

# ── 1. НАВБАР: додаємо Партнерам і Про нас ──────────────────────────────────
old_nav = '''  <div class="nlinks">
    <a href="/upgrade">Тарифи</a>
    <a href="/panas">Навчання</a>
    <a href="/blog">Блог</a>
    <a href="/support">Підтримка</a>
  </div>'''

new_nav = '''  <div class="nlinks">
    <a href="/upgrade">Тарифи</a>
    <a href="/panas">Навчання</a>
    <a href="/blog">Блог</a>
    <a href="/partners">Партнерам</a>
    <a href="/about">Про нас</a>
    <a href="/support">Підтримка</a>
  </div>'''

if old_nav in content:
    content = content.replace(old_nav, new_nav, 1)
    changes.append('✅ Навбар — додано Партнерам і Про нас')
elif new_nav in content:
    changes.append('⏭️  Навбар — вже пропатчено, пропускаємо')
else:
    changes.append('❌ Навбар — не знайдено, перевір вручну')

# ── 2. ФУТЕР: додаємо Блог, Про нас, Партнерам ──────────────────────────────
old_footer = '''    <div class="flinks">
      <a href="/privacy">Конфіденційність</a>
      <a href="/terms">Умови використання</a>
      <a href="/offer">Публічна оферта</a>
      <a href="/jobs">Вакансії</a>
    <a href="/upgrade">Тарифи</a>
      <a href="/support">Підтримка</a>
    </div>'''

new_footer = '''    <div class="flinks">
      <a href="/blog">Блог</a>
      <a href="/about">Про нас</a>
      <a href="/partners">Партнерам</a>
      <a href="/upgrade">Тарифи</a>
      <a href="/support">Підтримка</a>
      <a href="/privacy">Конфіденційність</a>
      <a href="/terms">Умови</a>
      <a href="/offer">Оферта</a>
      <a href="/jobs">Вакансії</a>
    </div>'''

if old_footer in content:
    content = content.replace(old_footer, new_footer, 1)
    changes.append('✅ Футер — оновлено посилання')
elif new_footer in content:
    changes.append('⏭️  Футер — вже пропатчено, пропускаємо')
else:
    changes.append('❌ Футер — не знайдено, перевір вручну')

# ── Звіт ─────────────────────────────────────────────────────────────────────
print(f'\n{"[DRY-RUN] " if DRY_RUN else ""}Патч index.html')
print(f'Файл: {PATH}  ({original.count(chr(10))+1} рядків)\n')
for c in changes:
    print(' ', c)

if DRY_RUN:
    print('\n→ Dry-run: файл НЕ змінено. Запусти без --check щоб застосувати.')
    sys.exit(0)

if content == original:
    print('\n→ Змін немає — файл не перезаписано.')
    sys.exit(0)

# Бекап
backup = PATH + '.bak'
with open(backup, 'w') as f:
    f.write(original)
print(f'\n  Бекап збережено: {backup}')

with open(PATH, 'w') as f:
    f.write(content)
print(f'  Файл оновлено: {PATH}')
print(f'  Рядків після патчу: {content.count(chr(10))+1}')
