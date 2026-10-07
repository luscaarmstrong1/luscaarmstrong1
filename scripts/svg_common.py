"""Shared self-contained SVG shell. Base attributes always show the final frame."""
from html import escape
import os
FONT = 'ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace'
def shell(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>text{{font-family:{FONT};fill:#c9d1d9}}.muted{{fill:#8b949e}}.green{{fill:#69f0a0}}@media(prefers-reduced-motion:reduce){{.animated{{display:none}}}}</style>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="#0d1117" stroke="#30363d"/>
{body}</svg>'''
def text(x, y, value, size=12, cls=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}">{escape(str(value))}</text>'
def fade(begin, duration=.35):
    if os.getenv('STATIC') == '1':
        return ''
    return f'<animate class="animated" attributeName="opacity" values="0;0;1" keyTimes="0;{begin/(begin+duration):.6f};1" dur="{begin+duration:.3f}s" fill="freeze"/>'
