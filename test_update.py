import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
if "updateDashboard" in content:
    print("Found updateDashboard")
