# Task #4 SEO fixes & improvements для https://iber.dev/

## Общая информация

**Цель:** устранить проблемы, выявленные SEO-аудитом от 2026-07-26, и довести сайт до production-ready состояния для поисковой и AI-выдачи.

**Контекст:** task #3 (`003_task.md`) уже внедрил базовую SEO-инфраструктуру — мета-теги, Open Graph, Twitter Cards, JSON-LD, `robots.txt`, favicon, canonical. Task #4 закрывает оставшиеся пробелы: sitemap на проде, GA4, on-page для постов, structured data, контент.

**Тип сайта:** статический Jekyll (Beautiful Jekyll theme), хостинг GitHub Pages, домен `iber.dev`.

**Ветка для реализации:** `task/004-seo-fixes`

**Commit message prefix:** `#4`

---

## Статус реализации (обновлено 2026-07-26)

| Фаза | Статус | Комментарий |
|---|---|---|
| 0. Подготовка | ✅ | Окружение Jekyll поднято, pre-commit хук собирает сайт перед каждым коммитом |
| 1.1 Sitemap | ✅ | Сделано в рамках Фазы 7 — кастомный `sitemap.xml` |
| 1.2 GA4 | ✅ | `G-ELXPSZHXH5`, property `547103578`. Проверено в браузере: `page_view` и `contact_click` долетают |
| 1.3 Timezone | ✅ | `Asia/Irkutsk` |
| 1.4 Enforce HTTPS | ✅ | Включено владельцем. Проверено: `maxsiz.github.io` → `https://iber.dev/`, `http://iber.dev` → `https://iber.dev/` |
| 2. On-page | ✅ | meta-description постам, meta-title страницам, пагинация noindex |
| 3. Технический SEO | ✅ | viewport, один H1, alt, https + `rel="noopener"` |
| 4. Structured data | ✅ | Organization sameAs, BreadcrumbList, Service, Person |
| 5. Open Graph | ✅ | Новая карточка 1200×630, размеры, `article:tag` |
| 6. Контент | ✅ | Опечатки, вычитка, перелинковка |
| 7. Sitemap и URL | ✅ | Кастомный sitemap; slug'и постов не меняли осознанно |
| 8. Верификация | 🟡 | Локальные проверки прогнаны; онлайн-чеклист — после деплоя |
| 9. Аналитика | ✅ | Сбор работает, конверсии считаются, еженедельная выгрузка прогнана вручную и зелёная |

### Аналитика: фактическое состояние (2026-07-26)

| Параметр | Значение |
|---|---|
| Measurement ID | `G-ELXPSZHXH5` |
| Property ID (Data API) | `547103578` |
| Data stream | `properties/547103578/dataStreams/15328786990` → `https://iber.dev` |
| GA4 account | `accounts/393356740` («Envelop_acc») |
| Key events | `contact_click` ✅, `file_download` ✅ — отмечены до первого хита |
| Enhanced measurement | включено полностью, в т.ч. `fileDownloadsEnabled` |
| Event data retention | 14 месяцев (дефолтные 2 отрезали бы годовые сравнения) |
| Custom dimensions | `method`, `link_location`, `link_url` — без регистрации эти параметры недоступны в отчётах и Data API |

**Проверено в браузере на проде:** `page_view` уходит с `tid=G-ELXPSZHXH5`; клики по реальным ссылкам футера дают `contact_click` с `method=email|telegram|github` и `link_location=footer`. Коллектор отвечает **HTTP 204** от `region1.google-analytics.com` на оба события — то есть хиты не просто отправляются, а принимаются.

### ⚠️ Ловушка: GA4 отбрасывает трафик headless-браузеров

**Стоила часа работы двоим. Записано, чтобы не повторять.**

Симптом: хиты уходят, коллектор отвечает **HTTP 204**, `tid` правильный, тег единственный, consent mode отсутствует — а в property не появляется ничего, ни в Realtime, ни в отчётах.

**Причина:** GA4 отфильтровывает трафик, опознанный как боты и пауки, **уже после того, как коллектор ответил 204**. Строка `HeadlessChrome` в User-Agent этот фильтр триггерит. Отключить фильтрацию нельзя — в интерфейсе такого переключателя не существует.

**Доказано разностью в один параметр:**

| Партия | User-Agent | Ответ | В property |
|---|---|---|---|
| 16:57 | headless | 204 | ничего |
| 17:06 | headless | 204 | ничего |
| 17:15 | обычный Chrome | 204 | **события через минуту** |

Между партиями менялся только User-Agent. `contact_click`, `page_view`, `first_visit`, `session_start`, `user_engagement` появились в Realtime меньше чем за минуту, разрез по `minutesAgo` корректно съезжал от замера к замеру.

**Правило на будущее:** проверять сбор GA4 из headless-браузера бесполезно в принципе. **204 доказывает приём, но никогда — обработку.** Если нужен автотест сбора, подменяйте User-Agent на обычный Chrome и убирайте прочие headless-признаки.

**Отдельная ловушка того же расследования:** мы отсекали версии про блокировщики и CMP аргументом «тест чистый, headless без расширений» — и именно эта чистота была причиной. Аргумент от стерильности среды сам оказался дефектным.

**Ложные версии, отработанные до этого** (каждая отсеяна проверкой, а не рассуждением): прогрев нового потока, consent mode с `analytics_storage: denied` (даёт ровно тот же симптом — 204 без данных, но в HTML нет ни одного CMP), дубли тегов, неверная конфигурация потока, задержка отчётов.

### Еженедельная выгрузка — работает

Прогнана вручную, зелёная, отчёт доставлен. Проверено чтением результата, а не статусом джоба.

