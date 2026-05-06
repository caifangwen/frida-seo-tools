import re, glob, os

def parse_css(css):
    rules = []
    i = 0
    n = len(css)
    while i < n:
        while i < n and css[i].isspace():
            i += 1
        if i >= n:
            break
        if css[i] == '@':
            brace = css.find('{', i)
            if brace == -1: break
            selector = css[i:brace].strip()
            depth = 0
            j = brace
            while j < n:
                c = css[j]
                if c in '"\'':
                    q = c
                    j += 1
                    while j < n and css[j] != q:
                        if css[j] == '\\': j += 2
                        else: j += 1
                    j += 1
                elif c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        break
                else:
                    j += 1
            block = css[brace+1:j]
            inner_rules = []
            k = 0
            m = len(block)
            while k < m:
                while k < m and block[k].isspace():
                    k += 1
                if k >= m: break
                inner_brace = block.find('{', k)
                if inner_brace == -1: break
                inner_sel = block[k:inner_brace].strip()
                inner_brace_end = block.find('}', inner_brace)
                if inner_brace_end == -1: break
                inner_decl = block[inner_brace+1:inner_brace_end].strip()
                inner_rules.append((inner_sel, inner_decl))
                k = inner_brace_end + 1
            rules.append(('media', selector, inner_rules))
            i = j + 1
        else:
            brace = css.find('{', i)
            if brace == -1: break
            selector = css[i:brace].strip()
            brace_end = css.find('}', brace)
            if brace_end == -1: break
            declarations = css[brace+1:brace_end].strip()
            rules.append(('rule', selector, declarations))
            i = brace_end + 1
    return rules

def classify(selector):
    s = selector.lower()
    def has_tag(tag):
        return bool(re.search(r'\b' + re.escape(tag) + r'\b', s))
    if s.startswith(':root'):
        return 'Design Tokens'
    if s in ('*', 'body', 'html') or s.startswith('body '):
        return 'Reset & Base'
    if any(k in s for k in ['.mt-', '.mb-', '.w-', '.text-secondary', '.text-center', '.text-left', '.text-xs', '.text-sm', '.text-base', '.text-muted', '.content-max', '.section-title-center', '.lead-center']):
        return 'Utility Classes'
    if any(k in s for k in ['.finder-', '.result-item', '.finder-cta']):
        return 'Steel Finder'
    if '.faq-' in s:
        return 'FAQ'
    if '.oem-' in s:
        return 'OEM Notes'
    if '.print-' in s:
        return 'Print Components'
    if any(k in s for k in ['.steel-', '.chip-row', '.b2b-', '.steel-product']):
        return 'Steel Deep-Dive Cards'
    if '.metric-' in s:
        return 'Metric Cards'
    if any(k in s for k in ['.progress-', '.d-bar', '.d-row']):
        return 'Progress Bars'
    if '.product-' in s:
        return 'Product Cards'
    if '.vs-' in s:
        return 'VS Comparison Cards'
    if '.data-' in s:
        return 'Data Grid'
    if any(k in s for k in ['.nav-card', '.nav-grid']):
        return 'Navigation Cards'
    if '.filter-' in s:
        return 'Filters'
    if any(k in s for k in ['.table-controls', '.table-wrap table']):
        return 'Table Components'
    if has_tag('table') and not s.startswith('.'):
        return 'Tables'
    if '.tag' in s or '.tier-tags' in s:
        return 'Tags & Badges'
    if '.family-' in s:
        return 'Family Row Cards'
    if any(k in s for k in ['.hero-', '.stats-strip', '.stat-', '.crumbs', '.pillar-kicker']):
        return 'Header & Hero Stats'
    if any(k in s for k in ['.section-title', '.section-sub', '.intro-narrative', '.narrative-content']):
        return 'Section Layout'
    if '.link-para' in s:
        return 'Links'
    if '.cta-' in s:
        return 'CTAs'
    if 'footer' in s:
        return 'Footer'
    if s.startswith('header') or ' header' in s:
        return 'Header'
    if '.btn' in s:
        return 'Buttons'
    if any(k in s for k in ['.content-note', '.key-takeaway', '.toc-wrap']):
        return 'Content Helpers'
    if any(k in s for k in ['.container', '.two-col', '.nav-grid', '.vs-grid', '.metric-grid', '.product-grid', '.data-grid', '.family-list']):
        return 'Layout & Grid'
    if any(has_tag(t) for t in ['h1','h2','h3','h4','h5','h6','p','a']) or '.hero-lead' in s:
        return 'Typography'
    return 'General Components'

