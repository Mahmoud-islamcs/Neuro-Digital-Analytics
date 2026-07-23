import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import (
    style_fig, empty_state, guard, get_theme_tokens, get_categorical_sequence
)

dash.register_page(
    __name__,
    path="/cohort",
    name="Cohort Analysis",
    title="Cohort Analysis | Brain Rot Analytics"
)


def layout():
    return html.Div([
        html.Div([
            html.H2("Cohort & Behavioral Segmentation Analysis", className="page-title"),
            html.P("Track user retention/engagement decay over time and identify behavioral user clusters.", className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="ch-cohort-heatmap", config={"displayModeBar": False})), md=12),
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="ch-cluster-scatter", config={"displayModeBar": False})), md=7),
            dbc.Col(dcc.Loading(dcc.Graph(id="ch-cluster-demographics", config={"displayModeBar": False})), md=5),
        ], className="g-3 mt-1"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="ch-cluster-radar", config={"displayModeBar": False})), md=12),
        ], className="g-3 mt-1"),
    ])


def _simple_kmeans(X, k=4, max_iter=100, random_state=42):
    np.random.seed(random_state)
    n_samples = len(X)
    if n_samples < k:
        return np.zeros(n_samples, dtype=int), X

    idx = np.random.choice(n_samples, k, replace=False)
    centroids = X[idx]

    labels = np.zeros(n_samples, dtype=int)
    for _ in range(max_iter):
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        new_labels = np.argmin(distances, axis=1)

        if np.all(labels == new_labels):
            break
        labels = new_labels

        for i in range(k):
            mask = labels == i
            if np.any(mask):
                centroids[i] = X[mask].mean(axis=0)

    return labels, centroids


@callback(
    Output("ch-cohort-heatmap", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def render_cohort_heatmap(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)

    tokens = get_theme_tokens(theme)
    sub = df.copy()
    sub["FullDate"] = pd.to_datetime(sub["FullDate"])
    
    user_cohorts = sub.groupby("UserKey")["FullDate"].min().dt.to_period("M").reset_index()
    user_cohorts.columns = ["UserKey", "CohortMonth"]
    sub = sub.merge(user_cohorts, on="UserKey", how="left")
    
    sub["ActivityMonth"] = sub["FullDate"].dt.to_period("M")
    
    pivot = sub.pivot_table(
        index="CohortMonth",
        columns="Month",
        values="Wellbeing_Score",
        aggfunc="mean"
    )
    
    bg_low = "#161c2e" if theme == "dark" else "#e2e8f0"
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=[str(r) for r in pivot.index],
        colorscale=[[0, bg_low], [0.5, tokens["primary"]], [1, tokens["green"]]],
        text=np.round(pivot.values, 1),
        texttemplate="%{text}",
        textfont=dict(family="Inter, sans-serif", size=11, color=tokens["text"]),
        colorbar=dict(title="Avg Wellbeing", thickness=15, len=0.85, xpad=15)
    ))

    fig.update_layout(
        title="Cohort Engagement Decay: Avg Wellbeing Score by Cohort & Activity Month",
        xaxis_title="Activity Month",
        yaxis_title="User Cohort (First Activity)",
    )

    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    fig = style_fig(fig, theme=theme, height=380)
    fig.update_layout(margin=dict(l=100, r=100, t=65, b=65))
    return fig


