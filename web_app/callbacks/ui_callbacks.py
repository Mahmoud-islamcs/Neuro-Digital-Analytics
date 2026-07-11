"""Small UI-only callbacks: sidebar collapse and persisted theme switching."""
from dash import callback, Input, Output, State, ctx, html

from components.sidebar import NAV_ITEMS


VALID_THEMES = {"dark", "light"}


def _clean_theme(theme):
    return theme if theme in VALID_THEMES else "dark"


def _nav_id(item):
    return f"nav-{item['href'].strip('/') or 'home'}"


def _normalize_path(pathname):
    if not pathname or pathname == "/":
        return "/"
    return "/" + pathname.strip("/")


@callback(
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks, current_theme):
    theme = _clean_theme(current_theme)
    return "light" if theme == "dark" else "dark"


@callback(
    Output("app-shell", "className"),
    Output("app-shell", "data-bs-theme"),
    Output("theme-toggle", "children"),
    Output("theme-toggle", "title"),
    Input("sidebar-toggle", "n_clicks"),
    Input("theme-store", "data"),
    State("app-shell", "className"),
    prevent_initial_call=False,
)
def sync_shell_state(n_clicks, theme, current_class):
    theme = _clean_theme(theme)
    classes = set((current_class or "app-shell").split())
    classes.discard("theme-dark")
    classes.discard("theme-light")

    if ctx.triggered_id == "sidebar-toggle":
        if "sidebar-collapsed" in classes:
            classes.remove("sidebar-collapsed")
        else:
            classes.add("sidebar-collapsed")

    classes.add("app-shell")
    classes.add(f"theme-{theme}")

    icon_class = "bi bi-sun-fill" if theme == "dark" else "bi bi-moon-stars-fill"
    title = "Switch to light mode" if theme == "dark" else "Switch to dark mode"
    ordered = ["app-shell"]
    if "sidebar-collapsed" in classes:
        ordered.append("sidebar-collapsed")
    ordered.append(f"theme-{theme}")
    return " ".join(ordered), theme, html.I(className=icon_class), title


@callback(
    [Output(_nav_id(item), "className") for item in NAV_ITEMS],
    Input("url", "pathname"),
)
def sync_active_nav(pathname):
    active_path = _normalize_path(pathname)
    return [
        "sidebar-link active" if item["href"] == active_path else "sidebar-link"
        for item in NAV_ITEMS
    ]


@callback(
    Output("global-filter-shell", "className"),
    Input("url", "pathname"),
)
def sync_filter_visibility(pathname):
    classes = ["global-filter-shell"]
    if _normalize_path(pathname) == "/about":
        classes.append("is-hidden")
    return " ".join(classes)
