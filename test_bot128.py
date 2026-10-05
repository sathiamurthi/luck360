import json
try:
    with open('draw_history.json', 'r') as f:
        data = json.load(f)
        for d in data[-5:]:
            print(d)
except Exception as e:
    print(e)
