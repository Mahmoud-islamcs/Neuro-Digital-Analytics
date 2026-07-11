"""Global filter bar. Lives in the app shell so it persists across pages."""
from dash import html, dcc
import dash_bootstrap_components as dbc

from data.loader import get_filter_options


def _multi(id_, options, placeholder):
    return dcc.Dropdown(
        id=id_, options=[{"label": o, "value": o} for o in options],
        multi=True, placeholder=placeholder, className="filter-dd",
        persistence=False,
    )


def filter_bar():
    opt = get_filter_options()
    return html.Div([
        html.Div([
            dbc.Button(
                [html.I(className="bi bi-funnel-fill me-2"), html.Span("Filters")],
                id="filters-collapse-btn", className="filters-collapse-btn", n_clicks=0,
            ),
        ], className="filter-bar-header"),
        dbc.Collapse(
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Label("Age Group", className="filter-label"),
                        _multi("f-age-group", opt["age_group"], "All ages"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                    dbc.Col([
                        html.Label("Region", className="filter-label"),
                        _multi("f-region", opt["region"], "All regions"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                    dbc.Col([
                        html.Label("Device", className="filter-label"),
                        _multi("f-device", opt["device"], "All devices"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                    dbc.Col([
                        html.Label("Brain Rot Stage", className="filter-label"),
                        _multi("f-stage", opt["brainrot_stage"], "All stages"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                ], className="filter-grid g-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label("Wellbeing Band", className="filter-label"),
                        _multi("f-wellbeing", opt["wellbeing_band"], "All bands"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                    dbc.Col([
                        html.Label("Coffee Level", className="filter-label"),
                        _multi("f-coffee", opt["coffee_level"], "All levels"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                    dbc.Col([
                        html.Label("Smoking Status", className="filter-label"),
                        _multi("f-smoking", opt["smoking_status"], "All statuses"),
                    ], lg=3, md=6, xs=12, className="filter-field"),
                    dbc.Col([
                        html.Label("Study Hours", className="filter-label"),
                        dcc.RangeSlider(
                            id="f-study-hours",
                            min=opt["study_hours_min"], max=opt["study_hours_max"],
                            value=[opt["study_hours_min"], opt["study_hours_max"]],
                            marks=None, tooltip={"placement": "bottom", "always_visible": False},
                            className="filter-slider pt-3",
                        ),
                    ], lg=3, md=6, xs=12, className="filter-field filter-field-slider"),
                ], className="filter-grid g-3 mt-1"),
                dbc.Row([
                    dbc.Col([
                        html.Label("Date Range", className="filter-label"),
                        dcc.DatePickerRange(
                            id="f-date-range",
                            min_date_allowed=opt["date_min"], max_date_allowed=opt["date_max"],
                            start_date=opt["date_min"], end_date=opt["date_max"],
                            display_format="MMM D, YYYY", className="filter-datepicker",
                        ),
                    ], md=6, xs=12, className="filter-field filter-field-date"),
                    dbc.Col([
                        html.Div([
                            dbc.Button([html.I(className="bi bi-check2 me-1"), "Apply"],
                                       id="f-apply", color="primary", className="filter-apply-btn"),
                            dbc.Button([html.I(className="bi bi-arrow-counterclockwise me-1"), "Reset"],
                                       id="f-reset", className="filter-reset-btn"),
                        ], className="filter-actions"),
                    ], md=6, xs=12, className="filter-action-col"),
                ], className="filter-grid g-3 align-items-end"),
            ], className="filter-panel"),
            id="filters-collapse", is_open=True,
        ),
        html.Div(id="active-filter-summary", className="active-filter-summary"),
    ], className="filter-bar")
