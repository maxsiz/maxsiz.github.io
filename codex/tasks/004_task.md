# Task #4 SEO fixes & improvements для https://iber.dev/

## Общая информация

**Цель:** устранить проблемы, выявленные SEO-аудитом от 2026-07-26, и довести сайт до production-ready состояния для поисковой и AI-выдачи.

**Контекст:** task #3 (`003_task.md`) уже внедрил базовую SEO-инфраструктуру — мета-теги, Open Graph, Twitter Cards, JSON-LD, `robots.txt`, favicon, canonical. Task #4 закрывает оставшиеся пробелы: sitemap на проде, GA4, on-page для постов, structured data, контент.

**Тип сайта:** статический Jekyll (Beautiful Jekyll theme), хостинг GitHub Pages, домен `iber.dev`.

**Ветка для реализации:** `task/004-seo-fixes`

**Commit message prefix:** `#4`

---

## Текущее состояние (аудит)

| Категория | Оценка | Комментарий |
|---|---|---|
| Технический SEO (шаблоны) | 8/10 | `_includes/head.html`, `structured-data.html` — хорошо |
| Индексация (sitemap, robots) | 4/10 | `sitemap.xml` на проде отдаёт HTTP 500 |
| On-page (страницы) | 7/10 | `meta-description` есть на основных страницах |
| On-page (посты) | 5/10 | 6 постов без `meta-description` |
| Structured data | 7/10 | Organization, WebSite, WebPage/BlogPosting — базово |
| Контент / E-E-A-T | 5/10 | опечатки, редкие публикации |
| Аналитика | 3/10 | Universal Analytics (UA) deprecated |

### Уже реализовано (task #3)

- Canonical URL — `_includes/head.html`
- Meta description — все основные страницы (`.md` в корне, `index.html`, `tags.html`, `404.html`)
- Open Graph / Twitter Cards — полный набор
- JSON-LD — Organization, WebSite, WebPage/BlogPosting
- `robots.txt` — `Allow: /` + ссылка на sitemap
- `404.html` — `noindex, nofollow`, `sitemap: false`
- `lang="en"` — `_layouts/base.html`
- Favicon — `favicon.svg` + PNG fallback
- RSS — `feed.xml`
- Lazy loading — превью постов в `index.html`

---

## Фаза 0. Подготовка

**Цель:** зафиксировать baseline и не сломать прод.

- [ ] Собрать сайт локально: `bundle exec jekyll build`
- [ ] Проверить, что `_site/sitemap.xml` генерируется без ошибок
- [ ] Сравнить локальный sitemap с продом: `curl -I https://iber.dev/sitemap.xml`
- [ ] Зафиксировать baseline в Search Console / GA (если есть доступ)
- [ ] Создать ветку `task/004-seo-fixes`

**Критерий готовности:** понятно, sitemap ломается при сборке или только на деплое.

---

## Фаза 1. Критические исправления (блокеры)

### 1.1. Починить sitemap.xml на проде

**Проблема:** `robots.txt` ссылается на sitemap, но `https://iber.dev/sitemap.xml` отдаёт HTTP 500.

**Файлы:** `_config.yml`, `robots.txt`, настройки GitHub Pages

**Шаги:**
1. Локально проверить `_site/sitemap.xml` после `jekyll build`
2. Убедиться, что `jekyll-sitemap` в `_config.yml` активен и не конфликтует с `exclude`
3. Проверить, что `404.html` с `sitemap: false` не ломает генерацию
4. Проверить GitHub Pages build log (Actions или Settings → Pages)
5. После деплоя: `curl -I https://iber.dev/sitemap.xml` → ожидается `200`
6. В Search Console отправить sitemap вручную

**Критерий:** sitemap доступен, содержит все основные URL (страницы, посты, `/tags`).

---

### 1.2. Миграция с Universal Analytics на GA4

**Проблема:** в `_config.yml` указан `gtag: "UA-129780126-1"`. UA не собирает данные с июля 2023.

**Файлы:** `_config.yml`, при необходимости `_includes/gtag.html`

