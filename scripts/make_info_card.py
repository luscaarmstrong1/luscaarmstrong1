"""Professional facts from the existing profile and audited public repositories."""
from pathlib import Path
import os
from svg_common import shell,text,fade
ROOT=Path(__file__).resolve().parents[1]
ROWS=[('Role','Electrical engineer / Developer'),('Focus','Energy · Automation · Applied AI'),('Building','Renovera · Prospecta Nicho'),('Languages','Python · TypeScript · JavaScript'),('Web','Next.js · React · Astro'),('Systems','APIs · Data pipelines · Dashboards'),('Automation','GitHub Actions · Python'),('Engineering','Solar PV · BESS · Power systems'),('Location','Brazil')]
def main():
    body=text(24,29,'lucas@github:~$ whoami',12,'green')
    body+=text(24,70,'Lucas Silva',26)+text(24,96,'Engineering ideas into working systems.',11,'muted')
    body+='<path d="M24 116H471" stroke="#30363d"/>'
    for i,(key,value) in enumerate(ROWS):
        begin=.35+i*.09
        motion=''
        if os.getenv('STATIC') != '1':
            end=begin+.35
            motion=f'<animateTransform class="animated" attributeName="transform" type="translate" values="0 5;0 5;0 0" keyTimes="0;{begin/end:.6f};1" dur="{end:.3f}s" fill="freeze"/>'
        body+='<g>'+text(24,145+i*25,key,11,'green')+text(122,145+i*25,value,10.5)+fade(begin)+motion+'</g>'
    body+=text(24,389,'source: public repositories + professional profile',9,'muted')
    (ROOT/'info-card.svg').write_text(shell(495,410,'Lucas Silva — engineering, software and automation',body),encoding='utf-8')
if __name__ == '__main__': main()
