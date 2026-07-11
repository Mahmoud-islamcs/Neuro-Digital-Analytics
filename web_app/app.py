"""
Brain Rot Analytics -- main application entry point.

Run with:  python app.py
Then open: http://127.0.0.1:8050
"""
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from components.sidebar import sidebar
from components.filters import filter_bar
from config.settings import APP_TITLE

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css",
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    ],
    suppress_callback_exceptions=True,
    title=APP_TITLE,
    update_title=None,
)

# app = dash.Dash(__name__, external_stylesheets=[...])     problem here 
server = app.server  # for gunicorn / wsgi deployment

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="global-filtered-data"),
    dcc.Store(id="theme-store", storage_type="local", data="dark"),
    html.Button(html.I(className="bi bi-list"), id="sidebar-toggle",
                className="sidebar-toggle-btn", title="Toggle navigation",
                **{"aria-label": "Toggle navigation"}),
    sidebar(),
    html.Div([
        html.Div([
            html.Div([
                html.H1(APP_TITLE, className="topbar-title"),
            ], className="topbar-left"),
            html.Div([
                html.Button(html.I(className="bi bi-moon-stars-fill"), id="theme-toggle",
                            className="icon-btn", title="Theme (dark mode default)"),
            ], className="topbar-right"),
        ], className="topbar"),

        html.Div(filter_bar(), id="global-filter-shell", className="global-filter-shell"),

        html.Div(dash.page_container, className="page-container"),
    ], className="main-content"),
    html.Button(html.I(className="bi bi-arrow-up-short"), id="back-to-top",
                className="back-to-top-btn", title="Back to top",
                **{"aria-label": "Back to top"}),
], className="app-shell theme-dark", id="app-shell", **{"data-bs-theme": "dark"})

# Register callback modules (they attach to `app` via the @callback decorator).
from callbacks import filter_callbacks, ui_callbacks  # noqa: E402,F401

if __name__ == "__main__":
    import os
    debug = os.environ.get("DASH_DEBUG", "true").lower() == "true"
    port = int(os.environ.get("DASH_PORT", "8050"))
    app.run(debug=debug, host="127.0.0.1", port=port)
