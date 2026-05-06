import glob, os

for html in sorted(glob.glob('*.html')):
    with open(html, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    if '[BAD]' not in content.replace('�', '[BAD]'):
        continue
    
    print('=== ' + html + ' ===')
    pos = 0
    while True:
        pos = content.find('�', pos)
        if pos == -1:
            break
        ctx = content[max(0,pos-40):pos+40]
        ctx = ctx.replace('�', '[BAD]')
        print(ctx)
        print('---')
        pos += 1
