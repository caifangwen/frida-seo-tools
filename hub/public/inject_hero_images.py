import re

hero_images = {
    'pillar-carbon-steels.html': 'https://img.leeknives.com/wp-content/uploads/2022/05/Japanese-High-Carbon-Steels-Aogami-vs-Shirogami.jpg',
    'pillar-stainless-steels.html': 'https://img.leeknives.com/wp-content/uploads/2022/05/What-is-stainless-steel.jpg',
    'pillar-tool-semi-stainless.html': 'https://img.leeknives.com/wp-content/uploads/2022/08/D2-Steel-Review-as-a-Knife-Material.jpg',
    'pillar-powder-metallurgy-steels.html': 'https://img.leeknives.com/wp-content/uploads/2023/04/Why-M390-Steel-Is-Taking-the-Knife-Making-World-by-Storm.jpg',
    'pillar-damascus-layered.html': 'https://img.leeknives.com/wp-content/uploads/2022/05/Origin-of-Damascus-steel.jpg',
}

for fname, img_url in hero_images.items():
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add background-image to <header> tag
    if '<header>' in html and 'background-image' not in html[html.find('<header'):html.find('<header')+200]:
        html = html.replace('<header>', '<header style="background-image:url(' + img_url + ')">')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'{fname}: hero image added')
    else:
        print(f'{fname}: skipped')
