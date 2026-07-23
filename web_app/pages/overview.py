import io
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.chart_helpers import style_fig, empty_state, guard, get_theme_tokens, get_categorical_sequence

dash.register_page(__name__, path="/overview", name="Overview", title="Overview | Brain Rot Analytics")

NUMERIC_COLS = ["Study_Hours", "Total_Reels_Watched", "Short_Content_Percentage",
                 "Focus_Sessions_Count", "Brainrot_Exposure_Score", "Wellbeing_Score"]


def layout():
    return html.Div([
        html.Div([
            html.H2("Dataset Overview", className="page-title"),
            html.P("Demographics, distributions, and summary statistics across the filtered sample.",
                   className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="ov-age-hist", config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="ov-device-pie", config={"displayModeBar": False})), md=6),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="ov-region-sunburst", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="ov-box-multi", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),

        html.H5("Summary Statistics", className="section-title mt-4"),
        html.Div(id="ov-summary-table"),
    ])


@callback(
    Output("ov-age-hist", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def age_hist(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    tokens = get_theme_tokens(theme)
    fig = px.histogram(df[df["Age"].notna()], x="Age", nbins=18, color_discrete_sequence=[tokens["primary"]])
    fig.update_layout(
        title="Age Distribution", 
        bargap=0.1,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    fig.update_yaxes(title=dict(standoff=20), ticklabelstandoff=12, automargin=True)
    fig.update_xaxes(ticklabelstandoff=12, automargin=True) 
    return style_fig(fig, theme=theme, height=360)


@callback(
    Output("ov-region-sunburst", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def region_sunburst(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    sub = df[df["Region"] != "Unknown"]
    grp = sub.groupby(["Region", "Device_Type"]).size().reset_index(name="Count")
    tokens = get_theme_tokens(theme)
    
    device_colors = {
        "Smartphone": tokens["primary"],
        "Tablet": tokens["accent"],
        "PC": tokens["pink"],
        "Unknown": tokens["amber"]
    }
    fig = px.sunburst(
        grp, 
        path=["Region", "Device_Type"], 
        values="Count",
        color="Device_Type",                 
        color_discrete_map=device_colors     
    )
    graph_ids = fig.data[0].ids
    colors_list = []
    for item_id in graph_ids:
        found_device = False
        for device in device_colors:
            if device in item_id:
                colors_list.append(device_colors[device])
                found_device = True
                break
        if not found_device:
            colors_list.append(tokens["primary"])
            
    fig.update_traces(
        marker=dict(colors=colors_list),
        leaf=dict(opacity=0.9)
    )
    fig.update_layout(
        title="Region → Device Breakdown",
        margin=dict(l=60, r=20, t=60, b=60)
    )
    fig = style_fig(fig, theme=theme, height=380)
    fig.update_layout(margin=dict(l=10, r=10, t=55, b=15))
    return fig


@callback(
    Output("ov-device-pie", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def device_pie(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    grp = df["Device_Type"].value_counts()
    if "Unknown" in grp.index:
        grp = grp.drop("Unknown")
    
    seq = get_categorical_sequence(theme)
    fig = go.Figure(go.Pie(
        labels=grp.index, 
        values=grp.values, 
        hole=0.45,
        marker=dict(colors=seq)
    ))
    fig.update_layout(title="Device Type Share")
    return style_fig(fig, theme=theme, height=360, legend_bottom=True)


@callback(
    Output("ov-box-multi", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def box_multi(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    seq = get_categorical_sequence(theme)
    cols = NUMERIC_COLS
    fig = make_subplots(rows=1, cols=len(cols))
    for i, c in enumerate(cols):
        fig.add_trace(go.Box(y=df[c], name=c.replace("_", " "), marker_color=seq[i % len(seq)], showlegend=False), row=1, col=i + 1)
    fig.update_layout(title="Distribution of Key Metrics (Box Plots)")
    return style_fig(fig, theme=theme, height=380)


@callback(Output("ov-summary-table", "children"), Input("global-filtered-data", "data"))
def summary_table(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return dbc.Alert("No data matches the current filters.", color="warning")
    stats = df[NUMERIC_COLS].describe().T.round(2).reset_index().rename(columns={"index": "Metric"})
    return dash_table.DataTable(
        data=stats.to_dict("records"),
        columns=[{"name": c, "id": c} for c in stats.columns],
        css=[
            {
                "selector": ".dash-spreadsheet tr:hover td, .dash-spreadsheet td:hover",
                "rule": "background-color: var(--table-row-hover) !important; color: var(--text) !important;"
            }
        ],
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "var(--table-header)", "color": "var(--text)", "fontWeight": "600","border": "none"},
        style_cell={"backgroundColor": "transparent", "color": "var(--text)", "border": "none",
                    "padding": "10px", "fontFamily": "Inter, sans-serif", "fontSize": "13px"},
        style_data={"borderBottom": "1px solid var(--surface-border)"},
        style_data_conditional=[
            {"if": {"state": "active"}, "backgroundColor": "var(--table-row-selected)","color": "var(--text)", "border": "1px solid var(--primary)"},
            {"if": {"state": "selected"}, "backgroundColor": "var(--table-row-selected)","color": "var(--text)", "border": "1px solid var(--primary)"},
        ],
        page_size=10,
    )
