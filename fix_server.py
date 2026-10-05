import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()

route = """
@app.get("/script1.js", summary="Main Dashboard Script", tags=["Dashboard"])
def get_script():
    try:
        with open(os.path.join(DB_DIR, "script1.js"), "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"script1.js not found: {e}")
"""

if 'def get_script' not in content:
    content = content.replace('@app.get("/kerala.jpeg"', route + '\n@app.get("/kerala.jpeg"')
    with io.open('luck360_api_server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added route for script1.js")
else:
    print("Route already exists")
