"""Real SVG text with a terminal print cursor and final-frame clipping fallback."""
import os
from pathlib import Path
import numpy as np
from PIL import Image
from html import escape
from svg_common import shell, text
ROOT = Path(__file__).resolve().parents[1]
RAMP = ' .`:-=+*cs#%@'
def main():
    image = Image.open(ROOT/'assets/source-prepped.png').convert('L')
    cols=100; rows=round(cols*image.height/image.width*.48)
    pixels=np.asarray(image.resize((cols,rows)))
    body=text(20,28,'~/portrait · ASCII / 100 cols',10,'muted')+'<defs>'
    step=3.15; line=6.55; duration=3.6/rows
    for i in range(rows):
        animation=''
        if os.getenv('STATIC') != '1':
            begin=i*duration; end=begin+duration
            animation=f'<animate class="animated" attributeName="width" values="0;0;315" keyTimes="0;{begin/end:.6f};1" dur="{end:.4f}s" fill="freeze"/>'
        body+=f'<clipPath id="r{i}"><rect x="20" y="{45+i*line}" width="315" height="{line}">{animation}</rect></clipPath>'
    body+='</defs>'
    for i,row in enumerate(pixels):
        chars=''.join(RAMP[min(len(RAMP)-1,int((255-int(p))*(len(RAMP)-1)/255))] for p in row)
        body+=f'<text x="20" y="{50+i*line}" font-size="5.3" textLength="315" lengthAdjust="spacingAndGlyphs" xml:space="preserve" clip-path="url(#r{i})" class="green">{escape(chars)}</text>'
        if os.getenv('STATIC') != '1':
            body+=f'<rect class="animated" x="20" y="{45+i*line}" width="3" height="6" fill="#69f0a0" opacity="0"><set attributeName="opacity" to="1" begin="{i*duration:.4f}s" dur="{duration:.4f}s"/><animate attributeName="x" from="20" to="335" begin="{i*duration:.4f}s" dur="{duration:.4f}s"/></rect>'
    body+=text(20,389,'[ portrait rendered locally ]',9,'muted')
    (ROOT/'avi-ascii.svg').write_text(shell(355,410,'ASCII portrait of Lucas Silva',body),encoding='utf-8')
if __name__ == '__main__': main()
