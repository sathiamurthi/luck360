import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print('Scripts count:', len(scripts))
main_js = scripts[-1]
print('Main JS length:', len(main_js))

for func in ['renderCrossSlotPatternTab', 'calculatePredictions', 'pollLiveDatabase', 'loadComprehensiveReport', 'syncCrossSlotInputs']:
    def_pos = main_js.find('function ' + func)
    calls = [m.start() for m in re.finditer(func + r'\s*\(', main_js)]
    print(f'Function {func:30}: def at {def_pos}, calls at {calls}')
