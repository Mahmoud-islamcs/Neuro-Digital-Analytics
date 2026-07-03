<div align="center">

<img src="README_Banner.png" alt="Brain Rot Analytics Banner" width="100%">

# Brain Rot Analytics

**Understanding the relationship between short-form content consumption and student wellbeing through data.**

An end-to-end data analytics project combining data cleaning, SQL-based data modeling, interactive dashboards, and machine learning to study how digital habits relate to attention span, study productivity, and wellbeing.

[Overview](#overview) • [Highlights](#project-highlights) • [Dataset](#dataset) • [Dashboard](#dashboard-preview) • [Machine Learning](#machine-learning) • [Tech Stack](#tech-stack) • [Repository Structure](#repository-structure) • [Installation](#installation) • [Future Work](#future-work) • [Contributors](#contributors)

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=flat-square&logo=microsoftsqlserver&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-008DE4?style=flat-square&logo=plotly&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

</div>

<br>

## Overview

Brain Rot Analytics examines how short-form social media consumption relates to student cognitive performance, focus habits, and self-reported wellbeing. The project follows a complete analytics lifecycle: raw data is cleaned and modeled into a SQL-based schema, explored through statistical analysis and mediation studies, and surfaced through a multi-page interactive dashboard. Machine learning notebooks extend the analysis into predictive experimentation, offering a research-oriented view of the relationships uncovered in the exploratory phase.

The project is designed as a portfolio-grade demonstration of data analysis, business intelligence, and applied machine learning practices working together in a single, cohesive repository.

<br>

## Project Highlights

| Feature | Description |
|---|---|
| **Interactive Dashboard** | Multi-page Plotly Dash application with cross-filtering across demographics, devices, and habits. |
| **Exploratory Data Analysis** | Structured Jupyter notebooks covering cleaning, transformation, and mediation analysis. |
| **SQL Data Warehouse** | Relational schema with load scripts for structured, query-ready analytical data. |
| **Behavior Analytics** | Derived metrics such as wellbeing bands, focus efficiency, and exposure ratios. |
| **Data Visualization** | Chart assets and dashboard views supporting Power BI and Tableau formats. |
| **Machine Learning Models** | Research notebooks exploring predictive modeling on behavioral and wellbeing indicators. |
| **Predictive Analytics** | Experimental models aimed at forecasting wellbeing-related outcomes from usage patterns. |

<br>

## Dataset

The analysis is built on a merged dataset of student digital habits and wellbeing indicators, including screen time, short-form video (reels) consumption, study hours, and device usage, alongside demographic attributes such as age group and region.

A few known data quality considerations are handled explicitly in the pipeline:

- Orphaned user keys are identified and addressed during data cleaning.
- Missing habit values are handled rather than silently dropped.
- The dataset does not include clinical anxiety, depression, or stress scores; proxy wellbeing measures are used instead, and this limitation is noted directly on the relevant analysis pages.



## Repository Structure

```
brain-rot-analytics/
│
├── notebooks/                 # Data exploration, cleaning, analysis, and mediation notebooks
├── raw_data/                  # Source CSV files used for the analysis
├── sql/                       # SQL schema and insert/query scripts
│
├── web_app/                   # Interactive Dash dashboard application
│   ├── app.py                 # Main application entry point
│   ├── pages/                 # Dashboard pages (Overview, Mental Health, Study, Social Media, Insights)
│   ├── components/            # Reusable UI components
│   ├── callbacks/             # App interactivity logic
│   ├── utils/                 # Charting and insight helpers
│   └── data/                  # App data loading and local CSV copies
│
├── machine_learning/          # Research notebooks and saved ML models
├── visuals/                   # Chart examples and dashboard screenshots
└── docs/                      # Supporting documentation and data dictionary
```

<br>

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language for data processing and application logic |
| Pandas / NumPy | Data cleaning, transformation, and numerical analysis |
| SQL Server | Schema design, data storage, and querying |
| Plotly / Dash | Interactive dashboard visualization and web app framework |
| Dash Bootstrap Components | UI layout and styling for the Dash application |
| Scikit-learn | Machine learning experimentation and modeling |
| Jupyter Notebook | Exploratory data analysis and research workflow |
| Power BI / Tableau | Supplementary dashboard visuals and reporting assets |

<br>

## Machine Learning

The `machine_learning/` directory contains research notebooks and saved models exploring predictive relationships between digital habits and wellbeing outcomes. These experiments are exploratory in nature and intended to complement the descriptive analysis found in the dashboard and notebooks, rather than serve as production-ready models.

<br>

## Installation

### Clone the repository

```bash
git clone https://github.com/Mahmoud-islamcs/Neuro-Digital-Analytics.git
cd brain-rot-analytics
```

### Run the dashboard

```bash
cd web_app
python app.py
```

### Open the app

```text
http://127.0.0.1:8050
```



## Contributors

<div align="left">

Developed as part of a Data Analytics graduation project.

1.	Abdelrahman Ayman Abdullah Matouk 
2.	Mahmoud Islam Mahmoud Ahmed 
3.	Ahmed Rabea Mohammed Abdelhameed
4.	Habiba Ahmed Abdelrazik Mansour

</div>

<br>

## License

This project is provided for academic and portfolio purposes. See the `LICENSE` file for details.
