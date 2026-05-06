with open('pillar-tool-semi-stainless.html', 'r', encoding='utf-8') as f:
    html = f.read()

d2_img = 'https://img.leeknives.com/wp-content/uploads/2022/08/D2-Steel-Review-as-a-Knife-Material.jpg'
a2_img = 'https://img.leeknives.com/wp-content/uploads/2023/12/Understanding-What-Is-the-A2-Tool-Steel.jpg'
m390_img = 'https://img.leeknives.com/wp-content/uploads/2023/04/Why-M390-Steel-Is-Taking-the-Knife-Making-World-by-Storm.jpg'

replacements = {
    '<div class="steel-card" id="dd-12c27">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-12c27">\n<div class="steel-card-header" style="background-image:url({d2_img})">',
    '<div class="steel-card" id="dd-niolox">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-niolox">\n<div class="steel-card-header" style="background-image:url({a2_img})">',
    '<div class="steel-card" id="dd-cpm3v">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-cpm3v">\n<div class="steel-card-header" style="background-image:url({m390_img})">',
    '<div class="steel-card" id="dd-cpmm4">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-cpmm4">\n<div class="steel-card-header" style="background-image:url({m390_img})">',
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open('pillar-tool-semi-stainless.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed tool headers')