**Шаги:**
1. Создать GA4 property для `iber.dev`
2. Получить Measurement ID (`G-XXXXXXXX`) — **нужен от владельца сайта**
3. Заменить `gtag` в `_config.yml`
4. Проверить, что `_includes/gtag.html` корректно инициализирует новый ID
5. Убедиться, что тег срабатывает на главной и на странице поста
6. Связать GA4 с Search Console

**Критерий:** в GA4 Realtime видны визиты после деплоя.

---

## Фаза 2. On-page SEO — страницы и посты

### 2.1. Meta description для всех постов

**Проблема:** у 6 постов в `_posts/` нет `meta-description`. Description берётся из `subtitle` или auto-excerpt — часто коротко и неоптимально.

**Требования:** уникальный `meta-description`, 150–160 символов, тема + контекст (Ethereum, Web3, blockchain).

| Файл | Текущий subtitle | Действие |
|---|---|---|
| `_posts/2025-12-09-Risks_Crypto_2026.md` | Additional risks for the crypto industry | Новый meta-description |
| `_posts/2024-11-27-Distributed_Liquidity.md` | NFT secured with ERC20 | Новый meta-description |
| `_posts/2021-02-03-Secured-NFT.md` | NFT secured with ERC20 | Новый meta-description |
| `_posts/2019-02-01-Short_forecast.md` | Short term forecast on Ethereum scalability | Новый meta-description |
| `_posts/2018-11-26-Ethereum-talks.md` | About ethereum "vulnerabilities" | Новый meta-description |
| `_posts/2016-03-20-Ethereum_blog_1.md` | My fisrt publication about Ethereum | Новый meta-description + правка опечаток в subtitle |

**Пример front matter:**
```yaml
meta-description: "Analysis of crypto industry risks in 2026: oracle delays, L2 outages, and Web2 infrastructure failures affecting DeFi protocols."
```

**Критерий:** у каждого поста свой description 150–160 символов, без дублей.

---

### 2.2. Усилить title коммерческих страниц через `meta-title`

**Проблема:** title вида `Development - Iber` слабо таргетирует поисковые запросы. Поле `meta-title` поддерживается в `_includes/head.html`, но нигде не используется.

| Страница | Предлагаемый `meta-title` |
|---|---|
| `development.md` | Smart Contract & Web3 Development \| Iber |
| `products_audit.md` | Ethereum Smart Contract Audits \| Iber |
| `products_eth.md` | Ethereum Smart Contract Projects \| Iber |
| `products_code.md` | Web3 Apps & Custom Blockchain Code \| Iber |
| `research.md` | Blockchain & Ethereum Research \| Iber |
| `aboutus.md` | About Iber — Blockchain R&D Team |
| `partner.md` | Iber Partners — Web3 & Blockchain |
| `iber-group-team.md` | Iber Group Team — Blockchain Engineers |

**Критерий:** `<title>` содержит ключевые слова, длина до ~60 символов.

---

### 2.3. Пагинация главной

**Проблема:** при росте числа постов `/page2/` будет с тем же title/description, что и `/`. Риск дублей в индексе.

**Файлы:** `index.html`, `_includes/head.html`

**Шаги:**
1. Добавить логику для `paginator.page`
2. Для page > 1:
   - title: `Blog — Page 2 | Iber`
   - description: отдельный или с суффиксом «Page 2»
3. Добавить `<link rel="prev">` / `<link rel="next">` для пагинатора
4. Альтернатива (проще): `robots: noindex, follow` для `/page2/` и далее

**Критерий:** нет дублей title/description между страницами пагинации.

---

## Фаза 3. Технический SEO — доработки шаблонов

### 3.1. Viewport и accessibility

**Проблема:** `maximum-scale=1.0` в viewport — минус для accessibility.

**Файл:** `_includes/head.html`

**Шаги:**
1. Убрать `maximum-scale=1.0`
2. Оставить: `width=device-width, initial-scale=1.0, viewport-fit=cover`

**Критерий:** zoom на мобильных работает, layout не ломается.

---

### 3.2. Дублирование H1 в header

**Проблема:** при `bigimg` в DOM два блока с `<h1>`. На экранах ≤365px один скрывается через CSS, но оба остаются в DOM.

**Файлы:** `_includes/header.html`, `css/main.css`

