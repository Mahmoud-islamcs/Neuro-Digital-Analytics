import io
import dash
from dash import dash_table, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About", title="About | Brain Rot Analytics")

DATA_DICTIONARY = [
    {"Table": "Dim_Users", "Column": "UserKey", "Role": "Primary Key", "Description": "Unique user identifier"},
    {"Table": "Dim_Users", "Column": "Age", "Role": "Attribute", "Description": "User age in years"},
    {"Table": "Dim_Users", "Column": "Age_Group", "Role": "Attribute", "Description": "Child / Teen / Young bucket"},
    {"Table": "Dim_Users", "Column": "Region", "Role": "Attribute", "Description": "User's region in Egypt"},
    {"Table": "Dim_Users", "Column": "Device_Type", "Role": "Attribute", "Description": "Smartphone / Tablet / PC"},
    {"Table": "Dim_Users", "Column": "Is_Smoker", "Role": "Flag", "Description": "1 if the user smokes, else 0"},
    {"Table": "Dim_Users", "Column": "Base_Focus_Level", "Role": "Attribute", "Description": "Baseline focus capacity score"},
    {"Table": "Dim_Date", "Column": "DateKey", "Role": "Primary Key", "Description": "YYYYMMDD integer date key"},
    {"Table": "Dim_Date", "Column": "Is_Late_Night", "Role": "Flag", "Description": "1 if activity logged late at night"},
    {"Table": "Dim_Date", "Column": "Is_Exam_Season", "Role": "Flag", "Description": "1 if date falls in exam season"},
    {"Table": "Dim_Date", "Column": "Is_Weekend", "Role": "Flag", "Description": "1 if the date is a weekend"},
    {"Table": "Dim_MentalState", "Column": "StateKey", "Role": "Primary Key", "Description": "Unique mental-state identifier"},
    {"Table": "Dim_MentalState", "Column": "Attention_Span_Level", "Role": "Attribute", "Description": "High / Medium / Cooked / Fried"},
    {"Table": "Dim_MentalState", "Column": "Brainrot_Stage", "Role": "Attribute", "Description": "Healthy / Casual / Advanced / Critical"},
    {"Table": "Dim_MentalState", "Column": "Aura_Color_Code", "Role": "Attribute", "Description": "Green / Yellow / Red aura tag"},
    {"Table": "Dim_Habits", "Column": "HabitKey", "Role": "Primary Key", "Description": "Unique habit combination identifier"},
    {"Table": "Dim_Habits", "Column": "Coffee_Level", "Role": "Attribute", "Description": "None / Moderate / Addict"},
    {"Table": "Dim_Habits", "Column": "Smoking_Status", "Role": "Attribute", "Description": "Non-Smoker / Occasional / Heavy-Smoker"},
    {"Table": "Fact_User_Activity", "Column": "ActivityID", "Role": "Primary Key", "Description": "Unique activity record id"},
    {"Table": "Fact_User_Activity", "Column": "Study_Hours", "Role": "Measure", "Description": "Hours studied that day"},
    {"Table": "Fact_User_Activity", "Column": "Coffee_Consumed_Per_Day", "Role": "Measure", "Description": "Cups of coffee consumed"},
    {"Table": "Fact_User_Activity", "Column": "Smoking_Breaks_Count", "Role": "Measure", "Description": "Number of smoking breaks"},
    {"Table": "Fact_User_Activity", "Column": "Total_Reels_Watched", "Role": "Measure", "Description": "Short-form video clips watched"},
    {"Table": "Fact_User_Activity", "Column": "Short_Content_Percentage", "Role": "Measure", "Description": "Share of viewing time that is short-form (0-1)"},
    {"Table": "Fact_User_Activity", "Column": "Peak_Hour", "Role": "Measure", "Description": "Hour of day (0-23) with peak activity"},
    {"Table": "Fact_User_Activity", "Column": "Focus_Sessions_Count", "Role": "Measure", "Description": "Number of deliberate focus sessions"},
    {"Table": "Fact_User_Activity", "Column": "Brainrot_Exposure_Score", "Role": "Measure", "Description": "0-100 composite brain-rot exposure score"},
    {"Table": "Fact_User_Activity", "Column": "Wellbeing_Score", "Role": "Measure", "Description": "0-100 composite wellbeing score"},
]

def layout():
    return html.Div([
        html.Div([
            html.H2("About This Project", className="page-title"),
            html.P("Brain Rot Analysis: how short-form social media consumption relates to student "
                   "wellbeing, attention, and study habits.", className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5([html.I(className="bi bi-diagram-3-fill me-2"), "Data Model"]),
                html.P("A star schema with one fact table and four dimensions:"),
                html.Ul([
                    html.Li("Fact_User_Activity — grain: one row per user per day (5,000 rows)"),
                    html.Li("Dim_Users — 99 real users + 1 synthetic 'Unknown User' for an orphan FK"),
                    html.Li("Dim_Date — full calendar year 2026, with exam-season / weekend / late-night flags"),
                    html.Li("Dim_MentalState — Brain Rot Stage: Healthy → Casual → Advanced → Critical"),
                    html.Li("Dim_Habits — coffee level and smoking status"),
                ]),
            ]), className="about-card"), md=6),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5([html.I(className="bi bi-exclamation-triangle-fill me-2"), "Data Quality Notes"]),
                html.P("Two issues were found and handled explicitly during ETL, not silently patched:"),
                html.Ul([
                    html.Li("UserKey=100 appears in 51 fact rows with no match in Dim_Users — kept and "
                            "labeled 'Unknown User' rather than dropped."),
                    html.Li("Dim_Habits had 1 null Coffee_Level (on the 'no habits' row) — filled as 'None'."),
                ]),
                html.P("GPA, Anxiety, Depression, and Stress are NOT present in this dataset. Wellbeing "
                       "Score, Brain Rot Exposure Score, and Attention Span Level are used as the real "
                       "proxies throughout the dashboard instead of fabricating clinical metrics.",
                       className="fw-semibold mt-2"),
            ]), className="about-card"), md=6),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5([html.I(className="bi bi-book-half me-2"), "Data Dictionary"]),
                dash_table.DataTable(
                    data=DATA_DICTIONARY,
                    columns=[{"name": c, "id": c} for c in DATA_DICTIONARY[0].keys()],
                    style_as_list_view=True,
                    page_action='none', 
                    
                    css=[
                        {
                            "selector": ".dash-spreadsheet tr:hover td, .dash-spreadsheet td:hover",
                            "rule": "background-color: var(--table-row-hover) !important; color: var(--text) !important;"
                        }
                    ],
                    
                    style_header={"backgroundColor": "var(--table-header)", "color": "var(--text)", "fontWeight": "600"},
                    style_cell={"backgroundColor": "transparent", "color": "var(--text)",
                               "border": "1px solid var(--surface-border)", "padding": "8px"},
                    style_table={"overflowX": "auto"},
                )
            ]), className="about-card"), md=12),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5([html.I(className="bi bi-tools me-2"), "Built With"]),
                html.Div([
                    dbc.Badge("Plotly Dash", className="tech-badge"),
                    dbc.Badge("Dash Bootstrap Components", className="tech-badge"),
                    dbc.Badge("Pandas", className="tech-badge"),
                    dbc.Badge("Plotly Express / Graph Objects", className="tech-badge"),
                ]),
            ]), className="about-card"), md=12),
        ], className="g-3 mt-1"),
    ])
