"""Lightweight validation, also used by the daily workflow."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    for name in ['avi-ascii.svg','info-card.svg','contrib-heatmap.svg']:
        p=ROOT/name
        assert p.stat().st_size > 100
        root=ET.parse(p).getroot()
        assert all(k in root.attrib for k in ('width','height','viewBox'))
        assert not any(el.tag.endswith('script') for el in root.iter())
    readme=(ROOT/'README.md').read_text(encoding='utf-8-sig')
    for path in re.findall(r'src="\./([^"]+)"',readme):
        assert (ROOT/path).is_file(), path
    data=json.loads((ROOT/'data/contributions.json').read_text())
    assert data['statistics']['total']==sum(d['count'] for d in data['days'])
    assert len(data['days']) >= 350
    print('Valid SVG XML, README image paths, and contribution totals')
if __name__=='__main__': main()
