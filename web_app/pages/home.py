import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.kpi_card import kpi_card, kpi_row
from utils.chart_helpers import style_fig, empty_state, guard
from config.settings import COLORS, STAGE_ORDER, STAGE_COLORS, WELLBEING_BAND_ORDER, WELLBEING_BAND_COLORS

dash.register_page(__name__, path="/", name="Home", title="Home | Brain Rot Analytics")


def layout():
    return html.Div([
        html.Div([
            html.H2("Executive Summary", className="page-title"),
            html.P("A real-time pulse on student attention, wellbeing, and social-media behavior.",className="page-subtitle"),
        ], className="page-header"),

        html.Div(id="home-kpis"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="home-trend-chart", config={"displayModeBar": False})), md=8),
            dbc.Col(dcc.Loading(dcc.Graph(id="home-stage-donut", config={"displayModeBar": False})), md=4),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="home-region-bar", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="home-device-treemap", config={"displayModeBar": False})), md=6),
        ], className="g-3 mt-1"),
    ])


@callback(Output("home-kpis", "children"), Input("global-filtered-data", "data"))
def update_home_kpis(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return dbc.Alert("No data matches the current filters.", color="warning")

    healthy_pct = df["Is_Healthy"].mean() * 100
    critical_pct = df["Is_Critical_Brainrot"].mean() * 100
    top_region = df[df["Region"] != "Unknown"]["Region"].value_counts().idxmax() if len(df) else "N/A"

    cards = [
        kpi_card("Activity Records", f"{len(df):,}", "bi bi-database-fill", COLORS["primary"]),
        kpi_card("Unique Users", f"{df['UserKey'].nunique():,}", "bi bi-people-fill", COLORS["accent"]),
        kpi_card("Avg Wellbeing Score", f"{df['Wellbeing_Score'].mean():.1f}", "bi bi-heart-fill",COLORS["green"], suffix="/100"),
        kpi_card("Avg Brain Rot Exposure", f"{df['Brainrot_Exposure_Score'].mean():.1f}","bi bi-cpu-fill", COLORS["red"], suffix="/100"),
        kpi_card("Healthy Users", f"{healthy_pct:.1f}%", "bi bi-shield-check", COLORS["green"]),
        kpi_card("Critical Users", f"{critical_pct:.1f}%", "bi bi-exclamation-triangle", COLORS["red"]),
        kpi_card("Avg Study Hours", f"{df['Study_Hours'].mean():.0f}h", "bi bi-book-fill", COLORS["amber"]),
        kpi_card("Avg Reels / Day", f"{df['Total_Reels_Watched'].mean():.0f}", "bi bi-phone-fill",COLORS["pink"]),
        kpi_card("Avg Focus Sessions", f"{df['Focus_Sessions_Count'].mean():.0f}", "bi bi-bullseye",COLORS["primary_soft"]),
        kpi_card("Avg Short-Content %", f"{df['Short_Content_Percentage'].mean()*100:.0f}%","bi bi-collection-play-fill", COLORS["accent"]),
        kpi_card("Top Region", top_region, "bi bi-geo-alt-fill", COLORS["green"]),
        kpi_card("Avg Coffee / Day", f"{df['Coffee_Consumed_Per_Day'].mean():.0f}", "bi bi-cup-hot-fill", "#c084fc"),
    ]
    return kpi_row(cards, cols=4)


@callback(Output("home-trend-chart", "figure"), Input("global-filtered-data", "data"))
def update_home_trend(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    df["FullDate"] = pd.to_datetime(df["FullDate"])
    daily = df.groupby(df["FullDate"].dt.date).agg(
        Wellbeing=("Wellbeing_Score", "mean"),
        BrainRot=("Brainrot_Exposure_Score", "mean"),
    ).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["FullDate"], y=daily["Wellbeing"], name="Wellbeing Score", mode="lines", line=dict(color=COLORS["green"], width=2.5), fill="tozeroy", fillcolor="rgba(52,211,153,0.08)"))
    fig.add_trace(go.Scatter(x=daily["FullDate"], y=daily["BrainRot"], name="Brain Rot Exposure", mode="lines", line=dict(color=COLORS["red"], width=2.5),fill="tozeroy", fillcolor="rgba(251,113,133,0.08)"))
    fig.update_layout(
        title="Wellbeing vs. Brain Rot Exposure Over Time",
        
        hoverlabel=dict(
            bgcolor="#1f2331",
            bordercolor="#7c5cff",
            font_size=13,
            font_color="#ffffff"
        ),
        
        margin=dict(l=60, r=20, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=12, automargin=True) 
    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    return style_fig(fig, height=380, legend_bottom=True)
    


@callback(Output("home-stage-donut", "figure"), Input("global-filtered-data", "data"))
def update_stage_donut(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    counts = df["Brainrot_Stage"].astype(str).value_counts().reindex(STAGE_ORDER).fillna(0)
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values, hole=0.62,
        marker=dict(colors=[STAGE_COLORS[s] for s in counts.index]),
        textinfo="percent", textfont=dict(size=12),
    ))
    fig.update_layout(
        title="Brain Rot Stage Distribution", 
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
        )]
    )
    
    return style_fig(fig, height=380)


@callback(Output("home-region-bar", "figure"), Input("global-filtered-data", "data"))
def update_region_bar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df[df["Region"] != "Unknown"].groupby("Region")["Wellbeing_Score"].mean().sort_values()
    fig = go.Figure(go.Bar(
        x=grp.values, y=grp.index, orientation="h",
        marker=dict(color=grp.values, colorscale=[[0, COLORS["red"]], [1, COLORS["green"]]]),
        text=[f"{v:.1f}" for v in grp.values], textposition="outside",
    ))
    fig.update_layout(
        title="Average Wellbeing Score by Region", 
        xaxis_title="Wellbeing Score",
        
        hoverlabel=dict(
            bgcolor="#1f2331",
            bordercolor="#7c5cff",
            font_size=13,
            font_color="#ffffff"
        ),
        
        margin=dict(l=100, r=40, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig.update_xaxes(title=dict(standoff=15), automargin=True)
    return style_fig(fig, height=380)


@callback(Output("home-device-treemap", "figure"), Input("global-filtered-data", "data"))
def update_device_treemap(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df.groupby(["Device_Type", "Brainrot_Stage"], observed=True).size().reset_index(name="Count")
    fig = px.treemap(grp, path=["Device_Type", "Brainrot_Stage"], values="Count",color="Brainrot_Stage", color_discrete_map=STAGE_COLORS)
    fig.update_layout(
        title="Device Usage x Brain Rot Stage",
        
        hoverlabel=dict(
            bgcolor="#1f2331",
            bordercolor="#7c5cff",
            font_size=13,
            font_color="#ffffff"
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    fig.update_traces(textinfo="label+percent parent")
    fig = style_fig(fig, height=380)
    fig.update_layout(
        margin=dict(l=5, r=5, t=50, b=5), 
    )
    
    return fig
