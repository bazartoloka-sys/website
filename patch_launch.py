#!/usr/bin/env python3
"""
Патч index.html — launch-секція (живий файл ~1413 рядків).

Виправляє:
  1. 🔴 БАГ: submitLaunch шле в канал ІНВЕСТОРІВ (-1004471347053).
        Має слати в канал ПРОДАВЦІВ (-1003989090256).
  2. 🔴 Поле email → «Telegram або email» (менше тертя)
  3. 🔴 Розмитий оффер → конкретний з числом
  4. 🟡 Лічильник місць «Залишилось N зі 100»

Запуск:
  python3 patch_launch.py --check
  python3 patch_launch.py
"""

import sys, os, shutil

INDEX = "/home/boot/website/index.html"
DRY = "--check" in sys.argv

CHAT_SELLERS = "-1003989090256"   # канал «Продавці» — СЮДИ мають падати ліди з головної

PATCHES = []

# ── 1. SUB-ТЕКСТ: конкретний оффер ──────────────────────────────
PATCHES.append((
    '<p class="launch-sub">Перші продавці отримають спеціальну ціну і пріоритетне розміщення. Залиш email — повідомимо в день запуску.</p>',
    '<p class="launch-sub">Перші <strong>100 продавців</strong> отримують тариф «Майстер» безкоштовно на 3 місяці та пріоритетне розміщення в стрічці. <strong id="launchSpots" style="color:var(--amber)">Залишилось 53 місця</strong>.</p>'
))

# ── 2. ПОЛЕ EMAIL → Telegram/email ──────────────────────────────
PATCHES.append((
    '''    <div class="launch-email-wrap" id="launchForm">
      <input type="email" id="launchEmail" class="launch-email-input" placeholder="твій@email.com">
      <button class="launch-btn" onclick="submitLaunch()">ЗАПИСАТИСЬ →</button>
    </div>''',
    '''    <div class="launch-email-wrap" id="launchForm">
      <input type="text" id="launchEmail" class="launch-email-input" placeholder="Telegram (@нік) або email">
      <button class="launch-btn" onclick="submitLaunch()">ЗАЙНЯТИ МІСЦЕ →</button>
    </div>'''
))

# ── 3. SUCCESS-ТЕКСТ ────────────────────────────────────────────
PATCHES.append((
    '<div class="launch-ok" id="launchOk">✅ Записано! Повідомимо 1 серпня 🎉</div>',
    "<div class=\"launch-ok\" id=\"launchOk\">✅ Місце за вами! Зв'яжемось до 1 серпня 🎉</div>"
))

# ── 4. JS submitLaunch: канал продавців + поле контакту + лічильник ──
OLD_JS = '''function submitLaunch() {
  const emailEl = document.getElementById('launchEmail');
  const email = emailEl.value.trim();
  if (!email || !email.includes('@')) {
    emailEl.style.borderColor='#E24B4A';
    setTimeout(()=>emailEl.style.borderColor='',2000);
    return;
  }
  const btn = document.querySelector('.launch-btn');
  if (!btn) return;
  const text = '🚀 <b>ПІДПИСКА НА ЗАПУСК</b>\\n━━━━━━━━━━━━━━━━\\n'
    + '📧 <b>Email:</b> ' + email + '\\n'
    + '🕐 ' + new Date().toLocaleString('uk-UA',{timeZone:'Europe/Kyiv'});
  btn.disabled=true; btn.textContent='⏳...';
  fetch('https://api.telegram.org/bot8699311467:AAFxYGz3v1zW56B9Zpokq8NHl1UW_i1iz5M/sendMessage',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat_id:'-1004471347053',text:text,parse_mode:'HTML'})})
    .then(()=>{
      document.getElementById('launchForm').style.display='none';
      document.getElementById('launchOk').style.display='block';
    })
    .catch(()=>{
      document.getElementById('launchForm').style.display='none';
      document.getElementById('launchOk').style.display='block';
    });
}'''

