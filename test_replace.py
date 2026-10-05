import io
content = io.open('script1.js', 'r', encoding='utf-8').read()

start_marker = "const bannerEl = document.getElementById('banner-hottest-recommendations');\n      if (bannerEl) {"
idx_start = content.find(start_marker)

end_marker = "// Populate TOP 7 RULES"
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    print(f"Found from {idx_start} to {idx_end}. Length: {idx_end - idx_start}")
else:
    print("Not found!")
