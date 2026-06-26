#!/usr/bin/env python3
"""
Замінює намальований phone-section на карусель реальних скріншотів.
Блок <!-- СКРІНШОТИ --> також видаляється (він стає частиною нової карусель).

Запуск:
  python3 patch_carousel.py --check   # dry-run
  python3 patch_carousel.py           # застосувати
"""
import sys

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r') as f:
    original = f.read()

content = original
changes = []

# ── СТАРИЙ БЛОК: намальований телефон + окремі скріншоти ────────────────────
OLD = '''<div class="phone-section">
  <div class="sh">
    <div class="sl">Як це виглядає</div>
    <h2 class="st">Живий додаток</h2>
    <p class="ss">TikTok-стрічка товарів, ШІ-пошук і захист — все в одному екрані</p>
  </div>
  <div class="phone-wrap">
    <div class="float-chip left" style="top:60px">🛡 Захист 360°</div>
    <div class="float-chip left" style="top:160px">⭐ Рейтинг ×2</div>
    <div class="float-chip left" style="top:260px">🤖 ШІ Пошук</div>
    <div class="float-chip right" style="top:60px">🎬 TikTok формат</div>
    <div class="float-chip right" style="top:160px">🎓 Навчання</div>
    <div class="float-chip right" style="top:260px">📢 Авто-реклама</div>
    <div class="phone">
      <div class="phone-screen">
        <div class="screen-header">
          <div class="screen-logo">БАЗАР.</div>
          <div class="screen-icons">
            <div class="sdot"></div>
            <div class="sdot" style="opacity:.4"></div>
            <div class="sdot" style="opacity:.2"></div>
          </div>
        </div>
        <div class="ai-search">
          <div class="ai-icon">✦</div>
          <div class="ai-text">ШІ пошук — просто напишіть...</div>
          <div class="ai-dot"></div>
        </div>
        <div class="video-card">
          <div class="video-bg"></div>
          <div class="tiktok-badge">▶ ВІДЕО</div>
          <div class="play-btn">▶</div>
          <div class="video-labels">
            <div class="video-action"><div class="video-action-icon">❤</div><span>2.4к</span></div>
            <div class="video-action"><div class="video-action-icon">💬</div><span>89</span></div>
            <div class="video-action"><div class="video-action-icon">↗</div><span>Share</span></div>
          </div>
          <div class="video-info">
            <div class="video-title">Свіжі овочі з поля 🌿<br>Без хімії. Вінниця</div>
            <div class="video-price">180 грн/кг</div>
          </div>
        </div>
        <div class="rating-card">
          <div class="avatar">👨‍🌾</div>
          <div class="rating-info">
            <div class="rating-name">Петро Коваленко</div>
            <div class="stars">★★★★★ <span style="color:var(--cream3);font-size:9px">Продавець</span></div>
          </div>
          <div class="rating-badge">4.9</div>
        </div>
        <div class="shield-row">
          <div class="shield-chip"><span>🛡</span>Захист</div>
          <div class="shield-chip"><span>🔒</span>Дані схов.</div>
          <div class="shield-chip"><span>✅</span>Верифік.</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- СКРІНШОТИ -->
<div style="padding:40px 5% 0;max-width:900px;margin:0 auto">
  <div class="sh" style="text-align:center;margin-bottom:24px">
    <div class="sl">Реальний додаток</div>
    <h2 class="st">Скріншоти</h2>
  </div>
  <div style="display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;padding-bottom:8px">
    <div style="flex-shrink:0;width:160px;background:var(--clay2);border-radius:20px;border:1px solid rgba(232,160,48,.15);overflow:hidden">
      <img src="screen_splash.png" alt="Вхід" style="width:100%;display:block">
      <div style="padding:6px 10px;font-size:10px;color:var(--cream2);font-weight:700">🌸 Вхід</div>
    </div>
    <div style="flex-shrink:0;width:160px;background:var(--clay2);border-radius:20px;border:1px solid rgba(232,160,48,.15);overflow:hidden">
      <img src="screen_cabinet.png" alt="Кабінет" style="width:100%;display:block">
      <div style="padding:6px 10px;font-size:10px;color:var(--cream2);font-weight:700">🏪 Кабінет продавця</div>
    </div>
    <div style="flex-shrink:0;width:160px;background:var(--clay2);border-radius:20px;border:1px solid rgba(232,160,48,.15);overflow:hidden">
      <img src="screen_feed.png" alt="Товар" style="width:100%;display:block">
      <div style="padding:6px 10px;font-size:10px;color:var(--cream2);font-weight:700">🐐 Екран товару</div>
    </div>
    <div style="flex-shrink:0;width:160px;background:var(--clay2);border-radius:20px;border:1px solid rgba(232,160,48,.15);overflow:hidden">
      <img src="buy.png" alt="Покупець" style="width:100%;display:block">
      <div style="padding:6px 10px;font-size:10px;color:var(--cream2);font-weight:700">🛍️ Кабінет покупця</div>
    </div>
    <div style="flex-shrink:0;width:160px;background:var(--clay2);border-radius:20px;border:1px solid rgba(232,160,48,.15);overflow:hidden">
      <img src="screen_payment.png" alt="Оплата" style="width:100%;display:block">
      <div style="padding:6px 10px;font-size:10px;color:var(--cream2);font-weight:700">💳 Способи оплати</div>
    </div>
    <div style="flex-shrink:0;width:160px;background:var(--clay2);border-radius:20px;border:1px solid rgba(232,160,48,.15);overflow:hidden">
      <img src="accounts.png" alt="Рахунки" style="width:100%;display:block">
      <div style="padding:6px 10px;font-size:10px;color:var(--cream2);font-weight:700">🏦 Рахунки виплат</div>
    </div>
  </div>
</div>'''

