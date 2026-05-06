import re, os

headers = {
    "nichehub-core.css": [
        "/* =============================================================================",
        "   NicheHub Core",
        "   Design tokens, CSS reset, base typography, layout grid, and utility classes.
        "   Loaded on every page.",
        "   ============================================================================= */",
        ""
    ],
    "nichehub-ui.css": [
        "/* =============================================================================",
        "   NicheHub UI Components",
        "   Buttons, tags, badges, tables, progress bars, filters, TOC, and content helpers.",
        "   Loaded on every page.",
        "   ============================================================================= */",
        ""
    ],
    "nichehub-content.css": [
        "/* =============================================================================",
        "   NicheHub Content Blocks",
        "   Header/Hero stats, footer CTA, steel deep-dive cards, product cards, FAQ,",
        "   steel finder, data grids, and OEM notes.",
        "   Loaded on every page.",
        "   ============================================================================= */",
        ""
    ],
    "nichehub-responsive.css": [
        "/* =============================================================================",
        "   NicheHub Responsive & Print",
        "   Breakpoint overrides and print-specific styles.",
        "   Loaded on every page.",
        "   ============================================================================= */",
        ""
    ]
}

def pretty(css_text):
    # Parse rules including @media inner rules
    out = []
    i = 0
    n = len(css_text)
    while i < n:
        while i < n and css_text[i].isspace():
            i += 1
        if i >= n:
            break
        if css_text[i] == '@':
            brace = css_text.find('{', i)
            if brace == -1: break
            selector = css_text[i:brace].strip()
            depth = 0
            j = brace
            while j < n:
                c = css_text[j]
                if c in '"\'':
                    q = c
                    j += 1
                    while j < n and css_text[j] != q:
                        if css_text[j] == '\\': j += 2
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
            block = css_text[brace+1:j]
            inner = []
            k = 0
            m = len(block)
            while k < m:
                while k < m and block[k].isspace():
                    k += 1
                if k >= m: break
                ib = block.find('{', k)
                if ib == -1: break
                isel = block[k:ib].strip()
                ie = block.find('}', ib)
                if ie == -1: break
                idecl = block[ib+1:ie].strip()
                inner.append((isel, idecl))
                k = ie + 1
            out.append("/* --- " + selector + " --- */")
            out.append(selector + " {")
            for isel, idecl in inner:
                decl_lines = []
                for prop in [p.strip() for p in idecl.split(';') if p.strip()]:
                    if ':' in prop and not prop.split(':', 1)[1].startswith(' '):
                        prop = prop.replace(':', ': ', 1)
                    decl_lines.append("  " + prop + ";")
                if len(isel) > 60 or ',' in isel:
                    out.append("  " + isel.replace(', ', ',\n  ') + " {")
                else:
                    out.append("  " + isel + " {")
                out.extend(decl_lines)
                out.append("  }")
            out.append("}")
            out.append("")
            i = j + 1
        else:
            brace = css_text.find('{', i)
            if brace == -1: break
            selector = css_text[i:brace].strip()
            brace_end = css_text.find('}', brace)
            if brace_end == -1: break
            decl = css_text[brace+1:brace_end].strip()
            if len(selector) > 60 or ',' in selector:
                out.append(selector.replace(', ', ',\n') + " {")
            else:
                out.append(selector + " {")
            for prop in [p.strip() for p in decl.split(';') if p.strip()]:
                if ':' in prop and not prop.split(':', 1)[1].startswith(' '):
                    prop = prop.replace(':', ': ', 1)
                out.append("  " + prop + ";")
            out.append("}")
            out.append("")
            i = brace_end + 1
    return "\n".join(out)

for fname, hdr in headers.items():
    if not os.path.exists(fname):
        continue
    with open(fname, "r", encoding="utf-8") as f:
        raw = f.read()
    formatted = pretty(raw)
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(hdr) + "\n" + formatted)
    print(f"[FORMATTED] {fname}")

print("[DONE]")
