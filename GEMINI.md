# Cabbage's Romania Macro Dashboard (Gemini Context)

A serverless, automated intelligence hub tracking Romanian economic indicators, fuel prices, and socio-political risk. Hosted on GitHub Pages and powered by GitHub Actions.

## 🏗️ Architecture & Technology Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript. Primary entry points are `index.html` and `dashboard.html`.
- **Backend (Data Ingestion):** Python scripts (`update_rates.py`, transitioning to `build_dashboard.py`).
  - Fetches XML rates from the National Bank of Romania (BNR).
  - Web scrapes fuel prices (planned) and news headlines (planned).
- **Data Storage:** Transitioning from direct HTML injection (via Regex) to a flat-file JSON database (`data/history.json`).
- **Automation:** GitHub Actions (`.github/workflows/update-dashboard.yml`) runs daily to update the dashboard.

## 🚀 Key Workflows

### 1. Data Update (Current)
Updates `dashboard.html` directly using Regex to replace values from BNR XML feed.
```bash
python update_rates.py
```

### 2. Data Update (Planned Phase 1 "JSON Pivot")
Updates a central JSON file which the frontend then fetches dynamically.
```bash
python build_dashboard.py
```

### 3. Automation
The GitHub Action `Update BNR Exchange Rate` runs at 11:30 UTC (13:30 Romanian Time) on weekdays.

## 🗺️ Current Development State (The JSON Pivot)

The project is currently in the middle of **Phase 1: Architecture Shift**.
- **Source Files:**
  - `update_rates.py`: Current production script using Regex injection.
  - `dashboard.html`: Main UI, currently being manually updated by Regex.
- **Planned Migration:**
  - Rename `update_rates.py` to `build_dashboard.py`.
  - Create `data/history.json` as the source of truth.
  - Update `dashboard.html` to fetch data via `fetch('data/history.json')`.
- **References:**
  - `docs/superpowers/plans/2026-03-25-phase-1-json-pivot.md`: Detailed implementation steps.
  - `docs/superpowers/specs/2026-03-25-phase-1-json-pivot-design.md`: Design spec for the pivot.

## 🧠 Recommendation Engine Logic

The dashboard features a rule-based engine (no external AI APIs) to provide actionable financial advice based on:
- **Fuel Algorithm:** Price vs. 14-day trailing average.
- **Financing Algorithm:** IRCC/ROBOR trends vs. CPI inflation.
- **Currency Algorithm:** EUR/RON volatility and Gold price spikes.

## 🛠️ Development Conventions

- **Lightweight Dependencies:** Avoid heavy frameworks. Use standard libraries (`urllib`, `xml.etree`) and vanilla JS where possible.
- **Surgical Updates:** When modifying HTML, ensure CSS classes for value containers (`<span class="value">`) are preserved for the scripts to find.
- **History First:** All new metrics should be appended to `data/history.json` to enable future historical charting (planned for Chart.js).
