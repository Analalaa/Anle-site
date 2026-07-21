# Milo Personal Website

This repository contains Milo's bilingual static personal website.

## Publish Directory

Deploy this directory:

```text
site/www.milo.me
```

It is a static site: HTML, CSS, JavaScript, images, and fonts only. There is no server, database, package install, or build step required.

## Current Structure

```text
site/www.milo.me/
├── index.html
├── about.html
├── photography.html
├── blogs.html
├── blogs/
│   ├── index.html
│   ├── meteor-record.html
│   ├── passage-migrant.html
│   └── sky-is-empty.html
├── zh/
│   ├── index.html
│   ├── about.html
│   ├── photography.html
│   ├── blogs.html
│   ├── blogs/
│   │   ├── index.html
│   │   ├── meteor-record.html
│   │   ├── passage-migrant.html
│   │   └── sky-is-empty.html
│   └── photography/
├── photography/
├── images/
├── _next/
├── favicon.ico
└── rss.xml
```

## Local Preview

```bash
cd site/www.milo.me
python3 -m http.server 8080
```

Open:

```text
http://localhost:8080
```

## Notes

- English and Chinese pages are separate static HTML files.
- The blog currently keeps only Milo's own posts: `Meteor Record`, `Passage Migrant`, and `The Sky Is Empty`.
- `_next/static/css` and `_next/static/media` are still required for styling and fonts.
- Old mirrored site cache, generated dependencies, and non-Milo blog files have been removed.
