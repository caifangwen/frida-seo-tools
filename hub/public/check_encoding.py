import glob

for html in sorted(glob.glob('*.html')):
    with open(html, 'rb') as f:
        raw = f.read()
    try:
        raw.decode('utf-8')
        print(f'[OK] {html}')
    except UnicodeDecodeError as e:
        print(f'[ERROR] {html} at {e.start}: {raw[e.start-2:e.end+2]}')
