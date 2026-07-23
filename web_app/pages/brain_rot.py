import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils.chart_helpers import (
    style_fig, empty_state, guard, get_theme_tokens, get_stage_colors
)
from config.settings import STAGE_ORDER

dash.register_page(__name__, path="/brain-rot", name="Brain Rot Score", title="Brain Rot Score | Brain Rot Analytics")


def layout():
    return html.Div([
        html.Div([
            html.H2("Brain Rot Score Deep-Dive", className="page-title"),
            html.P("Everything about Brain Rot Exposure: distribution, classification, and top drivers.",
                   className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="br-dist-hist", config={"displayModeBar": False})), md=7),
            dbc.Col(dcc.Loading(dcc.Graph(id="br-stage-bar", config={"displayModeBar": False})), md=5),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="br-driver-bar", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="br-3d-scatter", config={"displayModeBar": False})), md=6),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="br-region-heat", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),
    ])


@callback(
    Output("br-dist-hist", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def dist_hist(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    stage_colors = get_stage_colors(theme)
    fig = px.histogram(df, x="Brainrot_Exposure_Score", nbins=30, color="Brainrot_Stage",
                        category_orders={"Brainrot_Stage": STAGE_ORDER}, color_discrete_map=stage_colors)
    
    fig.update_layout(
        title="Brain Rot Exposure Score Distribution", 
        bargap=0.02,
    )
    fig.update_xaxes(ticklabelstandoff=12, title=dict(standoff=15), automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, title=dict(standoff=15), automargin=True)
    fig = style_fig(fig, theme=theme, height=390)
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",       
            yanchor="middle",
            y=0.5,                 
            xanchor="left",
            x=1.02                 
        ),
        margin=dict(l=75, r=120, t=65, b=65) 
    )
    return fig


@callback(
    Output("br-stage-bar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def stage_bar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    stage_colors = get_stage_colors(theme)
    tokens = get_theme_tokens(theme)
    grp = df["Brainrot_Stage"].astype(str).value_counts().reindex(STAGE_ORDER).fillna(0)
    
    fig = go.Figure(go.Bar(
        x=grp.index, 
        y=grp.values, 
        marker_color=[stage_colors[s] for s in grp.index],
        text=grp.values, 
        textposition="outside",
        textfont=dict(
            family="Inter, sans-serif",
            size=13,              
            color=tokens["text"]
        )
    ))
    
    fig.update_layout(title="Users by Brain Rot Stage", showlegend=False)
    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig = style_fig(fig, theme=theme, height=390)
    fig.update_layout(margin=dict(l=75, r=30, t=65, b=65))
    return fig


@callback(
    Output("br-driver-bar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def driver_bar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    drivers = ["Total_Reels_Watched", "Short_Content_Percentage", "Study_Hours",
               "Focus_Sessions_Count", "Coffee_Consumed_Per_Day", "Smoking_Breaks_Count"]
    corr = df[drivers + ["Brainrot_Exposure_Score"]].corr(numeric_only=True)["Brainrot_Exposure_Score"].drop(
        "Brainrot_Exposure_Score").sort_values()
    colors = [tokens["green"] if v < 0 else tokens["red"] for v in corr.values]
    
    fig = go.Figure(go.Bar(
        x=corr.values, 
        y=[c.replace("_", " ") for c in corr.index], 
        orientation="h",
        marker_color=colors, 
        text=[f"{v:.2f}" for v in corr.values], 
        textposition="outside",
        textfont=dict(
            family="Inter, sans-serif",
            size=12,                
            color=tokens["text"]
        )
    ))
    
    fig.update_layout(
        title="Top Drivers of Brain Rot Exposure (correlation)", 
        xaxis_title="Correlation",
        showlegend=False,
    )
    fig.update_xaxes(ticklabelstandoff=12, title=dict(standoff=15), automargin=True)
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    fig = style_fig(fig, theme=theme, height=390)
    fig.update_layout(margin=dict(l=160, r=40, t=65, b=65))
    return fig


@callback(
    Output("br-3d-scatter", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def scatter_3d(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    stage_colors = get_stage_colors(theme)
    sample = df.sample(min(1200, len(df)), random_state=42)
    
    fig = px.scatter_3d(sample, x="Total_Reels_Watched", y="Study_Hours", z="Wellbeing_Score",
                         color="Brainrot_Stage", category_orders={"Brainrot_Stage": STAGE_ORDER},
                         color_discrete_map=stage_colors, opacity=0.7)
    
    fig.update_layout(
        title="3D View: Reels x Study Hours x Wellbeing", 
        scene=dict(
            xaxis=dict(title=dict(text="Reels Watched")),
            yaxis=dict(title=dict(text="Study Hours")),
            zaxis=dict(title=dict(text="Wellbeing Score"))
        )
    )
    fig = style_fig(fig, theme=theme, height=420)
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",      
            yanchor="middle",
            y=0.5,                 
            xanchor="left",
            x=1.05                  
        ),
        margin=dict(l=40, r=120, t=65, b=40) 
    )
    return fig


@callback(
    Output("br-region-heat", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def region_heat(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    sub = df[df["Region"] != "Unknown"]
    pivot = sub.pivot_table(index="Region", columns="Brainrot_Stage", values="ActivityID",
                             aggfunc="count", observed=True).reindex(columns=STAGE_ORDER).fillna(0)
    pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    
    bg_low = "#161c2e" if theme == "dark" else "#e2e8f0"
    fig = go.Figure(go.Heatmap(
        z=pct.values, 
        x=pct.columns, 
        y=pct.index,
        colorscale=[[0, bg_low], [0.5, tokens["amber"]], [1, tokens["red"]]],
        text=pct.round(0).values,
        texttemplate="%{text}%",
        textfont=dict(
            family="Inter, sans-serif",
            size=12,                   
            color=tokens["text"]
        ),
        colorbar=dict(
            title="% of region",
            thickness=15,             
            thicknessmode="pixels",
            len=0.85,                
            ypad=10,
            xpad=15                     
        )
    ))
    
    fig.update_layout(title="Brain Rot Stage Composition by Region (% within region)")
    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig = style_fig(fig, theme=theme, height=420)
    fig.update_layout(margin=dict(l=110, r=120, t=65, b=65))
    return fig