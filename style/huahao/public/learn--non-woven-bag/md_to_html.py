import re
import sys
import markdown
from pathlib import Path

def parse_frontmatter(text):
    meta = {}
    lines = text.split('\n')
    for line in lines[:10]:
        if line.startswith('**Meta Title**:'):
            meta['title'] = line.split(':', 1)[1].strip()
        elif line.startswith('**Meta Description**:'):
            meta['desc'] = line.split(':', 1)[1].strip()
        elif line.startswith('**URL**:'):
            meta['url'] = line.split(':', 1)[1].strip()
    return meta

def convert_md_to_html(md_path, html_path):
    text = Path(md_path).read_text(encoding='utf-8')
    meta = parse_frontmatter(text)
    
    # Remove frontmatter lines
    lines = text.split('\n')
    content_lines = []
    for line in lines:
        if line.startswith('**Meta') or line.startswith('**URL'):
            continue
        if line.strip() == '---':
            continue
        content_lines.append(line)
    content = '\n'.join(content_lines)
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    html_content = md.convert(content)
    
    # Apply Huahao component transformations
    html_content = apply_huahao_components(html_content)
    
    # Wrap in hh-post
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta.get('title', '')}</title>
<meta name="description" content="{meta.get('desc', '')}">
<link rel="stylesheet" href="/huahao-blog.css">
</head>
<body>
<div class="hh-post">
{html_content}
</div>
<script src="/huahao-blog.js"></script>
</body>
</html>'''
    
    Path(html_path).write_text(full_html, encoding='utf-8')
    print(f"Converted: {md_path} -> {html_path}")

def apply_huahao_components(html):
    # H1 -> hh-hero (first h1 only)
    html = re.sub(
        r'<h1[^>]*>(.*?)</h1>',
        lambda m: f'<div class="hh-hero"><h1>{m.group(1)}</h1></div>',
        html, count=1
    )
    
    # H2 -> hh-section-header with auto-numbering (skip Introduction)
    h2_count = [0]
    def h2_repl(m):
        title = m.group(1).strip()
        h2_count[0] += 1
        num = f"{h2_count[0]:02d}"
        
        # Skip numbering for Introduction/Conclusion/Suggested Images
        if title.lower() in ('introduction', 'conclusion', 'suggested images', 'related resources', 'downloadable resources'):
            return f'<h2 class="hh-section-title-plain">{title}</h2>'
        
        tag = ""
        if ':' in title:
            parts = title.split(':', 1)
            tag_text = parts[0].strip()
            title = parts[1].strip()
            tag = f'<span class="hh-section-tag">{tag_text}</span>'
        
        return f'''<div class="hh-section-header">
  <div class="hh-section-num">{num}</div>
  <div>
    {tag}
    <h2 class="hh-section-title">{title}</h2>
  </div>
</div>'''
    
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', h2_repl, html)
    
    # H3 -> styled h3
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'<h3 class="hh-h3">\1</h3>', html)
    
    # Tables -> hh-table-wrap + hh-table
    def table_repl(m):
        table_html = m.group(1)
        table_html = table_html.replace('<table>', '<table class="hh-table">')
        # Try to find a caption from preceding text
        return f'<div class="hh-table-wrap">{table_html}<span class="hh-table-caption">Reference Data</span></div>'
    
    html = re.sub(r'(<table>.*?</table>)', table_repl, html, flags=re.DOTALL)
    
    # Blockquote -> hh-quote
    html = re.sub(
        r'<blockquote>(.*?)</blockquote>',
        r'<blockquote class="hh-quote">\1</blockquote>',
        html, flags=re.DOTALL
    )
    
    # Links ending in .md -> remove .md
    html = re.sub(r'href="([^"]*)\.md"', r'href="\1"', html)
    
    # Strong paragraph tips -> hh-box variants
    def tip_repl(m):
        marker = m.group(1)
        text = m.group(2)
        box_class = "info"
        if marker in ('⚠️', '❌', '🚫'):
            box_class = "warn"
        elif marker in ('💡', '✅', '✔️', '🔹'):
            box_class = "tip"
        return f'<div class="hh-box-{box_class}"><p>{text}</p></div>'
    
    html = re.sub(
        r'<p>(⚠️|✅|❌|💡|📝|🔹|✔️|🚫)\s*(.*?)</p>',
        tip_repl,
        html
    )
    
    return html

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python md_to_html.py <input.md> <output.html>")
        sys.exit(1)
    convert_md_to_html(sys.argv[1], sys.argv[2])
