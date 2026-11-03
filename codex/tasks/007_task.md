# Task #7 Скорость главной, перелинковка и SEO-мелочи для https://iber.dev/

## Общая информация

**Цель:** закрыть пункты 3–5 SEO-аудита 2026-11-03: mobile LCP главной (5.1 с), перелинковка, мелкие замечания.

**Ветка для реализации:** `task/007-perf-links-cleanup`

**Commit message prefix:** `#7`

---

## Статус реализации (2026-11-03)

| Пункт | Статус | Комментарий |
|---|---|---|
| Font Awesome без блокировки отрисовки | ✅ | `media="print"` + `onload`, `<noscript>` fallback |
| Google Fonts: 2 запроса → 1, без блокировки | ✅ | `Lora…%7COpen+Sans…`, тот же приём |
| `defer` на jQuery / bootstrap / main | ✅ | порядок сохранён; `document.write`-guard удалён (с `defer` несовместим, jQuery больше нигде не грузится) |
| canonical на 404 | ✅ | не выводится для `/404.html` |
| `/tags/` | ✅ | `noindex, follow`, выпала из sitemap (решение владельца) |
| og:image поста 2016 | ✅ | `share-img` → `iber_share_1200x630.png`; превью в ленте прежнее |
| `last_modified_at` на страницах | ✅ | дата последнего коммита файла; на главной нет — её содержание меняется с постами |
| `AGENTS.md` | ✅ | `url: https://iber.dev`, sitemap — свой шаблон |
| Ссылка на `/products_audit/` | ➖ | уже есть: меню, `development`, `research`, `ai-agents` |
| Ссылка на PDF с `products_audit` | ➖ | не делаем: PDF — отчёт Cryptosec об аудите CIX100, уже связан с `products_eth` |

## Проверено

- `bundle exec jekyll build --strict_front_matter`: sitemap 18 URL, `lastmod` у 16
- Chromium, 1280×900 и 360×780: ошибок консоли нет, `jQuery.fn.dropdown/collapse` на месте, меню Products и бургер работают, Font Awesome и Lora применены

## После деплоя

- [ ] PageSpeed Insights mobile для `/` — сравнить с LCP 5.1 с / score 76
