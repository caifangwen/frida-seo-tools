#!/usr/bin/env python3
"""Convert all markdown files in the directory to HTML with huahao styling."""

import os
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Installing python-markdown...")
    os.system("pip install markdown -q")
    import markdown


def parse_frontmatter(text):
    """Extract YAML frontmatter from markdown text."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            # Simple line-by-line parsing
            fm = {}
            for line in fm_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    fm[key] = val
            return fm, body
    return {}, text


def extract_faq_qa(html_body):
    """Extract FAQ Q&A pairs from HTML for JSON-LD."""
    # Find FAQ section
    faq_match = re.search(r'<h2[^>]*>FAQ</h2>(.*)', html_body, re.DOTALL | re.IGNORECASE)
    if not faq_match:
        return []
    faq_html = faq_match.group(1)
    # Split by h3 tags
    h3_pattern = re.compile(r'<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|$)', re.DOTALL)
    qa_pairs = []
    for m in h3_pattern.finditer(faq_html):
        question = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        answer_html = m.group(2).strip()
        # Clean up answer
        answer_text = re.sub(r'<[^>]+>', ' ', answer_html).strip()
        answer_text = re.sub(r'\s+', ' ', answer_text)
        if question and answer_text:
            qa_pairs.append((question, answer_text))
    return qa_pairs


def convert_md_links(html):
    """Convert .md links to .html links."""
    # [text](file.md) -> [text](file.html)
    # [text](file.md#anchor) -> [text](file.html#anchor)
    html = re.sub(r'href="([^"]+)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', html)
    return html


def process_body_html(html):
    """Post-process markdown-generated HTML with huahao classes."""
    # Wrap tables
    html = re.sub(
        r'(<table[^>]*>.*?)</table>',
        r'<div class="hh-table-wrap">\1</table></div>',
        html,
        flags=re.DOTALL
    )

    # Wrap blockquotes in hh-box-info
    html = re.sub(
        r'<blockquote>(.*?)</blockquote>',
        r'<div class="hh-box-info">\1</div>',
        html,
        flags=re.DOTALL
    )

    # Convert H2s to section headers (auto-numbered)
    h2_count = [0]
    def h2_repl(m):
        h2_count[0] += 1
        num = f"{h2_count[0]:02d}"
        content = m.group(1)
        # Extract id if present
        id_match = re.match(r'<a id="([^"]+)"></a>', content)
        anchor = f'<a id="{id_match.group(1)}"></a>' if id_match else ''
        clean_content = re.sub(r'<a id="[^"]+"></a>', '', content).strip()
        return (
            f'\n  <div class="hh-section-header">\n'
            f'    <div class="hh-section-num">{num}</div>\n'
            f'    <div>\n'
            f'      <span class="hh-section-tag"></span>\n'
            f'      <h2 class="hh-section-title">{anchor}{clean_content}</h2>\n'
            f'    </div>\n'
            f'  </div>\n'
        )

    html = re.sub(r'<h2>(.*?)</h2>', h2_repl, html, flags=re.DOTALL)

    # Convert FAQ h3s to details/summary
    # Find FAQ section and transform h3s within it
    faq_section = re.search(r'(<div class="hh-section-header">.*?FAQ.*?</div>)(.*)', html, re.DOTALL | re.IGNORECASE)
    if faq_section:
        faq_start = faq_section.group(1)
        faq_rest = faq_section.group(2)
        # Find next hh-section-header or end
        next_section = re.search(r'(<div class="hh-section-header">)', faq_rest)
        if next_section:
            faq_content = faq_rest[:next_section.start()]
            after_faq = faq_rest[next_section.start():]
        else:
            faq_content = faq_rest
            after_faq = ''

        # Transform h3s in faq_content
        def faq_h3_repl(m):
            question = m.group(1).strip()
            return (
                f'\n  <details class="hh-faq-item">\n'
                f'    <summary class="hh-faq-q">{question}</summary>\n'
                f'    <div class="hh-faq-a">\n'
            )

        faq_content = re.sub(r'<h3>(.*?)</h3>\s*', faq_h3_repl, faq_content, flags=re.DOTALL)
        # Close details before next h3 or section
        faq_content = re.sub(
            r'(</div>\s*)(?=<details|$)',
            r'\1    </div>\n  </details>\n',
            faq_content,
            flags=re.DOTALL
        )
        # Close any remaining open details
        if '<details' in faq_content and faq_content.rstrip().endswith('</div>'):
            faq_content = faq_content.rstrip() + '\n    </div>\n  </details>\n'

        html = html[:faq_section.start()] + faq_start + faq_content + after_faq

    # Wrap lists in hh-checklist (but not inside tables or faq)
    # Simple approach: wrap all ul that aren't already inside something
    html = re.sub(
        r'(<ul>)(.*?)(</ul>)',
        r'<ul class="hh-checklist">\2\3',
        html,
        flags=re.DOTALL
    )

    # Remove paragraph tags inside li for cleaner checklist
    html = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'<li>\1</li>', html, flags=re.DOTALL)

    # Remove paragraph tags inside summary
    html = re.sub(r'<summary([^>]*)>\s*<p>(.*?)</p>\s*</summary>', r'<summary\1>\2</summary>', html, flags=re.DOTALL)

    return html


def build_html(filename, fm, body_html, qa_pairs):
    """Build final HTML document."""
    title = fm.get("title", "Canvas Bag Guide")
    description = fm.get("description", "")
    keywords = fm.get("keywords", "")
    date = fm.get("date", "2026-04-15")
    slug = filename.replace(".md", "").replace(".html", "")

    # Build FAQ schema
    faq_schema = ""
    if qa_pairs:
        entities = []
        for q, a in qa_pairs:
            entities.append(
                f"""      {{
        "@type": "Question",
        "name": {repr(q)},
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": {repr(a)}
        }}
      }}"""
            )
        faq_schema = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{','.join(entities)}
    ]
  }}
  </script>
"""

    # Extract h1 for hero
    h1_match = re.search(r'<h1>(.*?)</h1>', body_html, re.DOTALL)
    if h1_match:
        h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        body_html = body_html.replace(h1_match.group(0), '', 1)
    else:
        h1_text = title

    # Extract first paragraph for hero sub
    first_p_match = re.search(r'<p>(.*?)</p>', body_html, re.DOTALL)
    hero_sub = ""
    if first_p_match:
        hero_sub_raw = re.sub(r'<[^>]+>', '', first_p_match.group(1)).strip()
        hero_sub = hero_sub_raw[:200] + ("..." if len(hero_sub_raw) > 200 else "")

    # Related articles (all other html files in directory)
    related = ""

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="stylesheet" href="./huahao.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{description}",
    "datePublished": "{date}",
    "dateModified": "{date}",
    "author": {{
      "@type": "Organization",
      "name": "Canvas Bag Manufacturer"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Canvas Bag Manufacturer"
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "https://example.com/blog/{slug}"
    }}
  }}
  </script>
{faq_schema}</head>
<body>

