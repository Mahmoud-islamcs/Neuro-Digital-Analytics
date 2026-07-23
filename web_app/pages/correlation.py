import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import (
    style_fig, empty_state, guard, get_theme_tokens, get_stage_colors
)

dash.register_page(__name__, path="/correlation", name="Correlation Analysis", title="Correlation | Brain Rot Analytics")

NUMERIC_COLS = ["Study_Hours", "Coffee_Consumed_Per_Day", "Smoking_Breaks_Count", "Total_Reels_Watched",
                 "Short_Content_Percentage", "Peak_Hour", "Focus_Sessions_Count",
                 "Brainrot_Exposure_Score", "Wellbeing_Score"]


def layout():
    return html.Div([
        html.Div([
            html.H2("Correlation Analysis", className="page-title"),
            html.P("Explore how numeric behaviors relate to each other across the filtered sample.",
                   className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="cr-heatmap", config={"displayModeBar": False})), md=12),
        ], className="g-3"),

        dbc.Row([
            dbc.Col([
                html.Label("X axis", className="filter-label"),
                dcc.Dropdown(id="cr-x", options=[{"label": c.replace("_", " "), "value": c} for c in NUMERIC_COLS],
                             value="Total_Reels_Watched", className="filter-dd"),
            ], md=3),
            dbc.Col([
                html.Label("Y axis", className="filter-label"),
                dcc.Dropdown(id="cr-y", options=[{"label": c.replace("_", " "), "value": c} for c in NUMERIC_COLS],
                             value="Wellbeing_Score", className="filter-dd"),
            ], md=3),
            dbc.Col([
                html.Label("Color by", className="filter-label"),
                dcc.Dropdown(id="cr-color",
                             options=[{"label": c, "value": c} for c in ["Brainrot_Stage", "Wellbeing_Band", "Device_Type", "Region"]],
                             value="Brainrot_Stage", className="filter-dd"),
            ], md=3),
        ], className="g-3 mt-2"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="cr-explorer-scatter", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="cr-scatter-matrix", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="cr-top-pos-neg", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),
    ])


@callback(
    Output("cr-heatmap", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def corr_heatmap(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    corr = df[NUMERIC_COLS].corr(numeric_only=True)
    bg_mid = "#161c2e" if theme == "dark" else "#f1f5f9"
    
    fig = go.Figure(go.Heatmap(
        z=corr.values, 
        x=[c.replace("_", " ") for c in corr.columns], 
        y=[c.replace("_", " ") for c in corr.index],
        colorscale=[[0, tokens["red"]], [0.5, bg_mid], [1, tokens["green"]]], 
        zmid=0,
        text=corr.round(2).values, 
        texttemplate="%{text}", 
        textfont=dict(
            family="Inter, sans-serif",
            size=10,                  
            color=tokens["text"]
        ),
        colorbar=dict(
            title="Correlation",
            thickness=15,           
            thicknessmode="pixels",
            len=0.8,                 
            ypad=10,
            xpad=15                     
        )
    ))
    
    fig.update_layout(title="Correlation Matrix - All Numeric Metrics")
    fig.update_xaxes(tickangle=45, ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig = style_fig(fig, theme=theme, height=520)
    fig.update_layout(margin=dict(l=150, r=110, t=75, b=120))
    return fig


@callback(
    Output("cr-explorer-scatter", "figure"),
    Input("global-filtered-data", "data"),
    Input("cr-x", "value"),
    Input("cr-y", "value"),
    Input("cr-color", "value"),
    Input("theme-store", "data"),
)
def explorer_scatter(data, x, y, color, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df) or not x or not y:
        return empty_state(theme=theme)
    
    r = df[x].corr(df[y])
    stage_colors = get_stage_colors(theme)
    fig = px.scatter(df, x=x, y=y, color=color, opacity=0.55,
                     color_discrete_map=stage_colors if color == "Brainrot_Stage" else None,
                     trendline="ols" if len(df) < 3000 else None)
    
    clean_x = x.replace('_', ' ')
    clean_y = y.replace('_', ' ')
    
    fig.update_layout(title=f"{clean_x} vs {clean_y} (r = {r:.2f})")
    fig.update_xaxes(title=dict(text=clean_x, standoff=15), ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(title=dict(text=clean_y, standoff=15), ticklabelstandoff=12, automargin=True)
    
    fig.update_coloraxes(
        colorbar=dict(
            thickness=15,             
            thicknessmode="pixels",
            len=0.85,                
            xpad=15                     
        )
    )
    fig = style_fig(fig, theme=theme, height=420)
    fig.update_layout(
        showlegend=True if color else False,
        legend=dict(
            orientation="v",          
            yanchor="middle",
            y=0.5,                     
            xanchor="left",
            x=1.03                      
        ),
        margin=dict(l=85, r=130, t=65, b=65)
    )
    return fig


@callback(
    Output("cr-scatter-matrix", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def scatter_matrix(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    dims = ["Study_Hours", "Total_Reels_Watched", "Brainrot_Exposure_Score", "Wellbeing_Score"]
    stage_colors = get_stage_colors(theme)
    sample = df.sample(min(800, len(df)), random_state=42)
    
    fig = px.scatter_matrix(sample, dimensions=dims, color="Brainrot_Stage",
                             color_discrete_map=stage_colors)
    fig.update_traces(diagonal_visible=False, showupperhalf=True, marker=dict(size=4, opacity=0.55))
    fig.update_layout(title="Scatter Matrix - Core Behavioral Metrics")
    return style_fig(fig, theme=theme, height=650, legend_bottom=True)


@callback(
    Output("cr-top-pos-neg", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def top_pos_neg(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    corr = df[NUMERIC_COLS].corr(numeric_only=True)
    vals = []
    cols = corr.columns.tolist()
    
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            clean_i = cols[i].replace("_", " ")
            clean_j = cols[j].replace("_", " ")
            vals.append((f"{clean_i} <-> {clean_j}", corr.iloc[i, j]))
            
    s = pd.Series({k: v for k, v in vals}).dropna().sort_values()
    top = pd.concat([s.head(5), s.tail(5)])
    colors = [tokens["red"] if v < 0 else tokens["green"] for v in top.values]
    
    fig = go.Figure(go.Bar(
        x=top.values, 
        y=top.index, 
        orientation="h",
        marker_color=colors, 
        text=[f"{v:.2f}" for v in top.values], 
        textposition="outside",
        textfont=dict(
            family="Inter, sans-serif",
            size=12,                  
            color=tokens["text"]
        )
    ))
    
    fig.update_layout(title="Strongest Positive & Negative Correlations", showlegend=False)
    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    fig = style_fig(fig, theme=theme, height=420)
    fig.update_layout(margin=dict(l=260, r=45, t=75, b=65))
    return fig