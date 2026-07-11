"""Professional collapsible sidebar navigation."""
from dash import html, dcc

from config.settings import GITHUB_REPOSITORY_URL

NAV_ITEMS = [
    {"label": "Home", "href": "/", "icon": "bi bi-house-door-fill"},
    {"label": "Overview", "href": "/overview", "icon": "bi bi-grid-1x2-fill"},
    {"label": "Users", "href": "/users", "icon": "bi bi-people-fill"},
    {"label": "Mental Health", "href": "/mental-health", "icon": "bi bi-heart-pulse-fill"},
    {"label": "Social Media", "href": "/social-media", "icon": "bi bi-phone-fill"},
    {"label": "Study & Productivity", "href": "/study", "icon": "bi bi-book-fill"},
    {"label": "Brain Rot Score", "href": "/brain-rot", "icon": "bi bi-cpu-fill"},
    {"label": "Correlation Analysis", "href": "/correlation", "icon": "bi bi-diagram-3-fill"},
    {"label": "Insights", "href": "/insights", "icon": "bi bi-lightbulb-fill"},
    {"label": "About", "href": "/about", "icon": "bi bi-info-circle-fill"},
]


def sidebar():
    return html.Div([
        html.Div([
            html.Div([
                html.Span(
                    html.I(className="bi bi-bar-chart-line-fill"),
                    className="brand-mark",
                    **{"aria-hidden": "true"},
                ),
                html.Div([
                    html.Div("Brain Rot", className="brand-title"),
                    html.Div("Analytics EGY", className="brand-subtitle"),
                ], className="brand-text"),
            ], className="brand-row"),
        ], className="sidebar-header"),

        html.Div([
            dcc.Link([
                html.I(className=f"{item['icon']} nav-icon"),
                html.Span(item["label"], className="nav-label"),
            ], href=item["href"], className="sidebar-link",
                id=f"nav-{item['href'].strip('/') or 'home'}", title=item["label"])

            for item in NAV_ITEMS
        ], className="sidebar-nav"),

        html.Div([
            html.A([
                html.I(className="bi bi-github github-icon"),
                html.Span("View on GitHub", className="github-label"),
            ], href=GITHUB_REPOSITORY_URL, target="_blank", rel="noopener noreferrer",
                className="github-sidebar-btn", title="View repository on GitHub"),
        ], className="sidebar-footer"),
    ], className="sidebar", id="sidebar")
