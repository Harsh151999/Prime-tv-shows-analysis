"""
Prime Video TV Shows — Data Analysis Project
============================================
Stack : Python · SQLite · pandas · matplotlib · seaborn
Data  : Prime_TV_Shows_Analysis.xlsx  (395 shows)
"""

import sqlite3
import warnings
import textwrap
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

warnings.filterwarnings("ignore")

# ── 0. CONFIG ────────────────────────────────────────────────────────────────
EXCEL_PATH = "/mnt/user-data/uploads/Prime_TV_Shows_Analysis__1_.xlsx"
DB_PATH    = "/home/claude/prime_tv.db"
OUT_PDF    = "/mnt/user-data/outputs/Prime_TV_Analysis_Report.pdf"

PALETTE = {
    "blue"   : "#185FA5",
    "teal"   : "#0F6E56",
    "coral"  : "#D85A30",
    "amber"  : "#BA7517",
    "purple" : "#534AB7",
    "green"  : "#3B6D11",
}

# matplotlib style
plt.rcParams.update({
    "font.family"       : "DejaVu Sans",
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.grid"         : True,
    "grid.alpha"        : 0.25,
    "axes.labelsize"    : 10,
    "xtick.labelsize"   : 9,
    "ytick.labelsize"   : 9,
    "figure.facecolor"  : "white",
    "axes.facecolor"    : "white",
})

# ── 1. LOAD & CLEAN ──────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — Loading & cleaning data")
print("=" * 60)

raw = pd.read_excel(EXCEL_PATH, sheet_name="Raw Data", header=1)
raw.columns = ["No", "Title", "Year", "Seasons", "Language", "Genre", "IMDb", "AgeRating"]
df = raw[raw["No"].apply(lambda x: str(x).strip().isdigit())].copy()

df["No"]      = df["No"].astype(int)
df["Year"]    = pd.to_numeric(df["Year"],    errors="coerce").astype("Int64")
df["Seasons"] = pd.to_numeric(df["Seasons"], errors="coerce").astype("Int64")
df["IMDb"]    = pd.to_numeric(df["IMDb"],    errors="coerce")

# Era buckets
def era(y):
    if pd.isna(y): return "Unknown"
    if y < 2000:   return "pre-2000"
    if y < 2005:   return "2000–04"
    if y < 2010:   return "2005–09"
    if y < 2015:   return "2010–14"
    if y < 2018:   return "2015–17"
    return "2018–20"

df["Era"]     = df["Year"].apply(era)
df["Rated"]   = df["IMDb"].notna()
df["IMDbBand"] = pd.cut(df["IMDb"], bins=[0,4,5,6,7,8,9,10],
                         labels=["<4","4–5","5–6","6–7","7–8","8–9","9–10"])

print(f"  Rows loaded : {len(df)}")
print(f"  IMDb-rated  : {df['Rated'].sum()}")
print(f"  Unrated     : {(~df['Rated']).sum()}")
print(f"  Unique genres: {df['Genre'].nunique()}")
print(f"  Year range  : {df['Year'].min()} – {df['Year'].max()}")
print()

# ── 2. SQLITE — LOAD & SQL QUERIES ──────────────────────────────────────────
print("=" * 60)
print("STEP 2 — Building SQLite database & running SQL queries")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)
df.to_sql("shows", conn, if_exists="replace", index=False)
print(f"  Table 'shows' written → {DB_PATH}\n")

