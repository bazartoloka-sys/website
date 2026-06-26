#!/usr/bin/env python3
"""
Патч index.html — зростаючий лічильник «ВЖЕ В ЧЕРЗІ» для ажіотажу + реальний оффер.

Логіка:
  • Старт 108 (на 26.06.2026). Щодня детерміновано додається +10…30.
  • Число СТАБІЛЬНЕ в межах дня (добре для скріншотів у соцмережі).
  • Кнопка «Зайняти місце» → +1 миттєво.
  • Countdown тікає до 1.08.26 = кінець акції.
  • Оффер: потрійний бонус (за 1 грн → +3 грн), 70% гроші / 30% бонуси.

Запуск:
  python3 patch_queue.py --check
  python3 patch_queue.py
"""
import sys, os, shutil

INDEX = "/home/boot/website/index.html"
DRY = "--check" in sys.argv

PATCHES = []

# ═══════════════════════════════════════════════════════════════
# 1. SUB-ТЕКСТ → реальний оффер (прибираємо старий launchSpots звідси)
# ═══════════════════════════════════════════════════════════════
PATCHES.append((
    '<p class="launch-sub">Перші <strong>100 продавців</strong> отримують тариф «Майстер» безкоштовно на 3 місяці та пріоритетне розміщення в стрічці. <strong id="launchSpots" style="color:var(--amber)">Залишилось 53 місця</strong>.</p>',
    '<p class="launch-sub">Перші <strong>1000 продавців</strong> отримують потрійний бонус: за кожну гривню на бонусний рахунок зараховуємо <strong>+3 грн</strong>. Бонусами оплачуєте до 30% будь-якої послуги чи реклами (70% гроші / 30% бонуси).</p>'
))

# ═══════════════════════════════════════════════════════════════
# 2. КРУПНИЙ ЛІЧИЛЬНИК-БЛОК — вставляємо ПЕРЕД countdown (.launch-cd)
# ═══════════════════════════════════════════════════════════════
PATCHES.append((
    '''    <div class="launch-cd">
      <div class="launch-cd-block"><span class="launch-cd-num" id="l-days">--</span><div class="launch-cd-unit">днів</div></div>''',
    '''    <div class="queue-box">
      <div class="queue-label">🔥 ВЖЕ В ЧЕРЗІ</div>
      <div class="queue-num" id="queueNum">108</div>
      <div class="queue-sub">продавців із <strong>1000</strong> першої хвилі</div>
      <div class="queue-bar"><div class="queue-bar-fill" id="queueBar"></div></div>
    </div>
    <div class="launch-cd-caption">⏳ До кінця акції · 1 серпня 2026</div>
    <div class="launch-cd">
      <div class="launch-cd-block"><span class="launch-cd-num" id="l-days">--</span><div class="launch-cd-unit">днів</div></div>'''
))

# ═══════════════════════════════════════════════════════════════
# 3. CSS — стилі крупного лічильника (вставляємо після .launch-cd-unit)
# ═══════════════════════════════════════════════════════════════
PATCHES.append((
    '.launch-cd-unit{font-size:10px;color:var(--cream3);margin-top:6px;letter-spacing:1px;text-transform:uppercase}',
    '''.launch-cd-unit{font-size:10px;color:var(--cream3);margin-top:6px;letter-spacing:1px;text-transform:uppercase}
.queue-box{background:linear-gradient(135deg,rgba(232,160,48,.12),rgba(46,204,142,.08));border:1px solid var(--aborder);border-radius:24px;padding:28px 24px;margin:0 auto 24px;max-width:420px}
.queue-label{font-family:'Unbounded',sans-serif;font-size:12px;font-weight:700;color:var(--amber);letter-spacing:2px;margin-bottom:10px}
.queue-num{font-family:'Unbounded',sans-serif;font-size:clamp(64px,14vw,96px);font-weight:900;color:var(--amber);line-height:.95;letter-spacing:-2px;text-shadow:0 4px 24px rgba(232,160,48,.3)}
.queue-sub{font-size:14px;color:var(--cream2);margin-top:8px}
.queue-sub strong{color:var(--cream)}
.queue-bar{height:8px;background:rgba(245,230,200,.08);border-radius:100px;margin-top:16px;overflow:hidden}
.queue-bar-fill{height:100%;background:linear-gradient(90deg,var(--amber),var(--green));border-radius:100px;width:11%;transition:width 1s ease}
.launch-cd-caption{font-size:11px;color:var(--cream3);letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;font-weight:700}'''
))