| Параметр | Значение |
|---|---|
| Воркфлоу | `.github/workflows/analytics-report.yml`, cron `0 6 * * 1` (понедельник, 06:00 UTC) |
| Ключ | `iber-analytics@digital-yeti-501512-j9`, `viewer` на property, `siteRestrictedUser` в GSC |
| Секреты | `GA4_PROPERTY_ID` = `547103578`, `GA_SERVICE_ACCOUNT_JSON` |
| Доставка | сводка прогона в Actions (основное) + ветка `analytics-reports`, файлы по месяцам |

**Почему не в `master`:** ветка защищена и требует PR, бот пушить не может — и это правильно. Автоматический PR каждый понедельник для файла, который никто не ревьюит, был бы шумом. Отчёт читают, а не ревьюят, поэтому основная доставка — сводка прогона.

**Про пустой первый отчёт:** окно `--days 7` заканчивается вчерашним днём. Первый прогон взял 19–25 июля, а тег заработал 26-го — отсюда `_no data_` во всех секциях. Это корректная работа, а не сбой. Прогон в понедельник возьмёт 20–26 июля и уже покажет данные.

**Ловушка, которую починили по дороге:** `fmt()` вызывалась с одним аргументом вместо двух в секциях Top queries и Top pages. Баг приехал с первым коммитом Фазы 9 и ни разу не исполнялся — сначала запрос падал с 403 раньше, потом обработчик отсутствия доступа возвращал заглушку и выходил раньше. Первый же реальный доступ к GSC довёл исполнение до этих строк, и они упали. То есть баг ждал ровно того момента, когда всё остальное заработает.

### Что осталось и от кого зависит

**Закрыто 2026-07-26:**
- ✅ **DNS TXT** — обе записи на apex `iber.dev`: токен сервис-аккаунта (`ddFX9ll…`, Cloudflare record `0f148281dc6fe661a730c2bec70aa5a7`) и токен `tech@niftsy.io` (`UdDc83q…`). Зона оказалась доступна нашему токену — предположение про чужой Cloudflare-аккаунт не подтвердилось, оно шло из устаревшей документации инфраструктуры
- ✅ **GSC верифицирован** владельцем под `tech@niftsy.io`, оба сервис-аккаунта добавлены: `iber-analytics@` — Restricted, `unisafe-driven@` — Full
- ✅ **Sitemap подан** 17:20 UTC, `isPending`, 0 ошибок и предупреждений
- ✅ **Repository secrets** заведены, выгрузка прогнана
- ✅ **`tech@niftsy.io`** видит property в GA4
- ✅ **Enforce HTTPS**

**Осталось:**
1. **Связать GA4 ↔ Search Console** — только через UI, ресурса в Admin API не существует (проверено в discovery-документе v1beta и v1alpha). Инструкция в разделе «Связка GA4 ↔ Search Console» ниже, включая неочевидную публикацию коллекции отчётов.
2. **Снять `roles/iam.serviceAccountKeyAdmin`** с `unisafe-driven@` — ключ выпущен, роль отработала. Пока она висит, это бессрочное право заново выпускать ключи к reporting-аккаунту, то есть возможность восстановить доступ после любого отзыва. Именно снятие делает выбранный вариант приемлемым:
   ```bash
   gcloud iam service-accounts remove-iam-policy-binding \
     iber-analytics@digital-yeti-501512-j9.iam.gserviceaccount.com \
     --member="serviceAccount:unisafe-driven@digital-yeti-501512-j9.iam.gserviceaccount.com" \
     --role="roles/iam.serviceAccountKeyAdmin" \
     --project=digital-yeti-501512-j9
   ```
   Проверить снятие извне нельзя — чтения политики проекта нет ни у одного из наших аккаунтов.
3. **Bing Webmaster Tools** — импорт из GSC, теперь возможен.
4. **Через 2–3 дня** — первый осмысленный baseline: показы и позиции в Search Analytics, статус разбора sitemap.

**Ротация ключа:** у выпущенного USER_MANAGED ключа `valid_before: 9999-12-31` — срока жизни нет, это дефолт GCP. Ротация только вручную. Ключ лежит в секретах публичного репозитория, поэтому стоит держать в поле зрения.

**Принятые решения (2026-07-26):**

- **Ключ сервис-аккаунта — заводим отдельный read-only.** Существующий `unisafe-driven@digital-yeti-501512-j9` использовать не будем: он админ на *всех* GA4-property Envelop и owner GSC-property `unisafe.envelop.is`, а репозиторий `maxsiz/maxsiz.github.io` публичный. Радиус поражения несоразмерен задаче «раз в неделю прочитать отчёт по одному сайту».

  **Блокер:** `iam.googleapis.com` в проекте `digital-yeti-501512-j9` выключен, включить может только владелец GCP-проекта:
  `https://console.developers.google.com/apis/api/iam.googleapis.com/overview?project=1049818977794`

  После включения: создать SA без ролей на проекте → выдать ему `predefinedRoles/viewer` только на `properties/547103578` → в GSC добавить руками как restricted user → положить ключ в secret `GA_SERVICE_ACCOUNT_JSON`.

  До этого момента `analytics-report.yml` штатно выходит без ошибки, потому что секрета нет. Отчёты при необходимости снимаются локально: `GOOGLE_APPLICATION_CREDENTIALS=... GA4_PROPERTY_ID=547103578 python3 codex/scripts/ga4_report.py --days 7`.

- **Timezone property остаётся `Etc/UTC`.** Аудитория глобальная, привязка к иркутскому времени не даёт пользы, а UTC проще сводить с другими источниками. Решение принято до накопления данных осознанно — менять его позже значит получить разрыв в исторических сравнениях. На `ga4_report.py` не влияет: скрипт задаёт диапазон датами, а не временем.

**Открытый вопрос:**
- **Размещение property.** Создан внутри GA4-аккаунта `Envelop_acc` (`accounts/393356740`), потому что другого доступного нет. Создание GA4-аккаунта через API запрещено правилами Google. Если iber.dev должен жить в отдельном аккаунте — аккаунт заводится руками в UI, потом Admin → Property → Move.

