Prime Video TV Shows Analysis

This project performs **Exploratory Data Analysis (EDA)** on a dataset of Prime Video TV shows to uncover insights into content distribution, genres, ratings, and growth trends.

---

## Overview

The objective of this project is to analyze Prime Video’s TV show catalog and extract meaningful insights using Python and data visualization techniques.

This analysis focuses on:
- Language distribution of shows  
- Genre popularity and performance  
- IMDb rating patterns  
- Growth of content over time  
- Relationship between seasons and ratings  

---

## Dataset

The dataset contains information on **395 TV shows**, including:

- Title  
- Release Year  
- Number of Seasons  
- Language  
- Genre  
- IMDb Rating  
- Age Rating  

---

## Workflow

### 1. Data Cleaning
- Removed invalid entries  
- Handled missing IMDb values using median imputation  
- Converted columns to appropriate data types  

### 2. Feature Engineering
- Created **Era categories** (pre-2000, 2000–2009, 2010–2014, 2015+)  
- Generated **IMDb rating bands** for analysis  

### 3. Exploratory Data Analysis (EDA)
- Language distribution analysis  
- Genre-based insights  
- IMDb rating distribution  
- Year-wise content growth  
- Seasons vs rating relationship  

### 4. Data Visualization
- Bar charts (language & genre)  
- Histograms (rating distribution)  
- Line plots (content growth)  
- Scatter plots (seasons vs ratings)  

---

##  Key Insights

- English dominates the catalog, followed by Hindi  
- Most shows have IMDb ratings between 6–8  
- Drama and Comedy are the most common genres  
- Significant growth in content after 2015  
- Majority of shows have 1–3 seasons  

---

##  Tech Stack

- Python  
- pandas  
- numpy  
- matplotlib  
- seaborn  
- Jupyter Notebook  

---

## Project Structure


Prime-tv-shows-analysis/
│
├── Amazon_Prime_TV_Shows_Data.csv
├── Prime_TV_Analysis.ipynb
└── README.md


---

## How to Run

```bash
git clone https://github.com/Harsh151999/Prime-tv-shows-analysis.git
cd Prime-tv-shows-analysis

pip install pandas numpy matplotlib seaborn
jupyter notebook
