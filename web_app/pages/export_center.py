import io
import json
import dash
from dash import html, dcc, callback, clientside_callback, Input, Output, ctx
import dash_bootstrap_components as dbc
import pandas as pd

from data.loader import get_master_df, get_filter_options
from utils.insights_engine import generate_insights
from utils.chart_helpers import guard
from config.settings import COLORS, APP_TITLE, APP_SUBTITLE

dash.register_page(
    __name__,
    path="/export-center",
    name="Export Center",
    title="Export Center | Brain Rot Analytics"
)


def layout():
    return html.Div([
        html.Div([
            html.H2("Executive Summary & Data Export Center", className="page-title"),
            html.P("Extract raw datasets, generate print-ready executive reports, and review active filter parameters.", className="page-subtitle"),
        ], className="page-header"),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Bulk Data Extraction", className="card-title text-primary mb-3"),
                html.P("Export the currently filtered dataset slice in standard machine-readable formats.", className="text-dim small mb-3"),
                
                html.Div([
                    dbc.Button([html.I(className="bi bi-file-earmark-spreadsheet me-2"), "Download CSV"],
                               id="btn-export-csv", color="primary", className="me-2 mb-2"),
                    dbc.Button([html.I(className="bi bi-filetype-json me-2"), "Download JSON"],
                               id="btn-export-json", color="secondary", outline=True, className="mb-2"),
                ]),
                
                dcc.Download(id="download-data-file"),
            ]), className="about-card"), md=6, xs=12),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Executive Report Generator", className="card-title text-primary mb-3"),
                html.P("Generate a clean, styled executive summary report ready for printing or PDF export.", className="text-dim small mb-3"),
                
                dbc.Button([html.I(className="bi bi-printer me-2"), "Print / Save PDF Report"],
                           id="btn-print-report", color="success", className="mb-2"),
            ]), className="about-card"), md=6, xs=12),
        ], className="g-3"),

        html.H5("Active Filter Configuration Log", className="section-title mt-4"),
        dbc.Card(dbc.CardBody([
            html.Div(id="export-filter-log"),
        ]), className="about-card mb-4"),

        html.Div([
            html.H5("Executive Report Preview", className="section-title mt-4"),
            html.Div(id="export-report-preview", className="report-preview-container p-4 rounded bg-alt border border-secondary"),
        ], className="printable-report-section"),
    ])


clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            window.print();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("btn-print-report", "id"),
    Input("btn-print-report", "n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output("download-data-file", "data"),
    Input("btn-export-csv", "n_clicks"),
    Input("btn-export-json", "n_clicks"),
    Input("global-filtered-data", "data"),
    prevent_initial_call=True,
)
def handle_data_export(n_csv, n_json, data):
    triggered = ctx.triggered_id
    if not triggered or not data:
        return dash.no_update

    df = pd.read_json(io.StringIO(data), orient="split")
    if guard(df):
        return dash.no_update

    filename = f"brain_rot_filtered_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"

    if triggered == "btn-export-csv":
        return dcc.send_data_frame(df.to_csv, f"{filename}.csv", index=False)
    elif triggered == "btn-export-json":
        return dcc.send_data_frame(df.to_json, f"{filename}.json", orient="records", date_format="iso")

    return dash.no_update


@callback(
    Output("export-filter-log", "children"),
    Output("export-report-preview", "children"),
    Input("global-filtered-data", "data"),
)
def render_export_center(data):
    df = pd.read_json(io.StringIO(data), orient="split") if data else pd.DataFrame()
    if guard(df):
        return (
            dbc.Alert("No data matches current filters.", color="warning"),
            dbc.Alert("No data matches current filters.", color="warning"),
        )

    base_df = get_master_df()

    min_date_str = str(pd.to_datetime(df['FullDate'].min()).strftime('%Y-%m-%d')) if 'FullDate' in df and len(df) else 'N/A'
    max_date_str = str(pd.to_datetime(df['FullDate'].max()).strftime('%Y-%m-%d')) if 'FullDate' in df and len(df) else 'N/A'

    log_items = [
        html.Div([html.Strong("Total Matching Records: "), f"{len(df):,} of {len(base_df):,} total ({len(df)/len(base_df)*100:.1f}%)"]),
        html.Div([html.Strong("Unique Active Users: "), f"{df['UserKey'].nunique():,} users"]),
        html.Div([html.Strong("Date Range in Sample: "), f"{min_date_str} to {max_date_str}"]),
    ]

    log_box = html.Div(log_items, className="filter-log-box font-monospace small")

    insights = generate_insights(df)

    insights_elements = []
    for ins in insights:
        insights_elements.append(
            html.Div([
                html.H6(ins["title"], className="fw-bold mb-1", style={"color": ins["color"]}),
                html.P(ins["text"], className="small text-light mb-2"),
            ], className="border-bottom border-secondary pb-2 mb-2")
        )

    report = html.Div([
        html.Div([
            html.H3(APP_TITLE, className="fw-bold text-primary mb-1"),
            html.H6(APP_SUBTITLE, className="text-dim mb-3"),
            html.Div(f"Report Generated: {pd.Timestamp.now().strftime('%B %d, %Y - %H:%M')}", className="small text-muted mb-4"),
        ], className="border-bottom border-secondary pb-3 mb-4"),

        html.H5("Key Executive Summary Metrics", className="text-light mb-3"),
        dbc.Row([
            dbc.Col(html.Div([
                html.Div("Total Records", className="small text-dim"),
                html.H4(f"{len(df):,}", className="fw-bold text-white"),
            ], className="p-3 bg-dark rounded border border-secondary mb-3"), md=3, xs=6),

            dbc.Col(html.Div([
                html.Div("Avg Wellbeing", className="small text-dim"),
                html.H4(f"{df['Wellbeing_Score'].mean():.1f}/100", className="fw-bold text-success"),
            ], className="p-3 bg-dark rounded border border-secondary mb-3"), md=3, xs=6),

            dbc.Col(html.Div([
                html.Div("Avg Brain Rot Exposure", className="small text-dim"),
                html.H4(f"{df['Brainrot_Exposure_Score'].mean():.1f}/100", className="fw-bold text-danger"),
            ], className="p-3 bg-dark rounded border border-secondary mb-3"), md=3, xs=6),

            dbc.Col(html.Div([
                html.Div("Avg Study Hours", className="small text-dim"),
                html.H4(f"{df['Study_Hours'].mean():.1f}h", className="fw-bold text-warning"),
            ], className="p-3 bg-dark rounded border border-secondary mb-3"), md=3, xs=6),
        ]),

        html.H5("Automated Statistical Insights", className="text-light mt-4 mb-3"),
        html.Div(insights_elements if insights_elements else html.P("No specific statistical contrast insights detected for this slice.", className="text-muted")),

        html.Div([
            html.P("Brain Rot Analytics Dashboard - Executive Summary Report", className="small text-muted text-center mt-4 mb-0"),
        ], className="border-top border-secondary pt-3 mt-4")
    ], className="executive-report-document")

    return log_box, report
