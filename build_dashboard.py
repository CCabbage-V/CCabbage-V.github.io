import urllib.request
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

def fetch_bnr_eur():
    url = "https://www.bnr.ro/nbrfxrates.xml"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    xml_data = response.read()
    root = ET.fromstring(xml_data)
    ns = {'bnr': 'http://www.bnr.ro/xsd'}
    eur_rate_element = root.find(".//bnr:Rate[@currency='EUR']", ns)
    if eur_rate_element is not None:
        return float(eur_rate_element.text)
    raise Exception("Could not find EUR rate in BNR feed.")

def update_history():
    json_path = 'data/history.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"currency": [], "fuel": [], "macro": [], "metadata": {}}

    today = datetime.now().strftime('%Y-%m-%d')
    eur_rate = fetch_bnr_eur()

    # Update Currency
    if not any(entry['date'] == today for entry in data['currency']):
        data['currency'].append({
            "date": today,
            "eur_ron": eur_rate,
            "usd_ron": 4.6821, # Placeholder
            "gold_gram": 321.45 # Placeholder
        })
    
    # Placeholders for Fuel & Macro (Phase 2)
    if not any(entry['date'] == today for entry in data['fuel']):
        data['fuel'].append({"date": today, "petrol": 7.15, "diesel": 7.32})
    
    if not any(entry['date'] == today for entry in data['macro']):
        data['macro'].append({"date": today, "cpi_ro": 9.3, "hicp_eu": 8.3})

    # Keep only last 90 days
    for key in ['currency', 'fuel', 'macro']:
        data[key] = data[key][-90:]

    data['metadata'] = {
        "last_updated": datetime.now().isoformat(),
        "status": "stable"
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✅ History updated for {today}")

if __name__ == "__main__":
    update_history()
