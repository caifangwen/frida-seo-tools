import csv
import re
import glob

# Load all images from CSV
csv_images = {}
with open('leeknives_media_export.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        pn = r.get('post_name', '').lower()
        guid = r.get('guid', '')
        if pn and guid:
            csv_images[pn] = guid

# Fallback images for steels without review pages
fallback_map = {
    'shirogami-1': 'japanese-high-carbon-steels-aogami-vs-shirogami',
    'aogami-2': 'japanese-high-carbon-steels-aogami-vs-shirogami',
    'aogami-super': 'japanese-high-carbon-steels-aogami-vs-shirogami',
    '1075': '1095-steel-a-commercial-success-and-heres-why',
    '5160': 'what-is-52100-steel-understanding-its-properties-and-uses',
    'o1': 'understanding-what-is-the-a2-tool-steel',
    '15n20': 'what-is-damascus-steel-origin-composition-and-properties',
    'vg-10': 'what-to-expect-from-aus-8-as-a-knife-blade-material',
    'nitro-v': 'what-to-expect-from-aus-8-as-a-knife-blade-material',
    '420hc': '3cr13-steel-yay-or-nay',
    '440c': '3cr13-steel-yay-or-nay',
    'x50crmov15': 'what-to-expect-from-aus-8-as-a-knife-blade-material',
    '154cm': 'a-detailed-breakdown-of-n690-stainless-steel',
    'lc200n': 'a-detailed-breakdown-of-n690-stainless-steel',
    'vg-10-damascus': 'what-is-damascus-steel-origin-composition-and-properties',
    'raindrop-damascus': 'raindrop-damascus',
    'ladder-damascus': 'different-patterns-of-damascus-steel',
    'mokume-gane': 'what-is-a-damascus-pattern-image',
    'spirograph-damascus': 'various-types-of-damascus-patterns',
    'cpm-s30v': 's35vn-vs-m390-comparing-properties-price',
    'cpm-s35vn': 's35vn-vs-m390-comparing-properties-price',
    'cpm-s45vn': 's35vn-vs-m390-comparing-properties-price',
    'cpm-20cv': 'why-m390-steel-is-taking-the-knife-making-world-by-storm',
    'cpm-m4': 'why-m390-steel-is-taking-the-knife-making-world-by-storm',
    'k390': 'why-m390-steel-is-taking-the-knife-making-world-by-storm',
    'cpm-cru-wear': 'why-m390-steel-is-taking-the-knife-making-world-by-storm',
    'cpm-3v': 'why-m390-steel-is-taking-the-knife-making-world-by-storm',
    'rex-121': 'why-m390-steel-is-taking-the-knife-making-world-by-storm',
    'd2': 'd2-steel-review-as-a-knife-material',
    'aus-8': 'what-to-expect-from-aus-8-as-a-knife-blade-material',
    '9cr18mov': '3cr13-steel-yay-or-nay',
    '7cr17mov': '3cr13-steel-yay-or-nay',
    '8cr14mov': '3cr13-steel-yay-or-nay',
}

# Build final image map
final_images = {}
for key, fallback_pn in fallback_map.items():
    if fallback_pn in csv_images:
        final_images[key] = csv_images[fallback_pn]

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
    for m in re.finditer(r'<div class="steel-card" id="(dd-[a-z0-9-]+)">', html):
        card_id = m.group(1)
        steel_name = card_id.replace('dd-', '')
        
        # Check if header already has background
        card_start = m.start()
        header_match = re.search(r'<div class="steel-card-header">', html[card_start:card_start+500])
        if header_match:
            header_pos = card_start + header_match.start()
            # Check if already has style
            if 'style=' not in html[header_pos:header_pos+80]:
                img_url = None
                # Try direct match
                if steel_name in final_images:
                    img_url = final_images[steel_name]
                else:
                    # Try partial match
                    for key, url in final_images.items():
                        if key in steel_name or steel_name in key:
                            img_url = url
                            break
                
                if img_url:
                    old = '<div class="steel-card-header">'
                    new = '<div class="steel-card-header" style="background-image:url(' + img_url + ')">'
                    html = html[:header_pos] + new + html[header_pos+len(old):]
                    modified = True
    
    if modified:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'{fname}: filled missing images')
    else:
        print(f'{fname}: no missing images')
