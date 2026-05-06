import glob

def extract_div_block(html, start_pos):
    """Extract a div block starting at start_pos by matching nested divs."""
    open_tag_end = html.find('>', start_pos) + 1
    depth = 1
    pos = open_tag_end
    while depth > 0 and pos < len(html):
        next_open = html.find('<div', pos)
        next_close = html.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return html[start_pos:pos]

def find_tag_start(html, class_name, search_pos=0):
    """Find the start of <div class=\"class_name\">."""
    cls_idx = html.find(f'class="{class_name}"', search_pos)
    if cls_idx == -1:
        return -1
    return html.rfind('<div', 0, cls_idx)

def process_file(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    search_pos = 0
    while True:
        # Find next steel-product-right
        prod_cls_idx = html.find('class="steel-product-right"', search_pos)
        if prod_cls_idx == -1:
            break
        
        prod_start = find_tag_start(html, 'steel-product-right', prod_cls_idx - 50)
        if prod_start == -1:
            search_pos = prod_cls_idx + 1
            continue
        
        # Extract the product block
        prod_block = extract_div_block(html, prod_start)
        prod_end = prod_start + len(prod_block)
        
        # Check if this is inside a steel-main-right
        right_cls_idx = html.rfind('class="steel-main-right"', 0, prod_start)
        if right_cls_idx == -1:
            search_pos = prod_end
            continue
        
        right_start = find_tag_start(html, 'steel-main-right', right_cls_idx - 50)
        if right_start == -1 or right_start > prod_start:
            search_pos = prod_end
            continue
        
        # Verify the steel-main-right contains this product block
        right_block = extract_div_block(html, right_start)
        right_end = right_start + len(right_block)
        if prod_start < right_start or prod_end > right_end:
            search_pos = prod_end
            continue
        
        # Find the corresponding steel-main-left before this steel-main-right
        left_cls_idx = html.rfind('class="steel-main-left"', 0, right_start)
        if left_cls_idx == -1:
            search_pos = prod_end
            continue
        
        left_start = find_tag_start(html, 'steel-main-left', left_cls_idx - 50)
        if left_start == -1:
            search_pos = prod_end
            continue
        
        # Get the left block to find its closing tag position
        left_block = extract_div_block(html, left_start)
        left_end = left_start + len(left_block)
        
        # The closing </div> of steel-main-left is at left_end - 6
        left_close_tag_start = left_end - 6  # position of </div>
        
        # Remove product block from steel-main-right (with surrounding whitespace)
        before = html[:prod_start].rstrip()
        after = html[prod_end:].lstrip()
        html = before + '\n      ' + after
        
        # Recalculate left_close_tag_start since we removed content before it
        removed_len = prod_end - prod_start
        left_close_tag_start -= (prod_end - len(after) - len(before) - len('\n      '))
        # Actually simpler: just redo the extraction on the modified html
        # But that would be expensive. Let's use string replacement instead.
        
        break  # Only process one per iteration, then restart
    
    # Actually the above approach with mutating html and recalculating positions is fragile.
    # Let's use a simpler approach: collect all blocks, then rebuild.
    return html

# Test approach: do it in two passes
# Pass 1: collect all (left_start, left_close, prod_block) tuples
# Pass 2: rebuild html by inserting prod blocks at left_close positions

def process_file_v2(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    moves = []
    search_pos = 0
    while True:
        prod_cls_idx = html.find('class="steel-product-right"', search_pos)
        if prod_cls_idx == -1:
            break
        
        prod_start = find_tag_start(html, 'steel-product-right', prod_cls_idx - 50)
        if prod_start == -1:
            search_pos = prod_cls_idx + 1
            continue
        
        prod_block = extract_div_block(html, prod_start)
        prod_end = prod_start + len(prod_block)
        
        # Check if inside steel-main-right
        right_cls_idx = html.rfind('class="steel-main-right"', 0, prod_start)
        if right_cls_idx == -1:
            search_pos = prod_end
            continue
        
        right_start = find_tag_start(html, 'steel-main-right', right_cls_idx - 50)
        if right_start == -1 or right_start > prod_start:
            search_pos = prod_end
            continue
        
        right_block = extract_div_block(html, right_start)
        right_end = right_start + len(right_block)
        if prod_start < right_start or prod_end > right_end:
            search_pos = prod_end
            continue
        
        # Find corresponding steel-main-left
        left_cls_idx = html.rfind('class="steel-main-left"', 0, right_start)
        if left_cls_idx == -1:
            search_pos = prod_end
            continue
        
        left_start = find_tag_start(html, 'steel-main-left', left_cls_idx - 50)
        if left_start == -1:
            search_pos = prod_end
            continue
        
        left_block = extract_div_block(html, left_start)
        left_end = left_start + len(left_block)
        
        moves.append((prod_start, prod_end, left_end - 6, prod_block))
        search_pos = prod_end
    
    # Apply moves in reverse order to preserve positions
    for prod_start, prod_end, left_insert_pos, prod_block in reversed(moves):
        # Remove from right
        before = html[:prod_start].rstrip()
        after = html[prod_end:].lstrip()
        html = before + '\n      ' + after
        
        # Recalculate insert position
        if left_insert_pos > prod_end:
            left_insert_pos -= (prod_end - prod_start)
        elif left_insert_pos > prod_start:
            left_insert_pos = prod_start
        
        # Insert at left (before </div>)
        # Add some indentation
        indented_block = '\n        ' + prod_block.replace('\n', '\n        ') + '\n      '
        html = html[:left_insert_pos] + indented_block + html[left_insert_pos:]
    
    return html

files = [
    'pillar-carbon-steels.html',
    'pillar-damascus-layered.html',
    'pillar-powder-metallurgy-steels.html',
    'pillar-stainless-steels.html',
    'pillar-tool-semi-stainless.html'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        original = f.read()
    
    new_html = process_file_v2(fname)
    
    orig_count = original.count('steel-product-right')
    new_count = new_html.count('steel-product-right')
    
    if new_count == orig_count:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'{fname}: moved {new_count} blocks')
    else:
        print(f'{fname}: ERROR ({orig_count} -> {new_count})')