**Baseline GSC снять сейчас невозможно:** данные начинают копиться с момента верификации, задним числом Search Console их не восстанавливает. Реальный baseline — примерно через 3 дня после появления TXT-записи.

### Почему одной TXT-записи мало

Токен верификации Google привязан к **конкретному аккаунту**. Если верифицировать домен только токеном сервис-аккаунта, единственным владельцем property станет он — и выбраться из этого нельзя:

- в Search Console API **нет методов управления доступом**. Проверено по discovery v1: есть `sites` (add/delete/get/list), `sitemaps`, `searchanalytics`, `urlInspection`, `urlTestingTools` — и всё;
- сервис-аккаунт не может выдать доступ человеку;
- человек не может выдать доступ сервис-аккаунту, не будучи сам владельцем;
- связка GA4 ↔ GSC требует живого аккаунта, у которого одновременно verified owner в GSC и Editor/Administrator в GA4.

**Поэтому на apex нужны две TXT-записи** (несколько TXT на одном имени сосуществуют нормально):
1. токен сервис-аккаунта — добавлен
2. токен `tech@niftsy.io` — берётся в GSC → Add property → Domain → `iber.dev`, значение будет другим

Верифицировать домен нужно **под `tech@niftsy.io`**, иначе владельцем станет сервис-аккаунт и связка GA4 ↔ GSC станет невозможной.

### Связка GA4 ↔ Search Console (только вручную)

Ресурса в Admin API нет ни в v1beta, ни в v1alpha — есть `bigQueryLinks`, `googleAdsLinks`, `adSenseLinks`, `searchAds360Links`, `displayVideo360AdvertiserLinks`, `firebaseLinks`, и всё. Автоматизировать нечем.

**Предусловия (без них кнопка связки не сработает):**
- аккаунт — verified owner в GSC для `iber.dev`
- тот же аккаунт — Editor или Administrator в GA4 property `547103578`

**Важно про порядок:** домен в GSC надо верифицировать **под тем аккаунтом, который потом делает связку**. Если верификацию выполнит сервис-аккаунт, owner'ом станет он, и список на шаге 5 окажется пустым.

**Шаги:**
1. `analytics.google.com` → убедиться, что выбрано property **iber.dev** (в аккаунте `Envelop_acc` есть ещё unisafe и Envelop Index)
2. **Admin** (шестерёнка внизу слева)
3. Колонка **Property** → **Product links** → **Search Console links**
4. **Link**
5. **Choose accounts** → `iber.dev` → **Confirm**
6. **Next** → web stream `iber.dev` (`https://iber.dev`) → **Next**
7. **Submit**

**Шаг, который обычно пропускают:** коллекция отчётов Search Console в GA4 по умолчанию не опубликована, и связка сама по себе ничего не показывает.

8. **Reports** → **Library** (внизу слева)
9. Карточка коллекции **Search Console** → «⋮» → **Publish**
10. В левом меню появляется раздел с отчётами «Queries» и «Google organic search traffic»

Данные подтягиваются в течение примерно 48 часов после связки.

**Требует уточнения у партнёров (§3.4):**
- `ubdn.com` — 404 на корне, 403 глубже. Похоже на WAF, а не на мёртвый сайт. Ссылка оставлена
- `exolover.io` — плавает между 200 и Cloudflare 520. Ссылка оставлена
- `demeter.site` — DNS не резолвится. Ссылка снята, логотип оставлен

**Осознанно не делалось:**
- Тела старых постов не редактировались — это переписывание, а не перелинковка
- Slug'и постов не менялись (§7.1)
- Performance/CWV, AI/GEO, CI с html-proofer — см. «Не в этом заходе»

---

## Текущее состояние (аудит)

| Категория | Оценка | Комментарий |
|---|---|---|
| Технический SEO (шаблоны) | 8/10 | `_includes/head.html`, `structured-data.html` — хорошо |
| Индексация (sitemap, robots) | 7/10 | ~~`sitemap.xml` на проде отдаёт HTTP 500~~ — **не подтвердилось**, см. «Перепроверка фактов» ниже |
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

## Перепроверка фактов (2026-07-26)

Часть находок аудита проверена повторно напрямую по проду и репозиторию. Результаты меняют приоритеты — читать до начала работ.

| Проверка | Результат | Следствие |
|---|---|---|
| `https://iber.dev/sitemap.xml` | **HTTP 200**, валидный XML, 18 `<loc>` | Блокер §1.1 **не подтверждён**, пункт переформулирован |
| `https://iber.dev/` `/robots.txt` `/feed.xml` | 200 | ок |
| `https://maxsiz.github.io/` | 301 → **`http://`**`iber.dev/` | Новый пункт §1.4 |
| `img/bigsolidity_black2.png` (`default_share_image`) | **1185×309** (≈3.8:1) | Новый пункт в §5.1 |
| `img/iber_0_300.png` (`logo`) | **300×184**, не квадрат | Новый пункт в §5.1 |
| `timezone` в `_config.yml` | `Irkutsk/IRKT` — невалидный TZ id | Новый пункт §1.3 |
| Внешние CDN (`maxcdn.bootstrapcdn.com`, Google Fonts) | 200, живы | ок, но см. «Не в этом заходе» |
| Контактные поверхности сайта | только footer (`mailto:`, `t.me/msmobile`, соцсети), `t.me/tasisita` на `iber-group-team.md`, PDF в `/files/`. **Форм нет** | Определяет состав конверсий, Фаза 9 |

**Вывод:** факты в задаче могут устареть между её написанием и исполнением. Перед стартом работ прогнать проверки из Фазы 0 заново.

---

## Фаза 0. Подготовка

**Цель:** зафиксировать baseline и не сломать прод.

