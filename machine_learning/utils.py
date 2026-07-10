import pandas as pd

FEATURE_COLUMNS = [
    "Age",
    "Total_Reels_Watched",
    "Coffee_Consumed_Per_Day",
    "Focus_Sessions_Count",
    "Study_Hours",
    "Is_Late_Night",
    "Device_Type",
]

TARGET_COLUMN = "Brainrot_Stage"

STAGE_ORDER = ["Healthy", "Casual", "Advanced", "Critical"]

STAGE_COLORS = {
    "Healthy": "#22C55E",
    "Casual": "#EAB308",
    "Advanced": "#F97316",
    "Critical": "#F43F5E",
}

STAGE_ICONS = {
    "Healthy": "",
    "Casual": "",
    "Advanced": "",
    "Critical": "",
}

STAGE_LABELS_AR = {
    "Healthy": "Healthy",
    "Casual": "Casual",
    "Advanced": "Advanced",
    "Critical": "Critical",
}

STAGE_RECOMMENDATIONS_AR = {
    "Healthy": "Keep up this healthy pattern. You have an excellent balance between screen time, focus sessions, and study hours. Maintain your current routine.",
    "Casual": "Distraction is still at a mild stage. Try gradually reducing your daily short-form video count and add one extra deep-focus session per week.",
    "Advanced": "Digital distraction is starting to noticeably affect your productivity. Consider setting a daily screen-time limit for short-form videos, increasing your deep-focus sessions, and reducing caffeine intake after 6 PM.",
    "Critical": "This is a critical stage that requires immediate attention: reduce short-form video consumption, especially before bed, try the Pomodoro technique to increase focus sessions, and avoid using your phone after midnight. If you feel this is affecting your daily life, it may help to speak with a specialist.",
}


def load_raw_data(path: str) -> pd.DataFrame:
    """Loads raw data from a specified CSV file path."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Performs missing value imputation across demographic and behavioral features 
    to preserve overall sample size.
    """
    df = df.copy()

    if df["Age"].isnull().any():
        df["Age"] = df["Age"].fillna(df["Age"].median())

    if df["Device_Type"].isnull().any():
        df["Device_Type"] = df["Device_Type"].fillna(df["Device_Type"].mode()[0])

    for col in ["Age_Group", "Region", "Username"]:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna("Unknown")

    for col in ["Is_Smoker", "Base_Focus_Level"]:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    return df

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts target features and performs one-hot encoding on categorical attributes."""
    X = df[FEATURE_COLUMNS].copy()
    X = pd.get_dummies(X, columns=["Device_Type"], prefix="Device")
    return X

def align_columns(X: pd.DataFrame, trained_columns: list) -> pd.DataFrame:
    """Aligns production/inference dataframe schema with training metadata columns."""
    return X.reindex(columns=trained_columns, fill_value=0)