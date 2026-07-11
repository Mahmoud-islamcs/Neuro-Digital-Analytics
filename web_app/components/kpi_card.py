"""Reusable KPI card -- icon, big number, label, and optional delta."""
import dash_bootstrap_components as dbc
from dash import html

from config.settings import COLORS


def kpi_card(title, value, icon, color=COLORS["primary"], suffix="", delta=None,
             spark_values=None, tooltip=None, card_id=None):
    """
    A single glassmorphism KPI tile.
    delta: tuple (text, is_positive) e.g. ("+4.2% vs prev period", True)
    """
    delta_el = None
    if delta:
        text, is_pos = delta
        delta_color = COLORS["green"] if is_pos else COLORS["red"]
        icon_cls = "bi bi-arrow-up-short" if is_pos else "bi bi-arrow-down-short"
        delta_el = html.Div([
            html.I(className=icon_cls),
            html.Span(text, className="ms-1"),
        ], className="kpi-delta", style={"color": delta_color})

    body = [
        html.Div([
            html.Div(html.I(className=icon), className="kpi-icon",
                     style={"background": f"{color}22", "color": color}),
        ], className="kpi-header"),
        html.Div([
            html.Span(f"{value}", className="kpi-value"),
            html.Span(suffix, className="kpi-suffix"),
        ], className="kpi-value-row"),
        html.Div(title, className="kpi-title", title=tooltip or title),
    ]
    if delta_el is not None:
        body.append(delta_el)

    card_kwargs = dict(className="kpi-card")
    if card_id is not None:
        card_kwargs["id"] = card_id
    return dbc.Card(dbc.CardBody(body), **card_kwargs)


def kpi_row(cards, cols=4):
    """Lay out a list of kpi_card() elements in a responsive grid."""
    width = max(1, 12 // cols)
    return dbc.Row(
        [dbc.Col(c, xs=12, sm=6, md=width, className="mb-3") for c in cards],
        className="g-3",
    )
