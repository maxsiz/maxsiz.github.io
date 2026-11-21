# Task #8 Индексация продуктовых страниц и LCP главной https://iber.dev/

## Общая информация

**Цель:** по итогам статуса SEO 2026-11-21 — пункты 1 и 2 (www/TLS отложен владельцем).

**Ветка:** `master` (решение владельца: сайт ведёт один агент, отдельные ветки не нужны).

**Commit message prefix:** `#8`

## Исходные данные (2026-11-21)

- GSC: `/products_audit/` и `/products_code/` — «URL is unknown to Google»; `/research/`, `/aboutus/`, `/partner/` — «Crawled – currently not indexed».
- Меню и внутренние ссылки вели на URL без слэша → 301 на версию со слэшем.
- PSI mobile `/`: score 78, LCP 5,2 с. LCP — фон `.big-img`, который ставил `js/main.js` после jQuery.

## Сделано

| Пункт | Комментарий |
|---|---|
| Слэш в `navbar-links` и во внутренних ссылках страниц | URL страниц не менялись, только href; `last_modified_at` → 2026-11-21 |
| Фон шапки в HTML | `_includes/header.html`: inline `background-image` для одиночного `bigimg`; ротация нескольких картинок по-прежнему в `main.js` |
| Preload картинки шапки | `_includes/head.html`, `fetchpriority="high"`, до стилей |
| PNG → WebP | `bigsolidity_black2.webp` lossless, 15,5 КБ вместо 44,8 КБ; PNG оставлен |
| `bootstrap-social.css` | только на постах с `social-share` |
| `pygment_highlights.css` | был `@import` в начале `main.css` — второй последовательный блокирующий запрос на каждой странице; теперь `<link>` только на постах (подсветки кода на сайте сейчас нет нигде) |

## Замер PSI после первого деплоя (2026-11-21 ~05:15 UTC)

- Mobile, 4 прогона: score 78 / 93 / 81 / 78, LCP 5,0 / 3,2 / 4,9 / 5,0 с (база 78 / 5,2 с). Медиана ~80 / 5,0 с.
- Desktop: 98–100, LCP 0,7–1,1 с (было 97 / 1,2 с).
- Загрузка картинки исправлена: load delay 518 → 153 мс. Теперь LCP на mobile почти целиком render delay (~2 с) — блокирующие `bootstrap.min.css` и `main.css`.
- Следующий шаг (не сделан): critical CSS шапки inline в `<head>`, основной CSS без блокировки.

## Проверено

- `bundle exec jekyll build --strict_front_matter`: sitemap 18 URL
- Chromium headless 360×780 и 1280×900: шапка с картинкой, меню на месте

## После деплоя

- [ ] GSC → Request indexing для `/products_audit/` и `/products_code/` (владелец, UI)
- [ ] PSI mobile `/` — сравнить с LCP 5,2 с / score 78
- [ ] Через 2–3 недели: URL Inspection для `/tags/`, `/products_audit/`, `/research/`, тренд показов GSC

## Отложено

- `https://www.iber.dev/` — ошибка TLS (www → CNAME `maxsiz.github.io` в Cloudflare)
- Аналитика: исключение ботов и внутреннего трафика в GA4, связка GA4 ↔ GSC (UI)
- Контент тонких страниц (`/research/`, `/aboutus/`, `/products_audit/`)
