import re

with open('pillar-tool-semi-stainless.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the old deep-dive blocks (D2/K110 merged, A2, O1)
# Using regex to handle Unicode smart quotes and em-dashes reliably
pattern = r'''  <!-- ── D2 / K110 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-d2">D2 / K110 Tool Steel</h2>
    <p class="deep-dive-lead">D2-class steels are used for strong wear resistance at attractive cost\. They are often called ["\u201c\u201d]semi-stainless["\u201c\u201d] because corrosion resistance is better than plain carbon but still below true stainless\.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>D2/K110 is a popular upgrade story in value-performance lines: noticeably longer working edge in abrasive tasks, strong market recognition in EDC/outdoor categories, and a relatively accessible material cost compared with premium PM programs\.</p>
        <p>It can also be attractive when you want a tougher ["\u201c\u201d]workhorse["\u201c\u201d] identity and can tolerate a bit more maintenance messaging\.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>The two most common problems are chipping complaints \(often geometry mismatch\) and corrosion complaints \(often marketing mismatch\)\. If you present it as ["\u201c\u201d]stainless,["\u201c\u201d] users will store it wet and then blame the steel\.</p>
        <p>Set a hardness ceiling and avoid over-thin edges\. In this category, the best-performing knives are usually the ones with slightly more edge support and consistent apex quality\.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1\.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>59[\u2013\-]61</td><td>Define a ceiling to protect toughness</td></tr>
          <tr><td>Corrosion positioning</td><td>Semi-stainless</td><td>Finish and care inserts reduce complaints</td></tr>
          <tr><td>Best fit</td><td>Outdoor / EDC</td><td>Wear-forward use cases</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ── A2 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-a2">A2 Tool Steel</h2>
    <p class="deep-dive-lead">A2 is often chosen when brands want a toughness-biased tool steel that still offers strong working-edge stability without chasing maximum wear resistance\.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>A2 is commonly positioned for impact-prone tasks where edge stability matters as much as retention\. If your users are likely to torque, chop, or cut through mixed materials, a toughness-biased grade can reduce negative ["\u201c\u201d]chipping["\u201c\u201d] reviews compared with wear-first choices\.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Because it is not stainless, corrosion expectations must be managed\. In kitchen use, A2 requires discipline: wipe-dry routines and appropriate storage\.</p>
        <p>Don[\u2019\']t oversell ["\u201c\u201d]high retention["\u201c\u201d] if you choose A2 primarily for toughness[\u2014\-]sell it as stable, reliable, and easy to maintain for its category\.</p>
      </div>
    </div>
  </div>

  <!-- ── O1 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-o1">O1 Tool Steel</h2>
    <p class="deep-dive-lead">O1 is a classic tool steel often selected for ["\u201c\u201d]heritage["\u201c\u201d] and ["\u201c\u201d]easy sharpening["\u201c\u201d] positioning\. It is not stainless and should be treated as a maintenance-requiring steel in real kitchens\.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>O1 appeals in craft-oriented lines because it communicates tradition and practicality\. Users often appreciate the sharpening feel and the predictable edge behavior[\u2014\-]especially when the brand teaches basic care and maintenance routines\.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>The biggest risk is audience mismatch\. If a product is sold into low-maintenance mainstream channels, O1 can generate rust complaints quickly\. For success, align distribution with an audience willing to care for the blade\.</p>
      </div>
    </div>

    <div class="content-note" style="margin-top:1\.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0\.4rem 0 0;">For tool steels, a simple ["\u201c\u201d]care insert["\u201c\u201d] is not just marketing[\u2014\-]it[\u2019\']s warranty prevention\. The brands with the lowest complaint rates standardize the same care language across listing pages, packaging, and retailer training\.</p>
    </div>
  </div>'''

match = re.search(pattern, content, re.DOTALL)
if not match:
    print('Pattern not found, trying simpler approach...')
    # Fallback: find by line markers
    start_marker = '  <!-- ── D2 / K110 ── -->'
    end_marker = '  </div>\n\n  <style>'
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1:
        print('Start marker not found')
        exit(1)
    if end_idx == -1:
        print('End marker not found')
        exit(1)
    print(f'Found start at {start_idx}, end at {end_idx}')
    old_section = content[start_idx:end_idx]
else:
    old_section = match.group(0)
    print('Regex matched successfully')

new_section = '''  <!-- ── D2 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-d2">D2 Tool Steel</h2>
    <p class="deep-dive-lead">D2 is a high-carbon, high-chromium tool steel (AISI D2 / DIN 1.2379) with ~1.5% carbon and ~12% chromium — just below the 13% threshold typically required for true stainless classification. It is often described as "semi-stainless," offering meaningfully better corrosion resistance than plain carbon steels while delivering tool-steel-grade edge retention driven by large chromium carbides.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>D2 is a high-carbon, high-chromium tool steel with ~1.5% carbon and ~12% chromium — just below the threshold for true stainless classification. It is often described as "semi-stainless," offering meaningfully better corrosion resistance than plain carbon steels while delivering tool-steel-grade edge retention driven by large chromium carbides.</p>
        <p>Developed originally for industrial dies and punches, its abrasion resistance translates directly to blade durability. D2 is the dominant mid-tier tool steel in the global EDC and working-knife market, widely positioned as a cost-effective alternative to powder metallurgy steels like S30V at a significantly lower price point.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Large carbides require precise heat-treatment temperature control; a vacuum furnace is preferred for best results. Mass production fit is moderate — D2 is widely produced in Yangjiang for EDC programs but not ideal for thin kitchen blades.</p>
        <p>Yield rate is 92–95%, with medium raw material cost and very healthy profit margin potential. Domestic D2-equivalent stock is widely available from tool steel distributors, making MOQ flexible for both small and large batch programs.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>58–62</td><td>Large carbides require precise HT temperature control; vacuum furnace preferred</td></tr>
          <tr><td>Edge Retention</td><td>8/10</td><td>Strong wear resistance from chromium carbides</td></tr>
          <tr><td>Toughness</td><td>5/10</td><td>Moderate; avoid over-thin edges</td></tr>
          <tr><td>Corrosion Resistance</td><td>5/10</td><td>Semi-stainless; better than carbon but below true stainless</td></tr>
          <tr><td>Ease of Sharpening</td><td>4/10</td><td>Slower than simple stainless due to carbide volume</td></tr>
          <tr><td>Best fit</td><td>EDC Folding Knives / Hard-Use Tools / Mid-Range Fixed Blades / Working Knives</td><td>Widely produced in Yangjiang for EDC programs</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">With a yield rate of 92–95%, D2 requires precise heat-treatment temperature control due to its large carbides. We recommend vacuum furnace processing and advise against thin kitchen blade profiles. The raw material cost is medium with very healthy profit margin potential, and domestic D2-equivalent stock is widely available for flexible MOQ on both small and large batch programs.</p>
    </div>
  </div>

  <!-- ── K110 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-k110">K110 Tool Steel</h2>
    <p class="deep-dive-lead">K110 is Böhler's (Austria) designation for their D2-equivalent tool steel, certified to EN 1.2379 standards. Chemically near-identical to AISI D2, it is the preferred specification for European brands that require traceable, certified European mill origin — the choice between K110 and D2 is typically a sourcing and documentation decision rather than a performance one.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>K110 is Böhler's designation for their D2-equivalent tool steel, certified to EN 1.2379 standards. Chemically near-identical to AISI D2, K110 is the preferred specification for European brands that require traceable, certified European mill origin — particularly relevant for EU procurement programs with material sourcing requirements.</p>
        <p>Its main distinction from American D2 is tighter mill tolerances and certified batch documentation, not meaningfully different blade performance. A direct alternative to D2 in all applications, the choice between them is typically a sourcing and documentation decision rather than a performance one.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Böhler's tight mill tolerances reduce batch-to-batch heat-treatment variance, contributing to a yield rate of 93–96%. Raw material cost is medium-to-high due to the Böhler import premium.</p>
        <p>Mass production fit is moderate with the same HT requirements as D2; best for quality-tier OEM programs. Supply is import only via the Böhler distribution network, and mid-range MOQ is recommended for European brand programs requiring certified origin.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>58–62</td><td>Same HT requirements as D2</td></tr>
          <tr><td>Edge Retention</td><td>8/10</td><td>Near-identical to D2 performance</td></tr>
          <tr><td>Toughness</td><td>5/10</td><td>Moderate; same as D2</td></tr>
          <tr><td>Corrosion Resistance</td><td>5/10</td><td>Semi-stainless; same as D2</td></tr>
          <tr><td>Ease of Sharpening</td><td>4/10</td><td>Slower than simple stainless</td></tr>
          <tr><td>Best fit</td><td>EDC Folding Knives / European Brand OEM / Hard-Use Tools / Fixed Blades</td><td>Best for quality-tier OEM programs requiring certified European origin</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">K110's Böhler tight mill tolerances reduce batch-to-batch heat-treatment variance, giving us a solid 93–96% yield rate. The import-only supply chain means planning lead times through the Böhler distribution network, and we recommend this steel for European brand programs that require certified origin with mid-range MOQ.</p>
    </div>
  </div>

  <!-- ── A2 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-a2">A2 Tool Steel</h2>
    <p class="deep-dive-lead">A2 is an air-hardening tool steel (AISI A2 / DIN 1.2363) with ~1.0% carbon and a chromium-molybdenum-vanadium alloying package. Its defining production advantage is air-hardening, which dramatically reduces quench distortion and cracking risk while delivering a rare combination of meaningful toughness and solid edge retention in the tool steel category.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>A2 is an air-hardening tool steel with ~1.0% carbon and a chromium-molybdenum-vanadium alloying package. Its defining production advantage is air-hardening: unlike oil or water quench steels, A2 hardens simply by cooling in still air, which dramatically reduces quench distortion and cracking risk.</p>
        <p>This translates to excellent dimensional stability in finished blades, particularly for thick-spined, large-format fixed blades. In performance terms, A2 delivers a rare combination of meaningful toughness and solid edge retention — comparable to O1 in general use but substantially tougher, a step below D2 in edge retention but significantly better in impact resistance.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Air quench virtually eliminates distortion, giving A2 best-in-class dimensional stability with a yield rate of 94–97%. Raw material cost is medium with healthy profit margin potential.</p>
        <p>Mass production fit is moderate; A2 is excellent for thick-grind fixed blades but not suited for thin kitchen knives. Supply is available via import or domestic equivalent in Yangjiang, though it is less common than D2. MOQ is moderate, best for specialty outdoor or tactical programs.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>57–61</td><td>Air quench virtually eliminates distortion</td></tr>
          <tr><td>Edge Retention</td><td>7/10</td><td>Solid edge retention; a step below D2</td></tr>
          <tr><td>Toughness</td><td>7/10</td><td>Best-in-class dimensional stability</td></tr>
          <tr><td>Corrosion Resistance</td><td>4/10</td><td>Not stainless; requires maintenance</td></tr>
          <tr><td>Ease of Sharpening</td><td>5/10</td><td>Moderate effort</td></tr>
          <tr><td>Best fit</td><td>Hunting Knives / Heavy-Duty Outdoor Fixed Blades / Working Fixed Blades / Hard-Use Tools</td><td>Excellent for thick-grind fixed blades; not suited for thin kitchen knives</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">A2's air quench gives us best-in-class dimensional stability with a 94–97% yield rate and virtually eliminates distortion. We use it for thick-grind fixed blades and heavy-duty outdoor programs where impact resistance matters. Raw material cost is medium with healthy margins, though it is less common than D2 in Yangjiang.</p>
    </div>
  </div>

  <!-- ── CPM Cru-Wear ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-cpm-cru-wear">CPM Cru-Wear Tool Steel</h2>
    <p class="deep-dive-lead">CPM Cru-Wear is a powder metallurgy tool steel produced by Crucible Industries (USA) via the CPM process. Based on a high-speed steel alloy chemistry, it delivers near-PM-steel edge retention levels while retaining better toughness than comparable alloy-rich conventional tool steels.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>CPM Cru-Wear is a powder metallurgy tool steel produced by Crucible Industries via the CPM (Crucible Particle Metallurgy) process. Its CPM processing eliminates the large carbide segregation typical of conventionally produced high-alloy steels, resulting in a more uniform microstructure.</p>
        <p>Comparable in edge retention to S30V but with higher toughness, it is positioned as the tool-steel alternative for users who want PM-level cutting performance without sacrificing shock resistance. It is primarily specified for high-end custom and production working knives.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>CPM Cru-Wear requires diamond or CBN grinding and a strict heat-treatment process; experienced operators are essential. Yield rate is 90–93%, with high raw material cost and moderate profit margins due to the niche premium market and lower volume.</p>
        <p>Mass production fit is low — artisan or specialty small-batch only. Supply is import only with limited local availability in Yangjiang, and low MOQ is appropriate for boutique or custom programs only.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>60–65</td><td>Requires diamond/CBN grinding; strict HT process</td></tr>
          <tr><td>Edge Retention</td><td>9/10</td><td>Near-PM-steel edge retention</td></tr>
          <tr><td>Toughness</td><td>6/10</td><td>Better toughness than comparable alloy-rich conventional tool steels</td></tr>
          <tr><td>Corrosion Resistance</td><td>4/10</td><td>Minimal corrosion protection</td></tr>
          <tr><td>Ease of Sharpening</td><td>3/10</td><td>Challenging due to PM carbide structure</td></tr>
          <tr><td>Best fit</td><td>High-End Working Knives / Custom Fixed Blades / Heavy-Duty Cutting / Collector EDC</td><td>Artisan or specialty small-batch only</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">CPM Cru-Wear demands diamond or CBN grinding and strict heat-treatment with experienced operators, giving us a 90–93% yield rate. We reserve it for boutique custom and high-end working knife programs. The high raw material cost suits niche premium positioning with low MOQ for collector-tier lines.</p>
    </div>
  </div>

  <!-- ── K390 ── -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-k390">K390 Tool Steel</h2>
    <p class="deep-dive-lead">K390 is a high-vanadium powder metallurgy tool steel from Böhler (Austria), engineered for extreme abrasion resistance. Its very high vanadium content (~9%) creates an exceptionally dense distribution of hard vanadium carbides, delivering edge retention that rivals or exceeds most PM stainless steels.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>K390 is a high-vanadium powder metallurgy tool steel from Böhler, engineered for extreme abrasion resistance applications. Its very high vanadium content (~9%) creates an exceptionally dense distribution of hard vanadium carbides, delivering edge retention that rivals or exceeds most PM stainless steels.</p>
        <p>Unlike PM steels such as M390 which prioritize the stainless balance, K390 is an unapologetically wear-resistant tool steel where corrosion resistance is minimal. Comparable in edge retention to CPM-10V, it is positioned as the performance ceiling of the Böhler tool steel line, primarily specified for high-end production knives targeting users who prioritize maximum cutting longevity.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Extreme vanadium content demands diamond grinding and precise vacuum heat treatment. Yield rate is 88–92%, with high raw material cost as a Böhler PM import and moderate profit margins supported by premium pricing.</p>
        <p>Mass production fit is low — specialist production only and not suited for standard Yangjiang lines. Supply is import only with limited availability, and low MOQ is appropriate for specialty or collector-tier programs.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>62–65</td><td>Extreme vanadium content demands diamond grinding and precise vacuum HT</td></tr>
          <tr><td>Edge Retention</td><td>9/10</td><td>Rivals or exceeds most PM stainless steels</td></tr>
          <tr><td>Toughness</td><td>5/10</td><td>Moderate; prioritizes wear resistance</td></tr>
          <tr><td>Corrosion Resistance</td><td>4/10</td><td>Minimal; maintenance required</td></tr>
          <tr><td>Ease of Sharpening</td><td>3/10</td><td>Challenging due to dense vanadium carbides</td></tr>
          <tr><td>Best fit</td><td>High-Wear Working Knives / Heavy-Duty Outdoor Fixed Blades / Industrial Cutting / High-End Collector Knives</td><td>Specialist production only; not suited for standard Yangjiang lines</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">K390's extreme vanadium content demands diamond grinding and precise vacuum heat treatment, yielding 88–92%. We use it for specialty collector-tier and high-wear working knife programs only. The high Böhler PM import cost fits premium pricing, with low MOQ appropriate for boutique production.</p>
    </div>
  </div>'''

content = content.replace(old_section, new_section)

with open('pillar-tool-semi-stainless.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
