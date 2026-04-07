# Prime-tv-shows-analysis


A complete end-to-end data analysis project on 395 Amazon Prime Video TV shows, built with Python, SQLite, pandas, matplotlib, and seaborn.

📌 Project Overview
This project explores the Prime Video TV shows catalogue to uncover patterns in content strategy, genre quality, language distribution, audience targeting, and show longevity — using real IMDb ratings and metadata.
Dataset: 395 shows · 223 IMDb-rated · 14 languages · Year range: 1926–2020

🛠️ Tech Stack
ToolPurposePython 3Core scripting and data pipelinepandasData loading, cleaning, feature engineeringSQLite3In-memory relational database + SQL queriesmatplotlibCharts and PDF report generationseabornHeatmap visualisationopenpyxlReading the Excel source dataset

📁 Repository Structure
Prime-tv-shows-analysis/
│
├── prime_tv_analysis.py           # Main analysis script (Python + SQL)
├── Prime_TV_Analysis_Report.pdf   # 10-page visual report (output)
├── Prime_TV_Interactive_Graphs.html  # Browser-based interactive charts
└── README.md

🔍 Analysis Performed
Data Cleaning (Python / pandas)

Type casting for Year, Seasons, IMDb columns
Era bucketing: pre-2000, 2000–04, 2005–09, 2010–14, 2015–17, 2018–20
IMDb band segmentation: <4, 4–5, 5–6, 6–7, 7–8, 8–9, 9–10
Null handling for unrated shows (172 of 395)

SQL Queries (SQLite — 10 queries)

Top 15 shows by IMDb rating
Bottom 10 shows by IMDb rating
Avg IMDb by genre (min 3 rated shows)
Language breakdown — count, rated %, avg IMDb
Age rating distribution
Era-wise content growth
Season longevity bands — quality vs length
Seasons vs IMDb correlation
Top Language × Genre combinations
IMDb band distribution

Visualisations (matplotlib + seaborn)

Language volume & quality bar charts
Genre avg IMDb + bubble chart (volume vs quality)
IMDb histogram + rating band distribution
Age rating pie chart + avg IMDb per rating
Era-wise content growth line chart
Seasons vs IMDb scatter with trend line
Top 15 / Bottom 10 rated shows
Language × Genre heatmap
Key insights summary page


📊 Key Findings
InsightFindingDominant languageEnglish — 79% (314/395 shows)Highest rated genreSci-fi — avg IMDb 8.03Largest genreDrama — 125 shows, avg 7.62Comedy vs Drama gap−0.76 IMDb pointsContent growth2018–20 added 177 shows — more than all prior decadesLongevity & quality7+ season shows avg 7.99 vs 7.05 for single-seasonBest language × genreHindi Drama — avg 8.21Top rated showMalgudi Days — IMDb 9.5Avg IMDb (rated shows)7.39 / 10

▶️ How to Run

Clone the repository

bashgit clone https://github.com/Harsh151999/Prime-tv-shows-analysis.git
cd Prime-tv-shows-analysis

Install dependencies

bashpip install pandas matplotlib seaborn openpyxl

Add the source Excel file (Prime_TV_Shows_Analysis.xlsx) to the project folder and update the path in the script if needed.
Run the analysis

bashpython prime_tv_analysis.py
This will:

Load and clean the data
Build a SQLite database and run all 10 SQL queries
Generate a 10-page PDF report


📄 Output
The script produces Prime_TV_Analysis_Report.pdf — a 10-page report with:

A cover page with key KPIs
8 chart sections (language, genre, IMDb, age rating, year trend, seasons, top/bottom shows, heatmap)
A key insights summary page
