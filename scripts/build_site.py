#!/usr/bin/env python3
"""Render the bilingual static site from content/, using one shared visual system."""
import json
import re
from pathlib import Path
from html import escape
from project_art import artwork

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/www.milo.me'
E = escape
ICONS = {
    'prompts': '<path d="M6 4h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-6l-5 4v-4H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"/><path d="m8 8 3 2-3 2m6 1h3"/>',
    'date': '<rect x="4" y="5" width="16" height="16" rx="3"/><path d="M8 3v4m8-4v4M4 10h16m-12 5 3 3 5-5"/>',
    'music': '<path d="M3 10v4m4-7v10m5-14v18m5-14v10m4-7v4"/>',
    'recoding': '<rect x="5" y="3" width="15" height="18" rx="2"/><path d="M3 7h4m-4 5h4m-4 5h4M11 8h5m-5 4h5m-5 4h3"/>',
    'color': '<path d="M12 3a9 9 0 1 0 0 18h1a2 2 0 0 0 1.5-3.3 1.8 1.8 0 0 1 1.4-3H18a3 3 0 0 0 3-3A9 9 0 0 0 12 3Z"/><circle cx="7.5" cy="10" r=".6"/><circle cx="11" cy="6.8" r=".6"/><circle cx="16" cy="8" r=".6"/>',
    'github': '<path d="M9 19c-4 1-4-2-5-2m10 4v-3.4c0-1 .1-1.5-.5-2.1 3.3-.4 6.5-1.6 6.5-6A4.7 4.7 0 0 0 18.7 6c.1-.9.1-1.7-.2-2.8 0 0-1.1-.3-3.6 1.3a12 12 0 0 0-6 0C6.4 2.9 5.3 3.2 5.3 3.2 5 4.3 5 5.1 5.1 6A4.7 4.7 0 0 0 3.8 9.5c0 4.4 3.2 5.6 6.5 6-.6.6-.6 1.2-.6 2.1V21"/>',
    'moon': '<path d="M20.5 13.1A8.8 8.8 0 0 1 10.9 3.5a8.8 8.8 0 1 0 9.6 9.6Z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    'close': '<path d="m6 6 12 12M6 18 18 6"/>',
    'left': '<path d="m15 5-7 7 7 7"/>',
    'right': '<path d="m9 5 7 7-7 7"/>',
}


def icon(name, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def url(lang, path='index.html'):
    return ('/zh/' if lang == 'zh' else '/') + path


def external(href, label, cls=''):
    return f'<a class="{cls}" href="{E(href, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>'


def contact(lang):
    heading = '在这些地方也能找到我。' if lang == 'zh' else 'You can also find me here.'
    links = [('https://github.com/Analalaa', 'GitHub'), ('https://x.com/anlading9', 'X'), ('https://www.instagram.com/anbelivablee/', 'Instagram'), ('https://t.me/anlading9', 'Telegram')]
    return f'<section class="contact" aria-label="Contact"><p>{heading}</p><div class="socials">' + ''.join(external(h, label) for h, label in links) + '</div><p><a class="text-link" href="mailto:an_missu@163.com">an_missu@163.com</a></p></section>'


def shell(lang, path, title, section, body, description='', extra_class=''):
    zh = lang == 'zh'
    page_title = title + (' · 安乐的个人网站' if zh else ' · Milo An')
    navigation = [('index.html', '首页' if zh else 'Home', 'home'), ('projects.html', '小作品' if zh else 'Projects', 'projects'), ('photography.html', '摄影' if zh else 'Photography', 'photography'), ('blogs.html', '博客' if zh else 'Blog', 'blogs'), ('about.html', '关于' if zh else 'About', 'about')]
    nav = ''.join(f'<a href="{url(lang,p)}"' + (' aria-current="page"' if current == section else '') + f'>{label}</a>' for p, label, current in navigation)
    languages = ' / '.join(f'<a href="{url(l,path)}" lang="{l}" hreflang="{l}"' + (' aria-current="page"' if lang == l else '') + f'>{l.upper()}</a>' for l in ['en','zh'])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(page_title)}</title>
