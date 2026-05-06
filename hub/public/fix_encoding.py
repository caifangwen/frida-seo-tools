import glob

replacements = {
    b'\xe2\x80\x3f': b'\xe2\x80\x99',
    b'\xe2\x86\x3f': b'\xe2\x86\x92',
    b'\xe5\x8f\x3f': b'\xe5\x8f\xb7',
}

for html in sorted(glob.glob('*.html')):
    with open(html, 'rb') as f:
        raw = f.read()
    
    fixed = raw
    for bad, good in replacements.items():
        fixed = fixed.replace(bad, good)
    
    if fixed != raw:
        with open(html, 'wb') as f:
            f.write(fixed)
        print('[FIXED]', html)
    else:
        print('[OK]', html)
    
    try:
        fixed.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f'  -> STILL BAD at {e.start}: {fixed[e.start-2:e.end+2]}')
