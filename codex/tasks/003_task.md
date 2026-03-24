# Task #3 SEO оптимизация статичного сайта  https://iber.dev/, 
хостинг  на github pages
## Общая информация
Цель оптимизации
Повысить позиции в традиционной выдаче (Google, Yandex)
Обеспечить корректное индексирование и понимание контента AI-поисковиками
Улучшить user experience и технические метрики
Подготовить сайт к эпохе семантического поиска и AI-агентов
Тип сайта: Статический сайт (HTML, CSS, JavaScript) - beautiful-jekyll
##  Технический SEO-аудит и оптимизация
Всегда Уччитывай best practice beautiful-jekyll
### 2.1. Мета-данные и структура
Необходимо проверить и оптимизировать:
```html
<!-- Пример целевого состояния -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <!-- Базовые мета-теги -->
    <title>Уникальный заголовок страницы | Бренд</title>
    <meta name="description" content="Четкое описание страницы (150-160 символов) с ключевыми словами">
    <meta name="keywords" content="ключевое слово1, ключевое слово2">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://example.com/page">
    
    <!-- Open Graph для социальных сетей -->
    <meta property="og:title" content="Заголовок для соцсетей">
    <meta property="og:description" content="Описание для соцсетей">
    <meta property="og:image" content="https://example.com/preview.jpg">
    <meta property="og:url" content="https://example.com/page">
    <meta property="og:type" content="website">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Заголовок для Twitter">
    <meta name="twitter:description" content="Описание для Twitter">
    <meta name="twitter:image" content="https://example.com/preview.jpg">
    
    <!-- Robots -->
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    
    <!-- Геотаргетинг (если применимо) -->
    <meta name="geo.region" content="RU">
</head>
```
Задачи:
Сгенерировать уникальные title и description для каждой страницы
Добавить Open Graph и Twitter Cards для всех страниц
Проверить и настроить canonical URL
Добавить hreflang для мультиязычных версий
Настроить robots meta и robots.txt

### 2.2. Структурированные данные (Schema.org)
Агенту необходимо добавить JSON-LD разметку для улучшения понимания контента AI-поисковиками:

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Название страницы",
  "description": "Описание страницы",
  "url": "https://example.com/page",
  "datePublished": "2016-01-01",
  "dateModified": "2026-03-20",
  "author": {
    "@type": "Organization",
    "name": "Название компании",
    "url": "https://example.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Название компании",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "mainEntity": {
    "@type": "Article",
    "headline": "Заголовок статьи",
    "articleBody": "Краткое содержание..."
  }
}
```
Типы Schema, которые могут потребоваться:
Article / BlogPosting (для статей и блога)
Product / Offer (для товаров и услуг)
FAQPage (для страниц с вопросами)
LocalBusiness (для локального бизнеса)
BreadcrumbList (для навигации)
SiteNavigationElement (для меню)

### 2.3. Семантическая HTML-структура
Необходимо проверить и оптимизировать HTML-разметку:

```html
<!-- Целевая структура -->
<body>
    <header>
        <nav aria-label="Главное меню">
            <ul>
                <li><a href="/" aria-current="page">Главная</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article>
            <header>
                <h1>Уникальный H1 на странице</h1>
                <p class="description">Краткое описание</p>
            </header>
            
            <section>
                <h2>Заголовок раздела H2</h2>
                <p>Содержимое...</p>
                
                <h3>Подраздел H3</h3>
                <p>Более детальное содержимое...</p>
            </section>
            
            <aside aria-label="Дополнительная информация">
                <!-- Связанный контент -->
            </aside>
        </article>
    </main>
    
    <footer>
        <nav aria-label="Нижнее меню">
            <!-- Ссылки -->
        </nav>
    </footer>
</body>
```
Проверки:
Один H1 на странице
Логическая иерархия заголовков (H2, H3, H4)
Использование семантических тегов: <article>, <section>, <aside>, <nav>
ARIA-метки для улучшения доступности
alt-атрибуты для всех изображений
title-атрибуты для ссылок (при необходимости)

### 2.4. Файлы robots.txt и sitemap.xml
robots.txt:
```txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/
Sitemap: https://example.com/sitemap.xml
sitemap.xml (с приоритетами и частотой обновления):
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/</loc>
        <lastmod>2024-03-20</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://example.com/article</loc>
        <lastmod>2024-03-19</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>
```

Примечание: Агент должен использовать актуальные данные по состоянию на 2025 год, учитывая последние обновления алгоритмов Google (Helpful Content Update, Core Web Vitals v2) и особенности работы AI-поисковиков.

