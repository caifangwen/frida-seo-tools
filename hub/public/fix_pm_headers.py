with open('pillar-powder-metallurgy-steels.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Use M390 as fallback for most PM steels
m390_img = 'https://img.leeknives.com/wp-content/uploads/2023/04/Why-M390-Steel-Is-Taking-the-Knife-Making-World-by-Storm.jpg'
sg2_img = 'https://img.leeknives.com/wp-content/uploads/2022/06/Review-of-SG2-Steel-as-a-Knife-Steel.jpg'

replacements = {
    '<div class="steel-card" id="dd-elmax">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-elmax">\n<div class="steel-card-header" style="background-image:url({m390_img})">',
    '<div class="steel-card" id="dd-s30v">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-s30v">\n<div class="steel-card-header" style="background-image:url({m390_img})">',
    '<div class="steel-card" id="dd-s90v">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-s90v">\n<div class="steel-card-header" style="background-image:url({m390_img})">',
    '<div class="steel-card" id="dd-cts204p">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-cts204p">\n<div class="steel-card-header" style="background-image:url({m390_img})">',
    '<div class="steel-card" id="dd-rwl34">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-rwl34">\n<div class="steel-card-header" style="background-image:url({sg2_img})">',
    '<div class="steel-card" id="dd-zdp189">\n<div class="steel-card-header">':
        f'<div class="steel-card" id="dd-zdp189">\n<div class="steel-card-header" style="background-image:url({sg2_img})">',
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open('pillar-powder-metallurgy-steels.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed PM headers')
