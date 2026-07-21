# Repository Notes

This is Milo's bilingual static personal website.

## Site Root

All publishable files live in:

```text
site/www.milo.me
```

There is no build step. Preview with:

```bash
cd site/www.milo.me
python3 -m http.server 8080
```

## Content Model

English and Chinese pages are separate HTML files.

- English pages: `index.html`, `about.html`, `photography.html`, `blogs.html`, `blogs/*.html`
- Chinese pages: `zh/index.html`, `zh/about.html`, `zh/photography.html`, `zh/blogs.html`, `zh/blogs/*.html`

The site currently keeps only Milo's own blog posts:

- `meteor-record.html`
- `passage-migrant.html`
- `sky-is-empty.html`

## Assets

Keep these directories unless replacing references in the HTML:

- `site/www.milo.me/_next/static/css`
- `site/www.milo.me/_next/static/media`
- `site/www.milo.me/images`
- `site/www.milo.me/photography/photos`

The old Next hydration scripts and embedded `__NEXT_DATA__` payloads have been removed so the site behaves as plain static HTML.