**Шаги:**
1. Проверить `header.html` + CSS (`.header-section.has-img .intro-header.no-img`)
2. Варианты:
   - рендерить только один блок (предпочтительно)
   - или заменить скрытый H1 на `h2` / `p` там, где он дублируется
3. Прогнать проверку на главной и страницах с `bigimg`

**Критерий:** на каждой странице ровно один `<h1>` в DOM.

---

### 3.3. Alt-тексты для изображений

**Проблема:** логотипы партнёров и другие картинки без описательного alt.

**Файлы:** `partner.md`, product pages

**Шаги:**
1. `partner.md` — добавить alt для каждого логотипа:
   ```markdown
   [![UBD Network logo — blockchain infrastructure partner](/img/ubd_network.png)](...)
   ```
2. Пройтись по product pages — скриншоты, диаграммы
3. Посты с `image:` — alt уже через `post.title` в index; проверить layout

**Критерий:** у всех значимых `<img>` есть осмысленный alt.

---

### 3.4. HTTPS для внешних ссылок

**Проблема:** на `partner.md` есть `http://` ссылки (`izzz.io`, `demeter.site`, `peaceplus.org`, и др.).

**Шаги:**
1. Проверить каждый HTTP URL — работает ли HTTPS
2. Заменить на `https://` где возможно
3. Для мёртвых — решить: убрать, nofollow, или оставить с пометкой

**Критерий:** нет mixed/outdated HTTP-ссылок на рабочие сайты.

---

## Фаза 4. Structured Data (Schema.org)

**Файл:** `_includes/structured-data.html`

### 4.1. Расширить Organization

- [ ] Добавить `sameAs` — GitHub, LinkedIn, Twitter из `_config.yml` / `_data/SocialNetworks.yml`
- [ ] При необходимости — `contactPoint` (email)

### 4.2. BreadcrumbList

- [ ] Новый partial или блок в `structured-data.html`
- [ ] Генерировать для внутренних страниц: Home → Section → Page
- [ ] Не добавлять на главную

**Пример цепочки:** Home → Products → Smart contracts audit

### 4.3. Service / ProfessionalService для коммерческих страниц

- [ ] Для `development.md`, `products_audit.md` — JSON-LD `@type: Service`
- [ ] Поля: `name`, `description`, `provider` (→ Organization), `areaServed`, `serviceType`

### 4.4. Person для team/about

- [ ] На `iber-group-team.md` и/или `aboutus.md` — JSON-LD `Person` для ключевых людей
- [ ] Связать с Organization через `worksFor`

**Критерий фазы 4:** Rich Results Test проходит без ошибок для главной, поста, development, about.

---

## Фаза 5. Open Graph и шаринг

### 5.1. Уникальные OG-изображения

- [ ] Для постов с `image:` — использовать как `share-img` (или автоматически в head)
- [ ] Для product pages — подготовить 1200×630 px превью (можно из существующих assets)
- [ ] Проверить абсолютные URL через `absolute_url`

**Файлы:** front matter страниц, `_includes/head.html` (если нужна автологика)

### 5.2. OG article tags для постов

**Файл:** `_includes/head.html`

- [ ] Для `layout == "post"` добавить `article:tag` для каждого tag
- [ ] `article:modified_time` если есть `last_modified_at`

---

## Фаза 6. Контент и E-E-A-T

### 6.1. Редактура ключевых страниц

| Страница | Что исправить |
|---|---|
| `development.md` | Softwear → Software, Hardwear → Hardware, planing → planning |
| `aboutus.md` | Грамматика, усилить expertise signals (годы, проекты, компания) |
| `index.html` | Subtitle: *hard recognizable* → *hard to recognize* |
| Старые посты | Минимальная вычитка без переписывания смысла |

### 6.2. Контент-стратегия (ongoing)

**Рекомендуемый минимум:**
- 1 пост в 1–2 месяца по темам: smart contracts, audits, DeFi risks, L2
- Обновление product pages при новых проектах
- Добавление case study блоков (задача → решение → результат)

**Формат нового поста:**
```yaml
layout: post
title: ...
subtitle: ...
meta-description: ...
tags: [Ethereum, ...]
image: /img/...
share-img: /img/...
```

### 6.3. Внутренняя перелинковка

