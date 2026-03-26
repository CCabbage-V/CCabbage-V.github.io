# Phase 1: The JSON Pivot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transition the RO Cost Signals dashboard from regex-based HTML updates to a JSON-driven data pipeline.

**Architecture:** A Python script fetches data and maintains a historical ledger in `data/history.json`. The `dashboard.html` file is updated to fetch this JSON and render the data dynamically using vanilla JavaScript.

**Tech Stack:** Python 3.x, HTML5, Vanilla JavaScript, GitHub Actions.

---

### Task 1: Initialize Data Store

**Files:**
- Create: `data/history.json`

- [ ] **Step 1: Create `data/history.json` with initial structure**

```json
{
  "currency": [],
  "fuel": [],
  "macro": [],
  "metadata": {
    "last_updated": null,
    "status": "initial"
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add data/history.json
git commit -m "chore: initialize data store"
```

---

### Task 2: Refactor Python Script

**Files:**
- Rename: `update_rates.py` -> `build_dashboard.py`
- Modify: `build_dashboard.py`

- [ ] **Step 1: Rename the script**

Run: `mv update_rates.py build_dashboard.py`

- [ ] **Step 2: Update `build_dashboard.py` to handle JSON operations**

Replace content of `build_dashboard.py` with:
```python
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
```

- [ ] **Step 3: Run the script to verify it works**

Run: `python build_dashboard.py`
Expected: `✅ History updated for YYYY-MM-DD` and `data/history.json` contains data.

- [ ] **Step 4: Commit**

```bash
git rm update_rates.py
git add build_dashboard.py data/history.json
git commit -m "refactor: pivot to JSON data store"
```

---

### Task 3: Update Frontend for JSON

**Files:**
- Modify: `dashboard.html`

- [ ] **Step 1: Update HTML placeholders and IDs**

Modify `dashboard.html` to replace static values with loading states and add specific IDs:
- EUR Value: `<span id="eur-value" class="value">---</span>`
- EUR Trend: `<span id="eur-trend" class="trend-flat">Loading...</span>`
- Petrol Value: `<span id="petrol-value" class="value">---</span>`
- Petrol Trend: `<span id="petrol-trend" class="trend-flat">Loading...</span>`
- Diesel Value: `<span id="diesel-value" class="value">---</span>`
- Diesel Trend: `<span id="diesel-trend" class="trend-flat">Loading...</span>`
- CPI Value: `<span id="cpi-value" class="value">---</span>`
- CPI Trend: `<span id="cpi-trend" class="trend-flat">Loading...</span>`
- HICP Value: `<span id="hicp-value" class="value">---</span>`
- HICP Trend: `<span id="hicp-trend" class="trend-flat">Loading...</span>`
- Add a status message area: `<div id="status-msg" style="color: red; padding: 10px; display: none;"></div>`
- Add a timestamp: `<div style="font-size: 0.8rem; color: #8e8e93; margin-top: 10px;">Last Updated: <span id="last-updated">---</span></div>`

- [ ] **Step 2: Implement robust JavaScript rendering**

Add a `<script>` tag before `</body>`:
```javascript
function updateTrend(id, current, prev, format = (v) => v) {
  const el = document.getElementById(id);
  if (!prev) {
    el.textContent = '→ Initial';
    el.className = 'trend-flat';
    return;
  }
  const diff = current - prev;
  if (diff > 0) {
    el.textContent = `↑ Rising (+${format(diff)})`;
    el.className = 'trend-up';
  } else if (diff < 0) {
    el.textContent = `↓ Falling (${format(diff)})`;
    el.className = 'trend-down';
  } else {
    el.textContent = '→ Stable';
    el.className = 'trend-flat';
  }
}

async function loadData() {
  const statusEl = document.getElementById('status-msg');
  try {
    const res = await fetch('data/history.json');
    if (!res.ok) throw new Error('Fetch failed');
    const data = await res.json();
    
    // Metadata & Staleness
    const lastUpdated = new Date(data.metadata.last_updated);
    document.getElementById('last-updated').textContent = lastUpdated.toLocaleString();
    const hoursOld = (new Date() - lastUpdated) / 36e5;
    if (hoursOld > 48) {
      statusEl.textContent = '⚠️ Data is more than 48 hours old.';
      statusEl.style.display = 'block';
    }

    // Currency
    const cur = data.currency;
    if (cur.length > 0) {
      const latest = cur[cur.length - 1];
      const prev = cur[cur.length - 2];
      document.getElementById('eur-value').textContent = latest.eur_ron.toFixed(4);
      updateTrend('eur-trend', latest.eur_ron, prev?.eur_ron, (v) => v.toFixed(4));
    }

    // Fuel
    const fuel = data.fuel;
    if (fuel.length > 0) {
      const latest = fuel[fuel.length - 1];
      const prev = fuel[fuel.length - 2];
      document.getElementById('petrol-value').textContent = `~${latest.petrol.toFixed(2)} RON`;
      updateTrend('petrol-trend', latest.petrol, prev?.petrol, (v) => v.toFixed(2));
      document.getElementById('diesel-value').textContent = `~${latest.diesel.toFixed(2)} RON`;
      updateTrend('diesel-trend', latest.diesel, prev?.diesel, (v) => v.toFixed(2));
    }

    // Macro
    const macro = data.macro;
    if (macro.length > 0) {
      const latest = macro[macro.length - 1];
      const prev = macro[macro.length - 2];
      document.getElementById('cpi-value').textContent = `${latest.cpi_ro}%`;
      updateTrend('cpi-trend', latest.cpi_ro, prev?.cpi_ro, (v) => v.toFixed(1) + '%');
      document.getElementById('hicp-value').textContent = `${latest.hicp_eu}%`;
      updateTrend('hicp-trend', latest.hicp_eu, prev?.hicp_eu, (v) => v.toFixed(1) + '%');
    }

  } catch (err) {
    statusEl.textContent = '❌ Data Offline: Could not load signals.';
    statusEl.style.display = 'block';
    console.error(err);
  }
}
loadData();
```

- [ ] **Step 3: Commit**

```bash
git add dashboard.html
git commit -m "feat: implement JSON-driven UI with error handling and trends"
```

---

### Task 4: Update GitHub Action

**Files:**
- Modify: `.github/workflows/update-dashboard.yml`

- [ ] **Step 1: Update script name and commit paths**

- Change `update_rates.py` to `build_dashboard.py`.
- Remove `git add dashboard.html` (it's no longer updated by script).
- Add `git add data/history.json`.

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/update-dashboard.yml
git commit -m "ci: update workflow for JSON pivot"
```