- [ ] Собрать сайт локально: `bundle exec jekyll build`
- [ ] Проверить, что `_site/sitemap.xml` генерируется без ошибок
- [ ] Сравнить локальный sitemap с продом: `curl -I https://iber.dev/sitemap.xml`
- [ ] Зафиксировать baseline в Search Console / GA (если есть доступ)
- [ ] Создать ветку `task/004-seo-fixes`
- [ ] **Прогнать перепроверку фактов заново** (таблица выше устареет):
  ```bash
  curl -sI https://iber.dev/sitemap.xml | head -1
  curl -sI https://maxsiz.github.io/ | grep -i location
  for u in https://ubdn.com/ https://izzz.io/ https://demeter.site/ https://exolover.io/ \
           https://itsynergis.ru/ https://peaceplus.org/ https://envelop.is/ https://iber.homes/; do
    printf "%-28s " "$u"; curl -sSo /dev/null -w "%{http_code}\n" -L --max-time 10 "$u" || echo DEAD
  done
  ```

**Критерий готовности:** актуальный список того, что реально сломано, а что уже нет.

---

## Фаза 1. Критические исправления (блокеры)

### 1.1. Sitemap: валидация и подача в Search Console

**Было заявлено:** `https://iber.dev/sitemap.xml` отдаёт HTTP 500.
**Фактически (2026-07-26):** отдаёт **200**, валидный XML, 18 URL — все посты, все страницы, `/tags`, `/`. Аварии нет, приоритет понижен с блокера.

**Реальные дефекты sitemap:**

1. **`/page2/` в sitemap** — страница пагинации с тем же title/description, что `/`. Прямой дубль в индексе. Связано с §2.3.
2. **Нет `lastmod` у страниц** — есть только у постов (берётся из даты поста). Для `aboutus`, `development`, product pages — пусто.
3. **`/files/CryptoIndexAudit_v3.00_eng.pdf` в sitemap** — PDF индексируется и может конкурировать в выдаче с `products_audit`. Решить осознанно: оставить или исключить.

**Важно:** `jekyll-sitemap` не умеет ни исключать пагинацию, ни задавать `priority`/`changefreq`. `sitemap: false` на `index.html` уберёт из sitemap и саму главную, потому что `/page2/` — её же сгенерированная копия с тем же front matter. Отсюда:

> **§1.1, §2.3 и §7.2 решаются одним изменением и должны идти вместе.**
> Варианты: (а) `noindex, follow` на `/page2+` через `head.html` и оставить их в sitemap как есть, (б) свой `sitemap.xml` Liquid-шаблоном вместо плагина — полный контроль над составом, `lastmod` и приоритетами.
> Рекомендация: (а) сейчас, (б) — если понадобятся приоритеты из §7.2.

**Шаги:**
1. `bundle exec jekyll build`, сверить `_site/sitemap.xml` с продом
2. Реализовать выбранный вариант исключения пагинации
3. После деплоя: `curl -I https://iber.dev/sitemap.xml` → `200`
4. Подать sitemap в Search Console (см. §9.4 — сначала нужна верификация домена)

**Критерий:** sitemap содержит все канонические URL и не содержит страниц пагинации; sitemap принят в GSC без ошибок.

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

> Замена ID — только первый шаг. Сам по себе он не даёт ни конверсий, ни регулярной отчётности, то есть KPI из §8.2 остаются неизмеримыми. Полный контур — **Фаза 9**.

---

### 1.3. Невалидный timezone в `_config.yml`

**Проблема:** `timezone: "Irkutsk/IRKT"` — такого идентификатора нет в базе TZ. Валидный — `Asia/Irkutsk`. Сейчас значение игнорируется, даты трактуются как UTC (в sitemap `lastmod` идёт с `+00:00`).

**Файл:** `_config.yml`

**Шаги:**
1. `timezone: "Asia/Irkutsk"`
2. `bundle exec jekyll build`, проверить, что даты постов и `lastmod` в `_site/sitemap.xml` не поехали на сутки

**Критерий:** сборка проходит, даты постов в листинге и в sitemap совпадают с датами в именах файлов.

---

### 1.4. Лишний http→https hop со старого домена

**Проблема:** `https://maxsiz.github.io/` отдаёт 301 на **`http://iber.dev/`** (не на https). Каждый переход со старого домена — лишний редирект и незашифрованный первый хоп.

**Шаги:**
1. GitHub → Settings → Pages → проверить, что **Enforce HTTPS** включён
2. Если включён, но редирект всё равно на http — пересохранить custom domain (перевыпуск сертификата)
3. Проверить: `curl -sI https://maxsiz.github.io/ | grep -i location` → ожидается `https://iber.dev/`

**Критерий:** редирект ведёт сразу на `https://iber.dev/`.

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

**Проблема:** `/page2/` уже существует (6 постов при `paginate: 5`), уже с тем же title/description, что и `/`, и **уже попал в sitemap** — это не риск на будущее, а текущий дубль. Делать вместе с §1.1 и §7.2.

**Файлы:** `index.html`, `_includes/head.html`

**Шаги:**
1. Добавить логику для `paginator.page`
2. Для page > 1:
   - title: `Blog — Page 2 | Iber`
   - description: отдельный или с суффиксом «Page 2»
3. Добавить `<link rel="prev">` / `<link rel="next">` для пагинатора
4. Альтернатива (проще и рекомендуется): `noindex, follow` для `/page2/` и далее

**Как сделать (вариант 4):** `head.html` уже поддерживает `page.robots`, но front matter у всех страниц пагинации общий — он наследуется от `index.html`. Различить их можно только по объекту `paginator`, доступному при рендере:

```liquid
{% assign seo_robots = page.robots | default: "index, follow, ..." %}
{% if paginator and paginator.page > 1 %}
  {% assign seo_robots = "noindex, follow" %}
{% endif %}
```

