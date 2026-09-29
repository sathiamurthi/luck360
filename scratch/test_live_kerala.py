import urllib.request
import re
from datetime import datetime

url = 'https://www.keralalotteries.net/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        print('Page length:', len(html))
        today_str = datetime.now().strftime('%d-%m-%Y')
        print('Looking for today date:', today_str)
        # Search for post links
        links = re.findall(r'https://www.keralalotteries.net/\d{4}/\d{2}/[^\"]+', html)
        print('Found links:', len(links))
        for l in links[:5]:
            print('Link:', l)
        
        # Check text mentioning today or 1st prize
        for line in html.split('\n'):
            if any(k in line.lower() for k in ['1st prize', 'karunya', 'kr-', 'first prize', today_str.lower()]):
                clean = re.sub(r'<[^>]+>', ' ', line).strip()
                if len(clean) > 5 and len(clean) < 150:
                    print('Match:', clean)
except Exception as e:
    print('Error:', e)
