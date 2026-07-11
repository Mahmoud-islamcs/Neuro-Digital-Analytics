import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import style_fig, empty_state, guard
from config.settings import COLORS, CATEGORICAL_SEQUENCE, WELLBEING_BAND_ORDER, WELLBEING_BAND_COLORS

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


@callback(Output("mh-wellbeing-hist", "figure"), Input("global-filtered-data", "data"))
def wellbeing_hist(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    fig = px.histogram(df, x="Wellbeing_Score", nbins=30, color="Wellbeing_Band",
                        category_orders={"Wellbeing_Band": WELLBEING_BAND_ORDER},
                        color_discrete_map=WELLBEING_BAND_COLORS)
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
    fig = style_fig(fig, height=370)
    return fig


@callback(Output("mh-band-bar", "figure"), Input("global-filtered-data", "data"))
def band_bar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df["Wellbeing_Band"].astype(str).value_counts().reindex(WELLBEING_BAND_ORDER).fillna(0)
    fig = go.Figure(go.Funnel(
        y=grp.index, x=grp.values,
        marker=dict(color=[WELLBEING_BAND_COLORS[b] for b in grp.index]),
        textinfo="value+percent total",
        textfont=dict(
            family="Inter, sans-serif",
            size=14,          
            color="#ffffff"    
        )
    ))
    fig.update_layout(
        title="Wellbeing Band Funnel",
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(
        ticklabelstandoff=15,
        automargin=True
    )
    
    return style_fig(fig, height=370)


@callback(Output("mh-attention-bar", "figure"), Input("global-filtered-data", "data"))
def attention_bar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df.groupby("Attention_Span_Level").agg(
        Avg_Focus=("Focus_Sessions_Count", "mean"),
        Avg_Wellbeing=("Wellbeing_Score", "mean"),
        Count=("ActivityID", "count"),
    ).reset_index()
    fig = px.bar(grp, x="Attention_Span_Level", y="Avg_Focus", color="Attention_Span_Level",
                 color_discrete_sequence=CATEGORICAL_SEQUENCE, text="Count")
    fig.update_traces(texttemplate="n=%{text}", textposition="outside")
    fig.update_layout(
        title="Avg Focus Sessions by Attention Span Level",
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(
        ticklabelstandoff=15,
        automargin=True
    )
    return style_fig(fig, height=370)


@callback(Output("mh-scatter-screen", "figure"), Input("global-filtered-data", "data"))
def scatter_screen(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    fig = px.scatter(df, x="Total_Reels_Watched", y="Wellbeing_Score", color="Brainrot_Exposure_Score",
                      color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
                      opacity=0.55, trendline="ols" if len(df) < 3000 else None)
    fig.update_layout(
        title="Reels Watched vs Wellbeing (color = Brain Rot Exposure)",
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(
        ticklabelstandoff=15,
        automargin=True
    )
    return style_fig(fig, height=370)


@callback(Output("mh-parallel", "figure"), Input("global-filtered-data", "data"))
def parallel_cats(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
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
        line=dict(color=sub["StageNum"], colorscale=[[0, COLORS["green"]], [0.33, COLORS["amber"]],
                                                       [0.66, "#fb923c"], [1, COLORS["red"]]]),
    ))
    fig.update_layout(
        title="Mental State Flow: Attention → Brain Rot Stage → Wellbeing → Exam Season",
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        ),
        margin=dict(l=110, r=60, t=60, b=60)
    )
    fig.update_yaxes(
        ticklabelstandoff=15,
        automargin=True
    )
    return style_fig(fig, height=420)
