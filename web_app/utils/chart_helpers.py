"""
Chart factory: one place that owns Plotly styling so every chart across
every page looks consistent (same fonts, same dark surface, same grid).
"""
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from config.settings import COLORS, CATEGORICAL_SEQUENCE, PLOTLY_TEMPLATE

# ------------------------------------------------------------------
# Register a shared dark template once at import time.
# ------------------------------------------------------------------
_template = go.layout.Template()
_template.layout = go.Layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, 'Segoe UI', sans-serif", color=COLORS["text"], size=12),
    colorway=CATEGORICAL_SEQUENCE,
    margin=dict(l=52, r=28, t=74, b=48),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], linecolor=COLORS["grid"]),
    yaxis=dict(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], linecolor=COLORS["grid"]),
    hoverlabel=dict(bgcolor="#1a2033", font_size=12, font_family="Inter, sans-serif",
                     bordercolor=COLORS["surface_border"]),
    title=dict(font=dict(size=15, color=COLORS["text"]), x=0.02, xanchor="left", y=0.96, pad=dict(b=18)),
)
pio.templates[PLOTLY_TEMPLATE] = _template
pio.templates.default = PLOTLY_TEMPLATE


def style_fig(fig: go.Figure, height=340, legend_bottom=False, title=None) -> go.Figure:
    """Apply final consistent touches to any figure before returning it."""
    fig.update_layout(height=height, autosize=False, template=PLOTLY_TEMPLATE,
                      margin=dict(l=52, r=28, t=74, b=48))
    if title:
        fig.update_layout(title=title)
    if legend_bottom:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.08,
                                       xanchor="right", x=1))
    fig.update_layout(uniformtext_minsize=9)
    return fig


def empty_state(message="No data matches the current filters"):
    """A friendly placeholder figure when a filtered slice is empty."""
    fig = go.Figure()
    fig.add_annotation(text=f"⚠️ {message}", showarrow=False, font=dict(size=14, color=COLORS["text_dim"]))
    fig.update_layout(template=PLOTLY_TEMPLATE, height=340, autosize=False,
                       xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig


def guard(df):
    """Return True if df is empty -- callers should render empty_state()."""
    return df is None or len(df) == 0
