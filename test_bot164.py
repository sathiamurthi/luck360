import json
try:
    with open('draw_history.json', 'r') as f:
        data = json.load(f)
        print("Total draws:", len(data))
except Exception as e:
    print(e)