<nav class="hh-nav">
  <a href="/" class="hh-logo">CanvasBag Manufacturer</a>
  <a href="/blog/" class="hh-nav-link">Blog</a>
</nav>

<article class="hh-post">

  <!-- HERO SECTION -->
  <div class="hh-hero">
    <span class="hh-hero-eyebrow">2026 Complete Guide</span>
    <h1>{h1_text}</h1>
    <p class="hh-hero-sub">{hero_sub}</p>
  </div>

  {body_html}

  <!-- CTA BANNER -->
  <div class="hh-cta">
    <span class="hh-cta-tag">Explore More</span>
    <h2>Ready to Choose the Right Canvas Bag?</h2>
    <p>Browse our comprehensive guides on canvas bag selection, customization, and wholesale sourcing—or contact our team for personalized recommendations.</p>
    <div class="hh-cta-btns">
      <a href="canvas-bag-complete-guide.html" class="hh-btn-primary">Complete Canvas Bag Guide</a>
      <a href="custom-canvas-bag-guide.html" class="hh-btn-outline">Explore Custom Options</a>
    </div>
  </div>

  <!-- RELATED ARTICLES -->
  <hr>
  <h3>Related Articles</h3>
  <ul class="hh-checklist">
    <li><a href="canvas-bag-complete-guide.html">Canvas Bag Complete Guide 2026</a></li>
    <li><a href="what-is-canvas-material.html">What Is Canvas Material?</a></li>
    <li><a href="custom-canvas-bag-guide.html">Custom Canvas Bag Guide</a></li>
    <li><a href="eco-friendly-canvas-bag.html">Eco Friendly Canvas Bag Guide</a></li>
    <li><a href="wholesale-canvas-bags.html">Wholesale Canvas Bags Buying Guide</a></li>
  </ul>

</article>

</body>
</html>
"""
    return html_out


def main():
    base_dir = Path("C:/Users/frida/Documents/seo-skill-main/style/huahao/public/learn--canvas-bag")
    md_files = sorted(base_dir.glob("*.md"))

    # Skip the outlines file
    skip = {"03-canvas-content-outlines.md"}

    for md_path in md_files:
        if md_path.name in skip:
            continue

        html_path = md_path.with_suffix(".html")

        text = md_path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        # Convert markdown to HTML
        md_converter = markdown.Markdown(extensions=["tables", "fenced_code"])
        body_html = md_converter.convert(body)

        # Post-process
        body_html = convert_md_links(body_html)
        body_html = process_body_html(body_html)

        # Extract FAQ for schema
        qa_pairs = extract_faq_qa(body_html)

        # Build final HTML
        final_html = build_html(md_path.name, fm, body_html, qa_pairs)

        html_path.write_text(final_html, encoding="utf-8")
        print(f"  Converted: {md_path.name} -> {html_path.name}")

    print("\nAll conversions complete!")


if __name__ == "__main__":
    main()
