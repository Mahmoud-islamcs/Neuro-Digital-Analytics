import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import style_fig, empty_state, guard
from config.settings import COLORS, CATEGORICAL_SEQUENCE, STAGE_ORDER, STAGE_COLORS

dash.register_page(__name__, path="/study", name="Study & Productivity", title="Study | Brain Rot Analytics")

NOTE = ("Note: GPA is not present in this dataset. Study Hours and Focus Sessions Count are used "
        "as the real productivity proxies instead.")


def layout():
    return html.Div([
        html.Div([
            html.H2("Study & Productivity", className="page-title"),
            html.P("Study hours, focus sessions, and how habits interact with productivity.",
                   className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="st-hours-density", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="st-coffee-bar", config={"displayModeBar": False})), md=6),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="st-scatter-brainrot", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="st-exam-box", config={"displayModeBar": False})), md=6),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="st-waterfall", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),
    ])


@callback(Output("st-hours-density", "figure"), Input("global-filtered-data", "data"))
def hours_density(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    fig = px.histogram(df, x="Study_Hours", color="Brainrot_Stage", nbins=25, marginal="rug",
                        category_orders={"Brainrot_Stage": STAGE_ORDER}, color_discrete_map=STAGE_COLORS,
                        histnorm="probability density")
    
    fig.update_layout(
        title="Study Hours Density by Brain Rot Stage", 
        bargap=0.02,
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        )
    )
    
    fig.update_xaxes(
        ticklabelstandoff=12,
        title=dict(standoff=15),   
        automargin=True
    )
    
    fig.update_yaxes(
        title=dict(standoff=25), 
        ticklabelstandoff=12,     
        automargin=True
    )
    
    fig = style_fig(fig, height=380)
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",        
            yanchor="middle",
            y=0.5,                  
            xanchor="left",
            x=1.02                  
        ),
        margin=dict(l=85, r=120, t=65, b=65) 
    )
    
    return fig


@callback(Output("st-coffee-bar", "figure"), Input("global-filtered-data", "data"))
def coffee_bar(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df.groupby("Coffee_Level").agg(Avg_Study=("Study_Hours", "mean"),
                                         Avg_Focus=("Focus_Sessions_Count", "mean")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=grp["Coffee_Level"], y=grp["Avg_Study"], name="Avg Study Hours",
                          marker_color=COLORS["amber"]))
    fig.add_trace(go.Bar(x=grp["Coffee_Level"], y=grp["Avg_Focus"], name="Avg Focus Sessions",
                          marker_color=COLORS["accent"]))
    
    fig.update_layout(
        title="Coffee Level vs Study Hours & Focus Sessions", 
        barmode="group",
        
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        )
    )
    
    fig.update_xaxes(
        ticklabelstandoff=12,
        automargin=True
    )
    fig.update_yaxes(
        ticklabelstandoff=12,
        automargin=True
    )
    
    fig = style_fig(fig, height=380)
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",      
            yanchor="middle",
            y=0.5,                 
            xanchor="left",
            x=1.02                 
        ),
        margin=dict(l=70, r=150, t=65, b=65) 
    )
    
    return fig


@callback(Output("st-scatter-brainrot", "figure"), Input("global-filtered-data", "data"))
def scatter_brainrot(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    
    fig = px.scatter(df, x="Study_Hours", y="Brainrot_Exposure_Score", color="Focus_Sessions_Count",
                      color_continuous_scale=[[0, COLORS["red"]], [1, COLORS["green"]]], opacity=0.6)
    
    fig.update_layout(
        title="Study Hours vs Brain Rot Exposure (color = Focus Sessions)",
        
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        )
    )
    
    fig.update_xaxes(
        ticklabelstandoff=12,
        title=dict(standoff=15),   
        automargin=True
    )
    fig.update_yaxes(
        ticklabelstandoff=12,
        title=dict(standoff=15), 
        automargin=True
    )
    
    fig.update_coloraxes(
        colorbar=dict(
            thickness=15,          
            thicknessmode="pixels",
            len=0.85,            
            xpad=15               
        )
    )
    
    fig = style_fig(fig, height=380)
    
    fig.update_layout(
        margin=dict(l=85, r=110, t=65, b=65)
    )
    
    return fig


@callback(Output("st-exam-box", "figure"), Input("global-filtered-data", "data"))
def exam_box(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    fig = px.box(df, x="Is_Exam_Season_Label", y="Study_Hours", color="Is_Exam_Season_Label",
                 color_discrete_sequence=[COLORS["accent"], COLORS["primary"]])
    
    fig.update_layout(
        title="Study Hours: Exam Season vs Regular Days", 
        showlegend=False,
        
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        )
    )
    
    fig.update_xaxes(
        ticklabelstandoff=12,
        title=dict(standoff=15),   
        automargin=True
    )
    fig.update_yaxes(
        ticklabelstandoff=12,
        title=dict(standoff=15),   
        automargin=True
    )
    
    fig = style_fig(fig, height=380)
    
    fig.update_layout(
        margin=dict(l=75, r=20, t=65, b=65)
    )
    
    return fig


@callback(Output("st-waterfall", "figure"), Input("global-filtered-data", "data"))
def waterfall(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state()
    grp = df.groupby("Brainrot_Stage", observed=True)["Focus_Sessions_Count"].mean().reindex(STAGE_ORDER).dropna()
    diffs = grp.diff().fillna(grp.iloc[0])
    
    fig = go.Figure(go.Waterfall(
        x=grp.index, y=diffs.values, measure=["absolute"] + ["relative"] * (len(grp) - 1),
        text=[f"{v:.1f}" for v in grp.values],
        textposition="outside",      
        
        textfont=dict(
            family="Inter, sans-serif",
            size=12,                
            color="#ffffff"          
        ),
        
        decreasing=dict(marker=dict(color=COLORS["red"])),
        increasing=dict(marker=dict(color=COLORS["green"])),
        totals=dict(marker=dict(color=COLORS["primary"])),
    ))
    
    fig.update_layout(
        title="Avg Focus Sessions Progression Across Brain Rot Stages",
        
        hoverlabel=dict(
            bgcolor="#1f2331",      
            bordercolor="#7c5cff",    
            font_size=13,             
            font_color="#ffffff"       
        )
    )
    
    fig.update_xaxes(
        ticklabelstandoff=12,
        automargin=True
    )
    fig.update_yaxes(
        ticklabelstandoff=12,
        automargin=True
    )
    
    fig = style_fig(fig, height=380)
    
    fig.update_layout(
        margin=dict(l=75, r=30, t=65, b=65)
    )
    
    return fig