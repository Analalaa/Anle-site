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

## Projects / 小作品

- Browse `projects.html` or `zh/projects.html` for the collection. Each project has an English and Chinese detail page under `projects/` and `zh/projects/`.
- Edit `content/projects.json` to update descriptions, order, or add projects. Set `url` to a verified public HTTPS address to show an “Open project” link, and update the availability note in both languages. An optional `source` provides a source-code link.
- Regenerate the static project pages with `python3 scripts/build_projects.py`. This only regenerates project pages; other pages are left intact. Commit/deploy the generated HTML with the rest of the site. No build is required to serve it.
- Project visuals are original HTML/SVG illustrations, not screenshots. Shared styling and navigation behavior live in `site/www.milo.me/assets/projects.css` and `projects.js`.
- Prompts and Date with me currently have no verified public link. Mood Recipe (the sail project) replaces Inner Music in the collection and accepts words or images to add music layers. Image interpretation requires a configured vision service; otherwise it uses a default image mood. The previous inner-music detail URLs redirect to Mood Recipe. Color Muse links to its source repository.

## Existing site notes

- English and Chinese pages are separate static HTML files.
- The blog currently keeps only Milo's own posts: `Meteor Record`, `Passage Migrant`, and `The Sky Is Empty`.
- `_next/static/css` and `_next/static/media` are still required for styling and fonts.
- Old mirrored site cache, generated dependencies, and non-Milo blog files have been removed.
