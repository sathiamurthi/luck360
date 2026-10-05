import urllib.request
try:
    response = urllib.request.urlopen('http://localhost:8001/')
    print("SUCCESS")
    print(response.read()[:50])
except Exception as e:
    print("ERROR:", e)
