import io
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import style_fig, empty_state, guard
from config.settings import COLORS, CATEGORICAL_SEQUENCE, STAGE_ORDER, STAGE_COLORS

dash.register_page(__name__, path="/users", name="Users", title="Users | Brain Rot Analytics")


def layout():
    return html.Div([
        html.Div([
            html.H2("Users", className="page-title"),
            html.P("Who the students are: demographics, device habits, and behavioral segments.",className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="us-gender-proxy", config={"displayModeBar": False})), md=4),
            dbc.Col(dcc.Loading(dcc.Graph(id="us-device-radar", config={"displayModeBar": False})), md=4),
            dbc.Col(dcc.Loading(dcc.Graph(id="us-smoker-donut", config={"displayModeBar": False})), md=4),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="us-segment-scatter", config={"displayModeBar": False})), md=7),
            dbc.Col(dcc.Loading(dcc.Graph(id="us-topusers-bar", config={"displayModeBar": False})), md=5),
        ], className="g-3 mt-1"),

        html.H5("User Directory", className="section-title mt-4"),
        html.Div(id="us-table"),
    ])


@callback(Output("us-gender-proxy", "figure"), Input("global-filtered-data", "data"))
def age_group_bar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df.groupby(["Age_Group", "Device_Type"]).size().reset_index(name="Count")
    fig = px.bar(grp, x="Age_Group", y="Count", color="Device_Type", barmode="group",color_discrete_sequence=CATEGORICAL_SEQUENCE)
    fig.update_layout(
        title="Age Group by Device Type",
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#1f2331",
            bordercolor="#7c5cff",
            font_size=13,
            font_color="#ffffff"
        ),
        
        margin=dict(l=70, r=20, t=60, b=80)
        )
    fig.update_yaxes(
        title=dict(standoff=15),    
        ticklabelstandoff=12,      
        automargin=True
    )
    
    fig.update_xaxes(
        title=dict(standoff=15),  
        ticklabelstandoff=12,      
        automargin=True
    )
    
    fig = style_fig(fig, height=350, legend_bottom=True)
    
    return fig


@callback(Output("us-device-radar", "figure"), Input("global-filtered-data", "data"))
def device_radar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    metrics = ["Study_Hours", "Total_Reels_Watched", "Focus_Sessions_Count", "Wellbeing_Score","Brainrot_Exposure_Score"]
    grp = df.groupby("Device_Type")[metrics].mean()
    norm = (grp - grp.min()) / (grp.max() - grp.min() + 1e-9)
    fig = go.Figure()
    for i, dev in enumerate(norm.index):
        fig.add_trace(go.Scatterpolar(
            r=norm.loc[dev].values.tolist() + [norm.loc[dev].values[0]],
            theta=metrics + [metrics[0]], fill="toself", name=dev,
            line_color=CATEGORICAL_SEQUENCE[i % len(CATEGORICAL_SEQUENCE)],
        ))
    fig.update_layout(
        title="Behavior Profile by Device (normalized)",
        polar=dict(radialaxis=dict(visible=True, showticklabels=False, gridcolor=COLORS["grid"]),
        bgcolor="rgba(0,0,0,0)"),
                showlegend=False,

        hoverlabel=dict(
            bgcolor="#1f2331",
            bordercolor="#7c5cff",
            font_size=13,
            font_color="#ffffff"
        ),
        # margin=dict(l=70, r=20, t=60, b=80)
        )
    return style_fig(fig, height=350, legend_bottom=True)


