"""Original project cover illustrations, reused with the shared site layout."""
import math
from html import escape as e

def artwork(project, lang):
    zh = lang == 'zh'
    visual = project['visual']
    if project.get('kind') == 'event-series' and project.get('cover'):
        cover = project['cover']
        alt = project[lang].get('coverAlt', project[lang].get('name',project['name']))
        return (f'<div class="pg-cover cover-event-photo"><img src="{e(cover["src"],quote=True)}" '
                f'width="{int(cover["width"])}" height="{int(cover["height"])}" '
                f'alt="{e(alt,quote=True)}" decoding="async"></div>')
    if visual == 'prompts':
        content = f'''<span class="pg-cover-label">A PLACE FOR YOUR THOUGHTS</span>
        <div class="prompt-window"><div class="prompt-top">Prompts <small>SEARCH & REVISIT</small></div>
        <div class="prompt-search"><svg viewBox="0 0 20 20"><circle cx="8" cy="8" r="5"/><path d="m12 12 5 5"/></svg>{'关于配色的灵感' if zh else 'A thought about color'}</div>
        <div class="prompt-result"><i>01</i><div>{'找回那个关于' if zh else 'Find that thought about'} <mark>{'配色' if zh else 'color'}</mark> {'的想法' if zh else 'again'}<small>MY PROMPTS · A LITTLE IDEA</small></div></div>
        <div class="prompt-result"><i>02</i><div>{'让灵感，回到手边。' if zh else 'Back within reach.'}<small>REPLIES · IN CONTEXT</small></div></div></div>
        <span class="pg-cover-foot">RECALL / REUSE / REIMAGINE</span>'''
    elif visual == 'gathering':
        content = f'''<span class="pg-cover-label">YUZHONG / AFTER THE GAME</span>
        <div class="gathering-type{' gathering-type-en' if not zh else ''}"><strong>{'羽冢' if zh else 'Yuzhong'}</strong><span>{'企划' if zh else 'PROJECT'}</span></div>
        <svg class="gathering-drawing" viewBox="0 0 720 420" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <g transform="rotate(8 490 208)"><ellipse cx="490" cy="112" rx="35" ry="12"/><path d="M455 112v180c0 16 70 16 70 0V112"/><path d="M455 280c0 16 70 16 70 0"/><path class="gathering-accent" d="M455 204c0 15 70 15 70 0v18c0 15-70 15-70 0Z" stroke="none"/></g>
          <g transform="translate(353 279) rotate(-24)"><path d="M-13 14h26v17c-6 14-20 14-26 0Z" fill="currentColor"/><path d="m-13 14-28-78 15-5 10 8 9-16L1-66l10-12 10 18 15-6 6 8-29 72"/><path d="m-26-64 17 78m-8-74 11 74M1-66v80m20-74-12 74m27-72L12 14M-23-13h46M-17 3h34"/><path d="m-33-48 14 6m-8 13 12 4m36-25 12-4"/></g>
          <g transform="translate(408 88) rotate(-34)"><path d="M0 54C-16 23-11 5 1-11c15 18 19 34-1 65ZM1-11v72M-9 9 1 18l12-9M-7 24l8 9 10-10"/></g>
          <path d="M573 300c28-16 47-7 58 10-27 12-44 12-58-10Zm0 0 66 13m-51-23 12 15m7-13 9 18"/>
          <path d="M303 340h270" opacity=".22"/>
        </svg><span class="pg-cover-foot">REASSEMBLE / GATHER / MAKE</span>'''
    elif visual == 'date':
        content = '''<span class="pg-cover-label">A LITTLE TIME, TOGETHER</span>
        <div class="date-pop"><span>LET’S</span><span>GO!</span><span>一</span><span>起</span></div>
        <span class="pg-cover-foot">DATE WITH MILO ↗</span>'''
    elif visual == 'recoding':
        content = f'''<span class="pg-cover-label">A SMALL PLACE FOR EVERYDAY LIFE</span>
        <div class="recoding-orbit"></div><div class="recoding-note"><div class="recoding-top">{'随记' if zh else 'Suiji'}<span>•••</span></div>
        <div class="recoding-words">{'今天有一个小小的想法。' if zh else 'A little thought from today.'}<br><span>{'先留下，再慢慢生长。' if zh else 'Keep it. Let it grow.'}</span></div>
        <div class="recoding-audio"><span>▶</span><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><small>00:18</small></div>
        <span class="recoding-saved">{'已保存在本机' if zh else 'Saved on this device'} ↗</span></div>
        <span class="pg-cover-foot">WORDS / PICTURES / VOICE</span>'''
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
