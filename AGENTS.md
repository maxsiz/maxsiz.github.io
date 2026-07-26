# AGENTS.md

## Working Rules

- Do not guess requirements.
- Ask questions if anything is unclear or ambiguous.
- Make a short plan first and get approval before substantial edits.
- Prefer small, isolated commits.
- Never rewrite unrelated code or content.
- Explain before any destructive action.
- If tests exist, run them.
- Ask for confirmation before adding new production dependencies.

## Project Summary

- This repository is a static Jekyll site based on the Beautiful Jekyll theme.
- The live site configuration in `_config.yml` uses `url: https://maxsiz.github.io` and `baseurl: ""`.
- Custom domain is set via `CNAME` to `iber.dev`.
- The current local branch is `master`.
- `README.md` is mostly upstream theme documentation, not project-specific operational documentation.

## Stack

- Ruby/Jekyll site with `github-pages` gem pinned in `Gemfile`.
- Jekyll plugins enabled in `_config.yml`: `jekyll-paginate`, `jekyll-sitemap`.
- Docker-based local run is supported via `Dockerfile`.
- Frontend assets are mostly static HTML, Liquid templates, CSS, and JS.

## Repository Map

- `_config.yml`: primary source of truth for site metadata, navbar links, colors, analytics, pagination, plugins.
- `index.html`: homepage and paginated post listing.
- Root `*.md` files: standalone site pages such as `aboutus.md`, `development.md`, `partner.md`, product pages.
- `_posts/`: blog posts in Jekyll format with YAML front matter.
- `_layouts/`: page/post layout templates.
- `_includes/`: shared partials for head, nav, footer, analytics, comments, external assets.
- `_data/SocialNetworks.yml`: social network metadata used by the theme.
- `css/`, `js/`: static frontend assets. Some files are vendored theme/bootstrap/jquery assets.
- `img/`: site images.
- `files/`: downloadable static files such as PDFs.
- `.github/`: generic issue/PR templates from the upstream theme repo.

## Content Conventions

- New pages should usually be added as root-level `.md` files with YAML front matter.
- New posts belong in `_posts/` and should follow Jekyll naming: `YYYY-MM-DD-title.md`.
- Existing posts use front matter like `layout`, `title`, `subtitle`, `tags`.
- Navigation labels and page routing are controlled from `_config.yml` under `navbar-links`.
- Site title/logo/colors/footer/social links are also controlled from `_config.yml`.

## Edit Guidelines

- Prefer minimal edits in the most local place that solves the task.
- Treat `README.md` as theme reference only; validate any project-specific claim against actual files.
- Avoid changing vendored assets in `css/` and `js/` unless the task explicitly requires it.
- Do not rename pages, permalinks, or navigation entries without confirming the intended public URL impact.
- Be careful with analytics/comment/includes changes because they affect the whole site.
- Preserve existing YAML front matter and Liquid syntax formatting unless there is a reason to normalize it.
- Check for user-authored content quality issues, but do not mass-rewrite copy unless asked.

## Verification

- There is no dedicated test suite in this repository.
- Default verification for site changes is:
  - `bundle exec jekyll build`
  - optionally `bundle exec jekyll serve` for manual inspection
- Docker workflow from repository docs:
  - `docker build -t beautiful-jekyll "$PWD"`
  - `docker run -d -p 4000:4000 --name beautiful-jekyll -v "$PWD":/srv/jekyll beautiful-jekyll`
- If Ruby gems or other dependencies are missing, ask before installing anything new.

### Local setup (once per clone)

```bash
bundle config set --local path vendor/bundle
bundle install
git config core.hooksPath .githooks
```

- Gems install into `vendor/bundle`, which is gitignored and excluded in `_config.yml`.
  `exclude` in `_config.yml` **replaces** Jekyll's defaults, so `vendor` and `.bundle`
  must stay in that list or the build breaks with a site_template error.
- `Gemfile` pins `github-pages` to the version GitHub Pages itself builds with, so a
  local build matches production. Check https://pages.github.com/versions/ before bumping.
- `webrick` is an explicit dependency because it left Ruby's stdlib in 3.0 and
  Jekyll 3.x needs it for `jekyll serve`.

### Pre-commit check

`.githooks/pre-commit` runs `bundle exec jekyll build --strict_front_matter` and asserts
that `_site/sitemap.xml` exists and is non-trivial. A failing build aborts the commit.

- Enable with `git config core.hooksPath .githooks` (the hook lives in the repo, but git
  does not enable hooks automatically on clone).
- It builds the working tree, not the staged snapshot — it catches the common case, not
  every case.
- Bypass with `git commit --no-verify` when committing docs-only changes and the build
  is known good.

## Safe Assumptions For Future Work

- Most routine tasks here will be one of:
  - editing page/post content
  - adjusting navigation or metadata in `_config.yml`
  - changing layouts/includes for site-wide presentation
  - updating static assets in `img/`, `css/`, `js/`, or `files/`
- For any task that may affect public URLs, generated structure, or dependencies, stop and confirm first.

## Tasks

- Task files path: `./codex/tasks/`.
- Task file name mask: `001_task.md`.
- The first 3 filename characters are digits; convert them to an integer and use it in commit messages as `#<number>`.
- Example: `001_task.md` maps to `#1`.
- Ask the user which task file to take into work before starting task execution.
- Solve each task in a new branch.
