import glob

CSS_LINKS = '''  <link rel="stylesheet" href="nichehub-core.css">
  <link rel="stylesheet" href="nichehub-ui.css">
  <link rel="stylesheet" href="nichehub-content.css">
  <link rel="stylesheet" href="nichehub-dataviz.css">
  <link rel="stylesheet" href="nichehub-responsive.css">
'''

files = [
    'pillar-carbon-steels.html',
    'pillar-damascus-layered.html',
    'pillar-powder-metallurgy-steels.html',
    'pillar-stainless-steels.html',
    'pillar-tool-semi-stainless.html'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace hub-common.css with nichehub links
    if 'hub-common.css' in html:
        html = html.replace('<link href="hub-common.css" rel="stylesheet"/>', CSS_LINKS.strip())
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'{fname}: replaced hub-common.css')
    elif 'nichehub-core.css' not in html:
        # If neither hub-common nor nichehub links exist, insert before </head>
        head_end = html.find('</head>')
        if head_end != -1:
            html = html[:head_end] + CSS_LINKS + '\n' + html[head_end:]
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'{fname}: inserted CSS links')
    else:
        print(f'{fname}: already has nichehub links')
