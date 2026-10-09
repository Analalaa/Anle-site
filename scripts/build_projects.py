#!/usr/bin/env python3
"""Regenerate only the bilingual project gallery and detail pages, using stdlib."""
import json
import math
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site' / 'www.milo.me'
PROJECTS = json.loads((ROOT / 'content' / 'projects.json').read_text())


def e(value):
    return escape(str(value), quote=True)


def path(lang, page='projects.html'):
    return ('/zh/' if lang == 'zh' else '/') + page


def external(url):
    if not url or urlsplit(url).scheme != 'https' or not urlsplit(url).netloc:
        raise ValueError('Project links must use a complete HTTPS URL')
    return e(url)


def artwork(project, lang):
    zh = lang == 'zh'
    visual = project['visual']
    if visual == 'prompts':
        content = f'''<span class="pg-cover-label">A PLACE FOR YOUR THOUGHTS</span>
        <div class="prompt-window"><div class="prompt-top">Prompts <small>SEARCH & REVISIT</small></div>
        <div class="prompt-search"><svg viewBox="0 0 20 20"><circle cx="8" cy="8" r="5"/><path d="m12 12 5 5"/></svg>{'关于配色的灵感' if zh else 'A thought about color'}</div>
        <div class="prompt-result"><i>01</i><div>{'找回那个关于' if zh else 'Find that thought about'} <mark>{'配色' if zh else 'color'}</mark> {'的想法' if zh else 'again'}<small>MY PROMPTS · A LITTLE IDEA</small></div></div>
        <div class="prompt-result"><i>02</i><div>{'让灵感，回到手边。' if zh else 'Back within reach.'}<small>REPLIES · IN CONTEXT</small></div></div></div>
        <span class="pg-cover-foot">RECALL / REUSE / REIMAGINE</span>'''
    elif visual == 'date':
        content = '''<span class="pg-cover-label">AN INVITATION TO SPEND TIME</span>
        <div class="date-type">Let's<br>make<br><em>time.</em></div><div class="date-ticket"><small>YOU + ME</small><strong>A little<br>rendezvous.</strong><span>NO OCCASION NEEDED.</span></div><div class="date-dot"></div>
        <span class="pg-cover-foot">SEE YOU SOON ↗</span>'''
    elif visual == 'music':
        waves = []
        for row in range(13):
            points = []
            for x in range(0, 721, 4):
                y = 96 + row * 8 + math.sin(x / 72 + row * .16) * (20 + 34 * math.sin(x / 300)) + math.sin(x / 35) * 7
                points.append(f'{x},{y:.1f}')
            waves.append(f'<polyline points="{" ".join(points)}"/>')
        content = f'''<span class="pg-cover-label">WORDS + IMAGES / LIVING SOUND</span><svg class="music-waves" viewBox="0 0 720 300" preserveAspectRatio="none" fill="none" stroke="#a5becb" stroke-width=".7">{"".join(waves)}</svg>
        <div class="music-title">A moment, in sound.</div><div class="music-prompt">{'写一句话，或放入一张图。' if zh else 'Write a moment. Add an image.'}</div><span class="pg-cover-foot">{e(project['name'].upper())}</span>'''
    else:
        content = '''<div class="color-strips"><span></span><span></span><span></span><span></span><span></span></div><span class="pg-cover-label">A STUDY IN BORROWED COLOR</span><div class="color-ring"></div><div class="color-title">Color<br><em>Muse.</em></div><span class="pg-cover-foot">FIND YOUR PALETTE</span>'''
    return f'<div class="pg-cover cover-{visual}" aria-hidden="true">{content}</div>'


