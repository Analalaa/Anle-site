"""Original project cover illustrations, reused with the shared site layout."""
import math
from html import escape as e

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
