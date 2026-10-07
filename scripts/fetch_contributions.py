"""Fetch GitHub's public calendar; fail closed instead of inventing counts."""
import json
import re
from datetime import date, timedelta
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
USER = 'luscaarmstrong1'

def parse_calendar(html):
    soup = BeautifulSoup(html, 'html.parser')
    tips = {t.get('for'): t.get_text(' ', strip=True) for t in soup.select('tool-tip[for]')}
    found = {}
    for cell in soup.select('[data-date]'):
        day = cell['data-date']
        date.fromisoformat(day)
        label = tips.get(cell.get('id'), '') or cell.get('aria-label', '') or cell.get('title', '')
        if not label and cell.get('aria-describedby'):
            target = soup.find(id=cell['aria-describedby'])
            label = target.get_text(' ', strip=True) if target else ''
        count = cell.get('data-count')
        if count is None:
            match = re.search(r'([\d,]+) contributions?\b', label, re.I)
            if match:
                count = match[1].replace(',', '')
            elif re.search(r'No contributions', label, re.I):
                count = 0
            else:
                raise ValueError(f'Cannot resolve contribution count for {day}')
        count = int(count)
        level = int(cell.get('data-level', min(count, 4)))
        if count < 0 or not 0 <= level <= 4:
            raise ValueError('Invalid count or level')
        item = {'date': day, 'count': count, 'level': level}
        if day in found and found[day] != item:
            raise ValueError(f'Conflicting calendar cells: {day}')
        found[day] = item
    days = sorted(found.values(), key=lambda d: d['date'])
    if len(days) < 350:
        raise ValueError('Incomplete calendar; preserving existing data')
    for a, b in zip(days, days[1:]):
        if date.fromisoformat(b['date']) - date.fromisoformat(a['date']) != timedelta(days=1):
            raise ValueError('Calendar has missing dates')
    return days

def statistics(days):
    total = sum(d['count'] for d in days)
    longest = run = 0
    monthly = {}
    for d in days:
        run = run + 1 if d['count'] else 0
        longest = max(longest, run)
        month = d['date'][:7]
        monthly[month] = monthly.get(month, 0) + d['count']
    # Today is still in progress: allow a streak ending yesterday.
    end = len(days) - 1
    if not days[end]['count']:
        end -= 1
    current = 0
    while end >= 0 and days[end]['count']:
        current += 1
        end -= 1
    best = max(days, key=lambda d: d['count'])
    active = sum(d['count'] > 0 for d in days)
    cutoff = date.fromisoformat(days[-1]['date']) - timedelta(days=364)
    return {'total': total, 'last_year': sum(d['count'] for d in days if date.fromisoformat(d['date']) >= cutoff),
            'current_streak': current, 'longest_streak': longest, 'best_day': best['date'],
            'best_day_count': best['count'], 'daily_average': round(total / len(days), 2),
            'active_days': active, 'active_percentage': round(100 * active / len(days), 2),
            'most_active_month': max(monthly, key=monthly.get), 'monthly_totals': monthly}

def main():
    session = requests.Session()
    session.headers['User-Agent'] = 'luscaarmstrong1-profile-calendar/1.0'
    session.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])))
    url = f'https://github.com/users/{USER}/contributions'
    response = session.get(url, timeout=(10, 45))
    response.raise_for_status()
    days = parse_calendar(response.text)
    data = {'username': USER, 'source': url, 'period_start': days[0]['date'], 'period_end': days[-1]['date'],
            'streak_policy': 'Calendar ending date, or previous day if ending date has zero contributions.',
            'statistics': statistics(days), 'days': days}
    path = ROOT / 'data/contributions.json'
    path.parent.mkdir(exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)
    print(f"Verified {len(days)} days; {data['statistics']['total']} contributions")

if __name__ == '__main__':
    main()