def shell(lang, title, description, page, body):
    zh = lang == 'zh'
    labels = [('index.html', '首页', 'Home'), ('about.html', '关于我', 'About'), ('photography.html', '摄影', 'Photography'), ('projects.html', '小作品', 'Projects'), ('blogs.html', '博客', 'Blog')]
    nav = ''.join(f'<a href="{path(lang, file)}"' + (' aria-current="page"' if file == 'projects.html' and page == 'projects.html' else ' aria-current="true"' if file == 'projects.html' else '') + f'>{cn if zh else en}</a>' for file, cn, en in labels)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} · {'安乐' if zh else 'Milo An'}</title>
  <meta name="description" content="{e(description)}"><meta name="author" content="Anle">
  <meta property="og:title" content="{e(title)} · {'安乐' if zh else 'Milo An'}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website">
  <link rel="icon" href="/favicon.ico"><link rel="alternate" hreflang="zh" href="{path('zh', page)}"><link rel="alternate" hreflang="en" href="{path('en', page)}"><link rel="alternate" hreflang="x-default" href="{path('en', page)}">
  <script>try{{var t=localStorage.getItem('theme');if(t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme: dark)').matches)){{document.documentElement.classList.add('dark');document.documentElement.style.colorScheme='dark'}}}}catch(e){{}}</script>
  <link rel="stylesheet" href="/assets/projects.css"><script src="/assets/projects.js" defer></script>
</head>
<body class="playground">
  <a class="pg-skip" href="#content">{'跳到内容' if zh else 'Skip to content'}</a>
  <div class="pg-shell">
    <header class="pg-header"><a class="pg-logo" href="{path(lang, 'index.html')}">Milo</a>
      <nav class="pg-nav" id="pg-nav" aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav>
      <div class="pg-controls"><a class="{'inactive' if zh else 'active'}" lang="en" hreflang="en" href="{path('en', page)}" aria-label="English">EN</a><span>/</span><a class="{'active' if zh else 'inactive'}" lang="zh" hreflang="zh" href="{path('zh', page)}" aria-label="中文">ZH</a>
        <button class="pg-theme" type="button" aria-label="{'切换深色模式' if zh else 'Switch to dark mode'}"><svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M20.7 13.1A8.7 8.7 0 0 1 10.9 3.3 8.8 8.8 0 1 0 20.7 13.1Z"/></svg><svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M19 5l-1.5 1.5m-11 11L5 19"/></svg></button>
        <button class="pg-menu" type="button" aria-controls="pg-nav" aria-expanded="false" aria-label="{'打开导航' if zh else 'Open navigation'}"><svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" aria-hidden="true"><path d="M2 5h16M2 10h16M2 15h16"/></svg></button>
      </div>
    </header>
    <main id="content">{body}</main>
    <footer class="pg-footer"><span>© 2026 Milo An</span><nav aria-label="{'页脚导航' if zh else 'Footer navigation'}"><a href="{path(lang, 'about.html')}">{'关于我' if zh else 'About me'}</a><a href="https://github.com/Analalaa" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav><span>MADE WITH CURIOSITY.</span></footer>
  </div>
</body></html>
'''


def gallery(lang):
    zh = lang == 'zh'
    cards = []
    for i, p in enumerate(PROJECTS, 1):
        t = p[lang]
        url = path(lang, f'projects/{p["slug"]}.html')
        cards.append(f'''<article class="pg-card"><a class="pg-cover-link" href="{url}" aria-label="{e(('了解 ' if zh else 'Explore ') + p['name'])}">{artwork(p, lang)}</a><div class="pg-card-meta"><span>{e(t['category'])}</span><span>{i:02d}</span></div><h3><a class="pg-card-heading" href="{url}">{e(p['name'])}<span class="pg-arrow" aria-hidden="true">↗</span></a></h3><p class="pg-tagline">{e(t['tagline'])}</p><p>{e(t['description'])}</p></article>''')
    body = f'''<section class="pg-hero" aria-labelledby="page-title"><p class="pg-kicker">ANLE'S PLAYGROUND / {'小作品，慢慢长出来' if zh else 'SMALL THINGS, STILL GROWING'}</p><h1 id="page-title">{'<span class="keep">把好奇心，</span><span class="keep">做成小东西。</span>' if zh else 'Small things.<br>Made out of curiosity.'}</h1><p class="intro">{'一些从自己的需要和兴趣出发的小产品。<br>关于创作、效率，也关于音乐、颜色和好好生活。做出来，玩一玩，再慢慢打磨。' if zh else 'A collection of little tools and experiments, born from things I need and things I love. For making, remembering, listening, seeing — and living a little more.'}</p><div class="pg-note" aria-hidden="true"><svg viewBox="0 0 50 50"><path d="M25 1v48M1 25h48M8 8l34 34M8 42 42 8M15 3l20 44M3 15l44 20M3 35l44-20M15 47 35 3"/></svg>Made to be used.<br>And played with.</div></section>
    <section aria-labelledby="collection-title"><div class="pg-section-label"><h2 id="collection-title">{'作品架' if zh else 'ON THE SHELF'}</h2><span>{len(PROJECTS):02d} {'件小作品 · 持续生长中' if zh else 'PROJECTS · AN ONGOING COLLECTION'}</span></div><div class="pg-grid">{''.join(cards)}</div></section>
    <section class="pg-closing"><p>{'还在继续做，也在继续玩。' if zh else 'Still making. Still playing.'}</p><a href="{path(lang, 'about.html')}">{'认识一下做这些东西的人' if zh else 'Meet the person behind these things'} ↗</a></section>'''
    names = ('、' if zh else ', ').join(p['name'] for p in PROJECTS)
    description = f'安乐的小产品与创作实验：{names}。' if zh else f'Small tools and creative experiments by Milo An: {names}.'
    return shell(lang, '小作品' if zh else 'Projects', description, 'projects.html', body)


def detail(p, lang):
    zh = lang == 'zh'
    t = p[lang]
    features = ''.join(f'<li><h2>{e(title)}</h2><p>{e(copy)}</p></li>' for title, copy in t['features'])
    actions = []
    if p.get('url'):
        actions.append(f'<a class="pg-action primary" href="{external(p["url"])}" target="_blank" rel="noopener noreferrer">{e(t.get("linkLabel", "打开作品" if zh else "Open project"))} ↗</a>')
    if p.get('source'):
        actions.append(f'<a class="pg-action" href="{external(p["source"])}" target="_blank" rel="noopener noreferrer">{"查看源码" if zh else "View source"} ↗</a>')
    actions.append(f'<a class="pg-action" href="{path(lang)}">{"返回作品架" if zh else "Back to all projects"} ←</a>')
    next_p = PROJECTS[(PROJECTS.index(p) + 1) % len(PROJECTS)]
    body = f'''<a class="pg-back" href="{path(lang)}">← {'全部小作品' if zh else 'All projects'}</a><section class="pg-hero pg-detail-hero"><p class="pg-kicker">{e(t['category'])}</p><h1>{e(p['name'])}</h1><p class="intro">{e(t['tagline'])}</p></section><figure class="pg-detail-art">{artwork(p, lang)}<figcaption class="pg-caption">{'作品概念视觉' if zh else 'A visual interpretation of the project'}</figcaption></figure><section class="pg-detail-body" aria-label="{'作品介绍' if zh else 'About this project'}"><p class="pg-story">{e(t['intro'])}</p><ul class="pg-features">{features}</ul><p class="pg-availability">{e(t['note'])}</p><div class="pg-actions">{''.join(actions)}</div></section><div class="pg-closing"><p>{'再逛一件。' if zh else 'One more little thing.'}</p><a href="{path(lang, 'projects/' + next_p['slug'] + '.html')}">{e(next_p['name'])} ↗</a></div>'''
    return shell(lang, p['name'], t['description'], f'projects/{p["slug"]}.html', body)


def main():
    slugs = [slug for p in PROJECTS for slug in [p['slug'], *p.get('aliases', [])]]
    if len(set(slugs)) != len(slugs) or any(not slug or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slug) for slug in slugs):
        raise ValueError('Project slugs must be unique lowercase names')
    for lang in ['zh', 'en']:
        folder = SITE / ('zh' if lang == 'zh' else '')
        (folder / 'projects').mkdir(parents=True, exist_ok=True)
        (folder / 'projects.html').write_text(gallery(lang), encoding='utf-8')
        for project in PROJECTS:
            (folder / 'projects' / (project['slug'] + '.html')).write_text(detail(project, lang), encoding='utf-8')
            for alias in project.get('aliases', []):
                target = path(lang, f'projects/{project["slug"]}.html')
                label = '查看更新后的作品' if lang == 'zh' else 'View the updated project'
                body = f'<section class="pg-hero"><h1>{e(project["name"])}</h1><a class="pg-action" href="{target}">{label} →</a></section>'
                html = shell(lang, project['name'], project[lang]['description'], f'projects/{project["slug"]}.html', body)
                html = html.replace('</head>', f'<meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{target}"></head>')
                (folder / 'projects' / (alias + '.html')).write_text(html, encoding='utf-8')
    print(f'Generated 2 gallery pages and {len(PROJECTS) * 2} project pages.')


if __name__ == '__main__':
    main()
