import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.kpi_card import kpi_card, kpi_row
from utils.chart_helpers import (
    style_fig, empty_state, guard, get_theme_tokens, get_stage_colors
)
from config.settings import STAGE_ORDER
from data.loader import get_master_df

dash.register_page(__name__, path="/", name="Home", title="Home | Brain Rot Analytics")


def layout():
    return html.Div([
        html.Div([
            html.H2("Executive Summary", className="page-title"),
            html.P("A real-time pulse on student attention, wellbeing, and social-media behavior.", className="page-subtitle"),
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

    base_df = get_master_df()
    tokens = get_theme_tokens("dark")
    
    def _delta(col, is_higher_good=True, suffix="%"):
        if col not in df or col not in base_df or len(df) == 0:
            return None
        cur = df[col].mean()
        base = base_df[col].mean()
        if base == 0:
            return None
        pct = (cur - base) / base * 100
        is_pos = (pct >= 0) if is_higher_good else (pct <= 0)
        return f"{pct:+.1f}% vs baseline", is_pos

    healthy_pct = df["Is_Healthy"].mean() * 100
    base_healthy_pct = base_df["Is_Healthy"].mean() * 100
    diff_healthy = healthy_pct - base_healthy_pct
    delta_healthy = (f"{diff_healthy:+.1f}% vs baseline", diff_healthy >= 0)

    critical_pct = df["Is_Critical_Brainrot"].mean() * 100
    base_critical_pct = base_df["Is_Critical_Brainrot"].mean() * 100
    diff_critical = critical_pct - base_critical_pct
    delta_critical = (f"{diff_critical:+.1f}% vs baseline", diff_critical <= 0)

    top_region = df[df["Region"] != "Unknown"]["Region"].value_counts().idxmax() if len(df) else "N/A"
    records_pct = (len(df) / len(base_df)) * 100

    cards = [
        kpi_card("Activity Records", f"{len(df):,}", "bi bi-database-fill", tokens["primary"], delta=(f"{records_pct:.1f}% of total data", True)),
        kpi_card("Unique Users", f"{df['UserKey'].nunique():,}", "bi bi-people-fill", tokens["accent"], delta=(f"{df['UserKey'].nunique()} active sample", True)),
        kpi_card("Avg Wellbeing Score", f"{df['Wellbeing_Score'].mean():.1f}", "bi bi-heart-fill", tokens["green"], suffix="/100", delta=_delta("Wellbeing_Score", True)),
        kpi_card("Avg Brain Rot Exposure", f"{df['Brainrot_Exposure_Score'].mean():.1f}", "bi bi-cpu-fill", tokens["red"], suffix="/100", delta=_delta("Brainrot_Exposure_Score", False)),
        kpi_card("Healthy Users", f"{healthy_pct:.1f}%", "bi bi-shield-check", tokens["green"], delta=delta_healthy),
        kpi_card("Critical Users", f"{critical_pct:.1f}%", "bi bi-exclamation-triangle", tokens["red"], delta=delta_critical),
        kpi_card("Avg Study Hours", f"{df['Study_Hours'].mean():.1f}h", "bi bi-book-fill", tokens["amber"], delta=_delta("Study_Hours", True)),
        kpi_card("Avg Reels / Day", f"{df['Total_Reels_Watched'].mean():.0f}", "bi bi-phone-fill", tokens["pink"], delta=_delta("Total_Reels_Watched", False)),
        kpi_card("Avg Focus Sessions", f"{df['Focus_Sessions_Count'].mean():.1f}", "bi bi-bullseye", tokens["primary_soft"], delta=_delta("Focus_Sessions_Count", True)),
        kpi_card("Avg Short-Content %", f"{df['Short_Content_Percentage'].mean()*100:.0f}%", "bi bi-collection-play-fill", tokens["accent"], delta=_delta("Short_Content_Percentage", False)),
        kpi_card("Top Region", top_region, "bi bi-geo-alt-fill", tokens["green"]),
        kpi_card("Avg Coffee / Day", f"{df['Coffee_Consumed_Per_Day'].mean():.1f}", "bi bi-cup-hot-fill", "#c084fc", delta=_delta("Coffee_Consumed_Per_Day", False)),
    ]
    return kpi_row(cards, cols=4)


@callback(
    Output("home-trend-chart", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def update_home_trend(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    df["FullDate"] = pd.to_datetime(df["FullDate"])
    daily = df.groupby(df["FullDate"].dt.date).agg(
        Wellbeing=("Wellbeing_Score", "mean"),
        BrainRot=("Brainrot_Exposure_Score", "mean"),
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["FullDate"], y=daily["Wellbeing"], name="Wellbeing Score", mode="lines",
        line=dict(color=tokens["green"], width=2.5), fill="tozeroy", fillcolor="rgba(52,211,153,0.08)" if theme=="dark" else "rgba(5,150,105,0.08)",
        hovertemplate="Date: %{x}<br>Wellbeing Score: %{y:.1f}/100<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=daily["FullDate"], y=daily["BrainRot"], name="Brain Rot Exposure", mode="lines",
        line=dict(color=tokens["red"], width=2.5), fill="tozeroy", fillcolor="rgba(251,113,133,0.08)" if theme=="dark" else "rgba(225,29,72,0.08)",
        hovertemplate="Date: %{x}<br>Brain Rot Exposure: %{y:.1f}/100<extra></extra>"
    ))
    fig.update_layout(
        title="Wellbeing vs. Brain Rot Exposure Over Time",
        margin=dict(l=60, r=20, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    return style_fig(fig, theme=theme, height=380, legend_bottom=True)


@callback(
    Output("home-stage-donut", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def update_stage_donut(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    stage_colors = get_stage_colors(theme)
    tokens = get_theme_tokens(theme)
    counts = df["Brainrot_Stage"].astype(str).value_counts().reindex(STAGE_ORDER).fillna(0)
    
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values, hole=0.62,
        marker=dict(colors=[stage_colors[s] for s in counts.index]),
        textinfo="percent", textfont=dict(size=12),
        hovertemplate="Stage: %{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
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
        annotations=[dict(
            text="Stage", x=0.5, y=0.5, 
            font_size=16, showarrow=False, 
            font_color=tokens["text_dim"]
        )]
    )
    return style_fig(fig, theme=theme, height=380)


@callback(
    Output("home-region-bar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def update_region_bar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    tokens = get_theme_tokens(theme)
    grp = df[df["Region"] != "Unknown"].groupby("Region")["Wellbeing_Score"].agg(["mean", "count"]).sort_values("mean")
    
    fig = go.Figure(go.Bar(
        x=grp["mean"], y=grp.index, orientation="h",
        marker=dict(color=grp["mean"], colorscale=[[0, tokens["red"]], [1, tokens["green"]]]),
        text=[f"{v:.1f}" for v in grp["mean"]], textposition="outside",
        customdata=grp["count"],
        hovertemplate="Region: %{y}<br>Avg Wellbeing: %{x:.1f}/100<br>Records: %{customdata:,}<extra></extra>"
    ))
    fig.update_layout(
        title="Average Wellbeing Score by Region", 
        xaxis_title="Wellbeing Score",
        margin=dict(l=100, r=40, t=60, b=60)
    )
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig.update_xaxes(title=dict(standoff=15), automargin=True)
    return style_fig(fig, theme=theme, height=380)


@callback(
    Output("home-device-treemap", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def update_device_treemap(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)
    
    stage_colors = get_stage_colors(theme)
    grp = df.groupby(["Device_Type", "Brainrot_Stage"], observed=True).size().reset_index(name="Count")
    
    fig = px.treemap(grp, path=["Device_Type", "Brainrot_Stage"], values="Count", color="Brainrot_Stage", color_discrete_map=stage_colors)
    fig.update_layout(
        title="Device Usage x Brain Rot Stage",
        margin=dict(l=20, r=20, t=60, b=20)
    )
    fig.update_traces(textinfo="label+percent parent", hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Parent Share: %{percentParent:.1%}<extra></extra>")
    fig = style_fig(fig, theme=theme, height=380)
    fig.update_layout(margin=dict(l=5, r=5, t=50, b=5))
    return fig
