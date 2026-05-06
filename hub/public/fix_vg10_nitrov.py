import re

for fname in ['pillar-stainless-steels.html', 'pillar-damascus-layered.html', 'pillar-powder-metallurgy-steels.html', 'pillar-tool-semi-stainless.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Fix vg10 -> AUS-8 image
    old_vg10 = '<div class="steel-card" id="dd-vg10">\n<div class="steel-card-header">'
    new_vg10 = '<div class="steel-card" id="dd-vg10">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2022/05/What-to-expect-from-AUS-8-as-a-knife-blade-material.jpg)">'
    html = html.replace(old_vg10, new_vg10)
    
    # Fix nitrov -> AUS-8 image
    old_nitrov = '<div class="steel-card" id="dd-nitrov">\n<div class="steel-card-header">'
    new_nitrov = '<div class="steel-card" id="dd-nitrov">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2022/05/What-to-expect-from-AUS-8-as-a-knife-blade-material.jpg)">'
    html = html.replace(old_nitrov, new_nitrov)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'{fname}: fixed vg10/nitrov')
