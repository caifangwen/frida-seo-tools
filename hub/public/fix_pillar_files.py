from bs4 import BeautifulSoup
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
    
    # Step 1: Replace inline CSS with external links
    if '<style>' in html and 'nichehub-core.css' not in html:
        # Find and remove the inline style block
        style_start = html.find('<style>')
        style_end = html.find('</style>', style_start) + len('</style>')
        
        # Replace with CSS links + a small style block for any page-specific styles if needed
        # But for now, just remove and add links before </head>
        html = html[:style_start] + CSS_LINKS + '\n' + html[style_end:]
        print(f'{fname}: replaced inline CSS with external links')
    
    # Step 2: Move steel-product-right blocks using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    product_rights = soup.find_all('div', class_='steel-product-right')
    moved = 0
    for prod_right in product_rights:
        # Find parent steel-main-right
        parent_right = prod_right.find_parent('div', class_='steel-main-right')
        if not parent_right:
            continue
        
        # Find corresponding steel-main-left (previous sibling of parent_right's parent or earlier)
        # The structure is: steel-card-main -> [steel-main-left, steel-main-right]
        # So steel-main-left should be a sibling of parent_right within the same parent
        card_main = parent_right.find_parent('div', class_='steel-card-main')
        if not card_main:
            continue
        
        left = card_main.find('div', class_='steel-main-left')
        if not left:
            continue
        
        # Move the element
        prod_right.extract()
        left.append(prod_right)
        moved += 1
    
    # Write back
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f'{fname}: moved {moved} product-right blocks')
