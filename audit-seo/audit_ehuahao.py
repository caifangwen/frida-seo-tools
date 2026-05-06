import urllib.request, re, ssl
ctx = ssl.create_default_context()
req = urllib.request.Request('https://e-huahao.com/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

print('=== 首页核心SEO元素 ===')
title = re.search(r'<title>(.*?)</title>', html, re.I)
print('Title:', title.group(1) if title else 'NOT FOUND')

desc = re.search(r'<meta name="description" content="(.*?)"', html, re.I)
print('Meta Desc:', (desc.group(1)[:140] + '...') if desc else 'NOT FOUND')

canonical = re.search(r'<link rel="canonical" href="(.*?)"', html, re.I)
print('Canonical:', canonical.group(1) if canonical else 'NOT FOUND')

robots = re.search(r'<meta name="robots" content="(.*?)"', html, re.I)
print('Robots:', robots.group(1) if robots else 'NOT FOUND')

h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S|re.I)
print('H1:', re.sub(r'<[^>]+>', '', h1.group(1)).strip()[:100] if h1 else 'NOT FOUND')

h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.S|re.I)
print('H2 count:', len(h2s))
for i, h in enumerate(h2s[:10]):
    txt = re.sub(r'<[^>]+>', '', h).strip()
    if txt:
        print(f'  H2-{i+1}: {txt[:90]}')

schemas = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
print('\nSchema.org 数量:', len(schemas))
for s in schemas[:5]:
    t = re.search(r'"@type":"(.*?)"', s)
    if t:
        print('  @type:', t.group(1))

http_links = re.findall(r'href="(http://[^"]+)"', html)
print('\nHTTP混合内容链接:', len(http_links))
for l in http_links[:8]:
    print(' ', l)

imgs = re.findall(r'<img[^>]*alt="(.*?)"', html, re.I)
empty_alt = imgs.count('')
print('\n图片 alt 标签:', len(imgs), '张, 空 alt:', empty_alt)

print('\n=== HTTP Response Headers ===')
print('Server:', resp.headers.get('Server'))
print('X-Content-Type-Options:', resp.headers.get('X-Content-Type-Options'))
print('X-XSS-Protection:', resp.headers.get('X-XSS-Protection'))
print('Strict-Transport-Security:', resp.headers.get('Strict-Transport-Security'))
print('Content-Security-Policy:', resp.headers.get('Content-Security-Policy'))
