#!/usr/bin/env python3
"""
Патч для blog.html — вставляє 27 нових карток статей.
Запуск:
  python3 patch_blog.py --check   # dry-run, тільки перевірка
  python3 patch_blog.py           # бойовий режим

Файл: /home/boot/website/blog.html
"""

import sys
import os
import shutil

BLOG_PATH = "/home/boot/website/blog.html"
DRY_RUN = "--check" in sys.argv

# =========================================================
# 27 НОВИХ КАРТОК (004–030)
# =========================================================
NEW_CARDS = """
  <a href="/blog/article-004.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">🚀</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Альтернатива Prom.ua: продавати без прихованих комісій</div>
      <div class="acard-desc">CPA-модель з'їдає 30–50% вашого чистого прибутку. Базар Толока — фіксована підписка, 0% комісії з продажів.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">7 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-005.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">😤</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Чому продавці йдуть з OLX — і що приходить на зміну</div>
      <div class="acard-desc">Дорогі пакети, трафік «торгуйтесь», відсутність ПРРО — три болі OLX, які вирішує відео-маркетплейс.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">6 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-006.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">📊</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Підписка проти відсотків: рахуємо чистий прибуток магазину</div>
      <div class="acard-desc">При обороті 300 000 грн/міс класичний маркетплейс забирає 36 000 грн. Базар — тільки фіксований тариф.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">6 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-007.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">⚖️</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Як маркетплейс без комісії допомагає тримати конкурентні ціни</div>
      <div class="acard-desc">Малий бізнес змушений закладати комісію у ціну. 0% на Базарі — шанс знизити ціну без втрати рентабельності.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-008.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">🚫</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Топ-5 помилок при виборі торговельного майданчика для старту</div>
      <div class="acard-desc">Власний сайт без бюджету, «ціна в дірект», CPA-пастка, відсутність ПРРО, фото замість відео — помилки, які закривають магазини.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">7 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-009.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">📲</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Ера «Ціна в дірект» закінчилася: автоматизуйте продажі з Instagram</div>
      <div class="acard-desc">Менеджери годинами копіюють ціни в Директ. Базар Толока — відео-картка + кошик + автоматизація в одному місці.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-010.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">🎬</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Як продавати через TikTok-формат без мільйона підписників</div>
      <div class="acard-desc">На Базарі охоплення залежать не від підписників, а від якості ролика. Кожен стартує на рівних умовах.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-011.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🎥</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Як зняти відео для картки товару, що продає за 15 секунд</div>
      <div class="acard-desc">3 секунди на зачіпку, 12 секунд на закриття потреби. Простий гайд з мобільної зйомки без режисера.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">6 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-012.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">⭐</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Відео-відгуки покупців: безкоштовний інструмент довіри до бренду</div>
      <div class="acard-desc">UGC-відео як соціальний доказ, прикріплений до картки товару. Краще будь-якої реклами і повністю безкоштовно.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-013.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🔄</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Імпорт відео з Instagram/TikTok на маркетплейс за пару кліків</div>
      <div class="acard-desc">Є сотні відзнятих Reels? Базар Толока імпортує їх автоматично — не потрібно починати з нуля.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">4 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-014.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🏛️</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Реєстрація ФОП для маркетплейсу 2026: покрокова інструкція</div>
      <div class="acard-desc">КВЕД 47.91, вибір групи оподаткування, реєстрація через Дію — повний алгоритм для старту легального інтернет-магазину.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">7 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-015.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🧾</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Автоматизація ПРРО: законно видавати чеки без рутини</div>
      <div class="acard-desc">Підключіть Вчасно.Каса або Checkbox один раз — і кожне замовлення автоматично отримує фіскальний чек.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">6 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-016.html" class="acard" data-tag="buyer">
    <div class="acard-img-placeholder">🛡️</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag blue">Покупцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Безпечні платежі в е-commerce: WayForPay та NovaPay на Базарі</div>
      <div class="acard-desc">Ескроу-захист, 4 форми оплати, B2B та ПДВ. Новий стандарт фінансової безпеки для покупців і продавців.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">6 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-017.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">📑</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Форма 20-ОПП та 1-ПРРО: що знати інтернет-магазину перед стартом</div>
      <div class="acard-desc">Об'єкт оподаткування для онлайн-магазину, заява на касу — два кроки, без яких прийом платежів незаконний.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">7 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-018.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🔒</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Як уникнути блокування рахунку ФОП та тіньового бану в соцмережах</div>
      <div class="acard-desc">Хаотичні перекази на картку → фінмоніторинг → блокування. Базар Толока: офіційний шлюз, білий бізнес, нульовий ризик.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-019.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">📦</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Як оформити картку товару на відео-маркетплейсі: чек-лист для старту</div>
      <div class="acard-desc">Відео 15–30 сек, ШІ-опис через Claude, автоматичний підбір тегів — чек-лист ідеальної картки на Базар Толока.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">6 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-020.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🔍</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Оптимізація описів товарів для ШІ-пошуку Google та Gemini у 2026</div>
      <div class="acard-desc">Покупці шукають через голосові ШІ-запити. Вбудований Claude аналізує відео і текст та автоматично оптимізує картку.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-021.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🚚</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Логістика для інтернет-магазину: Нова Пошта та Укрпошта в один клік</div>
      <div class="acard-desc">Дані для ТТН синхронізуються автоматично. Генерація накладної, трекінг і ПРРО — в одному кабінеті замовлень.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-022.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">📈</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Тренди українського e-commerce: що купуватимуть восени 2026</div>
      <div class="acard-desc">Автономні гаджети, крафтові продукти, локальний одяг — топ-3 категорії осіннього сезону і як ШІ-маркетинг Базару допомагає їх продавати.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-023.html" class="acard" data-tag="news">
    <div class="acard-img-placeholder">🤝</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Новини</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Толока для бізнесу: нова модель ринку в Україні</div>
      <div class="acard-desc">Чому Базар Толока — це не просто маркетплейс, а цифрова толока: партнерство замість хижого посередництва.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-024.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">🌾</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Фермерам та еко-виробникам: продавайте свіжі продукти через відео</div>
      <div class="acard-desc">Відео показує свіжість, текстуру, запах — те, чого фото ніколи не передасть. Базар Толока для фермерів і крафтових виробників.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-025.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">👗</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Продаж одягу онлайн: чому відео-примірка скорочує повернення на 70%</div>
      <div class="acard-desc">Колір не такий, розмір не підійшов — причини 80% повернень одягу. Відео на моделі в русі закриває ці питання ще до покупки.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-026.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">🎨</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Hand-made та крафт: як перетворити хобі на офіційний бізнес</div>
      <div class="acard-desc">Кераміка, шкіра, прикраси — ШІ-інструменти адмінпанелі допоможуть майстру швидко створювати описи і продавати унікальність.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">5 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-027.html" class="acard" data-tag="seller">
    <div class="acard-img-placeholder">🏭</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Продавцям</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">B2B-торгівля, аукціони та тендери: великий опт всередині одного додатка</div>
      <div class="acard-desc">Виробники та дистриб'ютори можуть виставити гуртову партію на аукціон або взяти участь у тендері — прямо в Базар Толока.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">7 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-028.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">📱</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Керування магазином з одного смартфона: огляд мобільного додатка</div>
      <div class="acard-desc">В один клік: ТТН, статус ПРРО, відповідь клієнту, відео-картка. Все з телефона, де б ви не були.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">4 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-029.html" class="acard" data-tag="news">
    <div class="acard-img-placeholder">🦾</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag">Новини</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">Нова ера SEO: чому методи «пром-шаманів» більше не працюють</div>
      <div class="acard-desc">Google SGE і Gemini оцінюють корисність, а не щільність ключових слів. Базар Толока будувався під нову пошукову реальність.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">7 хв читання</span></div>
    </div>
  </a>

  <a href="/blog/article-030.html" class="acard" data-tag="guide">
    <div class="acard-img-placeholder">🤖</div>
    <div class="acard-body">
      <div class="acard-meta"><span class="acard-tag green">Навчання</span><span class="acard-date">25 червня 2026</span></div>
      <div class="acard-title">ШІ-маркетинг без копірайтерів: Claude в адмінпанелі Базар Толока</div>
      <div class="acard-desc">5 слів від вас → структурований SEO-опис, теги і мета-дані від Claude — за 3 секунди. Без копірайтерів і складних промптів.</div>
      <div class="acard-footer"><span class="acard-read">Читати →</span><span class="acard-time">8 хв читання</span></div>
    </div>
  </a>
"""