# ═══════════════════════════════════════════════════════════════
# 4. JS submitLaunch: лічильник +1 (прибрати старий −1 launchSpots)
# ═══════════════════════════════════════════════════════════════
PATCHES.append((
    '''  btn.disabled=true; btn.textContent='⏳...';
  // лічильник місць −1
  const spots = document.getElementById('launchSpots');
  if (spots) {
    const cur = parseInt((spots.textContent.match(/[0-9]+/) || ['0'])[0]);
    spots.textContent = 'Залишилось ' + Math.max(0, cur - 1) + ' місця';
  }''',
    '''  btn.disabled=true; btn.textContent='⏳...';
  // лічильник черги +1
  const qn = document.getElementById('queueNum');
  if (qn) {
    const cur = parseInt((qn.textContent.match(/[0-9]+/) || ['0'])[0]) || 0;
    qn.textContent = cur + 1;
    const bar = document.getElementById('queueBar');
    if (bar) bar.style.width = Math.min(100, ((cur + 1) / 1000) * 100) + '%';
  }'''
))

# ═══════════════════════════════════════════════════════════════
# 5. JS — детермінований денний приріст лічильника (вставляємо перед submitLaunch)
# ═══════════════════════════════════════════════════════════════
PATCHES.append((
    'function submitLaunch() {',
    '''// ── Зростаючий лічильник черги (детермінований по днях) ──
(function initQueue(){
  var startDate = new Date(2026, 5, 26); // 26.06.2026 (місяць 0-індекс)
  var base = 108;
  var today = new Date();
  var days = Math.max(0, Math.floor((today - startDate) / 86400000));
  var total = base;
  for (var i = 1; i <= days; i++) {
    // детермінований псевдо-приріст 10..30 на день i
    var seed = (i * 9301 + 49297) % 233280;
    var rnd = seed / 233280;
    total += 10 + Math.floor(rnd * 21); // 10..30
  }
  if (total > 980) total = 980; // не перевищуємо 1000 до кінця акції
  var qn = document.getElementById('queueNum');
  if (qn) qn.textContent = total;
  var bar = document.getElementById('queueBar');
  if (bar) bar.style.width = Math.min(100, (total / 1000) * 100) + '%';
})();

function submitLaunch() {'''
))


def run():
    if not os.path.exists(INDEX):
        print(f"ПОМИЛКА: не знайдено {INDEX}"); sys.exit(1)
    with open(INDEX,"r",encoding="utf-8") as f:
        content = f.read()

    errors=[]
    for i,(old,new) in enumerate(PATCHES,1):
        c=content.count(old)
        if c==0: errors.append(f"  Патч #{i}: НЕ ЗНАЙДЕНО")
        elif c>1: errors.append(f"  Патч #{i}: знайдено {c}× (неоднозначно)")
    if errors:
        print("❌ Проблеми з якорями:")
        for e in errors: print(e)
        sys.exit(1)

    nc=content
    for old,new in PATCHES:
        nc=nc.replace(old,new,1)

    if DRY:
        print("✅ DRY-RUN: всі 5 патчів знайдено.")
        print("\nЩо зміниться:")
        print("  1. Sub-текст → реальний оффер (потрійний бонус, 70/30)")
        print("  2. Крупний блок «ВЖЕ В ЧЕРЗІ: 108» (для скріншотів) + прогрес-бар")
        print("  3. CSS крупного лічильника (64-96px, amber, тінь)")
        print("  4. submitLaunch → лічильник +1 при записі")
        print("  5. JS денного приросту (старт 108, +10…30/день, стеля 980)")
        print("\n  Countdown лишається = відлік до 1.08.26 (кінець акції)")
        print("\nЗапусти без --check щоб застосувати.")
    else:
        bak=INDEX+".bak_queue"
        shutil.copy2(INDEX,bak)
        print(f"📦 Бекап: {bak}")
        with open(INDEX,"w",encoding="utf-8") as f:
            f.write(nc)
        print("✅ Застосовано.")
        print("\n  git add index.html")
        print('  git commit -m "index: зростаючий лічильник черги + реальний оффер бонусу"')
        print("  git push")

if __name__=="__main__":
    run()