**Критерий:** нет дублей title/description между страницами пагинации; `/page2/` не индексируется и не лежит в sitemap.

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

### 3.3a. Хотлинк чужого логотипа в `partner.md`

**Проблема:** логотип Iber.Homes подключён напрямую с чужого сайта:

```
https://iber.homes/_next/static/media/logo.309b696f.svg
```

`309b696f` — хэш из бандла Next.js. При следующем деплое iber.homes имя файла изменится и картинка молча отвалится. Плюс лишний внешний запрос при рендере.

**Шаги:**
1. Скачать SVG в `img/iber_homes_logo.svg`
2. Заменить ссылку в `partner.md` на локальную

**Критерий:** ни один `<img>` на сайте не тянется с внешнего домена.

---

### 3.4. HTTPS и живость внешних ссылок

**Проблема:** на `partner.md` есть `http://` ссылки, и часть партнёрских сайтов недоступна.

**Фактическая проверка (2026-07-26) — перепроверить перед работой:**

| Ссылка | Статус | Решение |
|---|---|---|
| `demeter.site` | **DNS не резолвится** — домен мёртв | Убрать блок или заменить на актуальный URL |
| `ubdn.com` | **404** на корне | Уточнить у партнёра рабочий URL |
| `exolover.io` | **520** (ошибка Cloudflare на их стороне) | Перепроверить перед релизом, при повторе — уточнить у партнёра |
| `izzz.io` | HTTPS жив (403 только на HEAD — блокируют ботов) | `http://` → `https://` |
| `itsynergis.ru` | 200 по HTTPS | `http://` → `https://` |
| `peaceplus.org` | 200 по HTTPS | `http://` → `https://`, **убрать двойной слэш** в `http://peaceplus.org//` |
| `envelop.is`, `iber.homes` | 200 по HTTPS | ок |

**Дополнительно:** все внешние ссылки на `partner.md` идут с `{:target="_blank"}` **без `rel="noopener"`** — kramdown его не добавляет. Это и security-дыра (доступ к `window.opener`), и замечание Lighthouse Best Practices.

**Шаги:**
1. Прогнать проверку статусов заново (см. Фазу 0)
2. Заменить рабочие `http://` на `https://`
3. По мёртвым — убрать или заменить, решение зафиксировать в коммите
4. Добавить `rel="noopener"` ко всем `target="_blank"`
5. Решить вопрос `rel="nofollow"` / `sponsored` для партнёрских ссылок — если размещение взаимное/коммерческое, `sponsored` формально корректнее

**Критерий:** нет `http://`-ссылок на живые сайты, нет ссылок на мёртвые домены, у всех `target="_blank"` есть `rel="noopener"`.

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

**Приоритетная проблема, не отмеченная в аудите:** `default_share_image: /img/bigsolidity_black2.png` имеет размер **1185×309** — соотношение ≈3.8:1 вместо требуемых 1.91:1. Так как `default_share_image` задан всегда, `head.html` всегда выставляет `twitter:card = summary_large_image`. Итог: **на всех страницах сайта превью обрезается** — в Twitter/X, Facebook, LinkedIn, Telegram, Slack, WhatsApp. Это бьёт по CTR всех расшариваний, а исправляется одной картинкой.

- [ ] **Сделать `default_share_image` 1200×630** (логотип + название + краткий дескриптор на тёмном фоне)
- [ ] `logo: /img/iber_0_300.png` — **300×184, не квадрат**. В JSON-LD `Organization.logo` Google ожидает изображение с известными пропорциями: либо подготовить квадратный вариант, либо добавить `width`/`height` в `ImageObject` (см. §4.1)
- [ ] В `_includes/head.html` добавить `og:image:width`, `og:image:height`, `og:image:alt` — без них часть парсеров не показывает большую карточку
- [ ] Для постов с `image:` — использовать как `share-img` (или автоматически в head)
- [ ] Для product pages — подготовить 1200×630 px превью (можно из существующих assets)
- [ ] Проверить абсолютные URL через `absolute_url`

**Файлы:** `_config.yml`, `img/`, front matter страниц, `_includes/head.html`

**Проверка размера:**
```bash
python3 -c "from struct import unpack; d=open('img/bigsolidity_black2.png','rb').read(33); print(unpack('>II', d[16:24]))"
```

### 5.2. OG article tags для постов

**Файл:** `_includes/head.html`

- [ ] Для `layout == "post"` добавить `article:tag` для каждого tag
- [ ] `article:modified_time` если есть `last_modified_at`

---

## Фаза 6. Контент и E-E-A-T

### 6.1. Редактура ключевых страниц

| Страница | Что исправить |
|---|---|
| `_posts/2018-11-26-Ethereum-talks.md` | **`title: Ethereum tallks` → `Ethereum talks`** — приоритет выше остальных опечаток |
| `development.md` | Softwear → Software, Hardwear → Hardware, planing → planning |
| `aboutus.md` | Грамматика, усилить expertise signals (годы, проекты, компания) |
| `index.html` | Subtitle: *hard recognizable* → *hard to recognize* |
| `_posts/2016-03-20-Ethereum_blog_1.md` | `fisrt` → `first`; двойной пробел в `title: Ethereum blog review  - number 1` |
| `_posts/2025-12-09-Risks_Crypto_2026.md` | Ведущий пробел в `subtitle` |
| Старые посты | Минимальная вычитка без переписывания смысла |

> **Почему опечатка в заголовке поста важнее опечатки в subtitle:** `title` попадает в `<title>`, в `og:title`, в сниппет выдачи и в листинг главной. «Ethereum tallks» видят и Google, и посетитель.
>
> **URL при правке `title` не меняется** — `permalink: /:year-:month-:day-:title/` строит адрес из имени файла, а не из front matter. Редиректы не нужны, риска нет.

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

