import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import (
    style_fig, empty_state, guard, get_theme_tokens, get_wellbeing_colors, get_categorical_sequence
)
from config.settings import WELLBEING_BAND_ORDER

dash.register_page(__name__, path="/mental-health", name="Mental Health", title="Mental Health | Brain Rot Analytics")

NOTE = ("Note: this dataset does not include clinical anxiety/depression/stress scales. "
        "The metrics below (Wellbeing Score, Attention Span Level, Focus Sessions) are the "
        "closest real proxies available and are used instead of fabricated clinical scores.")


def layout():
    return html.Div([
        html.Div([
            html.H2("Mental Health & Wellbeing", className="page-title"),
            html.P("Wellbeing, attention span, and focus patterns across the student population.",
                   className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="mh-wellbeing-hist", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="mh-band-bar", config={"displayModeBar": False})), md=6),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="mh-attention-bar", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="mh-scatter-screen", config={"displayModeBar": False})), md=6),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="mh-parallel", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),
    ])


@callback(
    Output("mh-wellbeing-hist", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def wellbeing_hist(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    well_colors = get_wellbeing_colors(theme)
    tokens = get_theme_tokens(theme)
    
    fig = px.histogram(df, x="Wellbeing_Score", nbins=30, color="Wellbeing_Band",
                        category_orders={"Wellbeing_Band": WELLBEING_BAND_ORDER},
                        color_discrete_map=well_colors)
    
    mean_val = df["Wellbeing_Score"].mean()
    fig.add_vline(x=mean_val, line_dash="dash", line_color=tokens["accent"],
                  annotation_text=f"Sample Mean ({mean_val:.1f})", annotation_position="top left",
                  annotation_font=dict(color=tokens["accent"], size=11))

    fig.update_layout(
        title="Wellbeing Score Distribution", 
        bargap=0.05,
        showlegend=True,
        legend=dict(
            orientation="v",       
            yanchor="middle",
            y=0.5,                  
            xanchor="left",
            x=1.02                  
        ),
        margin=dict(l=70, r=120, t=60, b=60)
    )

    fig.update_yaxes(title=dict(standoff=15), ticklabelstandoff=12, automargin=True)
    fig.update_xaxes(title=dict(standoff=15), ticklabelstandoff=12, automargin=True)
    fig = style_fig(fig, theme=theme, height=370)
    return fig


@callback(
    Output("mh-band-bar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def band_bar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    well_colors = get_wellbeing_colors(theme)
    tokens = get_theme_tokens(theme)
    grp = df["Wellbeing_Band"].astype(str).value_counts().reindex(WELLBEING_BAND_ORDER).fillna(0)
    
    fig = go.Figure(go.Funnel(
        y=grp.index, x=grp.values,
        marker=dict(color=[well_colors[b] for b in grp.index]),
        textinfo="value+percent total",
        textfont=dict(
            family="Inter, sans-serif",
            size=14,          
            color="#ffffff" if theme == "dark" else "#0f172a"
        )
    ))
    fig.update_layout(
        title="Wellbeing Band Funnel",
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    return style_fig(fig, theme=theme, height=370)


@callback(
    Output("mh-attention-bar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def attention_bar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    seq = get_categorical_sequence(theme)
    grp = df.groupby("Attention_Span_Level").agg(
        Avg_Focus=("Focus_Sessions_Count", "mean"),
        Avg_Wellbeing=("Wellbeing_Score", "mean"),
        Count=("ActivityID", "count"),
    ).reset_index()
    
    fig = px.bar(grp, x="Attention_Span_Level", y="Avg_Focus", color="Attention_Span_Level",
                 color_discrete_sequence=seq, text="Count")
    fig.update_traces(texttemplate="n=%{text}", textposition="outside")
    fig.update_layout(
        title="Avg Focus Sessions by Attention Span Level",
        showlegend=False,
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    return style_fig(fig, theme=theme, height=370)


@callback(
    Output("mh-scatter-screen", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def scatter_screen(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    fig = px.scatter(df, x="Total_Reels_Watched", y="Wellbeing_Score", color="Brainrot_Exposure_Score",
                      color_continuous_scale=[[0, tokens["green"]], [0.5, tokens["amber"]], [1, tokens["red"]]],
                      opacity=0.55, trendline="ols" if len(df) < 3000 else None)
    
    fig.add_hline(y=50, line_dash="dot", line_color=tokens["amber"],
                  annotation_text="Wellbeing Threshold (50)", annotation_position="bottom right",
                  annotation_font=dict(color=tokens["amber"], size=11))
    mean_reels = df["Total_Reels_Watched"].mean()
    fig.add_vline(x=mean_reels, line_dash="dash", line_color=tokens["primary_soft"],
                  annotation_text=f"Avg Reels ({mean_reels:.0f})", annotation_position="top right",
                  annotation_font=dict(color=tokens["primary_soft"], size=11))

    fig.update_layout(
        title="Reels Watched vs Wellbeing (color = Brain Rot Exposure)",
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    return style_fig(fig, theme=theme, height=370)


@callback(
    Output("mh-parallel", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def parallel_cats(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    stage_map = {"Healthy": 0, "Casual": 1, "Advanced": 2, "Critical": 3}
    band_map = {"Critical": 0, "At Risk": 1, "Moderate": 2, "Healthy": 3}
    sub = df.copy()
    sub["StageNum"] = sub["Brainrot_Stage"].astype(str).map(stage_map)
    sub["BandNum"] = sub["Wellbeing_Band"].astype(str).map(band_map)
    
    fig = go.Figure(go.Parcats(
        dimensions=[
            dict(values=sub["Attention_Span_Level"], label="Attention Span"),
            dict(values=sub["Brainrot_Stage"].astype(str), label="Brain Rot Stage"),
            dict(values=sub["Wellbeing_Band"].astype(str), label="Wellbeing Band"),
            dict(values=sub["Is_Exam_Season_Label"], label="Exam Season"),
        ],
        line=dict(color=sub["StageNum"], colorscale=[[0, tokens["green"]], [0.33, tokens["amber"]],
                                                       [0.66, "#fb923c"], [1, tokens["red"]]]),
    ))
    fig.update_layout(
        title="Mental State Flow: Attention -> Brain Rot Stage -> Wellbeing -> Exam Season",
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    return style_fig(fig, theme=theme, height=420)
