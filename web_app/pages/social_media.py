import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import (
    style_fig, empty_state, guard, get_theme_tokens, get_categorical_sequence, get_stage_colors
)

dash.register_page(__name__, path="/social-media", name="Social Media", title="Social Media | Brain Rot Analytics")


def layout():
    return html.Div([
        html.Div([
            html.H2("Social Media Usage", className="page-title"),
            html.P("Reels, notifications proxy, screen-time behavior, and platform-adjacent patterns.",
                   className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="sm-reels-line", config={"displayModeBar": False})), md=8),
            dbc.Col(dcc.Loading(dcc.Graph(id="sm-peak-donut", config={"displayModeBar": False})), md=4),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="sm-hour-heatmap", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="sm-shortcontent-violin", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="sm-weekend-bar", config={"displayModeBar": False})), md=6),
        ], className="g-3 mt-1"),
    ])


@callback(
    Output("sm-reels-line", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def reels_line(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    df["FullDate"] = pd.to_datetime(df["FullDate"])
    daily = df.groupby(df["FullDate"].dt.date)["Total_Reels_Watched"].mean().reset_index()
    
    fig = go.Figure(go.Scatter(
        x=daily["FullDate"], y=daily["Total_Reels_Watched"], mode="lines",
        line=dict(color=tokens["pink"], width=2.5), fill="tozeroy",
        fillcolor="rgba(244,114,182,0.12)" if theme == "dark" else "rgba(219,39,119,0.10)"
    ))
    fig.update_layout(
        title="Average Reels Watched Over Time",
        margin=dict(l=60, r=60, t=60, b=60),
    )
    fig.update_yaxes(ticklabelstandoff=15, automargin=True)
    fig.update_xaxes(ticklabelstandoff=15, automargin=True)
    return style_fig(fig, theme=theme, height=360)


@callback(
    Output("sm-peak-donut", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def peak_donut(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    seq = get_categorical_sequence(theme)
    grp = df["Peak_Hour_Bucket"].value_counts()
    
    fig = go.Figure(go.Pie(
        labels=grp.index, 
        values=grp.values, 
        hole=0.55,
        marker=dict(colors=seq),
        textinfo="value+percent",    
        textposition="inside",         
        textfont=dict(
            family="Inter, sans-serif",
            size=13,                   
            color="#ffffff" if theme == "dark" else "#0f172a"
        )
    ))
    
    fig.update_layout(title="Peak Usage Hour Bucket")
    fig = style_fig(fig, theme=theme, height=360, legend_bottom=True)
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",     
            yanchor="top",
            y=-0.15,                
            xanchor="center",
            x=0.5                   
        ),
        margin=dict(l=20, r=20, t=65, b=100) 
    )
    return fig


@callback(
    Output("sm-hour-heatmap", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def hour_heatmap(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    df["FullDate"] = pd.to_datetime(df["FullDate"])
    pivot = df.pivot_table(index="DayOfWeek", columns="Peak_Hour", values="Total_Reels_Watched", aggfunc="mean")
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in order if d in pivot.index])
    
    bg_low = "#161c2e" if theme == "dark" else "#e2e8f0"
    fig = go.Figure(go.Heatmap(
        z=pivot.values, 
        x=pivot.columns, 
        y=pivot.index,
        colorscale=[[0, bg_low], [0.5, tokens["primary"]], [1, tokens["pink"]]],
        colorbar=dict(
            title="Reels",
            thickness=15,         
            thicknessmode="pixels",
            len=0.85,            
            ypad=10,
            xpad=15              
        )
    ))
    
    fig.update_layout(
        title="Reel Consumption Heatmap: Day of Week x Peak Hour",
        xaxis_title="Peak Hour", 
        yaxis_title=""
    )
    fig.update_xaxes(ticklabelstandoff=12, title=dict(standoff=15), automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig = style_fig(fig, theme=theme, height=380)
    fig.update_layout(margin=dict(l=90, r=110, t=65, b=65))
    return fig


@callback(
    Output("sm-shortcontent-violin", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def shortcontent_violin(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    stage_colors = get_stage_colors(theme)
    fig = px.violin(df, x="Brainrot_Stage", y="Short_Content_Percentage", color="Brainrot_Stage",
                     box=True, points=False, category_orders={"Brainrot_Stage": ["Healthy", "Casual", "Advanced", "Critical"]},
                     color_discrete_map=stage_colors)
    fig.update_layout(title="Short-Form Content % by Brain Rot Stage", showlegend=False)
    return style_fig(fig, theme=theme, height=380)


@callback(
    Output("sm-weekend-bar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def weekend_bar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    grp = df.groupby("Is_Weekend_Label")[["Total_Reels_Watched", "Short_Content_Percentage"]].mean().reset_index()
    grp["Short_Content_Percentage"] *= 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=grp["Is_Weekend_Label"], y=grp["Total_Reels_Watched"], name="Avg Reels",
                          marker_color=tokens["primary"]))
    fig.update_layout(title="Weekday vs Weekend Reel Consumption", yaxis_title="Avg Reels Watched")
    return style_fig(fig, theme=theme, height=380)
