# CCabbage-V.github.io
A tool or dasboard site for personal use made by CCabbage-V.

---
# Modules

# 🇷🇴 Cabbage's Romania Macro Dashboard

A serverless, automated intelligence hub tracking Romanian economic indicators, fuel prices, and socio-political risk. Built entirely on GitHub Pages using Python and GitHub Actions.

## 🏗️ Architecture

This project operates without a traditional backend server.
1. **Data Ingestion:** A daily GitHub Action runs a Python script (`build_dashboard.py`).
2. **Web Scraping & APIs:** The script fetches official XML feeds from the National Bank of Romania (BNR), scrapes local fuel aggregators, and parses news RSS feeds.
3. **Flat-File Database:** The processed data, along with historical records, is saved into `data/history.json`.
4. **Static Frontend:** `dashboard.html` uses vanilla JavaScript to fetch the JSON file and render UI elements dynamically.

## 📊 Tracked Metrics
* **Currency:** EUR/RON, USD/RON (Source: BNR)
* **Commodities:** Gram of Gold (Source: BNR), Fuel - Petrol & Diesel (Source: Peco-Online)
* **Macro:** Consumer Price Index / Inflation (Source: INSSE)
* **Risk:** Custom Socio-Political Tension Index (derived from RSS headline keyword analysis).

## ⚙️ How the Recommendation Engine Works
The dashboard features an automated "Action Panel". It does not use AI APIs. Instead, the Python script evaluates the daily data against a strict ruleset (e.g., comparing current fuel prices against a 14-day trailing average combined with the current RSS Tension Index) to output actionable financial advice (Buy, Wait, or Delay).

## 🚀 Setup & Execution
1. Clone the repository.
2. The UI is accessible natively via `index.html`.
3. To run the data update manually:
   ```bash
   python scripts/build_dashboard.py
   ```
4. Pushing changes to the `main` branch will trigger the GitHub Action to update the live site.