**Уточнение (в исходной формулировке было неверно):** утверждение «для GitHub Pages redirects ограничены» некорректно. Плагин **`jekyll-redirect-from` входит в allowlist GitHub Pages** и генерирует страницы-редиректы с meta-refresh и `rel=canonical`. Механизм есть.

Но это HTML-редирект, а не серверный 301: вес ссылок передаётся хуже, а старый URL остаётся физическим файлом в сборке.

**Рекомендация не меняется, но обоснование другое:**
- **Не менять** URL существующих постов — не потому что нельзя, а потому что выигрыш от косметики URL меньше цены работ и риска для 6 постов с накопленной историей
- **Для новых постов** — дефисы в filename: `2026-01-15-crypto-risks-outlook.md`
- Если URL всё же менять — только через `jekyll-redirect-from`, добавив плагин в `_config.yml` и `redirect_from:` в front matter каждого перенесённого поста

### 7.2. Sitemap с приоритетами

- [ ] Кастомный `sitemap.xml` layout — **`jekyll-sitemap` приоритеты не поддерживает**, конфигом это не решается
- [ ] Приоритеты: `/` = 1.0, product pages = 0.8, posts = 0.6, tags = 0.5
- [ ] `lastmod` из git или `last_modified_at` в front matter (сейчас `lastmod` есть только у постов)
- [ ] Исключить `/page2/` и далее (см. §1.1, §2.3)

*Кастомный шаблон закрывает разом все три дефекта sitemap из §1.1. Если решено идти этим путём — §1.1, §2.3 и §7.2 делаются одним коммитом, а не в разных спринтах. Google, впрочем, `priority` и `changefreq` игнорирует уже много лет, так что реальная ценность здесь — контроль состава и `lastmod`, а не приоритеты.*

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

## Фаза 9. Аналитика: автоматизация сбора статистики (GA4 + gtag)

**Зачем отдельная фаза.** §1.2 меняет один ID в конфиге — этого мало. Без событий, конверсий и регулярной выгрузки KPI из §8.2 («конверсии», «органический трафик») измерять нечем, а раз в месяц ходить руками в четыре разных интерфейса никто не будет. Фаза 9 делает сбор статистики автоматическим.

### 9.1. Решение по стеку тегирования

В репозитории лежат три взаимоисключающих механизма аналитики:

| Include | Ключ в `_config.yml` | Состояние |
|---|---|---|
| `_includes/gtag.html` | `gtag` | **Активен**, стоит UA-ID |
| `_includes/gtm_head.html` + `gtm_body.html` | `gtm` | Выключен (ключ закомментирован) |
| `_includes/google_analytics.html` | `google_analytics` | Выключен, это старый UA `analytics.js` |

**Рекомендация:** остаться на прямом gtag. Сайт статический, тегов мало, менять их часто никто не будет — GTM добавит ~30 КБ JS в критический путь без выигрыша. GTM оправдан только если появится потребность менять теги без редеплоя.

- [ ] Зафиксировать решение (gtag, не GTM)
- [ ] Удалить мёртвый `google_analytics.html` из цепочки `head.html` — или явно решить оставить

### 9.2. GA4 property и Measurement ID

**Требуется от владельца сайта — блокирует всю фазу:**
- [ ] Measurement ID `G-XXXXXXXXXX`
- [ ] Роль Editor на GA4 property (нужна, чтобы отмечать key events)
- [ ] Доступ к Search Console property `iber.dev`

**Шаги:**
1. Создать GA4 property для `iber.dev` (data stream — Web)
2. Заменить `gtag: "UA-129780126-1"` → `gtag: "G-XXXXXXXXXX"` в `_config.yml`
3. `_includes/gtag.html` править **не нужно** — он универсален и работает с `G-` как есть

### 9.3. События и ключевые конверсии

Enhanced Measurement в GA4 закрывает автоматически: `page_view`, `scroll`, `click` (исходящие), `file_download` — последний сработает на `/files/CryptoIndexAudit_v3.00_eng.pdf`.

**Не закрывает `mailto:` и `tel:`.** А на сайте **нет ни одной формы**, поэтому единственные конверсионные действия — это клики по контактам:

- footer: `mailto:maxsizmobile@gmail.com`, `t.me/msmobile`, github, linkedin, twitter, instagram, facebook
- `iber-group-team.md`: `t.me/tasisita`
- скачивание PDF из `/files/`

**Шаги:**
1. Новый `_includes/gtag-events.html`, подключается в `head.html` сразу после `{% include gtag.html %}`, весь код обёрнут в `{% if site.gtag %}` — чтобы при пустом ID ничего не ломалось
2. Один делегированный слушатель на `document` (не вешать обработчики на каждую ссылку):
   - событие **`contact_click`**, параметры: `method` (`email` | `telegram` | `github` | `linkedin` | `twitter`), `link_url`, `link_location` (`footer` | `body`)
   - селекторы: `a[href^="mailto:"]`, `a[href*="t.me/"]`, ссылки соцсетей футера, `a[href*="/files/"][href$=".pdf"]`
3. В GA4 Admin → Events отметить **`contact_click`** и **`file_download`** как **Key events** (бывшие conversions)
4. Проверить в GA4 DebugView: открыть прод, кликнуть по email и по Telegram — события должны появиться с корректным `method`

**Критерий:** есть измеримая конверсия. До этого шага метрика «конверсии» в §8.2 не существует.

### 9.4. Связки и верификация источников

- [ ] **GA4 ↔ Search Console** (Admin → Product links) — органические запросы становятся видны внутри GA4
- [ ] **Верификация домена в GSC** — метод: **DNS TXT** (предпочтительно: не слетает при редеплое и не зависит от шаблонов). Альтернатива — meta `google-site-verification` через новый ключ в `_config.yml` + строка в `head.html`
- [ ] **Подать sitemap в GSC** (см. §1.1)
- [ ] **Bing Webmaster Tools** — импорт настроек из GSC в один клик. Питает Bing, Copilot и ChatGPT Search, то есть работает напрямую на «AI-выдачу» из цели задачи
- [ ] Решить по Яндекс.Вебмастеру — у части старого контента RU-происхождение (LJ), но сайт англоязычный. Скорее нет, но решение зафиксировать

