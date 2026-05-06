import re

files = {
    'pillar-how-kitchen-knives-are-made.html': {
        'exclude': 'How Kitchen Knives Are Made',
        'links': [
            ('Types of Kitchen Knives', 'Japanese, Western, cleavers, and specialty profiles organized by use case.', 'pillar-types-of-kitchen-knives.html', 'Knife Types Pillar'),
            ('How to Care for Knives', 'Sharpening systems, storage methods, and routine maintenance workflows.', 'pillar-how-to-care-for-knives.html', 'Care Guide Pillar'),
            ('Pocket & Outdoor Knives', 'Folding mechanisms, fixed-blade outdoor knives, tactical profiles, and blade shapes.', 'pillar-pocket-outdoor-knives.html', 'Outdoor Knives Pillar'),
        ]
    },
    'pillar-types-of-kitchen-knives.html': {
        'exclude': 'Types of Kitchen Knives',
        'links': [
            ('How Kitchen Knives Are Made', 'Forging, heat treatment, grinding, handles, finishing, and QC checkpoints.', 'pillar-how-kitchen-knives-are-made.html', 'Manufacturing Pillar'),
            ('How to Care for Knives', 'Sharpening systems, storage methods, and routine maintenance workflows.', 'pillar-how-to-care-for-knives.html', 'Care Guide Pillar'),
            ('Pocket & Outdoor Knives', 'Folding mechanisms, fixed-blade outdoor knives, tactical profiles, and blade shapes.', 'pillar-pocket-outdoor-knives.html', 'Outdoor Knives Pillar'),
        ]
    },
    'pillar-how-to-care-for-knives.html': {
        'exclude': 'How to Care for Knives',
        'links': [
            ('How Kitchen Knives Are Made', 'Forging, heat treatment, grinding, handles, finishing, and QC checkpoints.', 'pillar-how-kitchen-knives-are-made.html', 'Manufacturing Pillar'),
            ('Types of Kitchen Knives', 'Japanese, Western, cleavers, and specialty profiles organized by use case.', 'pillar-types-of-kitchen-knives.html', 'Knife Types Pillar'),
            ('Pocket & Outdoor Knives', 'Folding mechanisms, fixed-blade outdoor knives, tactical profiles, and blade shapes.', 'pillar-pocket-outdoor-knives.html', 'Outdoor Knives Pillar'),
        ]
    },
    'pillar-pocket-outdoor-knives.html': {
        'exclude': 'Pocket & Outdoor Knives',
        'links': [
            ('How Kitchen Knives Are Made', 'Forging, heat treatment, grinding, handles, finishing, and QC checkpoints.', 'pillar-how-kitchen-knives-are-made.html', 'Manufacturing Pillar'),
            ('Types of Kitchen Knives', 'Japanese, Western, cleavers, and specialty profiles organized by use case.', 'pillar-types-of-kitchen-knives.html', 'Knife Types Pillar'),
            ('How to Care for Knives', 'Sharpening systems, storage methods, and routine maintenance workflows.', 'pillar-how-to-care-for-knives.html', 'Care Guide Pillar'),
        ]
    },
}

for fname, cfg in files.items():
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = '''    <div class="nav-card">
      <h3>Back to Hub</h3>
      <p>Return to the full steel knowledge center with comparison tables and Steel Finder.</p>
      <a class="btn-text" href="hub.html">&#8592; Knife Steel Knowledge Center</a>
    </div>'''
    for title, desc, href, label in cfg['links']:
        cards += f'''
    <div class="nav-card">
      <h3>{title}</h3>
      <p>{desc}</p>
      <a class="btn-text" href="{href}">{label} &#8594;</a>
    </div>'''
    
    new_grid = f'  <div class="nav-grid">\n{cards}\n  </div>'
    
    pattern = r'(<h2 class="section-title" id="continue">Continue Learning</h2>\n)  <div class="nav-grid">.*?</div>\n\n</div>'
    replacement = r'\1' + new_grid + '\n\n</div>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f'{fname}: NO CHANGE')
    else:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'{fname}: UPDATED')
