import io
content = io.open('script1.js', 'r', encoding='utf-8').read()

start_marker = "const bannerEl = document.getElementById('banner-hottest-recommendations');"
idx_start = content.find(start_marker)
idx_end = content.find("// Populate TOP 7 RULES", idx_start)

print(content[idx_end-100:idx_end+100])
