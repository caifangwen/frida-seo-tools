import sys

with open('pillar-tool-semi-stainless.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_tbody = '''      <tbody>
        <tr>
          <td>D2 / K110</td>
          <td>59–61</td>
          <td>Strong wear resistance for value-performance knives.</td>
          <td>Semi-stainless; finishing and care guidance matter.</td>
        </tr>
        <tr>
          <td>A2</td>
          <td>58–60</td>
          <td>Better toughness than D2-style, useful for impact-prone tasks.</td>
          <td>Lower corrosion resistance; emphasize maintenance.</td>
        </tr>
        <tr>
          <td>O1</td>
          <td>58–61</td>
          <td>Good sharpening feel; classic tool steel for traditional lines.</td>
          <td>Not stainless; rust risk in kitchens if users are careless.</td>
        </tr>
      </tbody>'''

new_tbody = '''      <tbody>
        <tr>
          <td>D2</td>
          <td>58–62</td>
          <td>Strong wear resistance and semi-stainless corrosion protection at a mid-range price point.</td>
          <td>Dominant mid-tier tool steel for EDC and working knives; cost-effective alternative to PM steels.</td>
        </tr>
        <tr>
          <td>K110</td>
          <td>58–62</td>
          <td>Böhler's D2-equivalent with tighter mill tolerances and certified European batch documentation.</td>
          <td>Preferred for EU procurement programs requiring traceable origin; near-identical blade performance to D2.</td>
        </tr>
        <tr>
          <td>A2</td>
          <td>57–61</td>
          <td>Air-hardening tool steel with excellent dimensional stability and rare toughness-edge retention balance.</td>
          <td>Best for thick-spined fixed blades; air quench reduces distortion and cracking risk versus oil/water steels.</td>
        </tr>
        <tr>
          <td>CPM Cru-Wear</td>
          <td>60–65</td>
          <td>PM tool steel with near-PM edge retention and better toughness than conventional alloy-rich tool steels.</td>
          <td>High-end custom and production working knives; requires diamond/CBN grinding and strict HT.</td>
        </tr>
        <tr>
          <td>K390</td>
          <td>62–65</td>
          <td>Extreme abrasion resistance from very high vanadium content; edge retention rivaling premium PM stainless.</td>
          <td>Böhler's performance-ceiling tool steel; specialist production only, not suited for standard lines.</td>
        </tr>
      </tbody>'''

content = content.replace(old_tbody, new_tbody)

with open('pillar-tool-semi-stainless.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Step 1 done')