### 9.5. Автоматическая выгрузка отчётов

Собственно автоматизация: регулярный машинный сбор без ручных заходов в интерфейсы.

**Стек:**
- GA4 Data API v1 — `google-analytics-data`
- Search Console API — `google-api-python-client`
- Авторизация — **service account**; выдать ему Viewer на GA4 property и на GSC property

**Окружение:** локально есть `python3` 3.12, библиотек `google-*` нет → отдельный venv. С Jekyll-стеком не смешивать, в `Gemfile` ничего не добавлять.

**Размещение:**
- `codex/scripts/ga4_report.py`, `codex/scripts/requirements.txt`
- каталог `codex/` уже в `exclude` в `_config.yml` → в собранный сайт не попадёт
- **JSON-ключ service account в репозиторий не класть.** Путь через `GOOGLE_APPLICATION_CREDENTIALS`, отдельно проверить `.gitignore`

**Состав отчёта:**

| Источник | Метрики |
|---|---|
| GA4 Data API | `sessions`, `totalUsers`, `sessionDefaultChannelGroup`, landing page, key events (`contact_click`) |
| Search Console API | impressions, clicks, CTR, position — всего и по целевым запросам из §8.2 |

**Периодичность:** еженедельно. Стандартные отчёты GA4 отстают на 24–48 ч, поэтому ежедневная выгрузка даст «дрожащие» цифры; realtime — отдельный эндпоинт и для отчётности не нужен.

**Запуск:** GitHub Actions `schedule` cron в этом же репозитории, service-account JSON в repository secret — своего сервера не требует. Альтернатива — cron на нашем хосте.

**Доставка:** markdown в `codex/reports/YYYY-MM.md` коммитом и/или сообщение в Telegram. Выбрать при реализации.

**Шаги:**
1. Создать service account + ключ, выдать доступы
2. `codex/scripts/ga4_report.py` — параметры `--start`, `--end`, вывод в markdown
3. Прогнать локально за прошлую неделю, сверить с интерфейсом GA4
4. Завести GitHub Actions workflow с cron и secret
5. Дождаться первого автоматического прогона

### 9.6. Consent и приватность

GA4 без баннера согласия для трафика из EEA/UK — это и потеря данных (без Consent Mode v2 Google режет сбор и переходит на моделирование), и compliance-риск. Компания зарегистрирована в SG, аудитория глобальная.

**Решение принято 2026-07-26: вернуться к вопросу после первых данных.**

Обоснование: доля трафика из ЕС и Великобритании сейчас неизвестна — GA4 ещё не собирал данные, а строить баннер под гипотетическую аудиторию значит гарантированно потерять часть статистики ради риска, величина которого не измерена.

**Порядок действий:**
1. Запускаем GA4 без consent-баннера
2. Через 1–2 месяца смотрим в GA4 отчёт по странам, доля EEA + UK
3. Если доля заметная — ставим минимальный баннер и `gtag('consent', 'default', {...})` до инициализации тега
4. Если единицы процентов — оставляем как есть и фиксируем это здесь

**Ревизия:** ориентировочно сентябрь–октябрь 2026, после первого полного месяца данных.

- [x] Решение записано в этот файл

### Definition of Done фазы 9

- [ ] GA4 Realtime видит визиты с прода
- [ ] `contact_click` появляется в DebugView при клике по email и по Telegram, с корректным `method`
- [ ] `contact_click` и `file_download` отмечены как key events
- [ ] GA4 связан с Search Console, домен верифицирован, sitemap подан
- [ ] Bing Webmaster подключён
- [ ] Скрипт выгружает отчёт за произвольный период одной командой
- [ ] Cron настроен и отработал минимум один раз
- [ ] Решение по Consent Mode зафиксировано

---

## Предлагаемый порядок работ (спринты)

*Порядок пересобран после перепроверки фактов: несуществующий фикс sitemap убран из блокеров, вверх подняты дешёвые правки с широким эффектом.*

### Спринт 1 (1 день) — дешёвое и с широким эффектом
1. `timezone` → `Asia/Irkutsk` (§1.3) — одна строка
2. Enforce HTTPS в GitHub Pages (§1.4) — настройка, не код
3. **OG-изображение 1200×630** (§5.1) — одна картинка, чинит превью всех страниц сразу
4. GA4 Measurement ID (§1.2, §9.2) — блокирует Фазу 9, запрашивать доступы в первый же день
5. Meta description для всех постов (§2.1)
6. Опечатка в заголовке поста `Ethereum tallks` (§6.1)

### Спринт 2 (1–2 дня) — on-page и ссылки
7. `meta-title` для коммерческих страниц (§2.2)
8. Alt для partner/product images (§3.3) + локальная копия логотипа Iber.Homes (§3.3a)
9. Viewport fix (§3.1)
10. HTTP → HTTPS, мёртвые ссылки, `rel="noopener"` на partner (§3.4)
11. **События `contact_click` + key events в GA4 (§9.3)** — после этого KPI «конверсии» становится измеримым

### Спринт 3 (2–3 дня) — sitemap, structured data, автоматизация
12. **Sitemap одним блоком: §1.1 + §2.3 + §7.2** — пагинация, `lastmod`, состав
13. Organization sameAs (§4.1) + `og:image:width/height/alt` (§5.1)
14. BreadcrumbList (§4.2)
15. Service schema для development/audit (§4.3)
16. OG article tags (§5.2)
17. **Автовыгрузка отчётов GA4 + GSC, cron (§9.5)**
18. GSC-верификация, Bing Webmaster (§9.4)

