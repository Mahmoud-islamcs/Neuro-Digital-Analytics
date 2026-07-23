from dash import html, dcc
import dash_bootstrap_components as dbc

from data.loader import get_filter_options


def _multi(id_, options, placeholder):
    return dcc.Dropdown(
        id=id_,
        options=[{"label": o, "value": o} for o in options],
        multi=True,
        placeholder=placeholder,
        className="filter-dd",
        persistence=False,
    )


def filter_bar():
    opt = get_filter_options()
    return html.Div([
        html.Div([
            dbc.Button(
                [html.I(className="bi bi-sliders me-2"), html.Span("Filter Command Center")],
                id="filters-collapse-btn", className="filters-collapse-btn", n_clicks=0,
            ),
            html.Div(id="active-filter-summary", className="active-filter-summary"),
        ], className="filter-bar-header mb-2"),
        html.Div(
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-people-fill me-2 text-primary"),
                                html.Span("Demographics & Device", className="filter-group-title"),
                            ], className="filter-group-header mb-3"),
                            html.Div([
                                html.Div([
                                    html.Label("Age Group", className="filter-label"),
                                    _multi("f-age-group", opt["age_group"], "All ages"),
                                ], className="filter-field mb-3"),
                                html.Div([
                                    html.Label("Region", className="filter-label"),
                                    _multi("f-region", opt["region"], "All regions"),
                                ], className="filter-field mb-3"),
                                html.Div([
                                    html.Label("Device Type", className="filter-label"),
                                    _multi("f-device", opt["device"], "All devices"),
                                ], className="filter-field mb-2"),
                            ], className="d-flex flex-column h-100 justify-content-start"),
                        ], className="filter-group-card h-100"),
                    ], lg=4, md=6, xs=12),

                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-heart-pulse-fill me-2 text-danger"),
                                html.Span("Mental State & Habits", className="filter-group-title"),
                            ], className="filter-group-header mb-3"),
                            html.Div([
                                html.Div([
                                    html.Label("Brain Rot Stage", className="filter-label"),
                                    _multi("f-stage", opt["brainrot_stage"], "All stages"),
                                ], className="filter-field"),
                                html.Div([
                                    html.Label("Wellbeing Band", className="filter-label"),
                                    _multi("f-wellbeing", opt["wellbeing_band"], "All bands"),
                                ], className="filter-field"),
                                html.Div([
                                    html.Label("Coffee Level", className="filter-label"),
                                    _multi("f-coffee", opt["coffee_level"], "All levels"),
                                ], className="filter-field"),
                                html.Div([
                                    html.Label("Smoking Status", className="filter-label"),
                                    _multi("f-smoking", opt["smoking_status"], "All statuses"),
                                ], className="filter-field"),
                            ], className="filter-2x2-grid"),
                        ], className="filter-group-card h-100"),
                    ], lg=4, md=6, xs=12),

                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-clock-history me-2 text-info"),
                                html.Span("Time & Study Thresholds", className="filter-group-title"),
                            ], className="filter-group-header mb-3"),
                            html.Div([
                                html.Div([
                                    html.Label("Study Hours Range", className="filter-label"),
                                    dcc.RangeSlider(
                                        id="f-study-hours",
                                        min=opt["study_hours_min"], max=opt["study_hours_max"],
                                        value=[opt["study_hours_min"], opt["study_hours_max"]],
                                        marks=None, tooltip={"placement": "bottom", "always_visible": False},
                                        className="filter-slider pt-2",
                                    ),
                                ], className="filter-field mb-3"),
                                html.Div([
                                    html.Label("Calendar Date Range", className="filter-label"),
                                    dcc.DatePickerRange(
                                        id="f-date-range",
                                        min_date_allowed=opt["date_min"], max_date_allowed=opt["date_max"],
                                        start_date=opt["date_min"], end_date=opt["date_max"],
                                        display_format="MMM D, YYYY", className="filter-datepicker w-100",
                                    ),
                                ], className="filter-field mb-3"),
                                html.Div([
                                    dbc.Button([html.I(className="bi bi-check2-circle me-1"), "Apply Filters"],
                                               id="f-apply", color="primary", className="filter-apply-btn flex-fill"),
                                    dbc.Button([html.I(className="bi bi-arrow-counterclockwise me-1"), "Reset All"],
                                               id="f-reset", className="filter-reset-btn flex-fill"),
                                ], className="filter-actions-row mt-auto pt-2"),
                            ], className="d-flex flex-column h-100 justify-content-between"),
                        ], className="filter-group-card h-100"),
                    ], lg=4, md=12, xs=12),
                ], className="g-3 align-items-stretch"),
            ], className="filter-panel"),
            id="filters-collapse", className="filter-container-collapsible",
        ),
    ], className="filter-bar")