# =========================================================
# ВСТАВКА В blog.html
# =========================================================
ANCHOR = '</a>\n\n  <!-- Порожній стан'

def patch(path, dry_run):
    if not os.path.exists(path):
        print(f"ПОМИЛКА: файл не знайдено: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if ANCHOR not in content:
        print(f"ПОМИЛКА: якірний рядок не знайдено в файлі.")
        print(f"Шукаємо: {repr(ANCHOR[:60])}")
        sys.exit(1)

    if "article-004.html" in content:
        print("ℹ️  Картки вже вставлені (article-004 знайдено). Нічого не змінюємо.")
        sys.exit(0)

    new_content = content.replace(ANCHOR, f'</a>\n{NEW_CARDS}\n  <!-- Порожній стан', 1)

    if dry_run:
        lines_before = content.count('\n')
        lines_after = new_content.count('\n')
        print(f"✅ DRY-RUN: файл знайдено, якір знайдено.")
        print(f"   Рядків до патча:   {lines_before}")
        print(f"   Рядків після патча: {lines_after}")
        print(f"   Додається ~{lines_after - lines_before} рядків (27 карток)")
        print(f"\nЗапустіть без --check щоб застосувати.")
    else:
        backup = path + ".bak"
        shutil.copy2(path, backup)
        print(f"📦 Бекап збережено: {backup}")

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        lines = new_content.count('\n')
        print(f"✅ Патч застосовано! Файл: {path}")
        print(f"   Рядків у файлі після патча: {lines}")
        print(f"\nНаступні кроки:")
        print(f"  cd /home/boot/website")
        print(f"  git add blog.html")
        print(f'  git commit -m "blog: додано 27 статей (article-004 — article-030)"')
        print(f"  git push")

if __name__ == "__main__":
    patch(BLOG_PATH, DRY_RUN)