@callback(
    Output("ch-cluster-scatter", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def render_cluster_scatter(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)

    tokens = get_theme_tokens(theme)
    user_agg = df.groupby("UserKey").agg(
        Avg_Study=("Study_Hours", "mean"),
        Avg_Reels=("Total_Reels_Watched", "mean"),
        Avg_Wellbeing=("Wellbeing_Score", "mean"),
        Avg_BrainRot=("Brainrot_Exposure_Score", "mean"),
        Records=("ActivityID", "count")
    ).reset_index()

    if len(user_agg) < 4:
        return empty_state("Not enough user records for cluster analysis", theme=theme)

    features = user_agg[["Avg_Study", "Avg_Reels", "Avg_Wellbeing", "Avg_BrainRot"]].values
    
    mean = np.mean(features, axis=0)
    std = np.std(features, axis=0) + 1e-9
    norm_features = (features - mean) / std

    try:
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        labels = kmeans.fit_predict(norm_features)
    except Exception:
        labels, _ = _simple_kmeans(norm_features, k=4)

    cluster_names = {
        0: "Balanced Users",
        1: "Extreme Consumers",
        2: "High Performers",
        3: "At Risk Users"
    }

    user_agg["Cluster"] = [cluster_names.get(l, f"Cluster {l}") for l in labels]

    fig = px.scatter(
        user_agg,
        x="Avg_Reels",
        y="Avg_Study",
        color="Cluster",
        size="Avg_BrainRot",
        size_max=18,
        hover_data=["UserKey", "Avg_Wellbeing", "Records"],
        color_discrete_sequence=[tokens["green"], tokens["red"], tokens["primary"], tokens["amber"]]
    )

    fig.add_hline(y=user_agg["Avg_Study"].mean(), line_dash="dash", line_color=tokens["grid"],
                  annotation_text="Avg Study Hours", annotation_position="top right")
    fig.add_vline(x=user_agg["Avg_Reels"].mean(), line_dash="dash", line_color=tokens["grid"],
                  annotation_text="Avg Reels Watched", annotation_position="top right")

    fig.update_layout(
        title="Behavioral Clustering: Study Hours vs Reels Watched (K-Means)",
        xaxis_title="Avg Daily Reels Watched",
        yaxis_title="Avg Daily Study Hours",
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
        margin=dict(l=70, r=120, t=65, b=65)
    )

    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    return style_fig(fig, theme=theme, height=420)


@callback(
    Output("ch-cluster-demographics", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def render_cluster_demographics(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)

    seq = get_categorical_sequence(theme)
    user_agg = df.groupby(["UserKey", "Age_Group", "Device_Type"], observed=True).agg(
        Avg_Study=("Study_Hours", "mean"),
        Avg_Reels=("Total_Reels_Watched", "mean"),
        Avg_Wellbeing=("Wellbeing_Score", "mean"),
        Avg_BrainRot=("Brainrot_Exposure_Score", "mean")
    ).reset_index()

    if len(user_agg) < 4:
        return empty_state(theme=theme)

    features = user_agg[["Avg_Study", "Avg_Reels", "Avg_Wellbeing", "Avg_BrainRot"]].values
    mean = np.mean(features, axis=0)
    std = np.std(features, axis=0) + 1e-9
    norm_features = (features - mean) / std

    try:
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        labels = kmeans.fit_predict(norm_features)
    except Exception:
        labels, _ = _simple_kmeans(norm_features, k=4)

    cluster_names = {
        0: "Balanced Users",
        1: "Extreme Consumers",
        2: "High Performers",
        3: "At Risk Users"
    }

    user_agg["Cluster"] = [cluster_names.get(l, f"Cluster {l}") for l in labels]

    grp = user_agg.groupby(["Cluster", "Device_Type"], observed=True).size().reset_index(name="Count")

    fig = px.bar(
        grp,
        x="Cluster",
        y="Count",
        color="Device_Type",
        barmode="stack",
        color_discrete_sequence=seq
    )

    fig.update_layout(
        title="Device Composition per Cluster Segment",
        xaxis_title="Cluster Segment",
        yaxis_title="User Count",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=70, r=30, t=65, b=80)
    )

    fig.update_xaxes(ticklabelstandoff=12, automargin=True)
    fig.update_yaxes(ticklabelstandoff=12, automargin=True)
    return style_fig(fig, theme=theme, height=420)


@callback(
    Output("ch-cluster-radar", "figure"),
    Input("global-filtered-data", "data"),
    Input("theme-store", "data"),
)
def render_cluster_radar(data, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return empty_state(theme=theme)

    tokens = get_theme_tokens(theme)
    user_agg = df.groupby("UserKey").agg(
        Avg_Study=("Study_Hours", "mean"),
        Avg_Reels=("Total_Reels_Watched", "mean"),
        Avg_Wellbeing=("Wellbeing_Score", "mean"),
        Avg_BrainRot=("Brainrot_Exposure_Score", "mean"),
        Avg_Focus=("Focus_Sessions_Count", "mean")
    ).reset_index()

    if len(user_agg) < 4:
        return empty_state(theme=theme)

    features = user_agg[["Avg_Study", "Avg_Reels", "Avg_Wellbeing", "Avg_BrainRot"]].values
    mean = np.mean(features, axis=0)
    std = np.std(features, axis=0) + 1e-9
    norm_features = (features - mean) / std

    try:
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        labels = kmeans.fit_predict(norm_features)
    except Exception:
        labels, _ = _simple_kmeans(norm_features, k=4)

    cluster_names = {
        0: "Balanced Users",
        1: "Extreme Consumers",
        2: "High Performers",
        3: "At Risk Users"
    }

    user_agg["Cluster"] = [cluster_names.get(l, f"Cluster {l}") for l in labels]

    metrics = ["Avg_Study", "Avg_Reels", "Avg_Wellbeing", "Avg_BrainRot", "Avg_Focus"]
    grp = user_agg.groupby("Cluster")[metrics].mean()
    norm = (grp - grp.min()) / (grp.max() - grp.min() + 1e-9)

    fig = go.Figure()
    cluster_colors = [tokens["green"], tokens["red"], tokens["primary"], tokens["amber"]]

    for i, clus in enumerate(norm.index):
        fig.add_trace(go.Scatterpolar(
            r=norm.loc[clus].values.tolist() + [norm.loc[clus].values[0]],
            theta=[m.replace("Avg_", "") for m in metrics] + [metrics[0].replace("Avg_", "")],
            fill="toself",
            name=clus,
            line_color=cluster_colors[i % len(cluster_colors)]
        ))

    fig.update_layout(
        title="Comparative Behavioral Profile Across Clusters (Normalized)",
        showlegend=True,
    )

    return style_fig(fig, theme=theme, height=380, legend_bottom=True)
