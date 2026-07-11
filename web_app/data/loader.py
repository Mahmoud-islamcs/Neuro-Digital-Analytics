"""
ETL layer for the Brain Rot Analytics dashboard.

Responsibilities:
    1. Load the 5 raw CSVs (star schema: 1 fact + 4 dims).
    2. Clean known data-quality issues (documented, not silently patched).
    3. Merge into one denormalised analytical dataframe (fast for a
       ~5k row dataset -- no need for a real warehouse/join-on-callback).
    4. Add calculated columns / derived KPIs used across every page.

The merged dataframe is cached in-process (module-level singleton) since
the dataset is small and static for the lifetime of the app.
"""
import os
import pandas as pd
import numpy as np

from config.settings import DATA_DIR, STAGE_ORDER, WELLBEING_BAND_ORDER

_CACHE = {}


def _read(name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATA_DIR, name), encoding="utf-8-sig")


def load_raw():
    """Load the five raw tables as-is."""
    return {
        "date": _read("Dim_Date.csv"),
        "habits": _read("Dim_Habits.csv"),
        "mental": _read("Dim_MentalState.csv"),
        "users": _read("Dim_Users.csv"),
        "fact": _read("Fact_User_Activity.csv"),
    }


def build_master_dataframe() -> pd.DataFrame:
    """
    Build the single wide analytical table the whole dashboard reads from.

    Data-quality handling (found during profiling, see chat writeup):
      - Fact_User_Activity.UserKey = 100 has no match in Dim_Users (51 rows).
        Rather than dropping real activity data, these are kept and labeled
        as an "Unknown User" dimension member -- standard BI practice for
        an orphan fact row instead of silently deleting ~1% of the data.
      - Dim_Habits.Coffee_Level has a null on HabitKey=1 (the "no habits"
        row) -- filled as "None" to match its Smoking_Status="Non-Smoker".
    """
    raw = load_raw()
    date, habits, mental, users, fact = (
        raw["date"], raw["habits"], raw["mental"], raw["users"], raw["fact"]
    )

    # --- clean dims -----------------------------------------------------
    habits = habits.copy()
    habits["Coffee_Level"] = habits["Coffee_Level"].fillna("None")
    habits["Smoking_Status"] = habits["Smoking_Status"].str.strip()

    mental = mental.copy()
    mental["Aura_Color_Code"] = mental["Aura_Color_Code"].str.strip()

    users = users.copy()
    # Synthetic "Unknown User" row so the orphan FK resolves cleanly.
    unknown_user = pd.DataFrame([{
        "UserKey": 100, "Username": "Unknown User", "Age": np.nan,
        "Age_Group": "Unknown", "Region": "Unknown", "Device_Type": "Unknown",
        "Is_Smoker": np.nan, "Base_Focus_Level": np.nan,
    }])
    users = pd.concat([users, unknown_user], ignore_index=True)

    date = date.copy()
    date["FullDate"] = pd.to_datetime(date["FullDate"])
    date["Month"] = date["FullDate"].dt.strftime("%b")
    date["MonthNum"] = date["FullDate"].dt.month
    date["Week"] = date["FullDate"].dt.isocalendar().week.astype(int)
    date["DayOfWeek"] = date["FullDate"].dt.day_name()
    date["DayLabel"] = date["FullDate"].dt.strftime("%b %d")

    # --- merge fact + dims ------------------------------------------------
    df = fact.merge(users, on="UserKey", how="left") \
             .merge(date, on="DateKey", how="left") \
             .merge(mental, on="StateKey", how="left") \
             .merge(habits, on="HabitKey", how="left")

    # --- calculated columns ------------------------------------------------
    # Wellbeing band: quartile-informed but human-readable bins (0-100 scale)
    df["Wellbeing_Band"] = pd.cut(
        df["Wellbeing_Score"], bins=[-0.1, 33, 55, 75, 100.1],
        labels=WELLBEING_BAND_ORDER,
    ).astype(str)

    # Brainrot risk flag for quick filtering / KPI counts
    df["Is_Critical_Brainrot"] = df["Brainrot_Stage"].eq("Critical")
    df["Is_Healthy"] = df["Brainrot_Stage"].eq("Healthy")

    # Screen-to-study ratio: how much reel consumption per study hour
    df["Reels_Per_Study_Hour"] = df["Total_Reels_Watched"] / df["Study_Hours"].replace(0, np.nan)
    df["Reels_Per_Study_Hour"] = df["Reels_Per_Study_Hour"].fillna(df["Total_Reels_Watched"])

    # Focus efficiency: focus sessions relative to study hours invested
    df["Focus_Sessions_Per_Hour"] = df["Focus_Sessions_Count"] / df["Study_Hours"].replace(0, np.nan)
    df["Focus_Sessions_Per_Hour"] = df["Focus_Sessions_Per_Hour"].fillna(0)

    # Peak hour bucket for readability in charts
    def _hour_bucket(h):
        if 5 <= h < 12:
            return "Morning (5-11)"
        if 12 <= h < 17:
            return "Afternoon (12-16)"
        if 17 <= h < 21:
            return "Evening (17-20)"
        return "Late Night (21-4)"
    df["Peak_Hour_Bucket"] = df["Peak_Hour"].apply(_hour_bucket)

    # Ordered categoricals so charts/legends render logically
    df["Brainrot_Stage"] = pd.Categorical(df["Brainrot_Stage"], categories=STAGE_ORDER, ordered=True)
    df["Wellbeing_Band"] = pd.Categorical(df["Wellbeing_Band"], categories=WELLBEING_BAND_ORDER, ordered=True)

    df["Is_Weekend_Label"] = df["Is_Weekend"].map({1: "Weekend", 0: "Weekday"})
    df["Is_Exam_Season_Label"] = df["Is_Exam_Season"].map({1: "Exam Season", 0: "Regular"})
    df["Is_Late_Night_Label"] = df["Is_Late_Night"].map({1: "Late-Night Activity", 0: "Daytime Activity"})
    df["Is_Smoker_Label"] = df["Is_Smoker"].map({1: "Smoker", 0: "Non-Smoker"})

    return df


