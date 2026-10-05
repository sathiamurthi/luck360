import io
content = io.open('all_scripts.js', 'r', encoding='utf-8').read()
if "banner-hottest-recommendations" in content:
    print("Found banner in all_scripts.js")
else:
    print("NOT FOUND banner")
