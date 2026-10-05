import io
content = io.open('index.html', 'r', encoding='utf-8').read()
for el in ['mp-prev', 'mp-curr', 'mp-min', 'mp-gaps', 'mp-sync', 'mp-copy', 'mp-banner-copy']:
    if f'id="{el}"' in content:
        print(f"Found {el}")
    else:
        print(f"MISSING {el}")
