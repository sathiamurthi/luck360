import io
import glob
for f in glob.glob("*.py"):
    content = io.open(f, 'r', encoding='utf-8').read()
    if "Populate TOP 7" in content:
        print(f"Found in {f}")
