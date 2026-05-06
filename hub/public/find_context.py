import glob, re

def get_context(text, pos, radius=40):
    start = max(0, pos - radius)
    end = min(len(text), pos + radius)
    return text[start:end]

for html in sorted(glob.glob('*.html')):
    with open(html, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    if '�' not in content:
        continue
    
    print(f'=== {html} ===')
    for m in re.finditer('�', content):
        ctx = get_context(content, m.start())
        print(f'  pos {m.start()}: {repr(ctx)}')
    print()
