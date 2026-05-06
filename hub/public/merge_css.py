import os, re, glob, shutil

def remove_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

def parse_css(css):
    rules = []
    i, n = 0, len(css)
    while i < n:
        while i < n and css[i].isspace():
            i += 1
        if i >= n:
            break
        if css[i] == '@':
            brace = css.find('{', i)
            if brace == -1: break
            selector = css[i:brace].strip()
            depth, j = 0, brace
            while j < n:
                c = css[j]
                if c in '"\'':
                    q = c
                    j += 1
                    while j < n and css[j] != q:
                        if css[j] == '\\': j += 2
                        else: j += 1
                    j += 1
                elif c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            block = css[brace+1:j]
            rules.append(('media', selector, parse_css(block)))
            i = j + 1
        else:
            brace = css.find('{', i)
            if brace == -1: break
            selector = css[i:brace].strip()
            depth, j = 1, brace + 1
            while j < n and depth > 0:
                c = css[j]
                if c in '"\'':
                    q = c
                    j += 1
                    while j < n and css[j] != q:
                        if css[j] == '\\': j += 2
                        else: j += 1
                    j += 1
                elif c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            declarations = css[brace+1:j].strip()
            rules.append(('rule', selector, declarations))
            i = j + 1
    return rules

def compress_decl(decl):
    decl = re.sub(r'\s+', ' ', decl).strip()
    decl = re.sub(r'\s*([:;,])\s*', r'\1', decl)
    return decl

def merge_and_compress(rules):
    normal = {}
    media = {}
    for rule in rules:
        if rule[0] == 'rule':
            _, sel, decl = rule
            decl = compress_decl(decl)
            if sel in normal:
                normal[sel] += ';' + decl
            else:
                normal[sel] = decl
        elif rule[0] == 'media':
            _, sel, inner = rule
            inner_dict = {}
            for ir in inner:
                if ir[0] == 'rule':
                    _, s, d = ir
                    d = compress_decl(d)
                    if s in inner_dict:
                        inner_dict[s] += ';' + d
                    else:
                        inner_dict[s] = d
            key = re.sub(r'\s+', ' ', sel).strip()
            if key not in media:
                media[key] = {}
            for s, d in inner_dict.items():
                if s in media[key]:
                    media[key][s] += ';' + d
                else:
                    media[key][s] = d
    parts = []
    for sel, decl in normal.items():
        parts.append(f"{sel}{{{decl}}}")
    for sel, inner_dict in media.items():
        inner_parts = [f"{s}{{{d}}}" for s, d in inner_dict.items()]
        parts.append(f"{sel}{{{''.join(inner_parts)}}}")
    return ''.join(parts)

css_files = sorted(glob.glob('*.css'))
all_css = ''
for f in css_files:
    with open(f, 'r', encoding='utf-8') as fh:
        all_css += fh.read() + '\n'

all_css = remove_comments(all_css)
rules = parse_css(all_css)
merged = merge_and_compress(rules)

with open('bundle.css', 'w', encoding='utf-8') as f:
    f.write(merged)

for html in sorted(glob.glob('*.html')):
    with open(html, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\s*<link rel="stylesheet" href="[^"]*\.css">\s*', '\n', content)
    link = '  <link rel="stylesheet" href="bundle.css">\n'
    content = content.replace('</head>', link + '</head>')
    with open(html, 'w', encoding='utf-8') as f:
        f.write(content)

os.makedirs('_css_backup', exist_ok=True)
for f in css_files:
    shutil.move(f, os.path.join('_css_backup', os.path.basename(f)))

orig = sum(os.path.getsize(os.path.join('_css_backup', f)) for f in css_files)
print(f'[BUNDLE] {len(merged)} bytes (was {orig} bytes)')
print('[DONE]')