<meta name="description" content="{E(description, quote=True)}"><meta name="author" content="Milo An">
<meta property="og:title" content="{E(page_title, quote=True)}"><meta property="og:description" content="{E(description, quote=True)}"><meta property="og:type" content="website">
<link rel="alternate" hreflang="en" href="{url('en',path)}"><link rel="alternate" hreflang="zh" href="{url('zh',path)}">
<link rel="icon" href="/favicon.ico"><link rel="alternate" type="application/rss+xml" title="Milo An — RSS" href="/rss.xml">
<script>try{{var t=localStorage.getItem('theme');if(t==='dark'||((!t||t==='system')&&matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.classList.add('dark')}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/site.css">{'<link rel="stylesheet" href="/assets/project-gallery.css">' if section=='projects' else ''}<script src="/assets/site.js" defer></script>
</head>
<body>
<a class="skip" href="#main-content">{'跳到正文' if zh else 'Skip to content'}</a>
<header class="site-header">
<a class="brand" href="{url(lang)}" aria-label="{'安乐 · 首页' if zh else 'Milo · Home'}">Milo<span>.</span></a>
<nav class="site-nav" aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav>
<div class="site-tools"><nav class="language" aria-label="{'语言' if zh else 'Language'}">{languages}</nav><a class="tool-link" href="https://github.com/Analalaa" aria-label="GitHub" target="_blank" rel="noopener noreferrer">{icon('github')}</a><button class="theme-toggle" type="button" aria-label="{'切换深色模式' if zh else 'Switch to dark mode'}">{icon('moon','moon')}{icon('sun','sun')}</button></div>
</header>
<main id="main-content" class="page {extra_class}">{body}</main>
<footer class="site-footer"><span>© Milo An · {'慢慢生长，认真生活。' if zh else 'A little corner of my world.'}</span><nav aria-label="{'页脚' if zh else 'Footer'}"><a href="{url(lang,'about.html')}">{'关于' if zh else 'About'}</a><a href="/rss.xml">RSS ↗</a></nav></footer>
</body></html>
'''


def heading(title, subtitle='', overline=''):
    return '<header class="page-heading">' + (f'<p class="overline">{E(overline)}</p>' if overline else '') + f'<h1>{E(title)}</h1>' + (f'<p class="subtitle">{E(subtitle)}</p>' if subtitle else '') + '</header>'


def write(path, html):
    dest = SITE / path.lstrip('/')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding='utf-8')


def redirect(path, target, lang):
    label = '页面已搬家，点击继续。' if lang == 'zh' else 'This page has moved. Continue here.'
    write(path, f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Milo An</title><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{target}"></head><body><a href="{target}">{label}</a></body></html>\n')


def post_list(posts, lang, full_date=False):
    return '<ul class="post-list">' + ''.join(f'<li data-category="{post["category"]}"><a class="post-link" href="{url(lang,"blogs/"+post["slug"]+".html")}"><span class="post-title">{E(post[lang]["title"])}</span><time datetime="{post["date"]}">{(post["date"] if full_date else post["date"][5:]).replace("-", "/")}</time></a></li>' for post in posts) + '</ul>'


def installation(project, lang):
    zh = lang == 'zh'
    if project.get('installation') == 'android':
        title = '在手机上试试随记' if zh else 'Try Suiji on your phone'
        steps = [
            '用 Android 手机打开这一页，下载 APK。也可以先下载到电脑，再传到手机。' if zh else 'Open this page on your Android phone and download the APK, or transfer it from your computer.',
            '打开下载的文件，按系统提示允许这次安装，再打开「随记」。' if zh else 'Open the downloaded file, follow Android’s installation prompt, and launch Suiji.',
            '写几句话，添加照片或录一段音。重要记录可以从应用内导出备份。' if zh else 'Write a few words, add photos, or record a sound. Export important notes from the app to keep a backup.',
        ]
        body = f'<section class="install-guide" id="use" aria-labelledby="install-title"><h2 id="install-title">{title}</h2>'
        body += f'<p>Android 8.0+ · {E(project["version"])} · {E(project["downloadSize"])} · {"测试版" if zh else "Test release"}</p>'
        body += f'<a class="work-primary" href="{E(project["download"],quote=True)}" download>{"下载 APK" if zh else "Download APK"} ↓</a>'
        body += '<ol>' + ''.join('<li>'+E(s)+'</li>' for s in steps) + '</ol>'
        body += '<p class="small">' + ('适用于 Android 手机，不支持在 iPhone 或网页中运行。' if zh else 'For Android phones. It does not run on iPhone or in a web browser.') + '</p>'
        body += f'<p class="small"><a class="text-link" href="{E(project["download"],quote=True)}.sha256.txt" download>{"安装包校验值" if zh else "Package checksum"} ↓</a></p></section>'
        return body
    title = '安装 Prompts' if zh else 'Install Prompts'
    steps = [
        '下载插件包并解压，把 prompts 文件夹放在准备长期保留的位置。' if zh else 'Download and extract the package. Keep the prompts folder in a permanent location.',
        '在 prompts 文件夹的上一级打开终端，运行下面的命令。' if zh else 'Open a terminal in the parent directory of the prompts folder and run the command below.',
        '在 Codex 的插件目录选择「Anle · Prompts」来源并安装 Prompts。如果暂时没有显示，重启 Codex 后再查看。' if zh else 'In the Codex Plugins directory, select the Anle · Prompts source and install Prompts. Restart Codex if it does not appear yet.',
        '新建一个对话，说「打开对话检索面板」。' if zh else 'Start a new chat and ask: “Open the conversation search panel.”',
    ]
    body = f'<section class="install-guide" id="use" aria-labelledby="install-title"><h2 id="install-title">{title}</h2><p>' + ('macOS · Codex 桌面应用与 CLI · Python 3.9+ · 测试版' if zh else 'macOS · Codex desktop & CLI · Python 3.9+ · Beta') + '</p>'
    body += f'<a class="work-primary" href="{E(project["download"],quote=True)}" download>{"下载插件包" if zh else "Download plugin"} ↓</a><ol>'
    for i,step in enumerate(steps):
        body += '<li>' + E(step) + ('<pre><code>codex plugin marketplace add ./prompts</code></pre>' if i==1 else '') + '</li>'
    body += '</ol><p class="small">' + ('安装包仅包含程序代码，不含我的对话、索引或缓存。检索在使用者自己的电脑上进行。' if zh else 'The package contains application code only, with none of my conversations, indexes, or caches. Searches run on the user’s own computer.') + '</p><p class="small">' + external('https://developers.openai.com/plugins/build/plugins','OpenAI '+('安装与分发说明' if zh else 'installation and distribution guide')+' ↗','text-link') + '</p></section>'
    return body


def main():
    data = {name: json.loads((ROOT/'content'/f'{name}.json').read_text()) for name in ['site','projects','posts','photos']}
    projects, posts, photos = data['projects'], sorted(data['posts'], key=lambda p:p['date'], reverse=True), data['photos']
    for lang in ['en','zh']:
        zh = lang == 'zh'
        def page(path, title, section, body, desc='', extra=''):
            write(url(lang,path), shell(lang,path,title,section,body,desc,extra))
        # Home: a short introduction; the complete original biography lives on About.
        body = f'<header class="home-heading"><div><h1>{"<span>你好，</span><span>我是安乐。</span>" if zh else "Hey, I’m Milo."}</h1><p class="name-note">{"Milo An · 创作与生活的记录" if zh else "Anle / 安乐 · Making things & living life"}</p></div><img class="avatar" src="{data["site"][lang]["portrait"]}" alt="Milo An" width="68" height="68"></header>'
        if zh:
            body += '<div class="prose"><p>喜欢奇思妙想，也喜欢把它们慢慢做出来。<br>我写作、拍照，做一些让生活更有意思的小工具。</p><p>最近，把散落在日常里的想法，做成了这些<a href="/zh/projects.html">小作品</a>：</p></div>'
        else:
            body += '<div class="prose"><p>I’m drawn to curious ideas, and I like making them real.<br>I write, take photographs, and build little tools for everyday life.</p><p>Some ideas have grown into <a href="/projects.html">small projects</a>:</p></div>'
        body += '<div class="project-chips">' + ''.join(f'<a class="project-chip" href="{url(lang,"projects/"+p["slug"]+".html")}">{icon(p["visual"])}{E(p["name"])}</a>' for p in projects) + '</div>'
        body += '<div class="prose"><p>' + ('创作之外，喜欢运动、旅行、音乐，和人与人之间真诚的交谈。相信很多东西是慢慢生长出来的，也希望一直保留玩儿的心态。' if zh else 'Away from the screen, I love sports, travel, music, and honest conversations. I believe good things take time to grow — and that a sense of play is worth keeping.') + f' <a href="{url(lang,"about.html")}">{"更多关于我" if zh else "More about me"} ↗</a></p></div>'
        body += f'<section class="section"><div class="section-heading"><h2>{"最近的文字" if zh else "Recent writing"}</h2><a href="{url(lang,"blogs.html")}">{"全部文章" if zh else "All posts"} →</a></div>{post_list(posts[:3],lang,full_date=True)}</section>'
        body += f'<section class="section"><div class="section-heading"><h2>{"一些看见的瞬间" if zh else "A few moments, kept"}</h2><a href="{url(lang,"photography.html")}">{"摄影" if zh else "Photography"} →</a></div><div class="photo-strip">'
        for photo in photos['main'][:3]:
            body += f'<a href="{url(lang,"photography.html")}"><img src="{photo["src"]}" width="{photo["width"]}" height="{photo["height"]}" alt="{E(photo["alt"],quote=True)}" loading="lazy"></a>'
        body += '</div></section>' + contact(lang)
        page('index.html','首页' if zh else 'Home','home',body,'安乐的个人角落：写作、摄影和一些小作品。' if zh else 'A personal corner for writing, photography, and small projects by Milo An.')
        # About retains all existing personal writing.
        body = heading('关于我' if zh else 'About me','保持好奇，慢慢生长。' if zh else 'Stay curious. Give things time to grow.')
        bio = '\n'.join(data['site'][lang]['original_bio']).replace('我同样喜欢文学与影视作品，也喜欢文学与影视作品。','我同样喜欢文学与影视作品。')
        body += '<div class="prose">' + bio + '</div>' + contact(lang)
        page('about.html','关于我' if zh else 'About me','about',body,'写作、摄影、运动、音乐，以及我想慢慢构建的生活。' if zh else 'Writing, photography, sport, music, and a life I am slowly making my own.')
        # Expressive project covers inside the shared site navigation and typography.
        intro = '从自己的需要和兴趣出发，把好奇心做成小东西。' if zh else 'Small things made from personal needs, passing thoughts, and a little curiosity.'
        body = heading('小作品' if zh else 'Projects',intro,"ANLE’S PLAYGROUND") + '<div class="collection-heading"><span>' + ('作品架' if zh else 'On the shelf') + f'</span><span>{len(projects):02d} / ' + ('持续生长中' if zh else 'An ongoing collection') + '</span></div><div class="work-grid">'
        for i,p in enumerate(projects,1):
            d = p[lang]
            detail_url = url(lang,'projects/'+p['slug']+'.html')
            body += f'<article class="work-card"><a class="work-cover" href="{detail_url}" aria-label="{E(("了解 " if zh else "About ")+p["name"],quote=True)}">{artwork(p,lang)}</a><div class="work-meta"><span>{E(d["category"])}</span><span>{i:02d}</span></div><h2><a href="{detail_url}">{E(p["name"])}</a></h2><p class="work-tagline">{E(d["tagline"])}</p><p class="work-description">{E(d["description"])}</p><div class="work-actions">'
            if p.get('url'):
                body += external(p['url'],E(d.get('linkLabel','在线体验' if zh else 'Try it online'))+' ↗','work-primary')
            elif p.get('download'):
                body += f'<a class="work-primary" href="{detail_url}#use">{E(d["linkLabel"])} ↓</a>'
            else:
                body += '<span class="work-status">' + E(d.get('availabilityLabel', '在线体验准备中' if zh else 'Online experience coming soon')) + '</span>'
            body += f'<a class="work-more" href="{detail_url}">{"了解作品" if zh else "About this project"} →</a></div></article>'
        body += '</div><p class="quiet-note">' + ('还在继续做，也在继续玩。' if zh else 'Still making. Still playing.') + '</p>'
        page('projects.html','小作品' if zh else 'Projects','projects',body,intro,'works-page')
        for i,p in enumerate(projects):
            d = p[lang]
            body = f'<a class="back-link" href="{url(lang,"projects.html")}">← {"所有小作品" if zh else "All projects"}</a>'
            body += heading(p['name'], d['tagline'], d['category'])
            if p.get('url'): body += '<div class="detail-launch">' + external(p['url'],E(d.get('linkLabel','在线体验' if zh else 'Try it online'))+' ↗','work-primary') + '</div>'
            elif p.get('download'): body += '<div class="detail-launch"><a class="work-primary" href="#use">' + E(d['linkLabel']) + ' ↓</a></div>'
            else: body += '<div class="detail-launch"><span class="work-status">' + E(d.get('availabilityLabel', '在线体验准备中' if zh else 'Online experience coming soon')) + '</span></div>'
            body += '<figure class="work-detail-art">' + artwork(p,lang) + '<figcaption>' + ('作品概念视觉' if zh else 'A visual interpretation of the project') + '</figcaption></figure>'
            body += f'<div class="prose"><p>{E(d["intro"])}</p></div><ul class="feature-list">' + ''.join(f'<li><h2>{E(t)}</h2><p>{E(v)}</p></li>' for t,v in d['features']) + '</ul>'
            actions = []
            if p.get('url'): actions.append(external(p['url'],E(d.get('linkLabel','在线体验' if zh else 'Try it online'))+' ↗','work-primary'))
            if p.get('source'): actions.append(external(p['source'],('查看源码' if zh else 'Source code')+' ↗','text-link'))
            if actions: body += '<div class="actions">' + ''.join(actions) + '</div>'
            body += f'<p class="quiet-note">{E(d["note"])}</p>'
            if p.get('download'): body += installation(p,lang)
            next_p = projects[(i+1)%len(projects)]
            body += f'<nav class="next-project" aria-label="{"下一个作品" if zh else "Next project"}"><span>{"继续看看" if zh else "Keep exploring"}</span><a href="{url(lang,"projects/"+next_p["slug"]+".html")}">{E(next_p["name"])} →</a></nav>'
            path = 'projects/'+p['slug']+'.html'
            page(path,p['name'],'projects',body,d['description'])
            for alias in p.get('aliases',[]): redirect(url(lang,'projects/'+alias+'.html'),url(lang,path),lang)
        # Blog index and original articles.
        body = heading('博客' if zh else 'Writing','把经历、念头和偶尔的诗，留在这里。' if zh else 'Notes from life, passing thoughts, and the occasional poem.')
        body += '<div class="filters" role="group" aria-label="'+('文章分类' if zh else 'Filter posts')+'">' + ''.join(f'<button type="button" data-filter="{v}" aria-pressed="{str(v=="all").lower()}">{t}</button>' for v,t in [('all','全部' if zh else 'All'),('essay','随笔' if zh else 'Essays'),('poem','诗歌' if zh else 'Poetry')]) + '</div><p class="sr-only" id="filter-status" role="status" aria-live="polite"></p>'
        for year in sorted({p['date'][:4] for p in posts},reverse=True):
            body += f'<section class="post-year"><h2>{year}</h2>' + post_list([p for p in posts if p['date'].startswith(year)],lang) + '</section>'
        page('blogs.html','博客' if zh else 'Writing','blogs',body,'安乐的随笔与诗歌。' if zh else 'Essays and poetry by Milo An.')
        for p in posts:
            d = p[lang]
            category = ('诗歌' if zh else 'Poetry') if p['category']=='poem' else ('随笔' if zh else 'Essay')
            body = f'<a class="back-link" href="{url(lang,"blogs.html")}">← {"所有文章" if zh else "All posts"}</a><header class="page-heading"><h1>{E(d["title"])}</h1><div class="post-meta"><time datetime="{p["date"]}">{p["date"]}</time><span>·</span><span>{category}</span></div></header>'
            if d.get('cover'): body += f'<figure class="article-cover"><img src="{d["cover"]}" alt="{E(d["title"],quote=True)}"></figure>'
            body += f'<article class="prose post-body {p["category"]}">{d["body"]}</article><div class="article-end"><span>Milo An / 安乐</span><a href="{url(lang,"blogs.html")}">{"返回博客" if zh else "Back to writing"} ↑</a></div>'
            desc = re.sub(r'<[^>]+>','',d['body']).strip()[:140]
            page('blogs/'+p['slug']+'.html',d['title'],'blogs',body,desc)
        # Photography: retain original files and the existing archive route.
        for key,path in [('main','photography.html'),('archive','photography/page/2.html')]:
            archive = key == 'archive'
            title = ('摄影 · 旧时片段' if zh else 'Photography · Archive') if archive else ('摄影' if zh else 'Photography')
            intro = ('一些更早的画面，和当时留下的文字。' if zh else 'Earlier frames, and the words that came with them.') if archive else ('用镜头留住经过，也留住当时的自己。' if zh else 'A record of places, passing moments, and the person behind the camera.')
            body = heading(title,intro) + '<div class="photo-grid">'
            for i,photo in enumerate(photos[key]):
                caption = photo['alt'] if archive else ''
                alt = photo['alt'] if archive else (f'安乐的摄影作品 {i+1}' if zh else f'Photograph by Milo An, {i+1}')
                body += f'<figure><button type="button" class="photo-open" data-caption="{E(caption,quote=True)}" aria-label="{E(("查看照片：" if zh else "View photo: ")+alt,quote=True)}"><img src="{photo["src"]}" alt="{E(alt,quote=True)}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy"></button>' + (f'<figcaption>{E(caption)}</figcaption>' if caption else '') + '</figure>'
            body += '</div><nav class="photo-pagination">'
            body += f'<span>{len(photos[key])} {"个瞬间" if zh else "moments"}</span><a href="{url(lang,"photography.html" if archive else "photography/page/2.html")}">' + (('← 最近的照片' if zh else '← Recent photographs') if archive else ('更早的片段 →' if zh else 'Earlier frames →')) + '</a></nav>'
            body += f'<dialog class="lightbox" aria-label="{"照片预览" if zh else "Photo viewer"}"><div class="lightbox-toolbar"><span class="lightbox-count" aria-live="polite"></span><button type="button" data-close aria-label="{"关闭" if zh else "Close"}" autofocus>{icon("close")}</button></div><img alt=""><div class="lightbox-bottom"><button type="button" data-prev aria-label="{"上一张" if zh else "Previous photo"}">{icon("left")}</button><p class="lightbox-caption"></p><a class="original-photo" target="_blank" rel="noopener noreferrer">{"查看原图" if zh else "Original"} ↗</a><button type="button" data-next aria-label="{"下一张" if zh else "Next photo"}">{icon("right")}</button></div></dialog>'
            page(path,title,'photography',body,intro,'photos-page')
        for folder in ['blogs','photography']: redirect(url(lang,folder+'/index.html'),url(lang,folder+'.html'),lang)
    print('Generated bilingual pages with shared navigation, typography, and themes.')


if __name__ == '__main__':
    main()
