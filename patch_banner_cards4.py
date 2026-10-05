import io
content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read().splitlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(content):
    if '<p class="text-xs text-slate-800 font-medium font-sans leading-relaxed">' in line:
        if "Dual Confluence" in content[i+1]:
            start_idx = i
    if start_idx != -1 and "</p>" in line and i <= start_idx + 6:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    content[start_idx] = """              <div id="dynamic-4-subcards" class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3 mb-4">
                <!-- 4 subcards injected here by JS below -->
              </div>"""
    for i in range(start_idx + 1, end_idx + 1):
        content[i] = ""
    
    with io.open('script1.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write('\n'.join(content))
    print("Replaced successfully!")
else:
    print("Could not find block.")
