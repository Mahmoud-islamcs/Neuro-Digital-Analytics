"""
Global configuration: paths, theme tokens, and shared constants.
Centralised here so nothing is hardcoded twice across the app.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

APP_TITLE = "Brain Rot Analytics"
APP_SUBTITLE = "Social Media Habits vs. Student Wellbeing & Focus"
GITHUB_REPOSITORY_URL = os.environ.get(
    "BRAINROT_GITHUB_URL",
    "https://github.com/Mahmoud-islamcs/Neuro-Digital-Analytics",
)

# ------------------------------------------------------------------
# Dark, glassmorphism-friendly palette. Every chart pulls from here
# so the whole app stays visually consistent (no ad-hoc chart colors).
# ------------------------------------------------------------------
COLORS = {
    "bg": "#0b0f19",
    "bg_alt": "#0f1420",
    "surface": "rgba(255,255,255,0.045)",
    "surface_border": "rgba(255,255,255,0.09)",
    "text": "#e9edf5",
    "text_dim": "#8b93a7",
    "primary": "#7c5cff",
    "primary_soft": "#a78bfa",
    "accent": "#22d3ee",
    "pink": "#f472b6",
    "amber": "#fbbf24",
    "green": "#34d399",
    "red": "#fb7185",
    "grid": "rgba(255,255,255,0.06)",
}

# Brainrot stage -> color, ordered from best to worst.
STAGE_ORDER = ["Healthy", "Casual", "Advanced", "Critical"]
STAGE_COLORS = {
    "Healthy": COLORS["green"],
    "Casual": COLORS["amber"],
    "Advanced": "#fb923c",
    "Critical": COLORS["red"],
}

WELLBEING_BAND_ORDER = ["Critical", "At Risk", "Moderate", "Healthy"]
WELLBEING_BAND_COLORS = {
    "Critical": COLORS["red"],
    "At Risk": "#fb923c",
    "Moderate": COLORS["amber"],
    "Healthy": COLORS["green"],
}

CATEGORICAL_SEQUENCE = [
    COLORS["primary"], COLORS["accent"], COLORS["pink"], COLORS["amber"],
    COLORS["green"], COLORS["red"], COLORS["primary_soft"], "#38bdf8",
]

# Plotly template shared by every chart builder in utils/chart_helpers.py
PLOTLY_TEMPLATE = "brainrot_dark"
