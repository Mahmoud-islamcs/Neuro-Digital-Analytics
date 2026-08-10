<div align="center">

<img src="README_Banner.png" alt="Neuro Digital Analytics Banner" width="100%">

---

**An end-to-end Data Analytics & AI platform studying the relationship between short-form content consumption and student attention, productivity, and wellbeing.**

From a modeled star schema and Jupyter-based EDA, to an executive **Power BI dashboard**, a **machine learning prediction app**, and a **natural-language AI chatbot** — this repository covers the full analytics lifecycle in one cohesive project.

[Overview](#overview) • [Power BI Dashboard](#power-bi-dashboard) • [Machine Learning & Prediction App](#machine-learning--prediction-app) • [AI Chatbot](#ai-chatbot) • [Plotly Dash App](#plotly-dash-web-application) • [Structure](#repository-structure) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Contributors](#contributors) • [License](#license)

<br>

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat-square&logo=xgboost&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=flat-square&logo=flutter&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)
![Plotly Dash](https://img.shields.io/badge/Plotly_Dash-008DE4?style=flat-square&logo=plotly&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=flat-square&logo=microsoftsqlserver&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

<br>

## Overview

**Neuro Digital Analytics** investigates how short-form social media consumption — reels, clips, and short videos — affects student cognitive performance, study productivity, and self-reported wellbeing. The project moves through the complete analytics lifecycle: raw data cleaned and structured into a relational star schema, explored through Jupyter notebooks, and delivered through three production-facing analytics products built on the same underlying dataset:

---
##  Project Deliverables

Deliverable | Purpose | Live Demo |
|---|---|---|
**Power BI Dashboard** | Executive-grade BI reporting for stakeholders — the primary analytical deliverable of the project |  [View Dashboard](https://app.powerbi.com/groups/07cb4191-b747-423b-b7b7-fdf21a0f55bc/reports/6da0176b-4e95-4349-9a00-efd328a6733d?ctid=dee1ed73-19ca-4ce0-8066-8261fbabbeaa&pbi_source=linkShare) |
**Streamlit ML Prediction App** | A trained classification model surfaced through an interactive, user-facing prediction tool |  [Launch App](https://brainrot-analytics-egy.streamlit.app/) |
**AI Chatbot** | A natural-language interface (English & Arabic) that lets anyone query the dataset conversationally |  *Under Development* |
**Plotly Dash Dashboard** | A modern 13-page interactive analytics dashboard built with Plotly Dash for advanced data exploration and insights |  [Open Dashboard](https://a58ad2a9-2b04-4b8b-9e4f-7d63c67e53c5.plotly.app/insights) |

A supplementary 13-page **Plotly Dash** web application is also included, offering a fully custom-built alternative front end over the same data model.

The motivating question is straightforward: does heavy short-form content consumption measurably reduce a student's ability to focus and study? The data says yes — and this project quantifies how and where that relationship is strongest.

The dataset covers **5,000 daily activity records from 99 Egyptian students**, tracked across a full calendar year with demographic, device, date, and behavioral attributes organized into a fact-and-dimension schema.

<br>

## Power BI Dashboard

The **Power BI dashboard is the flagship deliverable of this project** — a polished, five-page executive report built on a custom **"Brain Glitch Digital"** dark cyberpunk theme, designed for stakeholder presentation and graduation defense. It is the primary lens through which the project's findings are meant to be consumed.

📁 File: [`dashboards_BI/Brain-rot_final_Dashboard.pbix`](dashboards_BI/Brain-rot_final_Dashboard.pbix)  
🖼️ Executive Dashboard PDF Export: Available under [`visuals/dashboards_screenshots/power_bi/Brain-rot_final_Dashboard.pdf`](visuals/dashboards_screenshots/power_bi/Brain-rot_final_Dashboard.pdf)

### Landing Page

A branded cover page — a glitch-art brain dissolving into a smartphone under the tagline **"THINK BETTER, LIVE BETTER."** Four navigation buttons (Overview, Brainrot_Exposure, Habits & Lifestyle, Time Patterns) drive page-to-page navigation and set the tone for the rest of the report.

### Overview

The executive summary page. Four headline KPI cards — Average Brain-Rot Exposure (37.70), Average Reels Watched (91), Average Study Hours (3.96), and Critical Users (907) — sit above a donut chart showing the population split across four Brain-Rot Stages (Healthy 61%, Critical 18%, Advanced 13%, Casual 8%), a comparison of Exam vs. Non-Exam study hours and reel consumption, an Age Group slicer (Child / Teen / Young), and a 12-month area chart tracking the Brain-Rot trend across the year.

### Brainrot_Exposure

A deep-dive into the core risk metric. KPI cards for Max Brain-Rot Exposure, Average Reels, and Average Focus Sessions sit alongside a Brainrot Stage slicer. A scatter plot maps every user's Total Reels Watched against their Brain-Rot Score, color-coded by stage, next to a Min/Max Reels range bar broken down by stage. Below, a Study Hours vs. Wellbeing Score scatter and a funnel-style Mental State distribution chart (Healthy 3,044 → Critical 907 → Advanced 628 → Casual) complete the page.

### Habits & Lifestyle

Connects daily habits to behavioral outcomes. KPI cards report Average Coffee/Day (2), Average Smoking Breaks (3.15), and Average Focus Sessions (3.70). A radial gauge tracks the current Target Focus Level (77.57) against a 60–95 target band. Supporting visuals include a Device Type × Brain-Rot Exposure bar (Smartphone, Tablet, PC), a Coffee & Smoking Breaks by Age Group comparison, an Is_Smoker toggle, and an Exam Season Effect table contrasting average study hours and peak reels watched between exam and non-exam periods.

### Time_Patterns

Surfaces when risky behavior actually happens during the day and week. Headline cards show All Users (5K), Critical Users (907), and the Most Peak Hour (22:00). An hourly activity bar-and-trend chart spans all 24 hours, a weekly line chart tracks Focus Sessions by day, and a monthly area chart compares Reels Watched against Study Hours across the year — filterable by Day Name, Exam Season, and Late Night flags.

### Why Power BI Leads This Project

- **Stakeholder-ready.** Built for presentation to non-technical audiences — clean KPI framing, guided navigation, and a consistent visual identity.
- **Governed, single-file deliverable.** One `.pbix` file, versioned and portable, with no runtime or server dependency to view (beyond Power BI Desktop / Power BI Service).
- **Complements, not duplicates.** While the Plotly Dash app offers deeper custom interactivity for developers, the Power BI report is the version designed to be handed to evaluators, instructors, and business stakeholders.

<br>

## Machine Learning & Prediction App

The second-priority deliverable: a trained classifier that predicts a student's **Brain-Rot Stage** — served through an interactive **Streamlit** application anyone can use without touching code.

📁 Model Artifacts & Evaluation Charts: Persisted under [`machine_learning/model/`](machine_learning/model/)  
🖼️ Visual Analytics Gallery: Extended charts available under [`visuals/charts_gallery/`](visuals/charts_gallery/)  
📸 App Screenshots: UI walkthrough captures archived in [`machine_learning/screenshots/`](machine_learning/screenshots/)

### Objective

Classify a student's `Brainrot_Stage` — one of four ordered categories (Healthy, Casual, Advanced, Critical) — from 7 daily behavioral inputs. The goal is to flag digital distraction severity early, using only observable habits rather than derived composite scores.

### Data Considerations

The target variable is meaningfully imbalanced: Healthy 61%, Critical 18%, Advanced 12.5%, Casual 8.5%. Target-derived columns (`Brainrot_Exposure_Score`, `Wellbeing_Score`, `Attention_Span_Level`, `Aura_Color_Code`, `Coffee_Level`, `Smoking_Status`) were deliberately excluded from training features to prevent leakage — these are outputs of the same behavioral process the model predicts.

### Pipeline

| Step | Details |
|---|---|
| **Data loading** | `BrainRot_Final_Dataset.csv` (5,000 rows, 30 columns) loaded via `machine_learning/utils.py` |
| **Missing value imputation** | 51 rows with missing values across `Age`, `Age_Group`, `Region`, `Device_Type`, `Is_Smoker`, `Base_Focus_Level` — imputed via median/mode |
| **Feature selection** | 7 features: `Age`, `Total_Reels_Watched`, `Coffee_Consumed_Per_Day`, `Focus_Sessions_Count`, `Study_Hours`, `Is_Late_Night`, `Device_Type` |
| **Encoding** | One-hot encoding for `Device_Type`; `Is_Late_Night` already binary |
| **Train/test split** | Stratified 80/20 split to preserve class proportions |
| **Class imbalance** | Addressed via `class_weight='balanced'` |
| **Model comparison** | Logistic Regression (baseline), Random Forest, XGBoost — each tuned with `RandomizedSearchCV` |
| **Selection criterion** | Macro F1-score, to weight minority classes fairly |
| **Persistence** | Model, encoder, scaler, and column metadata serialized via Joblib to `machine_learning/model/` |

### Final Model Performance

| Metric | Value |
|---|---|
| **Best model** | Random Forest |
| **Accuracy** | 93.8% |
| **Macro F1-score** | 0.892 |
| **Weighted F1-score** | 0.939 |

**Per-class results:**

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Healthy | 0.987 | 0.982 | 0.984 | 609 |
| Casual | 0.830 | 0.869 | 0.849 | 84 |
| Advanced | 0.790 | 0.897 | 0.840 | 126 |
| Critical | 0.945 | 0.851 | 0.895 | 181 |

**Top drivers:** Total Reels Watched (55.8%), Focus Sessions Count (19.3%), Study Hours (8.0%), Is Late Night (5.8%), Age (4.1%), Coffee Consumed Per Day (2.6%), Device Type (4.4% combined).

> [!NOTE]  
> Model evaluation artifacts (such as [`confusion_matrix.png`](machine_learning/model/confusion_matrix.png), [`feature_importance.png`](machine_learning/model/feature_importance.png), and [`classification_report.txt`](machine_learning/model/classification_report.txt)) are located in [`machine_learning/model/`](machine_learning/model/). Additional exploratory charts are archived in [`visuals/charts_gallery/`](visuals/charts_gallery/).

### The Streamlit App

📁 File: [`machine_learning/streamlit_app.py`](machine_learning/streamlit_app.py)

A lightweight, interactive multi-page Streamlit application structured into three dedicated views:

- **Predict**: Enter 7 daily behavioral habits to calculate predicted Brain-Rot Stage, class probabilities, and personalized stage-specific recommendations.
- **Insights**: Interactive model evaluation hub featuring feature importance plots, confusion matrix displays, classification reports, and a numerical correlation heatmap.
- **About**: In-depth project documentation covering dataset imputation strategies, committee presentation points, and data leakage prevention architecture.

<br>

## AI Chatbot

The third-priority deliverable: a natural-language analytics assistant built with **Flutter**, **Flask**, **Google Gemini**, and **SQL Server** — letting anyone query the dataset in plain English or Arabic, with no SQL knowledge required.

### Features

- Natural language analytics in **English & Arabic**
- AI-powered SQL generation via **Google Gemini (`gemini-2.5-flash`)**
- Intent classification (`detect_intent`) to reject unrelated / out-of-scope questions
- SQL safety validation (`is_safe_query`, `validate_columns`) before execution
- Automatic chart selection — KPI, Bar, Line, Scatter, or Table
- AI-generated insight text for every response
- **Flutter** mobile/cross-platform interface
- **Flask** REST API backend (`chatbot/backend/dp.py`) with SQLAlchemy & PyODBC connection handling
- Full loading, error, and retry states

### Architecture

```
Flutter App
      │
      ▼
Provider (MVVM)
      │
      ▼
Flask REST API
      │
      ▼
Google Gemini  →  Generate SQL + Insight
      │
      ▼
SQL Validation
      │
      ▼
SQL Server  →  Query Results
      │
      ▼
Automatic Chart Selection
      │
      ▼
Flutter Visualization
```

### Technologies

Flutter · Provider · Flask · Google Gemini API · SQL Server · SQLAlchemy · Pandas

<br>

## Plotly Dash Web Application

A supplementary, fully custom-built multi-page dashboard — included as an engineering showcase alongside the Power BI report, demonstrating the same data model rebuilt as a standalone Python web application.

🖼️ Application Screenshots: Full multi-page screenshots are available under [`visuals/dashboards_screenshots/plotly_dash/`](visuals/dashboards_screenshots/plotly_dash/)

### Key Features

| Feature | Description |
|---|---|
| **13-page Plotly Dash application** | Each page has a distinct analytical purpose, linked by a persistent collapsible sidebar. |
| **Global cross-page filtering** | One filter bar (age group, region, device, brain rot stage, wellbeing band, coffee level, smoking status, study hours range, date range) broadcasts to every chart via a shared `dcc.Store`. |
| **12 dynamic KPI cards** | Live summary metrics recalculated on every filter change. |
| **Dark / Light mode with persistent state** | Theme stored in `localStorage`, synced to every Plotly figure via a MutationObserver-driven JS engine. |
| **Automated Insights engine** | Up to 8 statistically-grounded findings computed live — no hardcoded numbers. |
| **Glassmorphism UI** | Custom dark design system in CSS with semi-transparent surfaces and Inter typography. |
| **Interactive scatter explorer** | User-controlled X/Y/color axes with OLS trendline and live Pearson r. |
| **Star schema ETL layer** | `data/loader.py` loads 5 raw CSVs, resolves known data-quality issues, merges and derives columns — cached in-process. |
| **CSV export** | Native CSV export from the Users data table and dedicated Export Center. |

### Dashboard Pages

| Page | Focus |
|---|---|
| **Home** | Executive summary — 12 KPIs, Wellbeing vs. Brain Rot time series, stage donut, region ranking, device treemap |
| **Overview** | Demographic profile, distributions, summary statistics |
| **Users** | Segment analysis, device behavior radar, top users, filterable directory |
| **Mental Health & Wellbeing** | Wellbeing, attention span, and focus proxies |
| **Social Media Usage** | Reel consumption trends, peak hours, weekday vs. weekend |
| **Study & Productivity** | Study hours, focus sessions, exam season effects |
| **Brain Rot Score** | Deep-dive into the exposure score and 3D relationship view |
| **Correlation Analysis** | Full correlation matrix, interactive explorer, scatter matrix |
| **Cohort Analysis** | User retention/engagement decay over time and behavioral user clustering |
| **What-If Simulator** | Scenario adjustment controls simulating behavioral changes on wellbeing and exposure |
| **Export Center** | Bulk dataset downloads, executive summary reports, and active filter review |
| **Automated Insights** | Auto-generated, threshold-gated findings |
| **About** | Data model card, data quality notes, full data dictionary |

### Architecture Highlights

- **Filter architecture that scales.** One global filter bar writes a single JSON payload to `dcc.Store`; every chart on every page subscribes to it as its sole input.
- **Working theme engine.** `assets/theme.js` uses a MutationObserver to detect shell class changes and re-applies layout properties to every Plotly figure via `Plotly.relayout`.
- **Documented data quality.** The two known dataset issues (orphan `UserKey=100`, null `Coffee_Level` on `HabitKey=1`) are handled explicitly in `loader.py`, not silently dropped.
- **Clean separation of concerns.** ETL logic lives in `loader.py`, constants in `settings.py`, callbacks split between filter and UI logic, and each page owns only its own charts.

<br>

## Repository Structure

```
Neuro-Digital-Analytics/
│
├── README.md
├── README_Banner.png
├── LICENSE
│
├── dashboards_BI/                     # ⭐ Priority 1 — Power BI Dashboard
│   └── Brain-rot_final_Dashboard.pbix
│
├── machine_learning/                  # ⭐ Priority 2 — ML pipeline + Streamlit app
│   ├── train_model.ipynb              # Training notebook: EDA → preprocessing → model selection → evaluation
│   ├── streamlit_app.py               # Multi-page interactive prediction app (Predict, Insights, About)
│   ├── utils.py                       # Feature list, preprocessing, column alignment helpers
│   ├── requirements.txt               # ML-specific dependencies
│   ├── data/                          # Dataset copy for ML pipeline
│   │   └── BrainRot_Final_Dataset.csv
│   ├── screenshots/                   # Streamlit UI walkthrough screenshots
│   └── model/                         # Persisted model artifacts
│       ├── brainrot_model.pkl         # Trained Random Forest (~14 MB)
│       ├── encoder.pkl                # Fitted label encoder
│       ├── scaler.pkl                 # Fitted StandardScaler
│       ├── metadata.pkl               # Training column list for inference alignment
│       ├── feature_importance.csv
│       ├── feature_importance.png
│       ├── confusion_matrix.png
│       └── classification_report.txt
│
├── chatbot/                           # ⭐ Priority 3 — AI Chatbot (Flask API + Flutter Front-End)
│   ├── backend/
│   │   ├── dp.py                      # Flask REST API with Gemini 2.5 & SQL Server engine
│   │   ├── prompts.py                 # Gemini prompt engineering & SQL schema definitions
│   │   └── requirements.txt           # Chatbot backend dependencies
│   ├── pubspec.yaml                   # Flutter project configuration
│   └── README.md
│
├── web_app/                           # Plotly Dash web application (supplementary 13-page app)
│   ├── app.py                         # Entry point — initialize Dash, layout, import callbacks
│   ├── assets/
│   │   ├── style.css                  # Custom CSS design system (~36 KB)
│   │   └── theme.js                   # Dark/light theme sync engine for Plotly figures
│   ├── callbacks/
│   │   ├── filter_callbacks.py
│   │   └── ui_callbacks.py
│   ├── components/
│   │   ├── filters.py
│   │   ├── kpi_card.py
│   │   └── sidebar.py
│   ├── config/
│   │   └── settings.py
│   ├── data/
│   │   ├── loader.py
│   │   └── raw/                       # Star schema CSVs (Fact + 4 Dims)
│   ├── pages/
│   │   ├── home.py
│   │   ├── overview.py
│   │   ├── users.py
│   │   ├── mental_health.py
│   │   ├── social_media.py
│   │   ├── study.py
│   │   ├── brain_rot.py
│   │   ├── correlation.py
│   │   ├── cohort.py
│   │   ├── simulator.py
│   │   ├── export_center.py
│   │   ├── insights.py
│   │   └── about.py
│   └── utils/
│       ├── chart_helpers.py
│       └── insights_engine.py
│
├── data/                               # Source data
│   ├── BrainRot_Final_Dataset.csv      # Raw merged dataset (5,000 rows, 30 columns)
│   ├── raw/                            # Original star schema CSV files
│   └── processed/                      # Cleaned/transformed outputs
│
├── notebooks/                          # Jupyter EDA and analysis
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_analysis.ipynb
│   └── Brain_Rot_Data_Generator.ipynb
│
├── sql/                                # SQL Server schema and load scripts
│   ├── Setup_BrainRotAnalysis.sql
│   ├── Insert_BrainRotAnalysis_Data.sql
│   └── database_erd.png
│
├── visuals/                            # Chart exports and dashboard screenshots
│   ├── README.md
│   ├── charts_gallery/                 # 14 exploratory chart PNGs
│   └── dashboards_screenshots/
│       ├── power_bi/                  # Brain-rot_final_Dashboard.pdf (Full executive report export)
│       └── plotly_dash/                # 13 page screenshots for the Plotly Dash app
│
└── docs/
    ├── Data_Dictionry.csv
    └── Final Project Proposal Form.docx
```

<br>

## Tech Stack

| Technology | Role |
|---|---|
| **Power BI** | Primary BI dashboard (`.pbix`) — executive reporting and stakeholder presentation |
| **Streamlit** | Standalone prediction interface for the trained ML model |
| **Scikit-learn** | Random Forest, Logistic Regression, StandardScaler, LabelEncoder, RandomizedSearchCV |
| **XGBoost** | Candidate model evaluated during model selection |
| **imbalanced-learn** | Imbalanced class handling during ML experimentation |
| **Joblib** | Model and artifact serialization |
| **Flutter** | AI chatbot mobile front end (MVVM architecture) |
| **Flask** | Chatbot REST API backend |
| **Google Gemini API** | Natural-language-to-SQL generation for the chatbot (`gemini-2.5-flash`) |
| **Plotly Dash** | Supplementary multi-page web application (13 pages) |
| **Plotly (Express + Graph Objects)** | Interactive chart library across Dash and notebooks |
| **Dash Bootstrap Components** | Responsive grid, modals, alerts, collapse, badges |
| **SQL Server** | Relational schema design, DDL, and data loading |
| **Pandas / NumPy** | Data loading, cleaning, merging, feature engineering |
| **Matplotlib / Seaborn** | Static charts in the training notebook |
| **Jupyter Notebook** | EDA and ML training notebooks |
| **Python 3** | Core language across the entire project |
| **HTML5 / CSS3 / JavaScript** | Custom design system and theme engine for the Dash app |

<br>

## Installation

### Prerequisites

- **Power BI Desktop** (to open the `.pbix` dashboard)
- Python 3.9 or later, pip
- Flutter SDK (for the chatbot mobile app)

### Clone the repository

```bash
git clone https://github.com/Mahmoud-islamcs/Neuro-Digital-Analytics.git
cd Neuro-Digital-Analytics
```

### Open the Power BI Dashboard

Open `dashboards_BI/Brain-rot_final_Dashboard.pbix` directly in **Power BI Desktop**.

### Run the ML Prediction App (Streamlit)

```bash
cd machine_learning
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens automatically at `http://localhost:8501`.

### Run the AI Chatbot

```bash
cd chatbot/backend
pip install -r requirements.txt
python dp.py          # starts the Flask API

cd ../               # in a separate terminal
flutter pub get
flutter run
```

### Run the Plotly Dash Dashboard (supplementary)

```bash
cd web_app
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install dash dash-bootstrap-components pandas numpy plotly
python app.py
```

Opens at `http://127.0.0.1:8050`. Respects `DASH_DEBUG` and `DASH_PORT` environment variables.

<br>

## Project Highlights

- **BI-first delivery.** The Power BI report is the primary artifact shown to stakeholders — a governed, single-file, presentation-ready deliverable independent of any runtime.
- **A leakage-free ML pipeline.** Target-derived columns are explicitly excluded from training; the same preprocessing logic is centralized in `machine_learning/utils.py` and reused identically at training and inference time.
- **A real conversational layer.** The chatbot doesn't just template canned queries — it generates, validates, and executes SQL dynamically via Gemini, then chooses its own chart type.
- **Data quality documented, not hidden.** Known dataset issues are handled explicitly in code and surfaced to users rather than silently patched.
- **Engineering depth beyond the BI layer.** The supplementary Plotly Dash app demonstrates the same insights rebuilt with full custom control over UI, theming, and filtering logic.

<br>

## Contributors

Developed as part of a Data Analytics graduation project (DEPI Program).

1. Abdelrahman Ayman Abdullah Matouk
2. Mahmoud Islam Mahmoud Ahmed
3. Ahmed Rabea Mohammed Abdelhameed
4. Habiba Ahmed Abdelrazik Mansour

<br>

## License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for full terms.

Copyright (c) 2026 Mahmoud Islam