def format_declarations(decl):
    props = [p.strip() for p in decl.split(';') if p.strip()]
    lines = []
    for p in props:
        if ':' in p and not p.split(':', 1)[1].startswith(' '):
            p = p.replace(':', ': ', 1)
        lines.append('  ' + p + ';')
    return '\n'.join(lines)

def format_selector(sel):
    parts = [s.strip() for s in sel.split(',')]
    if len(parts) == 1:
        return parts[0]
    return ',\n'.join(parts)

with open('bundle.css', 'r', encoding='utf-8') as f:
    css = f.read()

rules = parse_css(css)
groups = {}
media_rules = []

for rule in rules:
    if rule[0] == 'rule':
        _, selector, decl = rule
        group = classify(selector)
        groups.setdefault(group, []).append((selector, decl))
    elif rule[0] == 'media':
        _, selector, inner = rule
        media_rules.append((selector, inner))

order = [
    'Design Tokens',
    'Reset & Base',
    'Utility Classes',
    'Layout & Grid',
    'Typography',
    'Header & Hero Stats',
    'Buttons',
    'Links',
    'Tags & Badges',
    'Family Row Cards',
    'VS Comparison Cards',
    'Product Cards',
    'Navigation Cards',
    'Metric Cards',
    'Progress Bars',
    'Steel Finder',
    'Data Grid',
    'Steel Deep-Dive Cards',
    'OEM Notes',
    'Table Components',
    'Tables',
    'Filters',
    'Table of Contents',
    'Content Helpers',
    'Section Layout',
    'FAQ',
    'CTAs',
    'Footer',
    'Header',
    'Print Components',
    'General Components',
]

output_lines = []
output_lines.append('/* =============================================================================')
output_lines.append('   NicheHub Stylesheet')
output_lines.append('   Source: leeknives.com knowledge hub + pillar pages')
output_lines.append('   Generated: merged, deduplicated, and formatted from all page-level CSS')
output_lines.append('   ============================================================================= */')
output_lines.append('')

for group in order:
    if group not in groups or not groups[group]:
        continue
    output_lines.append('/* -----------------------------------------------------------------------------')
    output_lines.append('   ' + group)
    output_lines.append('   ----------------------------------------------------------------------------- */')
    output_lines.append('')
    for selector, decl in groups[group]:
        sel_str = format_selector(selector)
        decl_str = format_declarations(decl)
        output_lines.append(sel_str + ' {')
        output_lines.append(decl_str)
        output_lines.append('}')
        output_lines.append('')

if media_rules:
    output_lines.append('/* -----------------------------------------------------------------------------')
    output_lines.append('   Responsive Breakpoints')
    output_lines.append('   ----------------------------------------------------------------------------- */')
    output_lines.append('')
    for selector, inner in media_rules:
        if 'print' in selector.lower():
            output_lines.append('/* --- Print Styles --- */')
        sel_str = format_selector(selector)
        output_lines.append(sel_str + ' {')
        for inner_sel, inner_decl in inner:
            inner_sel_str = '  ' + format_selector(inner_sel)
            inner_decl_str = format_declarations(inner_decl)
            inner_decl_str = '\n'.join('  ' + line for line in inner_decl_str.split('\n'))
            output_lines.append(inner_sel_str + ' {')
            output_lines.append(inner_decl_str)
            output_lines.append('  }')
        output_lines.append('}')
        output_lines.append('')

output = '\n'.join(output_lines)

with open('nichehub.css', 'w', encoding='utf-8') as f:
    f.write(output)

for html in sorted(glob.glob('*.html')):
    with open(html, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('bundle.css', 'nichehub.css')
    with open(html, 'w', encoding='utf-8') as f:
        f.write(content)

if os.path.exists('bundle.css'):
    os.remove('bundle.css')

print(f'[DONE] nichehub.css ({len(output)} bytes, {len(groups)} groups)')