# ── НОВИЙ БЛОК: карусель скріншотів ─────────────────────────────────────────
NEW = '''<!-- КАРУСЕЛЬ СКРІНШОТІВ -->
<div class="carousel-sec">
  <div class="sh" style="text-align:center;margin-bottom:36px">
    <div class="sl">Реальний додаток</div>
    <h2 class="st">Живий додаток</h2>
    <p class="ss">TikTok-стрічка товарів, ШІ-пошук і захист — все в одному екрані</p>
  </div>

  <div class="carousel-wrap">
    <!-- Кнопки навігації -->
    <button class="car-btn car-prev" onclick="carMove(-1)" aria-label="Назад">&#8592;</button>
    <button class="car-btn car-next" onclick="carMove(1)" aria-label="Вперед">&#8594;</button>

    <!-- Трек -->
    <div class="car-track-wrap">
      <div class="car-track" id="carTrack">

        <div class="car-slide">
          <div class="car-phone">
            <img src="screen_splash.png" alt="Екран входу" loading="lazy">
          </div>
          <div class="car-caption">
            <div class="car-cap-icon">🌸</div>
            <div class="car-cap-title">Екран входу</div>
            <div class="car-cap-desc">Авторизація через Google за 1 дотик. Без SMS, без паролів.</div>
          </div>
        </div>

        <div class="car-slide">
          <div class="car-phone">
            <img src="screen_cabinet.png" alt="Кабінет продавця" loading="lazy">
          </div>
          <div class="car-caption">
            <div class="car-cap-icon">🏪</div>
            <div class="car-cap-title">Кабінет продавця</div>
            <div class="car-cap-desc">Статистика, оголошення і замовлення — все в одному місці.</div>
          </div>
        </div>

        <div class="car-slide">
          <div class="car-phone">
            <img src="screen_feed.png" alt="Стрічка товарів" loading="lazy">
          </div>
          <div class="car-caption">
            <div class="car-cap-icon">🐐</div>
            <div class="car-cap-title">Стрічка товарів</div>
            <div class="car-cap-desc">TikTok-формат: гортай вертикально, купуй одним кліком.</div>
          </div>
        </div>

        <div class="car-slide">
          <div class="car-phone">
            <img src="buy.png" alt="Кабінет покупця" loading="lazy">
          </div>
          <div class="car-caption">
            <div class="car-cap-icon">🛍️</div>
            <div class="car-cap-title">Кабінет покупця</div>
            <div class="car-cap-desc">Замовлення, статус доставки і захист платежу в реальному часі.</div>
          </div>
        </div>

        <div class="car-slide">
          <div class="car-phone">
            <img src="screen_payment.png" alt="Способи оплати" loading="lazy">
          </div>
          <div class="car-caption">
            <div class="car-cap-icon">💳</div>
            <div class="car-cap-title">Оплата</div>
            <div class="car-cap-desc">4 способи: картка, NovaPay ескроу, НП Кредит, переказ на ФОП.</div>
          </div>
        </div>

        <div class="car-slide">
          <div class="car-phone">
            <img src="accounts.png" alt="Рахунки виплат" loading="lazy">
          </div>
          <div class="car-caption">
            <div class="car-cap-icon">🏦</div>
            <div class="car-cap-title">Рахунки виплат</div>
            <div class="car-cap-desc">Продавець підключає банківський рахунок і отримує виплати автоматично.</div>
          </div>
        </div>

      </div>
    </div>

    <!-- Індикатори -->
    <div class="car-dots" id="carDots">
      <button class="car-dot active" onclick="carGoTo(0)"></button>
      <button class="car-dot" onclick="carGoTo(1)"></button>
      <button class="car-dot" onclick="carGoTo(2)"></button>
      <button class="car-dot" onclick="carGoTo(3)"></button>
      <button class="car-dot" onclick="carGoTo(4)"></button>
      <button class="car-dot" onclick="carGoTo(5)"></button>
    </div>
  </div>
</div>

<style>
.carousel-sec{padding:60px 0 0;overflow:hidden}
.carousel-wrap{position:relative;max-width:900px;margin:0 auto;padding:0 5%}
.car-track-wrap{overflow:hidden;border-radius:24px}
.car-track{display:flex;transition:transform .42s cubic-bezier(.4,0,.2,1)}
.car-slide{min-width:100%;display:flex;align-items:center;justify-content:center;gap:40px;padding:0 8px}
.car-phone{flex-shrink:0;width:200px;border-radius:32px;overflow:hidden;border:2px solid rgba(232,160,48,.25);box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 40px rgba(232,160,48,.06)}
.car-phone img{width:100%;display:block}
.car-caption{max-width:280px;text-align:left}
.car-cap-icon{font-size:36px;margin-bottom:12px}
.car-cap-title{font-family:'Unbounded',sans-serif;font-size:20px;font-weight:900;color:var(--cream);margin-bottom:10px;line-height:1.2}
.car-cap-desc{font-size:15px;color:var(--cream2);line-height:1.7}
.car-btn{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;background:var(--clay2);border:1px solid var(--aborder);color:var(--amber);font-size:18px;cursor:pointer;transition:all .2s;z-index:10;display:flex;align-items:center;justify-content:center}
.car-btn:hover{background:rgba(232,160,48,.12);border-color:var(--amber)}
.car-prev{left:0}
.car-next{right:0}
.car-dots{display:flex;justify-content:center;gap:8px;margin-top:28px}
.car-dot{width:8px;height:8px;border-radius:50%;background:var(--clay3);border:1px solid var(--border);cursor:pointer;transition:all .2s;padding:0}
.car-dot.active{background:var(--amber);border-color:var(--amber);width:24px;border-radius:4px}
@media(max-width:600px){
  .car-slide{flex-direction:column;gap:24px;padding:0 4px}
  .car-phone{width:160px}
  .car-caption{text-align:center;max-width:100%}
  .car-btn{display:none}
}
</style>

<script>
(function(){
  let cur = 0;
  const total = 6;
  const track = document.getElementById('carTrack');
  const dots = document.querySelectorAll('.car-dot');

  function update(){
    track.style.transform = 'translateX(-' + (cur * 100) + '%)';
    dots.forEach((d,i) => d.classList.toggle('active', i === cur));
  }

  window.carMove = function(dir){
    cur = (cur + dir + total) % total;
    update();
  };
  window.carGoTo = function(i){
    cur = i;
    update();
  };

  // Свайп на мобільному
  let startX = 0;
  track.addEventListener('touchstart', e => startX = e.touches[0].clientX, {passive:true});
  track.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) carMove(dx < 0 ? 1 : -1);
  }, {passive:true});

  // Авто-прокрутка кожні 4 сек
  setInterval(() => carMove(1), 4000);
})();
</script>'''

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    changes.append('✅ Карусель встановлено (намальований телефон + старі скріни видалено)')
elif '<!-- КАРУСЕЛЬ СКРІНШОТІВ -->' in content:
    changes.append('⏭️  Карусель вже є — пропускаємо')
else:
    changes.append('❌ Старий блок не знайдено — перевір вручну')

# ── Звіт ─────────────────────────────────────────────────────────────────────
print(f'\n{"[DRY-RUN] " if DRY_RUN else ""}Патч карусель скріншотів')
print(f'Файл: {PATH}  ({original.count(chr(10))+1} рядків)\n')
for c in changes:
    print(' ', c)

if DRY_RUN:
    print('\n→ Dry-run: файл НЕ змінено.')
    sys.exit(0)

if content == original:
    print('\n→ Змін немає — файл не перезаписано.')
    sys.exit(0)

backup = PATH + '.bak2'
with open(backup, 'w') as f:
    f.write(original)
print(f'\n  Бекап: {backup}')

with open(PATH, 'w') as f:
    f.write(content)
print(f'  Файл оновлено. Рядків: {content.count(chr(10))+1}')
