with open('pillar-damascus-layered.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacements = {
    '<div class="steel-card" id="dd-sanmai">\n<div class="steel-card-header">':
        '<div class="steel-card" id="dd-sanmai">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2022/05/What-Is-Damascus-Steel-Origin-Composition-and-Properties.jpg)">',
    '<div class="steel-card" id="dd-damascusclad">\n<div class="steel-card-header">':
        '<div class="steel-card" id="dd-damascusclad">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2022/05/Damascus-steel-kitchen-knives.jpg)">',
    '<div class="steel-card" id="dd-patternwelded">\n<div class="steel-card-header">':
        '<div class="steel-card" id="dd-patternwelded">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2022/05/Damascus-Patterns-Different-Designs-and-Types.jpg)">',
    '<div class="steel-card" id="dd-damasteel">\n<div class="steel-card-header">':
        '<div class="steel-card" id="dd-damasteel">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2024/03/Damasteel-vs-Damascus-steel.jpg)">',
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open('pillar-damascus-layered.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed damascus headers')
