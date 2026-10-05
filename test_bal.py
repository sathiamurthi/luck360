import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
print("Backticks:", content.count('`'))
print("Braces:", content.count('{'), content.count('}'))
print("Parens:", content.count('('), content.count(')'))
