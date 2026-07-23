import io
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from utils.chart_helpers import style_fig, empty_state, guard, get_theme_tokens

dash.register_page(
    __name__,
    path="/simulator",
    name="What-If Simulator",
    title="What-If Simulator | Brain Rot Analytics"
)


def layout():
    return html.Div([
        html.Div([
            html.H2("Predictive Analytics & What-If Simulator", className="page-title"),
            html.P("Simulate behavioral changes and predict target wellbeing and brain-rot exposure outcomes.", className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Scenario Adjustment Controls", className="card-title text-primary mb-3"),
                
                html.Label("Adjust Daily Reels Watched (delta reels)", className="filter-label fw-bold mt-2"),
                dcc.Slider(
                    id="sim-reels-change", min=-100, max=100, step=5, value=-30,
                    marks={-100: "-100", -50: "-50", 0: "0 (Baseline)", 50: "+50", 100: "+100"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    className="filter-slider mb-4"
                ),

                html.Label("Adjust Daily Study Hours (delta hours)", className="filter-label fw-bold mt-2"),
                dcc.Slider(
                    id="sim-study-change", min=-5, max=5, step=0.5, value=2,
                    marks={-5: "-5h", -2.5: "-2.5h", 0: "0 (Baseline)", 2.5: "+2.5h", 5: "+5h"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    className="filter-slider mb-4"
                ),

                html.Label("Adjust Daily Focus Sessions (delta count)", className="filter-label fw-bold mt-2"),
                dcc.Slider(
                    id="sim-focus-change", min=-5, max=5, step=1, value=2,
                    marks={-5: "-5", 0: "0", 5: "+5"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    className="filter-slider mb-4"
                ),

                html.Label("Adjust Coffee Consumed (delta cups)", className="filter-label fw-bold mt-2"),
                dcc.Slider(
                    id="sim-coffee-change", min=-5, max=5, step=1, value=-1,
                    marks={-5: "-5", 0: "0", 5: "+5"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    className="filter-slider mb-2"
                ),
            ]), className="about-card"), md=5, xs=12),

            dbc.Col(html.Div(id="sim-results-container"), md=7, xs=12),
        ], className="g-3"),
    ])


def _fit_regression_model(df):
    feature_cols = ["Total_Reels_Watched", "Study_Hours", "Focus_Sessions_Count", "Coffee_Consumed_Per_Day"]
    
    clean = df[feature_cols + ["Wellbeing_Score", "Brainrot_Exposure_Score"]].dropna()
    if len(clean) < 20:
        return None

    X = clean[feature_cols].values
    X_design = np.hstack([np.ones((len(X), 1)), X])
    
    y_well = clean["Wellbeing_Score"].values
    y_rot = clean["Brainrot_Exposure_Score"].values

    try:
        coef_well, _, _, _ = np.linalg.lstsq(X_design, y_well, rcond=None)
        coef_rot, _, _, _ = np.linalg.lstsq(X_design, y_rot, rcond=None)
    except Exception:
        return None

    return {
        "feature_cols": feature_cols,
        "base_means": clean[feature_cols].mean().to_dict(),
        "base_wellbeing": clean["Wellbeing_Score"].mean(),
        "base_exposure": clean["Brainrot_Exposure_Score"].mean(),
        "coef_wellbeing": coef_well,
        "coef_exposure": coef_rot
    }


@callback(
    Output("sim-results-container", "children"),
    Input("global-filtered-data", "data"),
    Input("sim-reels-change", "value"),
    Input("sim-study-change", "value"),
    Input("sim-focus-change", "value"),
    Input("sim-coffee-change", "value"),
    Input("theme-store", "data"),
)
def render_simulation_results(data, d_reels, d_study, d_focus, d_coffee, theme):
    theme = theme or "dark"
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return dbc.Alert("No data matches the current filters for simulation.", color="warning")

    tokens = get_theme_tokens(theme)
    model = _fit_regression_model(df)
    if not model:
        return dbc.Alert("Insufficient data points to fit the statistical simulation model.", color="secondary")

    b_reels = model["base_means"]["Total_Reels_Watched"]
    b_study = model["base_means"]["Study_Hours"]
    b_focus = model["base_means"]["Focus_Sessions_Count"]
    b_coffee = model["base_means"]["Coffee_Consumed_Per_Day"]

    s_reels = max(0, b_reels + (d_reels or 0))
    s_study = max(0, b_study + (d_study or 0))
    s_focus = max(0, b_focus + (d_focus or 0))
    s_coffee = max(0, b_coffee + (d_coffee or 0))

    X_sim = np.array([1.0, s_reels, s_study, s_focus, s_coffee])

    pred_wellbeing = float(np.clip(np.dot(X_sim, model["coef_wellbeing"]), 0, 100))
    pred_exposure = float(np.clip(np.dot(X_sim, model["coef_exposure"]), 0, 100))

    base_well = model["base_wellbeing"]
    base_rot = model["base_exposure"]

    diff_well = pred_wellbeing - base_well
    diff_rot = pred_exposure - base_rot

    fig_well = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pred_wellbeing,
        number={"valueformat": ".1f", "font": {"size": 24, "color": tokens["text"]}},
        delta={"reference": base_well, "relative": False, "valueformat": "+.1f", "font": {"size": 14}},
        title={"text": "Simulated Wellbeing Score", "font": {"size": 14, "color": tokens["text"]}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": tokens["grid"]},
            "bar": {"color": tokens["green"]},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1,
            "bordercolor": tokens["grid"],
            "steps": [
                {"range": [0, 33], "color": "rgba(251,113,133,0.2)"},
                {"range": [33, 75], "color": "rgba(251,191,36,0.2)"},
                {"range": [75, 100], "color": "rgba(52,211,153,0.2)"},
            ],
            "threshold": {
                "line": {"color": tokens["text"], "width": 3},
                "thickness": 0.75,
                "value": base_well
            }
        }
    ))
    fig_well = style_fig(fig_well, theme=theme, height=270)
    fig_well.update_layout(margin=dict(l=35, r=35, t=55, b=35), autosize=True)

    fig_rot = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pred_exposure,
        number={"valueformat": ".1f", "font": {"size": 24, "color": tokens["text"]}},
        delta={"reference": base_rot, "relative": False, "valueformat": "+.1f", "increasing": {"color": tokens["red"]}, "decreasing": {"color": tokens["green"]}, "font": {"size": 14}},
        title={"text": "Simulated Brain Rot Exposure", "font": {"size": 14, "color": tokens["text"]}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": tokens["grid"]},
            "bar": {"color": tokens["red"]},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1,
            "bordercolor": tokens["grid"],
            "steps": [
                {"range": [0, 35], "color": "rgba(52,211,153,0.2)"},
                {"range": [35, 65], "color": "rgba(251,191,36,0.2)"},
                {"range": [65, 100], "color": "rgba(251,113,133,0.2)"},
            ],
            "threshold": {
                "line": {"color": tokens["text"], "width": 3},
                "thickness": 0.75,
                "value": base_rot
            }
        }
    ))
    fig_rot = style_fig(fig_rot, theme=theme, height=270)
    fig_rot.update_layout(margin=dict(l=35, r=35, t=55, b=35), autosize=True)

    color_well_badge = "success" if diff_well >= 0 else "danger"
    color_rot_badge = "success" if diff_rot <= 0 else "danger"

    return html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("Simulated Wellbeing Impact", className="text-dim mb-1"),
                html.H3(f"{pred_wellbeing:.1f} / 100", className="fw-bold mb-1", style={"color": tokens["green"]}),
                dbc.Badge(f"{diff_well:+.1f} pts vs baseline", color=color_well_badge, className="p-2"),
            ]), className="about-card text-center"), md=6),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("Simulated Brain Rot Impact", className="text-dim mb-1"),
                html.H3(f"{pred_exposure:.1f} / 100", className="fw-bold mb-1", style={"color": tokens["red"]}),
                dbc.Badge(f"{diff_rot:+.1f} pts vs baseline", color=color_rot_badge, className="p-2"),
            ]), className="about-card text-center"), md=6),
        ], className="g-3 mb-3"),

        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(figure=fig_well, config={"displayModeBar": False})), md=6),
            dbc.Col(dcc.Loading(dcc.Graph(figure=fig_rot, config={"displayModeBar": False})), md=6),
        ], className="g-3"),

        dbc.Card(dbc.CardBody([
            html.H6("Model Details & Baseline Summary", className="card-title text-primary mb-2"),
            html.P([
                f"Baseline state: {b_reels:.0f} reels/day, {b_study:.1f}h study, {b_focus:.1f} focus sessions, {b_coffee:.1f} cups coffee. ",
                f"Simulated state: {s_reels:.0f} reels/day, {s_study:.1f}h study, {s_focus:.1f} focus sessions, {s_coffee:.1f} cups coffee."
            ], className="mb-0 text-dim small"),
        ]), className="about-card mt-3")
    ])
