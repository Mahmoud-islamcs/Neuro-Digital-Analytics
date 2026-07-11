import io
import dash
from dash import html, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from utils.insights_engine import generate_insights
from utils.chart_helpers import guard

dash.register_page(__name__, path="/insights", name="Insights", title="Insights | Brain Rot Analytics")


def layout():
    return html.Div([
        html.Div([
            html.H2("Automated Insights", className="page-title"),
            html.P("Statistically-grounded findings, recomputed live from the current filtered sample.",
                   className="page-subtitle"),
        ], className="page-header"),
        html.Div(id="insights-cards"),
    ])


def _insight_card(ins):
    return dbc.Col(
        dbc.Card(dbc.CardBody([
            html.Div(html.I(className=ins["icon"]), className="insight-icon",
                      style={"background": f"{ins['color']}22", "color": ins["color"]}),
            html.H6(ins["title"], className="insight-title"),
            html.P(ins["text"], className="insight-text"),
        ]), className="insight-card"),
        md=6, xs=12, className="mb-3",
    )


@callback(Output("insights-cards", "children"), Input("global-filtered-data", "data"))
def render_insights(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return dbc.Alert("No data matches the current filters.", color="warning")
    insights = generate_insights(df)
    if not insights:
        return dbc.Alert(
            "Not enough contrast in the current filtered sample to generate confident insights. "
            "Try widening your filters.", color="secondary")
    return dbc.Row([_insight_card(i) for i in insights], className="g-3")
