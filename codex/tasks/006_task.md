# Task #6 Страница «AI Agents» для https://iber.dev/

## Общая информация

**Цель:** показать на сайте AI-направление команды — конвейеры ИИ-агентов и внедрение агентов в Web3-продукты — одной страницей с отдельным пунктом меню.

**Контекст:** на сайте нет ни одного упоминания AI. SEO-аудит 2026-11-03: сервисные страницы (`research`, `development`, `aboutus`, `partner`, `products_code`) в статусе «Crawled – currently not indexed», `products_audit` не обходилась. Новая страница с уникальным содержанием и перелинковкой работает и на эту проблему.

**Ветка для реализации:** `task/006-ai-agents`

**Commit message prefix:** `#6`

**Статус (2026-11-03):** ✅ выкачено на прод, Request indexing отправлен владельцем для `/ai-agents/`, `/research/`, `/development/`.

**Решения владельца (2026-11-03):**
- одна страница, на ней всё, что затрагивает AI;
- пункт меню верхнего уровня «AI Agents»;
- язык — английский, как весь сайт.

---

## Исходные факты (проверено 2026-11-03)

| Проект | Что это | Публичность |
|---|---|---|
| **AI-Sandbox** (DefiDash / detracker) | Конвейер агентного онбординга DeFi-протоколов: researcher находит протоколы по формальным критериям → analyst пишет спецификацию вызовов и расчёта показателей → проверки кодом → critic → explainer → гейт человека (Telegram) → dev готовит draft-MR → golden-тест на исторических блоках. Оркестратор — код, не агент: переходы, лимиты, гейты. | Дашборд публичный: https://detracker.github.io/ai-sandbox-dashboard. Репозиторий `detracker/ai-sandbox` **приватный** |
| **Agent Factory / LP strategies** (Think Tank) | Фабрика агентов на шаблоне `template-factory-01`: находит, проверяет и выпускает стратегии концентрированной ликвидности Uniswap v4 для агента UniSafe. Бэктест на отложенных 30 % истории против HODL, критик (переобучение, депег, оракул, издержки), ступенчатый выкат paper → small → full с гейтом человека на каждой ступени. Фабрика не торгует и не держит ключей. | Репозиторий **публичный**: https://gitlab.com/ai-solutions-pipelines/factory-lp-strategies |
| **UniSafe: агентный контур эксплуатации** | Агент-дежурный по расписанию (daily/weekly/monthly), агент-лекарь (сам чинит задачи в изолированной копии, деплоер выкатывает, лимит задач в сутки), внешняя синтетика каждые 5 минут, алерты в Telegram. | Продукт публичный: https://unisafe.envelop.is. `qa-workspace` **приватный** |
| **UniSafe: менеджеры с поддержкой агентов** | StableLPManager — NFT-owned менеджер стейбл-LP на Uniswap V4; агент исполняет стратегии внутри policy владельца (Manager, Bounded Executor, Sponsor), без доступа к ключам владельца. | Продукт публичный |

---

## План страницы `ai-agents.md`

Permalink: `/ai-agents/` (новый публичный URL). Layout `page`, front matter по образцу `development.md`: `meta-title`, `meta-description`, `service-name`, `service-type`, `faq`.

1. **Intro.** Как мы строим агентов для Web3: формальные критерии, проверка кодом и критиком, человек на гейте, агент действует только внутри policy и без ключей.
2. **Agent pipelines** — AI-Sandbox и Agent Factory: что находят, что выпускают, как проверяется результат. Ссылки на публичный дашборд и публичный репозиторий.
3. **Agents in Web3 products** — UniSafe: менеджеры с поддержкой агентов, bounded execution, policy владельца.
4. **Agentic operations** — дежурный, лекарь, синтетический мониторинг, алерты.
5. **Principles** — короткий список: human gate, bounded permissions, no custody of keys, audit log of decisions.
6. **FAQ** (4–5 вопросов) → FAQPage JSON-LD уже генерируется темой из `faq:`.
7. **Related** — ссылки на `/development/`, `/research/`, `/products_eth/`, `/products_audit/`, пост `/2026-07-30-Ownership_Without_Custody/`.

## Сопутствующие правки (минимальные)

- [ ] `_config.yml` → `navbar-links`: `AI Agents: "ai-agents"`. Место в меню предлагаю после `Development`.
- [ ] `research.md`: строка в домены «AI agents for DeFi» со ссылкой на `/ai-agents/`.
- [ ] `development.md`: пункт «AI agent pipelines and agent integration for Web3» со ссылкой.
- [ ] `llms.txt`: добавить страницу.
- [ ] `sitemap.xml` (свой шаблон): убедиться, что страница попала, `lastmod` задан.

## Чего не публикуем

- IP, hostname, провайдер хостов, пути на боксах, имена секретов и сервис-аккаунтов.
- Ссылки на приватные репозитории (`ai-sandbox`, `qa-workspace`).
- Внутренние имена (Think Tank), лимиты, детали решений владельца с датами.
- Конкретные цифры бэктестов/PnL — только если владелец даст явно.

## Проверка

- [ ] `bundle exec jekyll build --strict_front_matter` (pre-commit)
- [ ] `/ai-agents/` в `_site`, в `sitemap.xml`, в меню на десктопе и мобильном
- [ ] FAQPage и canonical в head страницы
- [ ] Внешние ссылки отвечают 200

## После деплоя

- [x] GSC → URL Inspection → Request indexing для `/ai-agents/`, `/research/`, `/development/` (вручную владельцем)
