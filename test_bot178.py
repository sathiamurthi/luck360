import io
import re

content = io.open('script1.js', 'r', encoding='utf-8', errors='surrogatepass').read()

stack = []
lines = content.splitlines()
for i, line in enumerate(lines):
    # Strip everything that is not a bracket just for quick check
    pass

print(content.count("// INJECT 4 SUBCARDS"))
