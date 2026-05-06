import re, glob, os

with open("bundle.css", "r", encoding="utf-8") as f:
    css = f.read()

# Extract @media blocks first
media_blocks = []
def extract_media(m):
    media_blocks.append(m.group(0))
    return ""
css_no_media = re.sub(r"@media[^{]+\{([^}]|\}[^@])*\}\}", extract_media, css)
# If the above regex fails, try simpler
if not media_blocks:
    # Simple regex for @media ... { ... }
    for m in re.finditer(r"(@media[^{]+\{[^}]*(?:\}[^}]*)*\})", css):
        media_blocks.append(m.group(1))
        css_no_media = css_no_media.replace(m.group(1), "")

# Parse normal rules
rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css_no_media)

def classify(sel):
    s = sel.lower()
    if s.startswith(":root"): return "core"
    if s in ("*", "body", "html") or s.startswith("body "): return "core"
    if any(k in s for k in [".mt-", ".mb-", ".w-", ".text-secondary", ".text-center", ".text-left", ".text-xs", ".text-sm", ".text-base", ".text-muted", ".content-max", ".section-title-center", ".lead-center"]):
        return "core"
    if any(k in s for k in [".container", ".two-col", ".nav-grid", ".vs-grid", ".metric-grid", ".product-grid", ".data-grid", ".family-list", ".table-wrap"]):
        return "core"
    if any(re.search(r"\b" + t + r"\b", s) for t in ["h1","h2","h3","h4","h5","h6","p","a"]) or ".hero-lead" in s:
        return "core"
    if any(k in s for k in [".btn", ".tag", ".tier-tags", ".family-", ".vs-", ".product-", ".nav-card", ".metric-", ".progress-", ".d-bar", ".d-row", ".filter-btn", ".table-controls", ".toc-wrap", ".content-note", ".key-takeaway"]):
        return "ui"
    if any(re.search(r"\b" + t + r"\b", s) for t in ["table","th","td","thead","tbody","tr"]) and not s.startswith("."):
        return "ui"
    if any(k in s for k in [".steel-", ".chip-row", ".b2b-", ".oem-", ".finder-", ".result-item", ".faq-", ".print-", ".cta-", "footer", "header", ".stats-strip", ".stat-", ".hero-", ".crumbs", ".pillar-kicker", ".link-para"]):
        return "content"
    return "ui"

files = {"core": [], "ui": [], "content": [], "responsive": []}

for sel, decl in rules:
    sel = sel.strip()
    decl = decl.strip()
    if not sel or not decl:
        continue
    files[classify(sel)].append(f"{sel} {{ {decl} }}")

# Add media blocks to responsive
for block in media_blocks:
    files["responsive"].append(block)

# Write files
mapping = {
    "core": "nichehub-core.css",
    "ui": "nichehub-ui.css",
    "content": "nichehub-content.css",
    "responsive": "nichehub-responsive.css"
}

for key, fname in mapping.items():
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(files[key]))
    print(f"[{key.upper()}] {fname}: {len(files[key])} rules")

# Update HTML
for html in sorted(glob.glob("*.html")):
    with open(html, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'\s*<link rel="stylesheet" href="[^"]*\.css">\s*', '\n', content)
    links = '  <link rel="stylesheet" href="nichehub-core.css">\n  <link rel="stylesheet" href="nichehub-ui.css">\n  <link rel="stylesheet" href="nichehub-content.css">\n  <link rel="stylesheet" href="nichehub-responsive.css">\n'
    content = content.replace("</head>", links + "</head>")
    with open(html, "w", encoding="utf-8") as f:
        f.write(content)

# Backup bundle.css
os.makedirs("_css_backup", exist_ok=True)
if os.path.exists("bundle.css"):
    os.replace("bundle.css", os.path.join("_css_backup", "bundle.css"))

print("[DONE]")
