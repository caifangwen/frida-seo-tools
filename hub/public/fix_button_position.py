import re
import glob

def extract_block(html, start_pos):
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
    return html[start_pos:pos], pos

def move_product_right_to_left(html):
    """Move steel-product-right blocks from steel-main-right to steel-main-left."""
    # Process each steel-card section
    result = html
    offset = 0
    
    # Find all steel-main-right sections that contain steel-product-right
    search_pos = 0
    while True:
        right_idx = result.find('class="steel-main-right"', search_pos)
        if right_idx == -1:
            break
        
        # Find the start of steel-main-right div
        right_start = result.rfind('<div', 0, right_idx)
        if right_start == -1:
            search_pos = right_idx + 1
            continue
        
        # Find steel-product-right inside this steel-main-right
        prod_idx = result.find('class="steel-product-right"', right_start)
        if prod_idx == -1:
            search_pos = right_idx + 1
            continue
        
        # Check if this steel-product-right is inside the current steel-main-right
        # Find the closing of steel-main-right
        right_tag_end = result.find('>', right_start) + 1
        right_close = result.find('</div>', right_tag_end)
        if prod_idx > right_close:
            search_pos = right_idx + 1
            continue
        
        # Extract the steel-product-right block
        prod_start = result.rfind('<div', right_start, prod_idx)
        prod_block, prod_end = extract_block(result, prod_start)
        
        # Find the matching steel-main-left before this steel-main-right
        left_idx = result.rfind('class="steel-main-left"', 0, right_start)
        if left_idx == -1:
            search_pos = right_idx + 1
            continue
        
        left_start = result.rfind('<div', 0, left_idx)
        left_tag_end = result.find('>', left_start) + 1
        left_close = result.find('</div>', left_tag_end)
        # Make sure we find the correct closing div for steel-main-left
        # by checking nested divs
        temp_pos = left_tag_end
        depth = 1
        while depth > 0 and temp_pos < len(result):
            next_open = result.find('<div', temp_pos)
            next_close = result.find('</div>', temp_pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close and next_open < right_start:
                depth += 1
                temp_pos = next_open + 4
            else:
                depth -= 1
                temp_pos = next_close + 6
        left_close = temp_pos - 6  # Back to </div>
        
        # Remove steel-product-right from steel-main-right
        # Find the content before and after prod_block within steel-main-right
        before_prod = result[right_tag_end:prod_start]
        after_prod = result[prod_end:right_close]
        
        # Clean up extra whitespace
        before_prod = before_prod.rstrip()
        after_prod = after_prod.lstrip()
        
        # Rebuild steel-main-right without steel-product-right
        new_right = result[right_start:right_tag_end] + before_prod + '\n      ' + result[right_close:right_close+6]
        
        # Insert steel-product-right before steel-main-left closing
        new_left = result[left_start:left_close] + '\n        ' + prod_block + '\n      ' + result[left_close:left_close+6]
        
        # Replace in result
        result = result[:left_start] + new_left + result[left_close+6:right_start] + new_right + result[right_close+6:]
        
        search_pos = left_start + len(new_left)
    
    return result

# Process all 5 pillar steel family pages
files = [
    'pillar-carbon-steels.html',
    'pillar-damascus-layered.html',
    'pillar-powder-metallurgy-steels.html',
    'pillar-stainless-steels.html',
    'pillar-tool-semi-stainless.html'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original_count = html.count('steel-product-right')
    new_html = move_product_right_to_left(html)
    new_count = new_html.count('steel-product-right')
    
    if new_count == original_count:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'{fname}: moved {new_count} blocks')
    else:
        print(f'{fname}: ERROR count mismatch ({original_count} -> {new_count})')