- [ ] Из постов — ссылки на `development`, `products_audit`, `research`
- [ ] С product pages — ссылки на релевантные посты
- [ ] На `aboutus` — ссылки на team, products, partners

---

## Фаза 7. URL и архитектура (опционально, с осторожностью)

### 7.1. Slug постов

**Проблема:** `/2025-12-09-Risks_Crypto_2026/` — подчёркивания в URL.

**Важно:** смена URL = 301 redirects. Для GitHub Pages redirects ограничены.

**Рекомендация:**
- **Не менять** URL существующих постов без redirect strategy
- **Для новых постов** — дефисы в filename: `2026-01-15-crypto-risks-outlook.md`

### 7.2. Sitemap с приоритетами

- [ ] Кастомный `sitemap.xml` layout или конфиг `jekyll-sitemap`
- [ ] Приоритеты: `/` = 1.0, product pages = 0.8, posts = 0.6, tags = 0.5
- [ ] `lastmod` из git или `last_modified_at` в front matter

*Делать только после починки базового sitemap (фаза 1.1).*

---

## Фаза 8. Верификация и мониторинг

### 8.1. После каждого деплоя

```bash
bundle exec jekyll build
# Проверить _site/sitemap.xml, несколько HTML на meta/canonical/JSON-LD
```

**Онлайн-чеклист:**
- [ ] [Google Rich Results Test](https://search.google.com/test/rich-results) — главная, пост, development
- [ ] [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) — OG tags
- [ ] Search Console — Coverage, Sitemaps, Core Web Vitals
- [ ] GA4 Realtime — трафик после деплоя

### 8.2. KPI для отслеживания (3–6 месяцев)

| Метрика | Инструмент |
|---|---|
| Индексированные страницы | Search Console |
| Impressions / clicks по ключевым запросам | Search Console |
| Органический трафик | GA4 |
| CTR сниппетов | Search Console → Performance |
| Core Web Vitals | PageSpeed Insights |

**Целевые запросы для мониторинга:**
- ethereum smart contract development
- smart contract audit
- blockchain R&D team
- web3 development company

---

## Предлагаемый порядок работ (спринты)

### Спринт 1 (1–2 дня) — блокеры
1. Sitemap на проде
2. GA4
3. Meta description для всех постов

### Спринт 2 (1–2 дня) — on-page
4. `meta-title` для коммерческих страниц
5. Alt для partner/product images
6. Viewport fix
7. HTTP → HTTPS на partner

### Спринт 3 (2–3 дня) — structured data
8. Organization sameAs
9. BreadcrumbList
10. Service schema для development/audit
11. OG article tags

### Спринт 4 (ongoing) — контент
12. Вычитка development/about/index
13. Пагинация SEO
14. H1 fix в header
15. Контент-план и новые посты

---

## Что сознательно не делать

| Не делать | Почему |
|---|---|
| `meta keywords` | Google не использует |
| `hreflang` | Сайт одноязычный (EN) |
| Массовая смена URL постов | Риск потери ссылочного веса без redirects |
| `geo.region` RU | Компания SG, аудитория global — не актуально |
| Переписывание всего контента | Disproportionate; точечные правки достаточно |

---

## Definition of Done

- [ ] `https://iber.dev/sitemap.xml` → 200, все URL в Search Console
- [ ] GA4 собирает данные
- [ ] У каждой страницы и поста уникальные title + description
- [ ] Rich Results Test без критических ошибок
- [ ] Нет дублей H1, проблем с viewport, пустых alt на ключевых страницах
- [ ] JSON-LD: Organization + WebSite + page-specific schemas
- [ ] Контент на ключевых страницах вычитан

---

## Ключевые файлы репозитория

| Файл | Роль в SEO |
|---|---|
| `_config.yml` | url, description, gtag, plugins, defaults |
| `_includes/head.html` | title, meta, canonical, OG, Twitter |
| `_includes/structured-data.html` | JSON-LD |
| `_includes/header.html` | H1, заголовки страниц |
| `_layouts/base.html` | `lang` attribute |
| `robots.txt` | crawl rules, sitemap URL |
| `index.html` | homepage meta, pagination |
| `_posts/*.md` | blog posts — нужны meta-description |
| `404.html` | noindex |
| `partner.md`, `development.md`, etc. | on-page content |
