import json
try:
    with open('draw_history.json', 'r') as f:
        data = json.load(f)
        for i in range(min(5, len(data))):
            print(data[i])
except Exception as e:
    print(e)
