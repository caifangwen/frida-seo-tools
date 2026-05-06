import os, re, glob, shutil

MAP = {
    "width:10%":"w-10","width:15%":"w-15","width:20%":"w-20","width:30%":"w-30",
    "width:35%":"w-35","width:40%":"w-40","width:45%":"w-45","width:50%":"w-50",
    "width:55%":"w-55","width:58%":"w-58","width:60%":"w-60","width:62%":"w-62",
    "width:64%":"w-64","width:65%":"w-65","width:66%":"w-66","width:68%":"w-68",
    "width:70%":"w-70","width:72%":"w-72","width:73%":"w-73","width:74%":"w-74",
    "width:75%":"w-75","width:78%":"w-78","width:79%":"w-79","width:80%":"w-80",
    "width:82%":"w-82","width:83%":"w-83","width:84%":"w-84","width:85%":"w-85",
    "width:86%":"w-86","width:88%":"w-88","width:90%":"w-90","width:91%":"w-91",
    "width:95%":"w-95","width:100%":"w-100",
    "margin-top:6px;":"mt-6","margin:0.4rem 0 0;":"mt-04",
    "margin-top:var(--gap-xs);font-size:0.82rem;color:var(--muted-500);":"mt-xs text-xs-muted",
    "margin-top:var(--gap-sm);":"mt-sm","margin-top:var(--gap-md);":"mt-md",
    "margin-top:var(--gap-lg);":"mt-lg","margin-top:var(--gap-xl):":"mt-xl",
    "margin-top:var(--gap-2xl):":"mt-2xl","margin-top:var(--gap-4xl):":"mt-4xl",
    "margin-top:20px;":"mt-20","margin-top:1.2rem;":"mt-12","margin-top:0;":"mt-0",
    "margin-top:0;text-align:left;":"mt-0 text-left","margin-bottom:0;":"mb-0",
    "margin-bottom:var(--gap-md);":"mb-md","margin-bottom:var(--gap-xl):":"mb-xl",
    "color:var(--secondary);":"text-secondary","text-align:center;":"text-center",
    "text-align:left;":"text-left",
    "font-size:0.88rem;color:var(--muted-800);margin:0;line-height:1.6;":"text-sm-muted",
    "font-size:0.95rem;color:var(--muted-800);line-height:1.6;margin:0;":"text-base-muted",
    "font-size:0.95rem;color:var(--muted-800);line-height:1.6;margin-top:var(--gap-md);":"text-base-muted mt-md",
    "max-width:var(--content-max); margin-bottom:var(--gap-2xl);":"content-max mb-2xl",
    "max-width:var(--content-max);color:var(--muted-900);font-size:1.05rem;line-height:1.7;":"content-max text-muted-900",
    "text-align:center;margin:40px 0 20px;font-size:1.3rem;":"section-title-center",
    "text-align:center;max-width:700px;margin:0 auto 30px;color:var(--muted-700);":"lead-center",
}

def extract(data,name):
    p=re.compile(r'<style[^>]*>(.*?)</style>',re.S)
    b=p.findall(data)
    if not b: return data,None
    css='\n\n'.join(x.strip() for x in b)
    data=p.sub('',data)
    link='  <link rel="stylesheet" href="'+name.replace('.html','.css')+'">\n'
    data=data.replace('</head>',link+'</head>') if '</head>' in data else data.replace('<body>',link+'<body>')
    return data,css

def repl(data):
    for m in reversed(list(re.finditer(r'style="([^"]*)"',data))):
        v=m.group(1).strip()
        if v not in MAP: continue
        c=MAP[v]; s,e=m.start(),m.end()
        ts=data.rfind('<',0,s); te=data.find('>',e)
        if ts==-1 or te==-1: continue
        tag=data[ts:te+1]
        tag=re.sub(r'\s+style="[^"]*"','',tag,count=1)
        cm=re.search(r'class="([^"]*)"',tag)
        if cm:
            tag=tag[:cm.start()]+'class="'+cm.group(1)+' '+c+'"'+tag[cm.end():]
        else:
            tag=tag[:-1]+' class="'+c+'"'+tag[-1]
        data=data[:ts]+tag+data[te+1:]
    return data

# Restore backups
for fp in sorted(glob.glob('*.html')):
    name=os.path.basename(fp)
    bk=os.path.join('_backup',name)
    if os.path.exists(bk):
        shutil.copy2(bk,fp)
        print('[RESTORE]',name)

# Re-process
for fp in sorted(glob.glob('*.html')):
    name=os.path.basename(fp)
    with open(fp,'r',encoding='utf-8') as f: d=f.read()
    d,css=extract(d,name)
    if css:
        with open(name.replace('.html','.css'),'w',encoding='utf-8') as f: f.write(css)
        print('[CSS]',name.replace('.html','.css'))
    d=repl(d)
    with open(fp,'w',encoding='utf-8') as f: f.write(d)
    print('[HTML]',name)

# Update to nichehub links
for fp in sorted(glob.glob('*.html')):
    with open(fp,'r',encoding='utf-8') as f: d=f.read()
    d=re.sub(r'\s*<link rel="stylesheet" href="[^"]*\.css">\s*','\n',d)
    links='  <link rel="stylesheet" href="nichehub-core.css">\n  <link rel="stylesheet" href="nichehub-ui.css">\n  <link rel="stylesheet" href="nichehub-content.css">\n  <link rel="stylesheet" href="nichehub-dataviz.css">\n  <link rel="stylesheet" href="nichehub-responsive.css">\n'
    d=d.replace('</head>',links+'</head>')
    with open(fp,'w',encoding='utf-8') as f: f.write(d)
    print('[UPDATE]',os.path.basename(fp))

print('[DONE]')