@callback(Output("us-smoker-donut", "figure"), Input("global-filtered-data", "data"))
def smoker_donut(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df["Smoking_Status"].value_counts()
    fig = go.Figure(go.Pie(labels=grp.index, values=grp.values, hole=0.55,
                            marker=dict(colors=CATEGORICAL_SEQUENCE)))
    fig.update_layout(
        title="Smoking Status Share",
        showlegend=True,
        legend=dict(
            orientation="h",       
            yanchor="bottom",      
            y=-0.30,              
            xanchor="center",     
            x=0.5                 
        ),
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        annotations=[dict(
            text="Stage", x=0.5, y=0.5, 
            font_size=16, showarrow=False, 
            font_color=COLORS["text_dim"]
        )])
    return style_fig(fig, height=350, legend_bottom=True)


@callback(Output("us-segment-scatter", "figure"), Input("global-filtered-data", "data"))
def segment_scatter(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    fig = px.scatter(df, x="Study_Hours", y="Wellbeing_Score", color="Brainrot_Stage",
                      size="Total_Reels_Watched", size_max=18, opacity=0.65,
                      category_orders={"Brainrot_Stage": STAGE_ORDER},
                      color_discrete_map=STAGE_COLORS,
                      hover_data=["Age_Group", "Region"])
    fig.update_layout(
        title="User Segmentation: Study Hours vs Wellbeing (bubble = reels watched)",
        showlegend=True,
        legend=dict(
            orientation="v",        
            yanchor="middle",
            y=0.5,                 
            xanchor="left",
            x=1.02                 
        ),
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        
        margin=dict(l=70, r=120, t=60, b=60)
    )
    fig.update_yaxes(
        title=dict(standoff=15),  
        ticklabelstandoff=12,      
        automargin=True
    )
    
    fig.update_xaxes(
        title=dict(standoff=15),   
        ticklabelstandoff=12,       
        automargin=True
    )
    fig = style_fig(fig, height=420)
    
    return fig


@callback(Output("us-topusers-bar", "figure"), Input("global-filtered-data", "data"))
def top_users_bar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df[df["Username"] != "Unknown User"].groupby("Username")["Wellbeing_Score"].mean() \
        .sort_values(ascending=False).head(10)
    fig = go.Figure(go.Bar(x=grp.values, y=grp.index, orientation="h",
                            marker=dict(color=COLORS["green"]),
                            text=[f"{v:.1f}" for v in grp.values], textposition="outside"))
    fig.update_layout(
        title="Top 10 Users by Avg Wellbeing Score", 
        yaxis=dict(autorange="reversed"),
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        margin=dict(l=110, r=60, t=60, b=60)
        )
    fig.update_yaxes(
        ticklabelstandoff=12, 
        automargin=True
    )
    
    fig.update_xaxes(
        ticklabelstandoff=12, 
        automargin=True
    )
    return style_fig(fig, height=420)


@callback(Output("us-table", "children"), Input("global-filtered-data", "data"))
def users_table(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return dbc.Alert("No data matches the current filters.", color="warning")
    agg = df.groupby(["UserKey", "Username", "Age_Group", "Region", "Device_Type"], observed=True).agg(
        Records=("ActivityID", "count"),
        Avg_Study_Hours=("Study_Hours", "mean"),
        Avg_Wellbeing=("Wellbeing_Score", "mean"),
        Avg_BrainRot=("Brainrot_Exposure_Score", "mean"),
    ).reset_index().round(1).sort_values("Avg_Wellbeing", ascending=False)
    return dash_table.DataTable(
        data=agg.to_dict("records"),
        columns=[{"name": c.replace("_", " "), "id": c} for c in agg.columns],
        css=[
            {
                "selector": ".dash-spreadsheet tr:hover td, .dash-spreadsheet td:hover",
                "rule": "background-color: #1f2331 !important; color: #ffffff !important;"
            },
            {
                "selector": ".dash-filter input",
                "rule": "background-color: #151a29 !important; color: var(--text) !important; border: 1px solid var(--surface-border) !important; border-radius: 6px !important; padding: 4px 8px !important;"
            },
            {
                "selector": ".export",
                "rule": "background-color: #7c5cff !important; color: white !important; border: none !important; border-radius: 6px !important; padding: 6px 16px !important; font-weight: 600 !important; cursor: pointer !important; margin-bottom: 12px !important; transition: background 0.2s;"
            },
            {
                "selector": ".export:hover",
                "rule": "background-color: #6346d1 !important;"
            }
        ],
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "var(--table-header)", 
            "color": "var(--text)",
            "fontWeight": "600", 
            "border": "none",
            "padding": "12px 10px",
            "fontFamily": "Inter, sans-serif"
        },
        style_cell={
            "backgroundColor": "transparent", 
            "color": "var(--text)", 
            "border": "none",
            "padding": "12px 10px", 
            "fontFamily": "Inter, sans-serif", 
            "fontSize": "13px"
        },
        style_data={"borderBottom": "1px solid var(--surface-border)"},
        style_data_conditional=[
            {"if": {"state": "active"}, "backgroundColor": "var(--table-row-selected)",
             "color": "var(--text)", "border": "1px solid var(--primary)"},
            {"if": {"state": "selected"}, "backgroundColor": "var(--table-row-selected)",
             "color": "var(--text)", "border": "1px solid var(--primary)"},
        ],
        sort_action="native", filter_action="native", page_size=10,export_format="csv",
    )
