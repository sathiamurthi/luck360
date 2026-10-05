import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
start_idx = content.find("bannerEl.innerHTML = `")
end_idx = content.find("        // 2. RENDER THE EXPECTED TIMELINE SLOTS", start_idx)
print(content[start_idx:end_idx].encode('ascii', 'ignore').decode('ascii'))
