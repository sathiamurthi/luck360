import io
content = io.open('script1.js', 'r', encoding='utf-8').read()

idx_is8pm = content.find("const is8PMComplete")
idx_banner = content.find("const bannerEl = document.getElementById('banner-hottest-recommendations');")

print(f"is8PMComplete is at {idx_is8pm}")
print(f"bannerEl is at {idx_banner}")
