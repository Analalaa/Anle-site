# Milo Personal Website

Milo's bilingual static personal website: writing, photography, and small projects.

## Preview and deploy

Publish `site/www.milo.me`. See [deployment and .me domain setup](docs/deployment.md) for the prepared GitHub Pages workflow and the one-time publishing-source change. The checked-in HTML works without a runtime, package install, database, or build step.

```bash
cd site/www.milo.me
python3 -m http.server 8080
```

Open `http://localhost:8080/zh/index.html` for Chinese or `/index.html` for English.

## Edit content and regenerate pages

All pages share the same layout, navigation, typography, and theme controls. Edit the source content, then regenerate the static HTML:

```bash
python3 scripts/build_site.py
```

Commit/deploy the generated pages alongside the source content. The previous command `python3 scripts/build_projects.py` is retained as a compatibility entry point and now rebuilds the whole site, so project updates cannot reintroduce a different design.

- `content/site.json`: full original biographies and portrait. The shorter home introduction and shared labels live in `scripts/build_site.py`.
- `content/projects.json`: project order, descriptions, features, links, and availability in both languages. Set `url` to a verified public HTTPS address to show an “Open project” link; update the availability note in both languages. Optional `source` links to source code.
- `content/posts.json`: the three existing posts, their dates, categories, full bilingual bodies, and optional cover images. Bodies are trusted author-supplied HTML.
- `content/photos.json`: photography image paths, dimensions, and existing archive captions. The main gallery has 57 unique photographs; the archive has 24. Two repeated entries in the old main gallery were deduplicated; original image files remain intact.
- `site/www.milo.me/assets/site.css`: shared styles for every page, including responsive layouts and light/dark themes.
- `site/www.milo.me/assets/site.js`: theme preference, blog filters, and accessible photo dialog with keyboard navigation.

English and Chinese routes mirror each other. Language switching keeps the current page. Existing `/blogs/index.html`, `/photography/index.html`, and their Chinese equivalents redirect to the matching index pages. Both languages expose `/photography/page/2.html` for the archive.

## Project collection

- **Prompts**: local Codex conversation search. `/downloads/prompts.zip` provides a portable, source-only marketplace package; both detail pages include macOS / Codex desktop + CLI / Python 3.9+ installation steps. The ZIP excludes conversations, indexes, runtime caches, and credentials. Repackage with `python3 scripts/package_prompts.py --source /path/to/prompt-atlas` when updating the plugin.
- **Date with me**: the red/yellow/blue/green pop-art edition from `codex/pop-art-activity-selection`. The existing public Site still runs the old white edition, so the new edition is marked awaiting publication until its deployment is verified.
- **Mood Recipe**: the `sail` project. Words or images add musical layers. Image interpretation requires a configured vision service; otherwise it uses a default image mood. Earlier `inner-music` detail URLs redirect here.
- **Color Muse**: browser-based color transfer and .CUBE export. Verified GitHub Pages deployment: https://analalaa.github.io/color/ — linked from the gallery and details.

- **Recoding · 随记**: local Android notebook with text, photographs, and original audio. `/downloads/recoding-0.6.1.apk` is the existing 0.6.1-device test release for Android 8.0+, with installation instructions and a SHA-256 file. No web/iOS version or offline transcription is claimed.

## Preserved assets

Original image directories, RSS, favicon, and legacy `_next` assets remain intact. The new pages use `assets/site.css` and `assets/site.js`; legacy Next styles and the previous project-only styles are no longer loaded. There are no Next hydration scripts or `__NEXT_DATA__` payloads in generated pages.

## Illustrated project gallery and launch links

The gallery and detail pages retain the original illustrated covers while using the shared site navigation, fonts, spacing, and light/dark theme. `scripts/project_art.py` renders the cover artwork, and `assets/project-gallery.css` contains styles scoped to project pages.

Each project in `content/projects.json` may define a verified HTTPS `url`, translated `linkLabel`, and an optional site-relative `download` path. Gallery buttons open live products directly, or jump to installation instructions for Prompts or Recoding. `url: null` displays a clear availability state without pretending the detail page is an online product.

Mood Recipe has no verified public URL. Before offering a general public experience, deploy its Node/Express service, configure image analysis if desired, and decide whether records are personal or shared: the current source broadcasts and persists one shared entry list for every visitor. Do not include existing `data/entries.json` or secrets in deployment artifacts. Update the bilingual availability note and `url` only after the deployment is verified.

Download projects may set `installation: "android"` for the APK guide and supply `version` and `downloadSize`; Prompts retains its own plugin guide. Optional bilingual `availabilityLabel` overrides the default pending label. Project counts are generated from the collection.
