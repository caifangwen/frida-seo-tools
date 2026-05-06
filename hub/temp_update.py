path = r'C:\Users\frida\Documents\seo-skill-main\hub\public\pillar-carbon-steels.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('  <!-- \u2500\u2500 1095 \u2500\u2500 -->')
end = content.find('  </div>\n\n  <style>')

if start == -1 or end == -1:
    print('markers not found', start, end)
    exit(1)

blocks = """  <!-- \u2500\u2500 1095 \u2500\u2500 -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-1095">1095 Carbon Steel</h2>
    <p class="deep-dive-lead">1095 is a plain high-carbon steel in the AISI 10XX series, with ~0.95% carbon and minimal alloying. Its simple composition makes it one of the most predictable and forgiving steels to heat treat, and it has served as the foundational material for American production and hand-forged outdoor knives for over a century.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>1095's simple composition makes it one of the most predictable and forgiving steels to heat treat. It has served as the foundational material for American production and hand-forged outdoor knives for over a century, and it is widely used in Yangjiang for economy-tier outdoor and survival knife programs destined for Western wholesale.</p>
        <p>Comparable to European C95 and similar in intent to SK-5 (Japan), it is the practical entry point for any knife maker learning carbon steel production. Its broad recognition and strong cost-performance make it an easy steel to communicate on product pages.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>1095 is reactive. Acidic foods will accelerate surface oxidation fast, and if care instructions are missing or unclear, rust complaints follow. A satin or forced-patina finish hides early reactivity better than a polished blade.</p>
        <p>Normalizing and quench protocol should be confirmed with your supplier. Poor HT on 1095 produces inconsistent hardness across the blade, which amplifies chipping risk at the tip.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>56\u201360</td><td>Simple alloy, wide HT tolerance; low risk of distortion or cracking</td></tr>
          <tr><td>Edge Retention</td><td>5/10</td><td>Good at typical kitchen hardness targets</td></tr>
          <tr><td>Toughness</td><td>8/10</td><td>Strong impact resistance for thin geometries</td></tr>
          <tr><td>Corrosion Resistance</td><td>2/10</td><td>Requires wipe-dry routine; avoid dishwasher</td></tr>
          <tr><td>Ease of Sharpening</td><td>9/10</td><td>Responds well to basic water stones</td></tr>
          <tr><td>Best fit</td><td>Outdoor Fixed Blades, Survival Knives, Traditional Bowie Knives, Wholesale Outdoor Programs</td><td>Strong for "American carbon" brand story; no MOQ constraint</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">1095 offers a 96\u201398% yield rate thanks to its simple alloy and wide heat-treatment tolerance, with very low raw material cost and excellent profit margin potential. It is fully compatible with Yangjiang standard quench-and-temper lines, with domestic equivalents like T10 widely stocked locally. There is no MOQ constraint, making it ideal for first-time B2B buyers entering the carbon craft segment.</p>
    </div>
  </div>

  <!-- \u2500\u2500 1084 \u2500\u2500 -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-1084">1084 Carbon Steel</h2>
    <p class="deep-dive-lead">1084 is a plain high-carbon steel with ~0.84% carbon \u2014 slightly lower than 1095 \u2014 which translates into marginally better toughness and more forgiving heat treatment behavior. It is chemically comparable to European C85 and functionally similar to 1095 for most end uses.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>1084 is a plain high-carbon steel with ~0.84% carbon, slightly lower than 1095, which translates into marginally better toughness and more forgiving heat treatment behavior. It is chemically comparable to European C85 and functionally similar to 1095 for most end uses.</p>
        <p>In the hand-forging and small-batch production world, it is the preferred starter steel for bladesmiths due to its reliable and readable heat treatment response. For production OEM, it offers essentially the same economics as 1095 with a slightly reduced risk of quench cracking on thinner profiles.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>1084 shares the same low corrosion resistance as other plain carbon steels. Care instructions and packaging inserts are essential to prevent rust complaints from end users.</p>
        <p>While 1084 is arguably the most forgiving carbon steel for heat treatment with a 97%+ yield rate, brands should still specify target HRC with tolerance and require batch hardness records to maintain consistency across production runs.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>58\u201361</td><td>Most forgiving carbon steel for HT; lower cracking risk than 1095</td></tr>
          <tr><td>Edge Retention</td><td>5/10</td><td>Good at typical kitchen hardness targets</td></tr>
          <tr><td>Toughness</td><td>8/10</td><td>Marginally better toughness than 1095</td></tr>
          <tr><td>Corrosion Resistance</td><td>2/10</td><td>Requires wipe-dry routine; avoid dishwasher</td></tr>
          <tr><td>Ease of Sharpening</td><td>9/10</td><td>Responds well to basic water stones</td></tr>
          <tr><td>Best fit</td><td>Outdoor Fixed Blades, Hunting Knives, Forged Custom Knives, Wholesale Outdoor Programs</td><td>Ideal for thin-grind fixed blades; no MOQ constraint</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">1084 delivers a 97%+ yield rate, making it arguably the most forgiving carbon steel for heat treatment with lower cracking risk than 1095. It is ideal for thin-grind fixed blades and fully compatible with standard production lines, with no MOQ constraint. Raw material cost is very low and profit margin potential is excellent, making it a strong alternative to 1095 for production OEM programs.</p>
    </div>
  </div>

  <!-- \u2500\u2500 52100 \u2500\u2500 -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-52100">52100 Carbon Steel</h2>
    <p class="deep-dive-lead">52100 is a chromium-vanadium bearing steel (AISI 52100 / DIN 100Cr6) originally developed for industrial ball-bearing applications, where extreme fatigue resistance and fine carbide distribution are essential. These same properties translate exceptionally well to knife blades.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>52100 is a chromium-vanadium bearing steel originally developed for industrial ball-bearing applications, where extreme fatigue resistance and fine carbide distribution are essential. These same properties translate exceptionally well to knife blades: the fine, evenly distributed carbides allow for a very refined edge at high hardness, while the vanadium content enhances toughness relative to plain high-carbon steels.</p>
        <p>It is the premium carbon steel choice for Western custom knife makers, often described as "the carbon steel equivalent of S35VN" in terms of balance. Comparable to the Japanese SK series in category, but significantly more refined in performance.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>52100 requires controlled heat treatment and is more sensitive to quench speed than 1095. Carbide dissolution and quench speed both affect final properties significantly \u2014 a supplier with limited experience on this steel can produce inconsistent results.</p>
        <p>It is available via import and is not standard local stock in Yangjiang, so plan accordingly. With a 93\u201396% yield rate, it is best suited for boutique or premium private-label programs rather than commodity volume runs.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>60\u201362</td><td>Requires controlled HT; more sensitive to quench speed than 1095</td></tr>
          <tr><td>Edge Retention</td><td>7/10</td><td>Fine carbides allow very refined edge at high hardness</td></tr>
          <tr><td>Toughness</td><td>7/10</td><td>Vanadium enhances toughness relative to plain carbon steels</td></tr>
          <tr><td>Corrosion Resistance</td><td>2/10</td><td>Still needs care routine despite chromium content</td></tr>
          <tr><td>Ease of Sharpening</td><td>7/10</td><td>Slightly more effort than plain carbon but rewards technique</td></tr>
          <tr><td>Best fit</td><td>Premium Carbon Chef Knives, Custom Hunting Knives, Collector Knives, High-End Private Label</td><td>Premium positioning justifies price; moderate MOQ</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">52100 has a 93\u201396% yield rate and requires controlled heat treatment, making it more sensitive to quench speed than simpler carbon grades. It is best suited for specialty small-batch or custom programs rather than high-speed mass production lines. Raw material cost is medium with healthy profit margin potential when premium positioning is used.</p>
    </div>
  </div>

  <!-- \u2500\u2500 W2 \u2500\u2500 -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-w2">W2 Carbon Steel</h2>
    <p class="deep-dive-lead">W2 is a water-hardening tool steel in the AISI W-series, characterized by its high carbon content (~1.0%) and trace vanadium for grain control. Its defining feature is an extremely fast quench requirement (water or brine), which produces a pronounced hardness differential between the hardened edge and the softer spine.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>W2 is a water-hardening tool steel characterized by its high carbon content (~1.0%) and trace vanadium for grain control. Its defining feature is an extremely fast quench requirement (water or brine), which produces a pronounced hardness differential between the hardened edge and the softer spine \u2014 the basis of the visual hamon line prized in Japanese-style blades.</p>
        <p>It is functionally comparable to Shirogami (White Paper) steels in use case and aesthetic potential. Primarily used in artisan and collector knife contexts where visual beauty and carbon steel performance are equally valued.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>W2's water quench creates real cracking risk, with a yield rate of only 85\u201392%. It requires experienced heat-treatment operators and is not suited for high-speed mass production lines.</p>
        <p>Supply chain availability in Yangjiang is limited; it is typically imported or sourced via specialty suppliers. Low MOQ is available, making it appropriate for custom and small-batch programs only.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>58\u201361</td><td>Water quench creates real cracking risk</td></tr>
          <tr><td>Edge Retention</td><td>6/10</td><td>Good balance for artisan applications</td></tr>
          <tr><td>Toughness</td><td>8/10</td><td>Strong impact resistance when properly heat treated</td></tr>
          <tr><td>Corrosion Resistance</td><td>1/10</td><td>Highest reactivity; demands diligent care routine</td></tr>
          <tr><td>Ease of Sharpening</td><td>8/10</td><td>Fast edge recovery; rewarding on natural stones</td></tr>
          <tr><td>Best fit</td><td>Artisan Custom Knives, Collector Knives, Hamon Display Blades, Traditional Fixed Blades</td><td>Niche premium positioning; low MOQ available</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">W2 offers a yield rate of 85\u201392% due to the water quench cracking risk, requiring experienced heat-treatment operators. It is not suited for high-speed production lines and is limited in local Yangjiang availability. Raw material cost is low-to-medium with healthy profit margin potential in niche premium positioning.</p>
    </div>
  </div>

  <!-- \u2500\u2500 Shirogami #1 \u2500\u2500 -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-shirogami-1">Shirogami #1 (White Paper Steel)</h2>
    <p class="deep-dive-lead">Shirogami #1 (\u767d\u7d19\u4e00\u53f7) is the highest-carbon variant of Hitachi Metals' White Paper steel series, containing approximately 1.25\u20131.35% carbon with very low alloying. Its purity enables an extremely fine grain structure that produces one of the sharpest edges achievable in any knife steel.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>Shirogami #1 is the highest-carbon variant of Hitachi Metals' White Paper steel series, containing approximately 1.25\u20131.35% carbon with very low alloying \u2014 essentially a refined, ultra-pure high-carbon steel. Its purity (minimal sulfur, phosphorus, and non-metallic inclusions) enables an extremely fine grain structure that, when properly heat-treated, produces one of the sharpest edges achievable in any knife steel.</p>
        <p>In the Japanese knife market, it is the prestige standard for traditional single-bevel knives (yanagiba, deba, kiritsuke). Comparable in carbon level to W2 but formulated specifically for the Japanese forging and HT tradition, with tighter mill purity controls.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Shirogami #1's purity demands precise atmosphere heat treatment; there is a risk of decarburization if improperly managed. The yield rate is 90\u201394%, reflecting the precision required.</p>
        <p>It is import only in Yangjiang, available through established Japanese steel channels. Mass production fit is low; this steel is suited for handcraft or semi-artisan production only, not automated lines.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>62\u201365</td><td>Purity demands precise atmosphere HT; decarburization risk if mismanaged</td></tr>
          <tr><td>Edge Retention</td><td>6/10</td><td>Extremely sharp edge achievable with proper heat treatment</td></tr>
          <tr><td>Toughness</td><td>7/10</td><td>Fine grain structure supports good stability</td></tr>
          <tr><td>Corrosion Resistance</td><td>1/10</td><td>Ultra-pure and extremely rust-prone; care inserts mandatory</td></tr>
          <tr><td>Ease of Sharpening</td><td>8/10</td><td>Classic keen edge character on natural stones</td></tr>
          <tr><td>Best fit</td><td>Traditional Japanese Chef Knives, Single-Bevel Kitchen Knives, Premium Culinary Retail</td><td>Strong brand recognition supports premium pricing; low-to-mid MOQ</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">Shirogami #1 demands precise atmosphere heat treatment with a 90\u201394% yield rate, and there is a real risk of decarburization if protocol is not properly managed. It is import only and suited for handcraft or semi-artisan production, not automated lines. Raw material cost is high with moderate-to-healthy profit margin potential supported by strong brand recognition.</p>
    </div>
  </div>

  <!-- \u2500\u2500 Aogami #2 \u2500\u2500 -->
  <div class="deep-dive-block">
    <h2 class="section-title" id="dd-aogami-2">Aogami #2 (Blue Paper Steel)</h2>
    <p class="deep-dive-lead">Aogami #2 (\u9752\u7d19\u4e8c\u53f7) is Hitachi Metals' tungsten- and chromium-alloyed upgrade to the Shirogami (White Paper) series. Among Japanese professional chefs, it is widely regarded as the best all-around Japanese carbon steel.</p>

    <div class="two-col">
      <div>
        <h3 class="sub-heading">Why Brands Choose It</h3>
        <p>Aogami #2 is Hitachi Metals' tungsten- and chromium-alloyed upgrade to the Shirogami series. The tungsten addition refines carbide distribution and significantly improves edge retention compared to White Paper steels, while the trace chromium provides a marginal improvement in corrosion resistance.</p>
        <p>Among Japanese professional chefs, it is widely regarded as the best all-around Japanese carbon steel \u2014 offering a performance upgrade over Shirogami without the extreme fragility of Aogami Super. It is functionally comparable to 52100 in the Western world, but with a distinctly Japanese character, and is the most commonly specified carbon steel for premium Japanese kitchen knife OEM programs.</p>
      </div>
      <div>
        <h3 class="sub-heading">Production Watch-Outs</h3>
        <p>Aogami #2's tungsten content raises heat-treatment sensitivity, and a controlled atmosphere is essential. The yield rate is 90\u201394%, reflecting the precision required in production.</p>
        <p>It is import only in Yangjiang with consistent availability through established channels. Mass production fit is low; it is best for semi-artisan or specialty batch production, not automated stamping lines.</p>
      </div>
    </div>

    <div class="table-wrap" style="margin-top:1.2rem;">
      <table>
        <thead><tr><th>Attribute</th><th>Typical Value</th><th>Production Note</th></tr></thead>
        <tbody>
          <tr><td>Target HRC</td><td>62\u201365</td><td>Tungsten content raises HT sensitivity; controlled atmosphere essential</td></tr>
          <tr><td>Edge Retention</td><td>7/10</td><td>Significantly improved edge retention over White Paper steels</td></tr>
          <tr><td>Toughness</td><td>6/10</td><td>Good stability but slightly less tough than Shirogami #1</td></tr>
          <tr><td>Corrosion Resistance</td><td>1/10</td><td>Marginal improvement over Shirogami; still high-maintenance</td></tr>
          <tr><td>Ease of Sharpening</td><td>7/10</td><td>Slightly more effort than Shirogami but rewards technique</td></tr>
          <tr><td>Best fit</td><td>Premium Japanese Chef Knives, Professional Kitchen Knives, High-End Culinary Retail</td><td>Best for Japanese-style brand programs; low-to-mid MOQ</td></tr>
        </tbody>
      </table>
    </div>

    <div class="content-note" style="margin-top:1.2rem;">
      <strong>From our production floor</strong>
      <p style="margin:0.4rem 0 0;">Aogami #2 has a 90\u201394% yield rate because its tungsten content raises heat-treatment sensitivity, making controlled atmosphere essential. It is import only with consistent availability through established channels, and is best suited for semi-artisan or specialty batch production. Raw material cost is high with moderate-to-healthy profit margin potential.</p>
    </div>
  </div>

  <style>"""

new_content = content[:start] + blocks + content[end + len('  </div>\n\n  <style>'):]
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('DONE')