QUERIES = {
    "Q1 — Top 15 shows by IMDb": """
        SELECT Title, Genre, Language, Year, IMDb
        FROM shows
        WHERE IMDb IS NOT NULL
        ORDER BY IMDb DESC
        LIMIT 15;
    """,

    "Q2 — Bottom 10 shows by IMDb": """
        SELECT Title, Genre, Language, Year, IMDb
        FROM shows
        WHERE IMDb IS NOT NULL
        ORDER BY IMDb ASC
        LIMIT 10;
    """,

    "Q3 — Avg IMDb by genre (≥3 rated shows)": """
        SELECT Genre,
               ROUND(AVG(IMDb), 2)  AS avg_imdb,
               COUNT(*)             AS total_shows,
               SUM(Rated)           AS rated_shows,
               ROUND(MIN(IMDb), 1)  AS min_imdb,
               ROUND(MAX(IMDb), 1)  AS max_imdb
        FROM shows
        GROUP BY Genre
        HAVING rated_shows >= 3
        ORDER BY avg_imdb DESC;
    """,

    "Q4 — Language breakdown": """
        SELECT Language,
               COUNT(*)                                AS total,
               SUM(Rated)                              AS rated,
               ROUND(AVG(IMDb), 2)                    AS avg_imdb,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shows), 1) AS pct
        FROM shows
        GROUP BY Language
        ORDER BY total DESC;
    """,

    "Q5 — Age rating distribution": """
        SELECT AgeRating,
               COUNT(*) AS shows,
               ROUND(AVG(IMDb), 2) AS avg_imdb
        FROM shows
        GROUP BY AgeRating
        ORDER BY shows DESC;
    """,

    "Q6 — Era-wise content growth": """
        SELECT Era,
               COUNT(*) AS shows,
               SUM(Rated) AS rated,
               ROUND(AVG(IMDb), 2) AS avg_imdb
        FROM shows
        WHERE Era != 'Unknown'
        GROUP BY Era
        ORDER BY MIN(Year);
    """,

    "Q7 — Season longevity bands": """
        SELECT
            CASE
                WHEN Seasons = 1  THEN '1 season'
                WHEN Seasons <= 3 THEN '2–3 seasons'
                WHEN Seasons <= 6 THEN '4–6 seasons'
                ELSE '7+ seasons'
            END AS season_band,
            COUNT(*) AS shows,
            ROUND(AVG(IMDb), 2) AS avg_imdb
        FROM shows
        WHERE Seasons IS NOT NULL
        GROUP BY season_band
        ORDER BY MIN(Seasons);
    """,

    "Q8 — Correlation: Seasons vs IMDb (rated shows)": """
        SELECT Seasons, ROUND(AVG(IMDb),2) AS avg_imdb, COUNT(*) AS shows
        FROM shows
        WHERE IMDb IS NOT NULL AND Seasons IS NOT NULL
        GROUP BY Seasons
        ORDER BY Seasons;
    """,

    "Q9 — Top language × genre combinations": """
        SELECT Language, Genre, COUNT(*) AS shows, ROUND(AVG(IMDb),2) AS avg_imdb
        FROM shows
        GROUP BY Language, Genre
        HAVING shows >= 3
        ORDER BY shows DESC
        LIMIT 15;
    """,

    "Q10 — IMDb rating band distribution": """
        SELECT IMDbBand,
               COUNT(*) AS shows
        FROM shows
        WHERE IMDbBand IS NOT NULL
        GROUP BY IMDbBand
        ORDER BY IMDbBand;
    """,
}

results = {}
for name, sql in QUERIES.items():
    res = pd.read_sql_query(textwrap.dedent(sql), conn)
    results[name] = res
    print(f"  {name}")
    print(res.to_string(index=False))
    print()

conn.close()

# ── 3. VISUALISATIONS ────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 3 — Generating visualisations → PDF")
print("=" * 60)

from matplotlib.backends.backend_pdf import PdfPages

def section_page(pdf, title, subtitle=""):
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.axis("off")
    fig.patch.set_facecolor("#f0f4fa")
    ax.text(0.5, 0.65, title, transform=ax.transAxes, fontsize=22,
            fontweight="bold", ha="center", va="center", color="#0C447C")
    if subtitle:
        ax.text(0.5, 0.25, subtitle, transform=ax.transAxes, fontsize=11,
                ha="center", va="center", color="#555")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

