"""Render actual counts using GitHub levels, Sunday-aligned calendar columns."""
import json
from datetime import date, timedelta
from pathlib import Path
from svg_common import shell, text, fade
ROOT = Path(__file__).resolve().parents[1]
PALETTE = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353', '#69f0a0']
def main():
    data = json.loads((ROOT / 'data/contributions.json').read_text())
    days = data['days']; stats = data['statistics']
    first = date.fromisoformat(days[0]['date'])
    start = first - timedelta(days=(first.weekday()+1)%7)
    weeks = (date.fromisoformat(days[-1]['date'])-start).days//7+1
    pitch = min(14, 758/weeks); box = pitch-3
    body = text(28, 31, 'CONTRIBUTION LOG', 12, 'green') + text(28, 54, f"{data['period_start']}  →  {data['period_end']}", 11, 'muted')
    for row, name in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        body += text(24, 95+row*pitch, name, 10, 'muted')
    last_month = None
    for d in days:
        day = date.fromisoformat(d['date']); delta = (day-start).days
        col, row = divmod(delta, 7); x=70+col*pitch; y=85+row*pitch
        if day.month != last_month and (day.day == 1 or last_month is None):
            if col < weeks-2:
                body += text(x, 75, day.strftime('%b'), 10, 'muted')
            last_month = day.month
        body += f'<rect x="{x:.2f}" y="{y:.2f}" width="{box:.2f}" height="{box:.2f}" rx="2" fill="{PALETTE[d["level"]]}"><title>{day}: {d["count"]} contributions</title>{fade(.035*col+.045*row)}</rect>'
    body += text(70, 208, f"{stats['last_year']:,} contributions in the last 365 days", 15)
    body += text(70, 234, f"Current streak {stats['current_streak']}d   /   Longest {stats['longest_streak']}d   /   Best day {stats['best_day_count']}", 11, 'muted')
    body += text(70, 258, f"{stats['active_days']} active days · {stats['active_percentage']}% active · {stats['daily_average']} / day", 10, 'muted')
    body += text(655, 258, 'Less', 10, 'muted')
    for i, color in enumerate(PALETTE[0:5]):
        body += f'<rect x="{689+i*15}" y="248" width="11" height="11" rx="2" fill="{color}"/>'
    body += text(770, 258, 'More', 10, 'muted')
    (ROOT/'contrib-heatmap.svg').write_text(shell(860, 280, 'Lucas Silva — public GitHub contribution calendar', body), encoding='utf-8')
if __name__ == '__main__': main()
