import re
import glob
import os

# Build a map of steel name -> review file -> background image
steel_to_image = {}

for f in glob.glob('*-steel-review.html') + glob.glob('*-steel.html') + glob.glob('*-guide.html'):
    basename = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    matches = re.findall(r'background-image:url\(([^)]+)\)', html)
    if matches:
        # Extract steel name from filename
        # e.g., '1095-steel-review.html' -> '1095'
        # e.g., 'aogami-2-blue-paper-steel-steel-review.html' -> 'aogami-2'
        name = basename.replace('-steel-review.html', '').replace('-steel.html', '').replace('-guide.html', '')
        steel_to_image[name] = matches[0]

print('Mapped', len(steel_to_image), 'steel review files')
for k, v in list(steel_to_image.items())[:5]:
    print(' ', k, '->', v[:60])

# Pillar files and their steel card IDs
pillar_files = [
    'pillar-carbon-steels.html',
    'pillar-damascus-layered.html',
    'pillar-powder-metallurgy-steels.html',
    'pillar-stainless-steels.html',
    'pillar-tool-semi-stainless.html'
]

for fname in pillar_files:
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    modified = False
    # Find all steel-card divs
    for m in re.finditer(r'<div class="steel-card" id="(dd-[a-z0-9-]+)">', html):
        card_id = m.group(1)
        steel_name = card_id.replace('dd-', '')
        
        # Find matching image
        img_url = None
        if steel_name in steel_to_image:
            img_url = steel_to_image[steel_name]
        else:
            # Try partial matches
            for key, url in steel_to_image.items():
                if steel_name in key or key in steel_name:
                    img_url = url
                    break
        
        if img_url:
            # Find the steel-card-header within this card
            card_start = m.start()
            card_end = html.find('</div>', card_start)
            # Need to find the correct closing div by counting
            # But simpler: find steel-card-header after card_start
            header_match = re.search(r'<div class="steel-card-header">', html[card_start:card_start+500])
            if header_match:
                header_pos = card_start + header_match.start()
                # Replace <div class="steel-card-header"> with <div class="steel-card-header" style="background-image:url(...)">
                old = '<div class="steel-card-header">'
                new = '<div class="steel-card-header" style="background-image:url(' + img_url + ')">'
                if old in html[header_pos:header_pos+100]:
                    html = html[:header_pos] + new + html[header_pos+len(old):]
                    modified = True
    
    if modified:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'{fname}: card header images injected')
    else:
        print(f'{fname}: no modifications')