with PdfPages(OUT_PDF) as pdf:

    # ── Cover ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis("off")
    fig.patch.set_facecolor("#0C447C")
    ax.text(0.5, 0.72, "Prime Video TV Shows", transform=ax.transAxes,
            fontsize=30, fontweight="bold", ha="center", color="white")
    ax.text(0.5, 0.58, "Data Analysis Report", transform=ax.transAxes,
            fontsize=20, ha="center", color="#85B7EB")
    ax.text(0.5, 0.42, "395 shows  ·  Python + SQLite + pandas + matplotlib",
            transform=ax.transAxes, fontsize=12, ha="center", color="#B5D4F4")
    stats = [("395", "Total Shows"), ("223", "IMDb Rated"), ("7.39", "Avg IMDb"),
             ("14", "Languages"), ("2.6", "Avg Seasons")]
    for i, (v, l) in enumerate(stats):
        x = 0.1 + i * 0.2
        ax.text(x, 0.20, v, transform=ax.transAxes, fontsize=18,
                fontweight="bold", ha="center", color="white")
        ax.text(x, 0.12, l, transform=ax.transAxes, fontsize=9,
                ha="center", color="#85B7EB")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # ── Section 1: Language ───────────────────────────────────────────────────
    section_page(pdf, "1. Language Analysis", "How content is distributed across spoken languages")

    lang = results["Q4 — Language breakdown"].head(10)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    bars = ax.barh(lang["Language"][::-1], lang["total"][::-1],
                   color=PALETTE["blue"], edgecolor="none")
    for bar in bars:
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                f'{int(bar.get_width())}', va="center", fontsize=9)
    ax.set_xlabel("Number of shows")
    ax.set_title("Shows by language (top 10)", fontweight="bold")

    ax2 = axes[1]
    lang_r = lang[lang["rated"] > 0].copy()
    bars2 = ax2.barh(lang_r["Language"][::-1], lang_r["avg_imdb"][::-1],
                     color=PALETTE["teal"], edgecolor="none")
    ax2.axvline(7.39, color=PALETTE["coral"], linestyle="--", lw=1.5, label="Overall avg 7.39")
    for bar in bars2:
        ax2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                 f'{bar.get_width():.2f}', va="center", fontsize=9)
    ax2.set_xlabel("Avg IMDb rating")
    ax2.set_title("Avg IMDb by language", fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.set_xlim(5.5, 9)
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 2: Genre ─────────────────────────────────────────────────────
    section_page(pdf, "2. Genre Analysis", "Volume, quality, and spread across genres")

    genre = results["Q3 — Avg IMDb by genre (≥3 rated shows)"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    colors_g = [PALETTE["blue"] if v >= 7.5 else PALETTE["teal"] if v >= 7.0
                else PALETTE["amber"] for v in genre["avg_imdb"]]
    bars = ax.barh(genre["Genre"][::-1], genre["avg_imdb"][::-1],
                   color=colors_g[::-1], edgecolor="none")
    ax.axvline(7.39, color=PALETTE["coral"], linestyle="--", lw=1.5, label="Overall avg")
    for bar in bars:
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.2f}', va="center", fontsize=9)
    ax.set_xlabel("Avg IMDb rating")
    ax.set_title("Avg IMDb rating by genre (≥3 shows)", fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(5.5, 8.8)

    ax2 = axes[1]
    sc = ax2.scatter(genre["total_shows"], genre["avg_imdb"],
                     s=genre["rated_shows"]*12, alpha=0.7,
                     c=genre["avg_imdb"], cmap="Blues", edgecolors="#185FA5", lw=0.8)
    for _, row in genre.iterrows():
        label = row["Genre"][:18] + "…" if len(row["Genre"]) > 18 else row["Genre"]
        ax2.annotate(label, (row["total_shows"], row["avg_imdb"]),
                     fontsize=7.5, ha="left", va="bottom",
                     xytext=(4, 3), textcoords="offset points")
    ax2.set_xlabel("Total shows in genre")
    ax2.set_ylabel("Avg IMDb rating")
    ax2.set_title("Volume vs quality bubble chart\n(bubble size = rated show count)", fontweight="bold")
    plt.colorbar(sc, ax=ax2, label="Avg IMDb", shrink=0.8)
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 3: IMDb Distribution ─────────────────────────────────────────
    section_page(pdf, "3. IMDb Rating Distribution", "How quality is spread across the catalogue")

    rated = df[df["IMDb"].notna()].copy()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    ax.hist(rated["IMDb"], bins=20, color=PALETTE["blue"], edgecolor="white", lw=0.5)
    ax.axvline(rated["IMDb"].mean(), color=PALETTE["coral"], lw=2,
               label=f'Mean: {rated["IMDb"].mean():.2f}')
    ax.axvline(rated["IMDb"].median(), color=PALETTE["amber"], lw=2, linestyle="--",
               label=f'Median: {rated["IMDb"].median():.2f}')
    ax.set_xlabel("IMDb rating"); ax.set_ylabel("Number of shows")
    ax.set_title("IMDb rating histogram (223 rated shows)", fontweight="bold")
    ax.legend()

    ax2 = axes[1]
    band = results["Q10 — IMDb rating band distribution"]
    bars = ax2.bar(band["IMDbBand"].astype(str), band["shows"],
                   color=[PALETTE["blue"] if i >= 4 else PALETTE["amber"] for i in range(len(band))],
                   edgecolor="none")
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 str(int(bar.get_height())), ha="center", fontsize=9)
    ax2.set_xlabel("IMDb band"); ax2.set_ylabel("Number of shows")
    ax2.set_title("Shows per IMDb rating band", fontweight="bold")
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 4: Age Rating ────────────────────────────────────────────────
    section_page(pdf, "4. Age Rating Analysis", "Audience targeting and content maturity breakdown")

    age = results["Q5 — Age rating distribution"]
    colors_age = [PALETTE["blue"], PALETTE["coral"], PALETTE["purple"],
                  PALETTE["teal"], PALETTE["amber"]]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    wedges, texts, autotexts = ax.pie(
        age["shows"], labels=age["AgeRating"], autopct="%1.0f%%",
        colors=colors_age, startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 2})
    for at in autotexts: at.set_fontsize(9)
    ax.set_title("Age rating share", fontweight="bold")

    ax2 = axes[1]
    age_r = age[age["avg_imdb"].notna()]
    bars = ax2.bar(age_r["AgeRating"], age_r["avg_imdb"],
                   color=colors_age[:len(age_r)], edgecolor="none")
    ax2.axhline(7.39, color=PALETTE["coral"], lw=1.5, linestyle="--", label="Overall avg 7.39")
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f'{bar.get_height():.2f}', ha="center", fontsize=9)
    ax2.set_ylabel("Avg IMDb"); ax2.set_ylim(0, 9)
    ax2.set_title("Avg IMDb by age rating", fontweight="bold")
    ax2.legend()
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 5: Year Trend ────────────────────────────────────────────────
    section_page(pdf, "5. Release Year Trend", "Content growth trajectory over time")

    era_data = results["Q6 — Era-wise content growth"]
    era_order = ["pre-2000","2000–04","2005–09","2010–14","2015–17","2018–20"]
    era_data = era_data.set_index("Era").reindex(era_order).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    ax.fill_between(range(len(era_data)), era_data["shows"],
                    color=PALETTE["blue"], alpha=0.25)
    ax.plot(range(len(era_data)), era_data["shows"],
            color=PALETTE["blue"], lw=2.5, marker="o", ms=7)
    for i, (cnt, er) in enumerate(zip(era_data["shows"], era_data["Era"])):
        ax.text(i, cnt + 3, str(cnt), ha="center", fontsize=9)
    ax.set_xticks(range(len(era_data)))
    ax.set_xticklabels(era_data["Era"], rotation=30, ha="right")
    ax.set_ylabel("Number of shows")
    ax.set_title("Content added by era", fontweight="bold")

    ax2 = axes[1]
    ax2.plot(range(len(era_data)), era_data["avg_imdb"],
             color=PALETTE["coral"], lw=2.5, marker="s", ms=7)
    ax2.fill_between(range(len(era_data)), era_data["avg_imdb"],
                     color=PALETTE["coral"], alpha=0.15)
    for i, v in enumerate(era_data["avg_imdb"]):
        ax2.text(i, v + 0.1, f'{v:.2f}', ha="center", fontsize=9)
    ax2.set_xticks(range(len(era_data)))
    ax2.set_xticklabels(era_data["Era"], rotation=30, ha="right")
    ax2.set_ylabel("Avg IMDb rating")
    ax2.set_ylim(5, 9)
    ax2.set_title("Avg IMDb by era", fontweight="bold")
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 6: Seasons ───────────────────────────────────────────────────
    section_page(pdf, "6. Seasons & Longevity", "How many seasons shows run and how that affects ratings")

    seas_corr = results["Q8 — Correlation: Seasons vs IMDb (rated shows)"]
    season_band = results["Q7 — Season longevity bands"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    ax.bar(season_band["season_band"], season_band["shows"],
           color=PALETTE["teal"], edgecolor="none")
    for i, (cnt, band) in enumerate(zip(season_band["shows"], season_band["season_band"])):
        ax.text(i, cnt + 1, str(cnt), ha="center", fontsize=9)
    ax.set_ylabel("Number of shows")
    ax.set_title("Show count by season band", fontweight="bold")

    ax2 = axes[1]
    ax2.scatter(seas_corr["Seasons"], seas_corr["avg_imdb"],
                s=seas_corr["shows"]*30, color=PALETTE["purple"],
                alpha=0.7, edgecolors="#3C3489", lw=0.8)
    z = np.polyfit(seas_corr["Seasons"].astype(float),
                   seas_corr["avg_imdb"].astype(float), 1)
    p = np.poly1d(z)
    xs = np.linspace(seas_corr["Seasons"].min(), seas_corr["Seasons"].max(), 100)
    ax2.plot(xs, p(xs), color=PALETTE["coral"], lw=2, linestyle="--", label="Trend")
    ax2.set_xlabel("Number of seasons")
    ax2.set_ylabel("Avg IMDb rating")
    ax2.set_title("Seasons vs avg IMDb\n(bubble size = show count)", fontweight="bold")
    ax2.legend()
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 7: Top Rated ─────────────────────────────────────────────────
    section_page(pdf, "7. Top & Bottom Rated Shows", "The best and worst of Prime Video's catalogue")

    top15 = results["Q1 — Top 15 shows by IMDb"]
    bot10 = results["Q2 — Bottom 10 shows by IMDb"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax = axes[0]
    labels_t = [t[:30]+"…" if len(t) > 30 else t for t in top15["Title"]]
    bars = ax.barh(labels_t[::-1], top15["IMDb"][::-1],
                   color=PALETTE["blue"], edgecolor="none")
    for bar in bars:
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.1f}', va="center", fontsize=8)
    ax.set_xlabel("IMDb rating"); ax.set_xlim(7, 10)
    ax.set_title("Top 15 rated shows", fontweight="bold")

    ax2 = axes[1]
    labels_b = [t[:30]+"…" if len(t) > 30 else t for t in bot10["Title"]]
    bars2 = ax2.barh(labels_b[::-1], bot10["IMDb"][::-1],
                     color=PALETTE["coral"], edgecolor="none")
    for bar in bars2:
        ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 f'{bar.get_width():.1f}', va="center", fontsize=8)
    ax2.set_xlabel("IMDb rating"); ax2.set_xlim(0, 7)
    ax2.set_title("Bottom 10 rated shows", fontweight="bold")
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 8: Heatmap — Language × Genre ────────────────────────────────
    section_page(pdf, "8. Language × Genre Heatmap", "Cross-dimensional content concentration")

    top_langs  = df["Language"].value_counts().head(6).index.tolist()
    top_genres = df["Genre"].value_counts().head(10).index.tolist()
    heat_df = df[df["Language"].isin(top_langs) & df["Genre"].isin(top_genres)]
    pivot = heat_df.pivot_table(index="Language", columns="Genre",
                                values="Title", aggfunc="count", fill_value=0)
    pivot = pivot.reindex(index=top_langs, fill_value=0)

    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues", linewidths=0.5,
                linecolor="#ddd", ax=ax, cbar_kws={"shrink": 0.7})
    ax.set_title("Show count by Language × Genre (top 6 languages, top 10 genres)",
                 fontweight="bold", fontsize=11)
    ax.set_xlabel("Genre"); ax.set_ylabel("Language")
    plt.xticks(rotation=35, ha="right", fontsize=8)
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Section 9: Key Insights Summary ──────────────────────────────────────
    section_page(pdf, "9. Key Insights Summary", "What the data tells us")

    insights = [
        ("Content Language",
         "English dominates at 79% (314/395). Hindi is 2nd at 10% (39 shows), reflecting\n"
         "Prime India's regional push. 12 other languages share the remaining 11%."),
        ("Genre Quality",
         "Sci-fi leads avg IMDb at 8.03 but has only 4 rated shows. Drama (66 shows, avg 7.62)\n"
         "offers the best balance of volume and quality. Comedy lags by 0.76 points vs Drama."),
        ("Content Growth",
         "Explosive growth post-2015: 2018–2020 alone added 177 shows — more than all\n"
         "previous decades combined. This mirrors Prime Video's original content investment."),
        ("IMDb Distribution",
         "77% of rated shows score ≥7. The distribution is right-skewed — quality is\n"
         "generally high. Only 7 shows reach 9+; the top is Malgudi Days at 9.5."),
        ("Age Rating",
         "58% of content is rated 13+ or 16+. Family-friendly content (All ages + 7+)\n"
         "is just 24%. Prime Video clearly targets adult and teen audiences."),
        ("Longevity",
         "45% of shows have just 1 season (178 shows) — many are limited series or early\n"
         "cancellations. Avg seasons = 2.6; the longest runs reach 20 seasons."),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(14, 8))
    fig.patch.set_facecolor("white")
    for i, (title, body) in enumerate(insights):
        ax = axes[i // 2][i % 2]
        ax.axis("off")
        ax.set_facecolor("#f0f4fa")
        ax.text(0.03, 0.85, title, transform=ax.transAxes, fontsize=11,
                fontweight="bold", color="#0C447C", va="top")
        ax.text(0.03, 0.55, body, transform=ax.transAxes, fontsize=9,
                color="#333", va="top", linespacing=1.6)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.patch.set_facecolor("#f0f4fa")
        ax.patch.set_alpha(1)
    plt.tight_layout(pad=2)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

print(f"\n  PDF saved → {OUT_PDF}")
print("\n" + "=" * 60)
print("DONE — Full analysis complete.")
print("=" * 60)
