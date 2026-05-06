with open('pillar-carbon-steels.html', 'r', encoding='utf-8') as f:
    html = f.read()

old1 = '<div class="steel-card" id="dd-5160">\n<div class="steel-card-header">'
new1 = '<div class="steel-card" id="dd-5160">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2023/12/What-Is-52100-Steel-Understanding-Its-Properties-and-Uses.jpg)">'

old2 = '<div class="steel-card" id="dd-o1">\n<div class="steel-card-header">'
new2 = '<div class="steel-card" id="dd-o1">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2023/12/Understanding-What-Is-the-A2-Tool-Steel.jpg)">'

old3 = '<div class="steel-card" id="dd-15n20">\n<div class="steel-card-header">'
new3 = '<div class="steel-card" id="dd-15n20">\n<div class="steel-card-header" style="background-image:url(https://img.leeknives.com/wp-content/uploads/2022/05/What-Is-Damascus-Steel-Origin-Composition-and-Properties.jpg)">'

html = html.replace(old1, new1)
html = html.replace(old2, new2)
html = html.replace(old3, new3)

with open('pillar-carbon-steels.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed remaining 3 headers')
