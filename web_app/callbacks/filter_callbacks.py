"""
The single source of truth for filtering: reads every filter widget in the
global filter bar, applies them to the master dataframe, and pushes the
resulting filtered slice (as JSON) into dcc.Store(id='global-filtered-data').
Every page's charts subscribe to that store as their only Input.
"""
from dash import callback, Input, Output, State, ctx, html
import pandas as pd

from data.loader import get_master_df, apply_filters, get_filter_options


@callback(
    Output("global-filtered-data", "data"),
    Output("active-filter-summary", "children"),
    Input("f-apply", "n_clicks"),
    Input("f-reset", "n_clicks"),
    State("f-age-group", "value"), State("f-region", "value"), State("f-device", "value"),
    State("f-stage", "value"), State("f-wellbeing", "value"), State("f-coffee", "value"),
    State("f-smoking", "value"), State("f-study-hours", "value"),
    State("f-date-range", "start_date"), State("f-date-range", "end_date"),
    prevent_initial_call=False,
)
def apply_global_filters(n_apply, n_reset, age_group, region, device, stage, wellbeing,
                          coffee, smoking, study_hours, start_date, end_date):
    df = get_master_df()

    triggered = ctx.triggered_id
    if triggered == "f-reset":
        filtered = df
        summary = html.Span([html.I(className="bi bi-check-circle me-1"), "Showing all data (filters reset)"])
        return filtered.to_json(date_format="iso", orient="split"), summary

    f = {
        "age_group": age_group, "region": region, "device": device,
        "brainrot_stage": stage, "wellbeing_band": wellbeing,
        "coffee_level": coffee, "smoking_status": smoking,
    }
    if study_hours:
        f["study_hours_range"] = study_hours
    if start_date and end_date:
        f["date_range"] = [pd.to_datetime(start_date), pd.to_datetime(end_date)]

    filtered = apply_filters(df, f)

    active_bits = []
    for label, val in [("Age", age_group), ("Region", region), ("Device", device),
                        ("Stage", stage), ("Wellbeing", wellbeing), ("Coffee", coffee),
                        ("Smoking", smoking)]:
        if val:
            active_bits.append(f"{label}: {', '.join(val)}")
    summary_text = " • ".join(active_bits) if active_bits else "No filters applied"
    summary = html.Span([
        html.I(className="bi bi-funnel me-1"),
        f"{len(filtered):,} of {len(df):,} records — {summary_text}",
    ])
    return filtered.to_json(date_format="iso", orient="split"), summary


@callback(
    Output("f-age-group", "value"), Output("f-region", "value"), Output("f-device", "value"),
    Output("f-stage", "value"), Output("f-wellbeing", "value"), Output("f-coffee", "value"),
    Output("f-smoking", "value"), Output("f-study-hours", "value"),
    Output("f-date-range", "start_date"), Output("f-date-range", "end_date"),
    Input("f-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filter_widgets(n):
    opt = get_filter_options()
    return (None, None, None, None, None, None, None,
            [opt["study_hours_min"], opt["study_hours_max"]], opt["date_min"], opt["date_max"])


@callback(
    Output("filters-collapse", "is_open"),
    Input("filters-collapse-btn", "n_clicks"),
    State("filters-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_filters(n, is_open):
    return not is_open