def get_master_df() -> pd.DataFrame:
    """Cached accessor -- build once per process."""
    if "master" not in _CACHE:
        _CACHE["master"] = build_master_dataframe()
    return _CACHE["master"]


# ------------------------------------------------------------------
# Filter option helpers (used by components/filters.py)
# ------------------------------------------------------------------
def get_filter_options():
    df = get_master_df()
    return {
        "age_group": sorted(df["Age_Group"].dropna().unique().tolist()),
        "region": sorted(df["Region"].dropna().unique().tolist()),
        "device": sorted(df["Device_Type"].dropna().unique().tolist()),
        "brainrot_stage": [s for s in STAGE_ORDER if s in df["Brainrot_Stage"].astype(str).unique()],
        "wellbeing_band": [s for s in WELLBEING_BAND_ORDER if s in df["Wellbeing_Band"].astype(str).unique()],
        "coffee_level": sorted(df["Coffee_Level"].dropna().unique().tolist()),
        "smoking_status": sorted(df["Smoking_Status"].dropna().unique().tolist()),
        "date_min": df["FullDate"].min(),
        "date_max": df["FullDate"].max(),
        "study_hours_min": float(df["Study_Hours"].min()),
        "study_hours_max": float(df["Study_Hours"].max()),
    }


def apply_filters(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    """Apply the global filter dict (from dcc.Store) to the master dataframe."""
    out = df
    if f.get("age_group"):
        out = out[out["Age_Group"].isin(f["age_group"])]
    if f.get("region"):
        out = out[out["Region"].isin(f["region"])]
    if f.get("device"):
        out = out[out["Device_Type"].isin(f["device"])]
    if f.get("brainrot_stage"):
        out = out[out["Brainrot_Stage"].astype(str).isin(f["brainrot_stage"])]
    if f.get("wellbeing_band"):
        out = out[out["Wellbeing_Band"].astype(str).isin(f["wellbeing_band"])]
    if f.get("coffee_level"):
        out = out[out["Coffee_Level"].isin(f["coffee_level"])]
    if f.get("smoking_status"):
        out = out[out["Smoking_Status"].isin(f["smoking_status"])]
    if f.get("date_range"):
        start, end = f["date_range"]
        out = out[(out["FullDate"] >= start) & (out["FullDate"] <= end)]
    if f.get("study_hours_range"):
        lo, hi = f["study_hours_range"]
        out = out[(out["Study_Hours"] >= lo) & (out["Study_Hours"] <= hi)]
    return out
