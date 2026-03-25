import urllib.request
import xml.etree.ElementTree as ET
import re

# 1. Fetch the live XML feed from BNR
url = "https://www.bnr.ro/nbrfxrates.xml"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
xml_data = response.read()

# 2. Parse the XML to find the EUR rate
root = ET.fromstring(xml_data)
ns = {'bnr': 'http://www.bnr.ro/xsd'}
eur_rate_element = root.find(".//bnr:Rate[@currency='EUR']", ns)

if eur_rate_element is not None:
    eur_rate = eur_rate_element.text
    print(f"✅ Successfully fetched BNR EUR Rate: {eur_rate}")
else:
    raise Exception("❌ Could not find the EUR rate in the BNR XML feed.")

# 3. Read your dashboard HTML file
# Note: If you named your file something other than 'index.html', change it here!
html_filename = 'index.html'

with open(html_filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 4. Update the HTML using Regex
# This looks for the EUR/RON label and replaces the number inside the <span class="value"> directly below it.
pattern = r'(<span class="label">EUR/RON \(BNR\)</span>\s*<div class="value-container">\s*<span class="value">)[0-9.]+(</span>)'
new_html_content = re.sub(pattern, rf'\g<1>{eur_rate}\g<2>', html_content)

# 5. Save the updated HTML
with open(html_filename, 'w', encoding='utf-8') as file:
    file.write(new_html_content)

print("✅ Dashboard HTML updated successfully!")
