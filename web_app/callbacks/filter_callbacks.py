from dash import callback, Input, Output, State, ctx, html
import dash_bootstrap_components as dbc
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
    opt = get_filter_options()

    triggered = ctx.triggered_id
    if triggered == "f-reset":
        filtered = df
        summary = html.Div([
            html.Span([
                html.I(className="bi bi-funnel me-1 text-secondary"),
                "All Data (0 Active Filters)",
                html.Span(" • ", className="mx-1 text-muted"),
                html.I(className="bi bi-database me-1 text-muted"),
                f"{len(df):,} total records"
            ], className="filter-status-pill")
        ], className="d-inline-flex align-items-center")
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
    active_count = 0
    for label, val in [("Age", age_group), ("Region", region), ("Device", device),
                        ("Stage", stage), ("Wellbeing", wellbeing), ("Coffee", coffee),
                        ("Smoking", smoking)]:
        if val:
            active_bits.append(f"{label}: {', '.join(val)}")
            active_count += 1

    if study_hours and (study_hours[0] > opt["study_hours_min"] or study_hours[1] < opt["study_hours_max"]):
        active_count += 1
        active_bits.append(f"Study: {study_hours[0]:.1f}h - {study_hours[1]:.1f}h")

    if start_date and end_date and (pd.to_datetime(start_date) > pd.to_datetime(opt["date_min"]) or pd.to_datetime(end_date) < pd.to_datetime(opt["date_max"])):
        active_count += 1
        active_bits.append("Custom Date Range")

    summary_text = " • ".join(active_bits) if active_bits else "No active filters"
    badge_label = f"{active_count} Active Filter{'s' if active_count != 1 else ''}" if active_count > 0 else "All Data"

    summary = html.Div([
        html.Span([
            html.I(className="bi bi-funnel-fill me-1 text-primary" if active_count > 0 else "bi bi-funnel me-1"),
            badge_label,
            html.Span(" • ", className="mx-1 text-muted"),
            html.I(className="bi bi-database-check me-1 text-success" if active_count > 0 else "bi bi-database me-1"),
            f"{len(filtered):,} of {len(df):,} records ({len(filtered)/len(df)*100:.1f}%)",
            f" — {summary_text}" if active_bits else ""
        ], className="filter-status-pill")
    ], className="d-inline-flex align-items-center")

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
    Output("filters-collapse", "className"),
    Output("filters-collapse-btn", "children"),
    Input("filters-collapse-btn", "n_clicks"),
    State("filters-collapse", "className"),
    prevent_initial_call=True,
)
def toggle_filters(n, current_class):
    current = current_class or "filter-container-collapsible"
    if "filter-container-collapsed" in current:
        return "filter-container-collapsible", [
            html.I(className="bi bi-sliders me-2"),
            html.Span("Filter Command Center")
        ]
    else:
        return "filter-container-collapsible filter-container-collapsed", [
            html.I(className="bi bi-funnel me-2"),
            html.Span("Filter Command Center")
        ]
