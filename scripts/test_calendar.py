import unittest
from datetime import date,timedelta
from fetch_contributions import parse_calendar,statistics
class CalendarTests(unittest.TestCase):
    def fixture(self,mode):
        cells=[]
        for i in range(365):
            day=date(2025,1,1)+timedelta(days=i)
            if mode=='count':
                cells.append(f'<rect data-date="{day}" data-count="2" data-level="1"/>')
            else:
                cells.append(f'<td id="d{i}" data-date="{day}" data-level="1"></td><tool-tip for="d{i}">2 contributions on day</tool-tip>')
        return ''.join(cells)
    def test_two_html_structures(self):
        self.assertEqual(parse_calendar(self.fixture('count')),parse_calendar(self.fixture('tooltip')))
    def test_missing_counts_fail(self):
        with self.assertRaises(ValueError): parse_calendar('<td data-date="2025-01-01" data-level="2"/>')
    def test_missing_day_fails(self):
        html=self.fixture('count').replace('<rect data-date="2025-01-02" data-count="2" data-level="1"/>','')
        with self.assertRaises(ValueError): parse_calendar(html)
    def test_streaks_and_totals(self):
        days=[{'date':f'2026-01-0{i+1}','count':n} for i,n in enumerate([1,2,0,3,4,0])]
        s=statistics(days)
        self.assertEqual((s['total'],s['current_streak'],s['longest_streak'],s['active_days']),(10,2,2,4))
        self.assertEqual(s['best_day'],'2026-01-05')
    def test_zero_calendar(self):
        s=statistics([{'date':'2026-01-01','count':0}])
        self.assertEqual(s['current_streak'],0)
if __name__=='__main__': unittest.main()
