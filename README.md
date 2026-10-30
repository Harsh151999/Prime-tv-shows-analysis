# Prime Video TV Shows — Exploratory Data Analysis

An end-to-end exploratory data analysis (EDA) and automated reporting pipeline examining **395 Amazon Prime Video TV shows**. Built with **Python**, **SQLite3**, **pandas**, **matplotlib/seaborn**, **Plotly**, and **ReportLab**, this project ingests raw catalog records, constructs a relational SQL database, executes analytical queries across six dimensions, and generates both interactive HTML visualizations and a 9-section executive PDF report.

**Repository:** [Harsh151999/Prime-tv-shows-analysis](https://github.com/Harsh151999/Prime-tv-shows-analysis)  
**Author:** Harsh Parashar

## Headline Metrics

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Total TV Shows Analyzed** | **395** | Cleaned catalog snapshot from `Prime_TV_Shows_Analysis (1).xlsx` |
| **IMDb-Rated Shows** | **223** | 56.5% of catalog carries verified IMDb ratings |
| **Average / Median IMDb Rating** | **7.39 / 7.50** | 77% of rated titles score $\ge 7.0$; 7 titles score $\ge 9.0$ |
| **Languages Represented** | **14** | Led by English (79%) and Hindi (10%) |
| **Average Show Longevity** | **2.6 Seasons** | 192 shows (~48%) are single-season releases; max run is 20 seasons |

## Key Analytical Outcomes

### 1. Language Distribution & Quality
* **Volume Dominance:** English accounts for **314 shows (79%)**, followed by **Hindi with 39 shows (10%)**, **Japanese (13)**, **Italiano (7)**, and **Spanish (6)**. Eight additional languages (including Serbian, Nederlands, Marathi, French, and Deutsch) account for the remaining titles.
* **Rating Performance by Language:** Among languages with multiple rated releases, **Spanish (8.10)** and **Deutsch (8.10)** achieve the highest mean IMDb ratings, while high-volume catalogs maintain strong averages: **Hindi (7.49)** and **English (7.41)** both outperform the overall mean (7.39), whereas **Japanese** averages **6.49**.

### 2. Genre Volume vs. Rating Quality
* **Top-Rated Genres (Minimum 3 Rated Shows):** **Sci-Fi** leads all genres with an average IMDb score of **8.03** (across 4 rated shows), followed by **Drama, Action, Suspense (7.90)** and **Drama, Suspense (7.73)**.
* **Core Catalog Anchor:** **Drama** (66 shows, **7.62** avg IMDb) delivers the strongest balance of catalog scale and critical reception, followed by **Drama, Comedy (7.51)** and **Drama, Action (7.48)**.
* **Underperforming Categories:** Standalone **Comedy (6.86)** and **Action (6.78)** lag behind Drama by 0.76 and 0.84 IMDb points, respectively.

| Genre Category *(3+ Rated Shows)* | Average IMDb Score | Catalog Role |
| :--- | :--- | :--- |
| **Sci-Fi** | **8.03** | Highest quality niche (4 rated shows) |
| **Drama, Action, Suspense** | **7.90** | High-performing multi-genre thrillers |
| **Drama, Suspense** | **7.73** | Strong critical reception |
| **Drama** | **7.62** | Core catalog anchor (66 shows) |
| **Drama, Comedy** | **7.51** | Above-average hybrid format |
| **Drama, Action** | **7.48** | Above-average hybrid format |
| **Kids** | **7.03** | Family programming baseline |
| **Drama, Sci-Fi** | **6.96** | Mid-tier genre blend |
| **Arts, Entertainment, Culture** | **6.87** | Documentary & factual lifestyle |
| **Comedy** | **6.86** | Trails Drama by 0.76 points |
| **Action** | **6.78** | Lowest average among major genres |

### 3. IMDb Rating Distribution
* **Right-Skewed Quality Curve:** Of the 223 rated shows, **77% score 7.0 or higher**, demonstrating consistent catalog quality.
* **Rating Band Breakdown:**
  * **9.0 – 10.0:** 1 top-band title (*Malgudi Days Swami & Friends 1* at 9.5; 7 shows reach $\ge 9.0$ inclusive of boundary ties)
  * **8.0 – 9.0:** 54 shows
  * **7.0 – 8.0:** 104 shows (largest concentration)
  * **6.0 – 7.0:** 47 shows
  * **5.0 – 6.0:** 12 shows
  * **4.0 – 5.0:** 3 shows
  * **< 4.0:** 2 shows

### 4. Age Rating Alignment
* **Mature Audience Focus:** **58% of the catalog** is rated **16+ (38%)** or **18+ (20%)**, while teen **13+ (17%)** and family-oriented tiers (**All Ages at 17%** and **7+ at 7%**) make up the remainder (with 1% unrated).
* **Ratings by Maturity Tier:** **18+ shows** achieve the highest average IMDb rating (**7.58**), closely followed by **7+ (7.53)** and **16+ (7.41)**, while **13+ (7.12)** and **All Ages (7.10)** score slightly lower.

### 5. Release Era & Catalog Growth
* **Post-2015 Expansion Surge:** Catalog additions accelerated sharply after 2015, reflecting Amazon Prime Video's aggressive global expansion and original content investment.
* **Era Breakdown (Volume & Mean IMDb):**
  * **pre-2000:** 48 shows — **7.57** avg IMDb
  * **2000–2004:** 9 shows — **7.33** avg IMDb
  * **2005–2009:** 31 shows — **8.18** avg IMDb *(highest-rated era)*
  * **2010–2014:** 61 shows — **7.68** avg IMDb
  * **2015–2017:** 109 shows — **7.46** avg IMDb
  * **2018–2020:** 135 shows — **7.04** avg IMDb *(highest volume era)*

### 6. Show Longevity & Multi-Season Retention
* **Single-Season Concentration:** **192 shows (~48%)** consist of a single season, reflecting limited miniseries and first-season cancellations.
* **Multi-Season Tiers:** **108 shows** run for **2–3 seasons**, **63 shows** span **4–6 seasons**, and **30 long-running franchises** reach **7+ seasons** (extending up to 20 seasons).

## Top 15 Highest-Rated & Bottom 10 Lowest-Rated Shows

| Rank | Top-Rated TV Shows | IMDb | Lowest-Rated TV Shows | IMDb |
| :--- | :--- | :--- | :--- | :--- |
| **1** | *Malgudi Days Swami & Friends 1* | **9.5** | *Ilana Glazer: The Planet is Burning* | **3.7** |
| **2** | *The Test: A New Era for Australia's Team* | **9.0** | *Tokyo Alice* | **4.0** |
| **3** | *Seinfeld* | **8.8** | *Skulls and Roses* | **4.3** |
| **4** | *The Marvelous Mrs. Maisel* | **8.7** | *Businessmen VS Aliens* | **4.5** |
| **5** | *Fleabag* | **8.7** | *Alice Wetterlund: My Mama is a Human...* | **4.7** |
| **6** | *The Boys* | **8.7** | *Final Life* | **5.2** |
| **7** | *House* | **8.7** | *Four More Shots Please* | **5.3** |
| **8** | *Hostel Daze* | **8.7** | *The Adventures of Rocky and Bullwinkle* | **5.4** |
| **9** | *Downton Abbey* | **8.7** | *#IMomSoHard Live* | **5.4** |
| **10** | *This Is Us* | **8.7** | *Alonzo Bodden: Heavy Lightweight* | **5.6** |
| **11** | *The Grand Tour* | **8.7** | — | — |
| **12** | *The Family Man* | **8.6** | — | — |
| **13** | *Doctor Who* | **8.6** | — | — |
| **14** | *Dexter* | **8.6** | — | — |
| **15** | *Shameless* | **8.6** | — | — |

## Repository Structure

* [`prime_tv_analysis.py`](https://github.com/Harsh151999/Prime-tv-shows-analysis/blob/main/prime_tv_analysis.py) — End-to-end Python pipeline (536 lines) covering Excel ingestion, data cleaning, SQLite database creation, SQL querying, static chart styling, Plotly HTML export, and multi-page ReportLab PDF generation.
* [Prime\_TV\_Shows\_Analysis (1).xlsx](https://www.google.com/search?q=https://github.com/Harsh151999/Prime-tv-shows-analysis/blob/main/Prime_TV_Shows_Analysis%2520%281%29.xlsx) — Source dataset containing 395 Prime Video TV show records (`Raw Data` sheet).
* [prime\_tv.db](https://www.google.com/search?q=https://github.com/Harsh151999/Prime-tv-shows-analysis/blob/main/prime_tv.db) — Auto-generated SQLite relational database containing the normalized `shows` table.
* [Prime\_TV\_Interactive\_Graphs (1).html](https://www.google.com/search?q=https://github.com/Harsh151999/Prime-tv-shows-analysis/blob/main/Prime_TV_Interactive_Graphs%2520%281%29.html) — Standalone interactive Plotly dashboard.
* [`Prime_TV_Analysis_Report.pdf`](https://github.com/Harsh151999/Prime-tv-shows-analysis/blob/main/Prime_TV_Analysis_Report.pdf) — Generated 9-section analytical PDF report.

## Tech Stack

* **Programming & Querying:** Python 3.10+, SQLite3 (`sqlite3`)
* **Data Manipulation:** `pandas`, `numpy`, `openpyxl`
* **Data Visualization:** `matplotlib`, `seaborn`, `plotly`
* **Automated Reporting:** `reportlab`

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Harsh151999/Prime-tv-shows-analysis.git
cd Prime-tv-shows-analysis

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn plotly openpyxl reportlab

# 3. Run the full ETL, SQL analysis, and report generation pipeline
python prime_tv_analysis.py
```

## License

Distributed under the [MIT License](https://www.google.com/search?q=https://github.com/Harsh151999/Prime-tv-shows-analysis/blob/main/LICENSE).

