#!/usr/bin/env python3
"""
Видаляє залишок invest-form з index.html (рядки 954-972 приблизно).
  python3 patch_remove_invest_form.py --check
  python3 patch_remove_invest_form.py
"""
import sys

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r', encoding='utf-8') as f:
    original = f.read()

OLD = '''    <div class="invest-form">
      <div class="iform-title">📩 Залишити заявку</div>
      <div class="field"><label>Ваше ім'я</label><input type="text" placeholder="Іван Петренко"></div>
      <div class="field"><label>Email</label><input type="email" placeholder="ivan@example.com"></div>
      <div class="field"><label>Я цікавлюсь як</label>
        <select>
          <option>Інвестор — хочу вкласти кошти</option>
          <option>Партнер — хочу співпрацювати</option>
          <option>Медіа — хочу написати про проект</option>
          <option>Інше</option>
        </select>
      </div>
      <div class="field"><label>Коротко про себе</label><textarea placeholder="Розкажіть хто ви і чим можете бути корисні проекту..."></textarea></div>
      <button class="btn-invest" onclick="handleInvestForm(event)">НАДІСЛАТИ ЗАЯВКУ →</button>
      <p class="iform-note">Відповідаємо протягом 24 годин · <a href="mailto:bazartoloka@gmail.com" style="color:var(--cream2)">bazartoloka@gmail.com</a></p>
    </div>
  </div>
</div>'''

NEW = '''</div>'''

content = original
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('✅ invest-form видалено')
else:
    print('❌ не знайдено — перевір вручну')
    sys.exit(1)

if DRY_RUN:
    print('→ Dry-run: НЕ змінено.')
    sys.exit(0)

with open(PATH+'.bak7','w',encoding='utf-8') as f:
    f.write(original)
with open(PATH,'w',encoding='utf-8') as f:
    f.write(content)
print('Готово. Рядків: {}'.format(content.count('\n')+1))
