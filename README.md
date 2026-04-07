## Prime Video TV Shows Analysis

This project explores and analyzes a dataset of Amazon Prime TV shows to uncover insights related to content distribution, genres, ratings, and release trends.

---

##  Overview

The objective of this project is to perform **exploratory data analysis (EDA)** on Prime Video TV shows and derive meaningful insights using Python and data visualization techniques.

---

## Dataset

The dataset includes:
- Title of TV shows
- Release year
- Number of seasons
- Language
- Genre
- IMDb rating
- Age rating

---

##  Workflow

1. Data Cleaning
   - Handled missing IMDb values using median
   - Converted columns to appropriate data types  

2. Exploratory Data Analysis (EDA)
   - Genre distribution analysis  
   - Language-based insights  
   - Year-wise content trends  
   - Rating analysis  

3. Data Visualization
   - Count plots  
   - Histograms  
   - Pair plots  
   - Box plots  
   - Line plots  

---

##  Key Insights

- English dominates the content library, followed by Hindi  
- Most popular genres: Drama, Comedy, Action  
- Significant growth in content after 2016–2018  
- Several long-running shows have 10+ seasons  
- Majority of shows have moderate to high IMDb ratings  

---

##  Tech Stack

- Python  
- pandas  
- numpy  
- matplotlib  
- seaborn  
- Jupyter Notebook  

---

##  Project Structure


Prime-tv-shows-analysis/
│
├── Amazon_Prime_TV_Shows_Data.csv
├── main.ipynb
├── images/
└── README.md


---

## ▶️ How to Run

```bash
git clone https://github.com/Harsh151999/Prime-tv-shows-analysis.git
cd Prime-tv-shows-analysis

pip install pandas numpy matplotlib seaborn
jupyter notebook