NEW_JS = '''function submitLaunch() {
  const el = document.getElementById('launchEmail');
  const contact = el.value.trim();
  if (contact.length < 3) {
    el.style.borderColor='#E24B4A';
    setTimeout(()=>el.style.borderColor='',2000);
    return;
  }
  const btn = document.querySelector('.launch-btn');
  if (!btn) return;
  const text = '🌾 <b>НОВИЙ ПРОДАВЕЦЬ У ЧЕРЗІ</b>\\n━━━━━━━━━━━━━━━━\\n'
    + '📨 <b>Контакт:</b> ' + contact + '\\n'
    + '🕐 ' + new Date().toLocaleString('uk-UA',{timeZone:'Europe/Kyiv'})
    + '\\n🌐 bazar.in.ua → запуск';
  btn.disabled=true; btn.textContent='⏳...';
  // лічильник місць −1
  const spots = document.getElementById('launchSpots');
  if (spots) {
    const cur = parseInt((spots.textContent.match(/[0-9]+/) || ['0'])[0]);
    spots.textContent = 'Залишилось ' + Math.max(0, cur - 1) + ' місця';
  }
  fetch('https://api.telegram.org/bot8898378336:AAHAPpy5HFTxp5J58TfSP4HoVJkZVJiPHuM/sendMessage',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat_id:'%s',text:text,parse_mode:'HTML'})})
    .then(()=>{
      document.getElementById('launchForm').style.display='none';
      document.getElementById('launchOk').style.display='block';
    })
    .catch(()=>{
      document.getElementById('launchForm').style.display='none';
      document.getElementById('launchOk').style.display='block';
    });
}''' % CHAT_SELLERS

PATCHES.append((OLD_JS, NEW_JS))


def run():
    if not os.path.exists(INDEX):
        print(f"ПОМИЛКА: не знайдено {INDEX}"); sys.exit(1)
    with open(INDEX, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    for i,(old,new) in enumerate(PATCHES,1):
        c = content.count(old)
        if c == 0: errors.append(f"  Патч #{i}: НЕ ЗНАЙДЕНО")
        elif c > 1: errors.append(f"  Патч #{i}: знайдено {c}× (неоднозначно)")
    if errors:
        print("❌ Проблеми з якорями:")
        for e in errors: print(e)
        print("\nПокажи відповідні рядки index.html — підправлю якорі.")
        sys.exit(1)

    new_content = content
    for old,new in PATCHES:
        new_content = new_content.replace(old,new,1)

    # перевірка: токен бота продавців відрізняється від інвесторів
    seller_bot = "8898378336"
    invest_bot = "8699311467"

    if DRY:
        print("✅ DRY-RUN: всі 4 патчі знайдено.")
        print("\nЩо зміниться:")
        print(f"  1. 🔴 РОУТИНГ: ліди з головної → канал ПРОДАВЦІВ ({CHAT_SELLERS})")
        print(f"        (було помилково → канал інвесторів -1004471347053)")
        print(f"        бот: {invest_bot}(інвест) → {seller_bot}(продавці)")
        print("  2. 🔴 Поле email → «Telegram (@нік) або email»")
        print("  3. 🔴 Оффер: «100 продавців — Майстер безкоштовно 3 міс» + лічильник")
        print("  4. 🟡 Лічильник «Залишилось 53 місця» (−1 при кожному записі)")
        print("\nЗапусти без --check щоб застосувати.")
    else:
        bak = INDEX + ".bak_launch"
        shutil.copy2(INDEX, bak)
        print(f"📦 Бекап: {bak}")
        with open(INDEX,"w",encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Застосовано. {INDEX}")
        print("\nПеревір що працює, потім:")
        print("  git add index.html")
        print('  git commit -m "index: фікс роутингу лідів у канал продавців + оффер launch"')
        print("  git push")

if __name__ == "__main__":
    run()
