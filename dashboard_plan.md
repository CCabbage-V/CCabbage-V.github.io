## 🗺️ Step-by-Step Plan: The Data Pipeline Upgrade

### Phase 1: Architecture Shift (The JSON Pivot)
We need to stop using Regex to inject text directly into HTML. It is too fragile for complex data.
1.  **Create a Data Store:** Python creates and updates a file called `history.json`.
2.  **Separate Frontend/Backend:** The Python script handles *only* data fetching, logic, and saving to JSON.
3.  **JavaScript Integration:** We update `dashboard.html` with vanilla JavaScript to `fetch('history.json')` and render the data dynamically. This allows us to easily implement historical charts later using a library like Chart.js.

### Phase 2: Expanding Data Sourcing
We will upgrade `update_rates.py` (which we should rename to `build_dashboard.py`) to pull from multiple sources:
1.  **BNR Feed (XML):** EUR/RON, USD/RON, Gram of Gold (XAU), and ROBOR/IRCC (critical for the loan recommendations).
2.  **Fuel Prices (Web Scraping):** Use the `BeautifulSoup` library to scrape Peco-online or a similar aggregator for average standard Petrol and Diesel prices.
3.  **Macro Inflation:** Query the Eurostat API or scrape INSSE for the latest monthly CPI print.

### Phase 3: Socio-Political Context Engine (No AI API)
How do we analyze geopolitics and local politics without an expensive AI API? We build a **Keyword Sentiment Scorer using RSS feeds.**
1.  **The Inputs:** The script fetches RSS feeds from major local/global news outlets (e.g., Ziarul Financiar, Euro News).
2.  **The Dictionary:** We define a weighted dictionary of trigger words:
    * *High Risk (+2):* "război", "mobilizare", "criză energetică", "suprataxare", "deficit excesiv".
    * *Medium Risk (+1):* "proteste", "grevă", "scumpiri", "inflație".
    * *Stability (-1):* "scădere", "subvenții", "creștere economică".
3.  **The Output:** The script scans the last 50 headlines, tallies the score, and generates a "Socio-Political Tension Index" from 1 to 10.

### Phase 4: Building the Recommendation Engine
The Python script will execute a hardcoded logic tree (detailed below) comparing current data to historical averages and the Tension Index to output a specific string of advice.

---

## 🧠 The Recommendation Engine: Rule Set (to be developed further)

This logic matrix determines what the dashboard actually tells you to do.

### 1. The Fuel Algorithm (Petrol/Diesel)
* **Variable Checked:** Current Price vs. 14-Day Trailing Average (TA).
* **Rule A (Urgent Buy):** If Current Price > 14-Day TA by **2% or more** OR Tension Index > 7 ➡️ *"🔴 URGENT REFILL: Prices are on an aggressive upward trend or geopolitical tension is high. Lock in current prices now."*
* **Rule B (Wait):** If Current Price < 14-Day TA by **1% or more** ➡️ *"🟢 WAIT: Prices are currently trending downward. Delay filling up if you have half a tank."*
* **Rule C (Neutral):** Price is within +/- 1% of 14-Day TA ➡️ *"⚪ NEUTRAL: Prices are stable. Refill at your convenience."*

### 2. The Financing Algorithm (ROBOR / IRCC / CPI)
* **Variables Checked:** Current IRCC/ROBOR vs. 3-Month Trend, CPI Trailing Trend.
* **Rule A (Delay Debt):** If CPI > 5% AND IRCC/ROBOR is flat or rising ➡️ *"🔴 DELAY FINANCING: Borrowing costs are highly restrictive due to sticky inflation. Avoid new variable-rate debt."*
* **Rule B (Lock Fixed Rate):** If CPI is falling consecutively for 3 months BUT Tension Index is rising ➡️ *"🟡 LOCK FIXED RATE: Inflation is cooling, but macro risks are rising. If buying, secure a fixed-rate loan before shocks hit."*
* **Rule C (Favorable Borrowing):** If IRCC/ROBOR drops by > 0.25% in a quarter ➡️ *"🟢 BORROWING EASING: Central bank policies are loosening. Good time to refinance or take planned loans."*

### 3. The Currency & Asset Algorithm (EUR/RON & Gold)
* **Variables Checked:** EUR/RON 30-Day Volatility, Gram of Gold (XAU).
* **Rule A (Capital Flight/Hedging):** If Tension Index > 8 OR Gold spikes > 3% in a week ➡️ *"🔴 HEDGE: High macro-stress detected. Consider moving liquid RON savings into EUR or Gold."*
* **Rule B (Safe to hold RON):** EUR/RON daily variance is < 0.05% AND Tension Index < 5 ➡️ *"🟢 STABLE: The BNR peg holds strong. Enjoy higher interest rates on RON deposits; no urgent need to convert to EUR."*