### Спринт 4 (ongoing) — контент
19. Вычитка development/about/index (§6.1)
20. H1 fix в header (§3.2)
21. Person schema для team/about (§4.4)
22. Внутренняя перелинковка (§6.3)
23. Контент-план и новые посты (§6.2)

---

## Что сознательно не делать

| Не делать | Почему |
|---|---|
| `meta keywords` | Google не использует |
| `hreflang` | Сайт одноязычный (EN) |
| Массовая смена URL постов | Риск потери ссылочного веса без redirects |
| `geo.region` RU | Компания SG, аудитория global — не актуально |
| Переписывание всего контента | Disproportionate; точечные правки достаточно |
| Переход на GTM | Статический сайт, теги меняются редко — лишний JS в критическом пути (§9.1) |
| Ежедневная выгрузка GA4 | Данные отстают на 24–48 ч, ежедневные цифры нестабильны (§9.5) |

---

## Не в этом заходе — кандидаты в задачу #5

Найдено при перепроверке, но выходит за рамки SEO-задачи. Записано, чтобы не потерялось.

### Performance / Core Web Vitals
CWV присутствует в KPI (§8.2), но ни одного пункта работ под него в задаче нет:
- Google Fonts (2 семейства, много начертаний) и font-awesome с `maxcdn.bootstrapcdn.com` — рендер-блокирующие, без `preconnect` и без `&display=swap`, подключены протокол-относительными `//` URL
- у `<img>` нет `width`/`height` → CLS на превью постов и логотипах партнёров
- jQuery 1.11.2 (2015 г.; в jQuery <3.5 известные XSS) + Bootstrap 3 — решить: обновлять или осознанно оставить
- неиспользуемые ассеты темы: `img/install-steps.gif` — 803 КБ, `img/path.jpg` — 268 КБ (это половина всего каталога `img/`)

### AI / GEO
В цели задачи заявлена «AI-выдача», но ни одного пункта под неё нет:
- `llms.txt` в корне — машиночитаемая справка: чем занимается Iber, услуги, ключевые страницы, контакты
- осознанная политика по AI-краулерам в `robots.txt`: `GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`, `CCBot`, `Google-Extended`. Сейчас `Allow: /` для всех — это умолчание, а не решение
- `FAQPage` schema на `development.md` и `products_audit.md` — короткие вопрос-ответ блоки хорошо цитируются AI-поиском
- частично закрывается из этой задачи: Bing Webmaster (§9.4) питает Copilot и ChatGPT Search

### CI и защита от регрессий
- GitHub Actions: `bundle exec jekyll build --strict_front_matter` + `html-proofer` на каждый PR — битые внутренние ссылки, отсутствующие alt, недоступные внешние URL
- ловит ровно тот класс проблем, из-за которого в этой задаче появился «блокер» с sitemap
- сейчас в `.github/` только шаблоны issue/PR, workflow'ов нет

---

## Definition of Done

- [ ] `https://iber.dev/sitemap.xml` → 200, все канонические URL в Search Console, страниц пагинации в sitemap нет
- [ ] GA4 собирает данные, `contact_click` работает и отмечен как key event
- [ ] Отчёт GA4 + GSC выгружается автоматически по расписанию
- [ ] У каждой страницы и поста уникальные title + description
- [ ] Rich Results Test без критических ошибок
- [ ] OG-превью не обрезается (изображение 1200×630), проверено в Facebook Sharing Debugger
- [ ] Нет дублей H1, проблем с viewport, пустых alt на ключевых страницах
- [ ] Нет ссылок на мёртвые домены и `http://` на живые сайты
- [ ] JSON-LD: Organization + WebSite + page-specific schemas
- [ ] Контент на ключевых страницах вычитан
- [ ] Решение по Consent Mode зафиксировано

### Откат

Каждая фаза — отдельный коммит с префиксом `#4`. Откат любого шага = `git revert` коммита, GitHub Pages пересобирает сайт автоматически. Отдельного rollback-плана не требуется — исключение составляют изменения вне репозитория (настройки GA4, GSC, GitHub Pages), их нужно откатывать руками в интерфейсах.

---

## Ключевые файлы репозитория

| Файл | Роль в SEO |
|---|---|
| `_config.yml` | url, description, gtag, timezone, plugins, defaults |
| `_includes/head.html` | title, meta, canonical, OG, Twitter, подключение аналитики |
| `_includes/structured-data.html` | JSON-LD |
| `_includes/header.html` | H1, заголовки страниц |
| `_includes/gtag.html` | GA4 tag (менять не нужно, ID берётся из `_config.yml`) |
| `_includes/google_analytics.html` | мёртвый UA `analytics.js` — кандидат на удаление (§9.1) |
| `_layouts/base.html` | `lang` attribute, подключение CSS/JS |
| `robots.txt` | crawl rules, sitemap URL |
| `index.html` | homepage meta, pagination |
| `_posts/*.md` | blog posts — нужны meta-description |
| `404.html` | noindex |
| `partner.md`, `development.md`, etc. | on-page content |
| `img/bigsolidity_black2.png` | `default_share_image` — требует замены на 1200×630 (§5.1) |

### Новые файлы, создаваемые по задаче

| Файл | Назначение |
|---|---|
| `_includes/gtag-events.html` | события `contact_click` (§9.3) |
| `codex/scripts/ga4_report.py` | выгрузка отчётов GA4 + GSC (§9.5) |
| `codex/scripts/requirements.txt` | зависимости выгрузки (вне Jekyll-стека) |
| `codex/reports/YYYY-MM.md` | результаты автоматических выгрузок |
| `.github/workflows/analytics-report.yml` | cron для автовыгрузки (§9.5) |
| `img/iber_homes_logo.svg` | локальная копия хотлинкнутого логотипа (§3.3a) |
