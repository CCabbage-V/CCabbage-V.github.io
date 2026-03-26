# Design Spec: Phase 1 - The JSON Pivot (RO Cost Signals)

**Date:** 2026-03-25
**Topic:** Transitioning from regex-based HTML updates to a structured JSON-driven data pipeline.

## 1. Overview
The goal is to decouple the data fetching (Python) from the UI rendering (HTML/JS). This enables historical tracking, trend analysis, and easier expansion of data sources (Phase 2) without fragile HTML manipulation.

## 2. Architecture & Data Flow
- **Data Producer (Python):** `build_dashboard.py` (formerly `update_rates.py`) will manage a `data/history.json` file.
- **Data Store (JSON):** A categorized historical ledger.
- **Data Consumer (JavaScript):** `dashboard.html` will fetch and render the latest data from the JSON file.

## 3. Data Schema (`data/history.json`)
The JSON structure will categorize data by frequency and type:

```json
{
  "currency": [
    { "date": "ISO-8601", "eur_ron": 0.0, "usd_ron": 0.0, "gold_gram": 0.0 }
  ],
  "fuel": [
    { "date": "ISO-8601", "petrol": 0.0, "diesel": 0.0 }
  ],
  "macro": [
    { "date": "ISO-8601", "cpi_ro": 0.0, "hicp_eu": 0.0 }
  ],
  "metadata": {
    "last_updated": "ISO-8601-TIMESTAMP",
    "status": "stable"
  }
}
```

## 4. Component Design

### 4.1 Python Producer (`build_dashboard.py`)
- **Load:** Read `data/history.json`. If not found, initialize with an empty structure.
- **Fetch:** Use the existing BNR XML parser for `eur_ron`. Use placeholders for other metrics for now.
- **Update Logic:**
  - Check if the current date already exists in the `currency`, `fuel`, and `macro` arrays.
  - If not, append a new object with today's values.
  - Limit arrays to the last 90 entries to maintain performance.
- **Save:** Atomic write to `data/history.json`.

### 4.2 JavaScript Consumer (`dashboard.html`)
- **Fetch:** `window.addEventListener('DOMContentLoaded', ...)` fetches the JSON.
- **Parse:**
  - Get the latest object from each category array (last index).
  - Get the previous object (second to last index) to calculate trends.
- **Render:**
  - Inject values into DOM elements (e.g., `id="eur-value"`, `id="petrol-value"`).
  - Update trend indicators (arrows and colors) based on the comparison.
  - Update a "Last Updated" timestamp in the footer or header.

## 5. Error Handling & Validation
- **Python:**
  - Validate BNR XML structure before updating.
  - Ensure the JSON file is valid before saving.
- **JavaScript:**
  - Show loading states (e.g., `---` or `...`) before data arrives.
  - Handle fetch failures by displaying a "Data Offline" notice.
  - Check if the date in the JSON is more than 48 hours old and warn the user.

## 6. Success Criteria
1. `data/history.json` is automatically updated by GitHub Actions.
2. `dashboard.html` displays the latest values without any direct HTML modification by the Python script.
3. No duplicate entries for the same date in the JSON history.
4. Trend arrows correctly reflect changes between the last two data points.
