import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

THEME_TOKENS = {
    "dark": {
        "text": "#e9edf5",
        "text_dim": "#8b93a7",
        "grid": "rgba(255,255,255,0.06)",
        "paper_bg": "rgba(0,0,0,0)",
        "plot_bg": "rgba(0,0,0,0)",
        "hover_bg": "#1e293b",
        "hover_border": "#7c5cff",
        "hover_text": "#ffffff",
        "template": "plotly_dark",
        "primary": "#7c5cff",
        "primary_soft": "#a78bfa",
        "accent": "#22d3ee",
        "pink": "#f472b6",
        "amber": "#fbbf24",
        "green": "#34d399",
        "red": "#fb7185",
        "categorical": [
            "#7c5cff", "#22d3ee", "#f472b6", "#fbbf24",
            "#34d399", "#fb7185", "#a78bfa", "#38bdf8",
        ],
        "stage_colors": {
            "Healthy": "#34d399",
            "Casual": "#fbbf24",
            "Advanced": "#fb923c",
            "Critical": "#fb7185",
        },
        "wellbeing_colors": {
            "Critical": "#fb7185",
            "At Risk": "#fb923c",
            "Moderate": "#fbbf24",
            "Healthy": "#34d399",
        }
    },
    "light": {
        "text": "#0f172a",
        "text_dim": "#5d687b",
        "grid": "rgba(17,24,39,0.08)",
        "paper_bg": "rgba(0,0,0,0)",
        "plot_bg": "rgba(0,0,0,0)",
        "hover_bg": "#ffffff",
        "hover_border": "#6366f1",
        "hover_text": "#0f172a",
        "template": "plotly_white",
        "primary": "#4f46e5",
        "primary_soft": "#6366f1",
        "accent": "#0284c7",
        "pink": "#db2777",
        "amber": "#d97706",
        "green": "#059669",
        "red": "#e11d48",
        "categorical": [
            "#4f46e5", "#0284c7", "#db2777", "#d97706",
            "#059669", "#e11d48", "#6366f1", "#0ea5e9",
        ],
        "stage_colors": {
            "Healthy": "#059669",
            "Casual": "#d97706",
            "Advanced": "#ea580c",
            "Critical": "#e11d48",
        },
        "wellbeing_colors": {
            "Critical": "#e11d48",
            "At Risk": "#ea580c",
            "Moderate": "#d97706",
            "Healthy": "#059669",
        }
    }
}


def get_theme_tokens(theme="dark"):
    t = (theme or "dark").lower()
    return THEME_TOKENS.get(t, THEME_TOKENS["dark"])


def get_stage_colors(theme="dark"):
    return get_theme_tokens(theme)["stage_colors"]


def get_wellbeing_colors(theme="dark"):
    return get_theme_tokens(theme)["wellbeing_colors"]


def get_categorical_sequence(theme="dark"):
    return get_theme_tokens(theme)["categorical"]


def style_fig(fig: go.Figure, theme="dark", height=340, legend_bottom=False, title=None) -> go.Figure:
    tokens = get_theme_tokens(theme)
    
    is_auto = bool(fig.layout.autosize) if hasattr(fig.layout, "autosize") and fig.layout.autosize is not None else False

    fig.update_layout(
        height=height,
        template=tokens["template"],
        paper_bgcolor=tokens["paper_bg"],
        plot_bgcolor=tokens["plot_bg"],
        font=dict(family="Inter, 'Segoe UI', sans-serif", color=tokens["text"], size=12),
    )
    if not is_auto:
        fig.update_layout(autosize=False)

    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=15, color=tokens["text"])))
    elif hasattr(fig.layout, "title") and fig.layout.title and hasattr(fig.layout.title, "text") and fig.layout.title.text:
        fig.update_layout(title=dict(font=dict(size=15, color=tokens["text"])))

    axis_kwargs = dict(
        gridcolor=tokens["grid"],
        zerolinecolor=tokens["grid"],
        linecolor=tokens["grid"],
        tickfont=dict(color=tokens["text_dim"]),
        title_font=dict(color=tokens["text"])
    )
    fig.update_xaxes(**axis_kwargs)
    fig.update_yaxes(**axis_kwargs)

    fig.update_layout(
        hoverlabel=dict(
            bgcolor=tokens["hover_bg"],
            font_size=12,
            font_family="Inter, sans-serif",
            font_color=tokens["hover_text"],
            bordercolor=tokens["hover_border"]
        )
    )

    if legend_bottom:
        fig.update_layout(legend=dict(
            orientation="h", yanchor="bottom", y=1.08, xanchor="right", x=1,
            font=dict(color=tokens["text"], size=11)
        ))
    else:
        fig.update_layout(legend=dict(font=dict(color=tokens["text"], size=11)))

    if hasattr(fig.layout, "polar") and fig.layout.polar:
        fig.update_layout(
            polar=dict(
                radialaxis=dict(gridcolor=tokens["grid"], tickfont=dict(color=tokens["text_dim"])),
                angularaxis=dict(gridcolor=tokens["grid"], tickfont=dict(color=tokens["text"])),
                bgcolor="rgba(0,0,0,0)"
            )
        )

    if hasattr(fig.layout, "scene") and fig.layout.scene:
        fig.update_layout(
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor=tokens["grid"], tickfont=dict(color=tokens["text_dim"]), title=dict(font=dict(color=tokens["text"]))),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor=tokens["grid"], tickfont=dict(color=tokens["text_dim"]), title=dict(font=dict(color=tokens["text"]))),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor=tokens["grid"], tickfont=dict(color=tokens["text_dim"]), title=dict(font=dict(color=tokens["text"]))),
            )
        )

    fig.update_layout(uniformtext_minsize=9)
    return fig


def empty_state(message="No data matches the current filters", theme="dark"):
    tokens = get_theme_tokens(theme)
    fig = go.Figure()
    fig.add_annotation(text=f"Notice: {message}", showarrow=False, font=dict(size=14, color=tokens["text_dim"]))
    fig.update_layout(template=tokens["template"], height=340, autosize=False,
                       xaxis=dict(visible=False), yaxis=dict(visible=False))
    return style_fig(fig, theme=theme, height=340)


def guard(df):
    return df is None or len(df) == 0
