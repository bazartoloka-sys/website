#!/usr/bin/env python3
"""
Замінює рядки 576-595 (value-cards + </section>) на карусель.
Патчує по номерах рядків — надійно незалежно від кодування.
  python3 patch_carousel_move.py --check
  python3 patch_carousel_move.py
"""
import sys

PATH = '/home/boot/website/index.html'
DRY_RUN = '--check' in sys.argv

with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

original_lines = lines[:]
changes = []

# Перевіряємо що рядки 575-595 (0-based: 575-595) — це наш блок
start_idx = 575  # рядок 576 (0-based)
end_idx   = 595  # рядок 596 (0-based, не включно)

marker_start = '<!-- 3 VALUE CARDS -->'
marker_end   = '</section>'

# Верифікація
line576 = lines[start_idx].strip()
if marker_start not in line576:
    # Шукаємо динамічно
    found = False
    for i, l in enumerate(lines):
        if marker_start in l:
            start_idx = i
            # Шукаємо </section> після нього
            for j in range(i+1, min(i+30, len(lines))):
                if lines[j].strip() == marker_end:
                    end_idx = j + 1
                    found = True
                    break
            break
    if not found:
        print('❌ Блок value-cards не знайдено')
        sys.exit(1)
else:
    # Знаходимо end динамічно від start
    for j in range(start_idx+1, min(start_idx+30, len(lines))):
        if lines[j].strip() == marker_end:
            end_idx = j + 1
            break

print(f'  Знайдено: рядки {start_idx+1}–{end_idx} (0-based {start_idx}–{end_idx-1})')
print(f'  Перший: {lines[start_idx].rstrip()}')
print(f'  Останній: {lines[end_idx-1].rstrip()}')

new_block = '''  <!-- КАРУСЕЛЬ СКРІНШОТІВ -->
  <div class="carousel-hero">
    <div class="car-wrap-hero">
      <button class="car-btn car-prev" onclick="carMove(-1)" aria-label="Назад">&#8592;</button>
      <button class="car-btn car-next" onclick="carMove(1)" aria-label="Вперед">&#8594;</button>
      <div class="car-track-outer">
        <div class="car-track" id="carTrack">
          <div class="car-slide">
            <div class="car-phone"><img src="screen_splash.png" alt="Вхід" loading="lazy"></div>
            <div class="car-caption">
              <div class="car-cap-icon">🌸</div>
              <div class="car-cap-title">Вхід в додаток</div>
              <div class="car-cap-desc">Авторизація через Google за 1 дотик. Без SMS, без паролів.</div>
            </div>
          </div>
          <div class="car-slide">
            <div class="car-phone"><img src="screen_feed.png" alt="Стрічка" loading="lazy"></div>
            <div class="car-caption">
              <div class="car-cap-icon">🎬</div>
              <div class="car-cap-title">TikTok-стрічка</div>
              <div class="car-cap-desc">Гортай вертикально — купуй одним кліком. Алгоритм підбирає саме те що цікавить.</div>
            </div>
          </div>
          <div class="car-slide">
            <div class="car-phone"><img src="screen_cabinet.png" alt="Кабінет продавця" loading="lazy"></div>
            <div class="car-caption">
              <div class="car-cap-icon">🏪</div>
              <div class="car-cap-title">Кабінет продавця</div>
              <div class="car-cap-desc">Статистика, оголошення і замовлення — все в одному місці.</div>
            </div>
          </div>
          <div class="car-slide">
            <div class="car-phone"><img src="buy.png" alt="Кабінет покупця" loading="lazy"></div>
            <div class="car-caption">
              <div class="car-cap-icon">🛍️</div>
              <div class="car-cap-title">Кабінет покупця</div>
              <div class="car-cap-desc">Замовлення, статус доставки і захист платежу в реальному часі.</div>
            </div>
          </div>
          <div class="car-slide">
            <div class="car-phone"><img src="screen_payment.png" alt="Оплата" loading="lazy"></div>
            <div class="car-caption">
              <div class="car-cap-icon">💳</div>
              <div class="car-cap-title">4 способи оплати</div>
              <div class="car-cap-desc">Картка, NovaPay ескроу, НП Кредит або переказ на ФОП.</div>
            </div>
          </div>
          <div class="car-slide">
            <div class="car-phone"><img src="accounts.png" alt="Рахунки" loading="lazy"></div>
            <div class="car-caption">
              <div class="car-cap-icon">🏦</div>
              <div class="car-cap-title">Рахунки виплат</div>
              <div class="car-cap-desc">Продавець підключає банківський рахунок і отримує виплати автоматично.</div>
            </div>
          </div>
        </div>
      </div>
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
</section>
'''

