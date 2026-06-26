#!/usr/bin/env python3
"""
Патч blog.html — виправляє ОДИН битий лінк на article-001.

Проблема: article-001.html лежить у /blog/, а посилання веде на корінь /article-001.html (404).
Рішення: лінк → /blog/article-001.html

(002, 003 не чіпаємо — вони в корені й лінкуються правильно.)

Запуск:
  python3 patch_blog_link.py --check
  python3 patch_blog_link.py
"""
import sys, os, shutil

BLOG = "/home/boot/website/blog.html"
DRY = "--check" in sys.argv

OLD = '<a href="/article-001.html" class="acard" data-tag="news">'
NEW = '<a href="/blog/article-001.html" class="acard" data-tag="news">'

def run():
    if not os.path.exists(BLOG):
        print(f"ПОМИЛКА: не знайдено {BLOG}"); sys.exit(1)
    with open(BLOG,"r",encoding="utf-8") as f:
        c = f.read()
    n = c.count(OLD)
    if n == 0:
        if '/blog/article-001.html' in c:
            print("ℹ️  Лінк уже виправлено. Нічого не змінюємо.")
            sys.exit(0)
        print("❌ Якір не знайдено."); sys.exit(1)
    if n > 1:
        print(f"❌ Якір знайдено {n}× — неоднозначно."); sys.exit(1)

    nc = c.replace(OLD, NEW, 1)
    if DRY:
        print("✅ DRY-RUN: битий лінк на article-001 знайдено.")
        print("   /article-001.html → /blog/article-001.html")
        print("\nЗапусти без --check щоб застосувати.")
    else:
        shutil.copy2(BLOG, BLOG + ".bak_link")
        with open(BLOG,"w",encoding="utf-8") as f:
            f.write(nc)
        print("✅ Лінк виправлено.")

if __name__ == "__main__":
    run()
