import numpy as np
from config.settings import COLORS


def _pct(a, b):
    if b == 0:
        return 0
    return (a - b) / b * 100


def generate_insights(df):
    insights = []
    if df is None or len(df) < 20:
        return insights

    median_reels = df["Total_Reels_Watched"].median()
    high = df[df["Total_Reels_Watched"] > median_reels]
    low = df[df["Total_Reels_Watched"] <= median_reels]
    if len(high) > 10 and len(low) > 10:
        diff = _pct(low["Wellbeing_Score"].mean(), high["Wellbeing_Score"].mean())
        if abs(diff) > 5:
            insights.append({
                "icon": "bi bi-phone-vibrate", "color": COLORS["red"],
                "title": "High reel consumption drags down wellbeing",
                "text": (f"Users watching more than {median_reels:.0f} reels/day score "
                         f"{diff:.1f}% higher on wellbeing when they watch fewer reels "
                         f"({low['Wellbeing_Score'].mean():.1f} vs {high['Wellbeing_Score'].mean():.1f})."),
            })

    if "Is_Late_Night_Label" in df:
        late = df[df["Is_Late_Night_Label"] == "Late-Night Activity"]
        day = df[df["Is_Late_Night_Label"] == "Daytime Activity"]
        if len(late) > 10 and len(day) > 10:
            diff = _pct(day["Wellbeing_Score"].mean(), late["Wellbeing_Score"].mean())
            if abs(diff) > 4:
                insights.append({
                    "icon": "bi bi-moon-stars-fill", "color": COLORS["accent"],
                    "title": "Late-night activity correlates with lower wellbeing",
                    "text": (f"Wellbeing score is {diff:.1f}% higher during daytime activity windows "
                             f"than during late-night sessions."),
                })

    if "Is_Exam_Season_Label" in df:
        exam = df[df["Is_Exam_Season_Label"] == "Exam Season"]
        reg = df[df["Is_Exam_Season_Label"] == "Regular"]
        if len(exam) > 10 and len(reg) > 10:
            diff = _pct(exam["Brainrot_Exposure_Score"].mean(), reg["Brainrot_Exposure_Score"].mean())
            if abs(diff) > 4:
                direction = "higher" if diff > 0 else "lower"
                insights.append({
                    "icon": "bi bi-mortarboard-fill", "color": COLORS["amber"],
                    "title": f"Brain Rot exposure is {direction} during exam season",
                    "text": (f"Average Brain Rot Exposure Score is {abs(diff):.1f}% {direction} during "
                             f"exam season ({exam['Brainrot_Exposure_Score'].mean():.1f}) vs regular days "
                             f"({reg['Brainrot_Exposure_Score'].mean():.1f})."),
                })

    if "Coffee_Level" in df and df["Coffee_Level"].nunique() > 1:
        grp = df.groupby("Coffee_Level")["Focus_Sessions_Count"].mean().sort_values()
        if len(grp) >= 2:
            lo_lvl, hi_lvl = grp.index[0], grp.index[-1]
            diff = _pct(grp.iloc[-1], grp.iloc[0])
            if abs(diff) > 5:
                insights.append({
                    "icon": "bi bi-cup-hot-fill", "color": "#c084fc",
                    "title": f"'{hi_lvl}' coffee users log more focus sessions than '{lo_lvl}' users",
                    "text": (f"Average focus sessions: {grp.iloc[-1]:.1f} ({hi_lvl}) vs "
                             f"{grp.iloc[0]:.1f} ({lo_lvl}) -- a {abs(diff):.1f}% gap."),
                })

    if "Brainrot_Stage" in df:
        grp = df.groupby("Brainrot_Stage", observed=True)["Study_Hours"].mean()
        if "Healthy" in grp.index and "Critical" in grp.index:
            diff = _pct(grp["Healthy"], grp["Critical"])
            if abs(diff) > 5:
                insights.append({
                    "icon": "bi bi-book-half", "color": COLORS["green"],
                    "title": "Healthy-stage users study significantly more",
                    "text": (f"Users in the 'Healthy' Brain Rot stage study {grp['Healthy']:.1f}h/day on average "
                             f"vs {grp['Critical']:.1f}h/day for 'Critical' stage users ({abs(diff):.1f}% gap)."),
                })

    if "Attention_Span_Level" in df:
        grp = df.groupby("Attention_Span_Level")["Short_Content_Percentage"].mean().sort_values()
        if len(grp) >= 2:
            diff = _pct(grp.iloc[-1], grp.iloc[0])
            if abs(diff) > 5:
                insights.append({
                    "icon": "bi bi-hourglass-split", "color": COLORS["pink"],
                    "title": "Short-form content share tracks attention span decline",
                    "text": (f"'{grp.index[-1]}' attention-span users consume {grp.iloc[-1]*100:.0f}% short-form "
                             f"content on average, vs {grp.iloc[0]*100:.0f}% for '{grp.index[0]}' users."),
                })

    if "Is_Weekend_Label" in df:
        we = df[df["Is_Weekend_Label"] == "Weekend"]["Total_Reels_Watched"].mean()
        wd = df[df["Is_Weekend_Label"] == "Weekday"]["Total_Reels_Watched"].mean()
        if not np.isnan(we) and not np.isnan(wd) and wd > 0:
            diff = _pct(we, wd)
            if abs(diff) > 5:
                insights.append({
                    "icon": "bi bi-calendar-week-fill", "color": COLORS["primary_soft"],
                    "title": "Weekend reel consumption spikes",
                    "text": f"Users watch {abs(diff):.1f}% {'more' if diff>0 else 'fewer'} reels on weekends ({we:.0f}/day) than weekdays ({wd:.0f}/day).",
                })

    if "Region" in df and df["Region"].nunique() > 1:
        grp = df[df["Region"] != "Unknown"].groupby("Region")["Brainrot_Exposure_Score"].mean().sort_values(ascending=False)
        if len(grp) > 1:
            insights.append({
                "icon": "bi bi-geo-alt-fill", "color": COLORS["accent"],
                "title": f"{grp.index[0]} shows the highest average Brain Rot exposure",
                "text": (f"{grp.index[0]} averages a {grp.iloc[0]:.1f} exposure score, compared to the overall "
                         f"average of {df['Brainrot_Exposure_Score'].mean():.1f}."),
            })

    return insights