new_lines = lines[:start_idx] + [new_block] + lines[end_idx:]
changes.append(f'✅ Рядки {start_idx+1}–{end_idx} замінено на карусель')

# ── CSS ──────────────────────────────────────────────────────────────────────
content = ''.join(new_lines)

if '.carousel-hero' not in content:
    css = '''
/* Карусель скріншотів */
.carousel-hero{padding:40px 5% 20px;max-width:900px;margin:0 auto}
.car-wrap-hero{position:relative}
.car-track-outer{overflow:hidden;border-radius:24px}
.car-track{display:flex;transition:transform .45s cubic-bezier(.4,0,.2,1)}
.car-slide{min-width:100%;display:flex;align-items:center;justify-content:center;gap:40px;padding:8px}
.car-phone{flex-shrink:0;width:200px;border-radius:32px;overflow:hidden;border:2px solid rgba(232,160,48,.25);box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 40px rgba(232,160,48,.06)}
.car-phone img{width:100%;display:block}
.car-caption{max-width:280px;text-align:left}
.car-cap-icon{font-size:36px;margin-bottom:12px}
.car-cap-title{font-family:'Unbounded',sans-serif;font-size:20px;font-weight:900;color:var(--cream);margin-bottom:10px;line-height:1.2}
.car-cap-desc{font-size:15px;color:var(--cream2);line-height:1.7}
.car-btn{position:absolute;top:45%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;background:var(--clay2);border:1px solid var(--aborder);color:var(--amber);font-size:18px;cursor:pointer;transition:all .2s;z-index:10;display:flex;align-items:center;justify-content:center}
.car-btn:hover{background:rgba(232,160,48,.12);border-color:var(--amber)}
.car-prev{left:-22px}
.car-next{right:-22px}
.car-dots{display:flex;justify-content:center;gap:8px;margin-top:24px}
.car-dot{width:8px;height:8px;border-radius:50%;background:var(--clay3);border:1px solid var(--border);cursor:pointer;transition:all .25s;padding:0}
.car-dot.active{background:var(--amber);border-color:var(--amber);width:24px;border-radius:4px}
@media(max-width:600px){
  .car-slide{flex-direction:column;gap:20px}
  .car-phone{width:150px}
  .car-caption{text-align:center;max-width:100%}
  .car-btn{display:none}
}'''
    content = content.replace('</style>', css + '\n</style>', 1)
    changes.append('✅ CSS додано')
else:
    changes.append('⏭️  CSS вже є')

# ── JS ───────────────────────────────────────────────────────────────────────
import re
m = re.search(r'<script>\s*\(function\(\)\{[\s\S]*?carMove\(1\).*?\}\)\(\);\s*</script>', content)
if m:
    content = content[:m.start()] + content[m.end():]
    changes.append('✅ Старий JS видалено')

js = '''<script>
(function(){
  var cur=0,total=6;
  var track=document.getElementById('carTrack');
  var dots=document.querySelectorAll('.car-dot');
  function upd(){
    track.style.transform='translateX(-'+(cur*100)+'%)';
    dots.forEach(function(d,i){d.classList.toggle('active',i===cur);});
  }
  window.carMove=function(d){cur=(cur+d+total)%total;upd();};
  window.carGoTo=function(i){cur=i;upd();};
  track.addEventListener('touchstart',function(e){track._sx=e.touches[0].clientX;},{passive:true});
  track.addEventListener('touchend',function(e){
    var dx=e.changedTouches[0].clientX-track._sx;
    if(Math.abs(dx)>50)carMove(dx<0?1:-1);
  },{passive:true});
  setInterval(function(){carMove(1);},8000);
})();
</script>'''
content = content.replace('</body>', js + '\n</body>', 1)
changes.append('✅ JS додано (8000 мс)')

# ── Звіт ─────────────────────────────────────────────────────────────────────
print('\n{}Патч: карусель → hero'.format('[DRY-RUN] ' if DRY_RUN else ''))
print('Файл: {}  ({} рядків)\n'.format(PATH, len(original_lines)))
for c in changes:
    print(' ', c)

if DRY_RUN:
    print('\n→ Dry-run: НЕ змінено.')
    sys.exit(0)

with open(PATH+'.bak3','w',encoding='utf-8') as f:
    f.writelines(original_lines)
with open(PATH,'w',encoding='utf-8') as f:
    f.write(content)
print('\n  Готово. Рядків: {}'.format(content.count('\n')+1))
