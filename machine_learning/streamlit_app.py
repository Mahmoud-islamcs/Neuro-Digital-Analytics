import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import time

from utils import (
    load_raw_data,
    clean_data,
    prepare_features,
    align_columns,
    STAGE_ORDER,
    STAGE_COLORS,
    STAGE_LABELS_AR,
    STAGE_RECOMMENDATIONS_AR,
)

# PAGE CONFIG
st.set_page_config(
    page_title="Brain Rot Analytics",
    page_icon="https://cdn-icons-png.flaticon.com/512/2103/2103633.png", 
    layout="wide",
    initial_sidebar_state="expanded",
)

# GLASSMORPHISM DARK THEME CSS
st.markdown(
    """
    <style>

    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    /* Metric-style glass card */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 18px 20px;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
    }
    .metric-card .metric-label {
        font-size: 13px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Result card */
    .result-card {
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(16px);
        margin: 16px 0 24px 0;
    }
    .result-title {
        font-size: 22px;
        color: #E5E7EB;
        margin-bottom: 6px;
    }
    .result-stage {
        font-size: 38px;
        font-weight: 900;
        margin: 8px 0;
    }
    .recommendation-box {
        background: rgba(255,255,255,0.04);
        border-left: 4px solid #7C5CFC;
        border-radius: 10px;
        padding: 16px 20px;
        color: #E2E8F0;
        line-height: 1.8;
    }

    /* Buttons */
    div.stButton > button {
        # background: linear-gradient(90deg, #7C5CFC 0%, #22D3EE 100%);
        # color: white;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        width: 100%;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        opacity: 0.85;
        transform: scale(1.01);
    }

    /* Inputs */
    .stSlider, .stNumberInput, .stSelectbox, .stRadio {
        color: #F5F7FA;
    }
    
    /* Hide default streamlit footer/menu clutter (keep header) */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# CACHED LOADERS
@st.cache_data
def get_data():
    df = load_raw_data("data/BrainRot_Final_Dataset.csv")
    df = clean_data(df)
    return df

@st.cache_resource
def get_model_artifacts():
    model = joblib.load("model/brainrot_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    metadata = joblib.load("model/metadata.pkl")
    return model, scaler, metadata

df = get_data()
model, scaler, metadata = get_model_artifacts()
trained_columns = metadata["trained_columns"]
uses_scaled = metadata["uses_scaled"]
best_model_name = metadata["best_model_name"]

# SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;">
            <h2 style="margin-bottom:0;">BrainRot Analytics</h2>
            <p style="margin-top:-4px; font-size:0.9rem; color:#9CA3AF;">
                AI-Powered Behavioral Intelligence Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "Predict"

    if st.button("Predict", use_container_width=True):
        st.session_state.page = "Predict"

    if st.button("Insights", use_container_width=True):
        st.session_state.page = "Insights"

    if st.button("About", use_container_width=True):
        st.session_state.page = "About"

    page = st.session_state.page

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    # with st.container():
    st.write(f"**Model:** {best_model_name}")
    st.write(f"**Records:** {len(df):,}")
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("Made by [Mahmoud Islam](https://www.linkedin.com/in/mahmoud-islam-analytics/)", unsafe_allow_html=True)


# PAGE 1: PREDICT
if page == "Predict":
    st.title("Mental Health & Wellbeing Predictor")
    st.markdown(
        "Enter your daily habits below to predict your current digital distraction "
        "stage (Brain Rot Stage), based on a machine learning model trained on 5,000 "
        "Egyptian student records."
    )

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        reels = st.slider("Daily Short-Form Videos Watched (Reels/Shorts/TikTok)", 0, 270, 60)
        coffee = st.slider("Daily Caffeinated Drinks Consumed", 0, 10, 2)
        device = st.selectbox("Primary Device Used", ["Smartphone", "Tablet", "PC"])
        q_col, a_col = st.columns([2, 1])  
        with q_col:
            st.write("") 
            st.write("Do you use your phone after midnight?")
        with a_col:
            late_night = st.radio("", ["Yes", "No"], horizontal=True, label_visibility="collapsed")
    with col2:
        study_hours = st.slider("Daily Effective Study/Productivity Hours", 0.0, 11.0, 4.0, step=0.5)
        focus_sessions = st.slider("Daily Deep Focus Sessions (Uninterrupted)", 0, 11, 4)
        age = st.number_input("Age", min_value=8, max_value=25, value=20, step=1)
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    predict_clicked = st.button(
        "Execute AI Prediction", 
        type="primary", 
        use_container_width=True,
        key="btn_predict_main"
    )

    if predict_clicked:
        with st.spinner("Analyzing your data..."):
            time.sleep(1.5) 
            input_df = pd.DataFrame(
                [
                    {
                        "Age": age,
                        "Total_Reels_Watched": reels,
                        "Coffee_Consumed_Per_Day": coffee,
                        "Focus_Sessions_Count": focus_sessions,
                        "Study_Hours": study_hours,
                        "Is_Late_Night": 1 if late_night == "Yes" else 0,
                        "Device_Type": device,
                    }
                ]
            )
            X_input = prepare_features(input_df)
            X_input = align_columns(X_input, trained_columns)

            if uses_scaled:
                X_input_for_model = scaler.transform(X_input)
            else:
                X_input_for_model = X_input

            pred_int = model.predict(X_input_for_model)[0]
            proba = model.predict_proba(X_input_for_model)[0]
            pred_stage = STAGE_ORDER[pred_int]

            color = STAGE_COLORS[pred_stage]
            label_ar = STAGE_LABELS_AR[pred_stage]
            recommendation = STAGE_RECOMMENDATIONS_AR[pred_stage]

        st.markdown(
            f"""
            <div class='result-card' style='background: linear-gradient(135deg, {color}22, {color}08); border-color:{color}55;'>
                <div class='result-title'>Current Digital Distraction Stage</div>
                <div class='result-stage' style='color:{color};'>{label_ar}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div class='recommendation-box'><b>Recommendation:</b> {recommendation}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Prediction Probabilities")

        proba_df = pd.DataFrame(
            {"Stage": STAGE_ORDER, "Probability": proba}
        ).sort_values("Probability", ascending=True)

        fig = go.Figure(
            go.Bar(
                x=proba_df["Probability"],
                y=proba_df["Stage"],
                orientation="h",
                marker_color=[STAGE_COLORS[s] for s in proba_df["Stage"]],
                text=[f"{p:.1%}" for p in proba_df["Probability"]],
                textposition="outside",
            )
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#E5E7EB",
            xaxis=dict(range=[0, 1], tickformat=".0%", gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)


# PAGE 3: INSIGHTS
elif page == "Insights":
    st.title("Model Insights")
    st.markdown(f"Performance details and interpretation of the winning model: **{best_model_name}**")

    dark_layout = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB",
        margin=dict(l=10, r=10, t=40, b=10),
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Feature Importance")
        try:
            fi_df = pd.read_csv("model/feature_importance.csv")
            fig = px.bar(fi_df, x="importance", y="feature", orientation="h",color="importance", color_continuous_scale="Purples")
            fig.update_layout(**dark_layout, yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig, use_container_width=True)
        except FileNotFoundError:
            st.info("Run train_model.ipynb first to generate this chart.")

    with col2:
        st.markdown("#### Confusion Matrix")
        try:
            st.image("model/confusion_matrix.png", use_container_width=True)
        except Exception:
            st.info("Run train_model.ipynb first to generate this image.")

    st.markdown("#### Classification Report")
    try:
        with open("model/classification_report.txt") as f:
            st.code(f.read(), language="text")
    except FileNotFoundError:
        st.info("No saved report found. Run train_model.ipynb first.")

    st.markdown("#### Correlation Analysis")
    numeric_df = df.select_dtypes(include=[np.number]).drop(
        columns=["ActivityID", "UserKey", "DateKey", "StateKey", "HabitKey"], errors="ignore"
    )
    corr = numeric_df.corr()
    fig = px.imshow(corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto",title="Correlation Heatmap")
    fig.update_layout(**dark_layout, height=550)
    st.plotly_chart(fig, use_container_width=True)


# PAGE 4: ABOUT
else:
    st.title("About Brain Rot Analytics")
    st.markdown(
        """
        <div class='glass-card'>
        
        <h3>About the Project</h3>
        <p style='color:#CBD5E1; line-height:1.9;'>
        <b>"Brain Rot Analytics"</b> is a comprehensive Data Science and Machine Learning graduation project designed to analyze digital wellbeing. 
        It studies the profound relationship between daily behavioral habits—specifically short-form video consumption—and student productivity. 
        The project delivers a predictive model that successfully classifies a student's digital distraction level into one of four distinct stages: 
        <span style='color:#10B981; font-weight:bold;'>Healthy</span>, 
        <span style='color:#3B82F6; font-weight:bold;'>Casual</span>, 
        <span style='color:#F59E0B; font-weight:bold;'>Advanced</span>, or 
        <span style='color:#EF4444; font-weight:bold;'>Critical</span>.
        </p>

        <h3>About the Dataset & Preprocessing</h3>
        <p style='color:#CBD5E1; line-height:1.9;'>
        The model is built on a comprehensive dataset containing <b>5,000 rows and 30 columns</b>. 
        To preserve full sample size and statistical integrity, missing values found across 51 rows (in features like Age, Region, and Device Type) 
        were meticulously imputed using median and mode strategies rather than being discarded.
        </p>

        <h3>Key Project Benefits</h3>
        <ul style='color:#CBD5E1; line-height:1.9; padding-left: 20px;'>
            <li>Detects early indicators of digital distraction before escalating to critical stages.</li>
            <li>Provides personalized, actionable recommendations to mitigate screen-time harms.</li>
            <li>Empowers awareness campaigns with robust, data-driven insights into modern digital habits.</li>
            <li>Pinpoints specific destructive behaviors (e.g., late-night usage, short-video loops) that heavily impair cognitive focus.</li>
        </ul>

        <h3>How to Explain the Model to the Committee</h3>
        <p style='color:#CBD5E1; line-height:1.9;'>
        <b>1) Machine Learning Pipeline & Models Evaluated:</b><br>
        We implemented a comparative benchmark across three diverse algorithms: <b>Logistic Regression</b> (as our baseline model), 
        <b>Random Forest</b>, and <b>XGBoost</b>. Every model was optimized utilizing <code>RandomizedSearchCV</code> for hyperparameter tuning, 
        and strict class balancing was enforced via <code>class_weight='balanced'</code> alongside a stratified train/test split to address the 
        highly imbalanced class distribution (Healthy: 61%, Critical: 18%, Advanced: 12.5%, Casual: 8.5%).
        <br><br>
        <b>2) Rigorous Metric Selection & Winning Model:</b><br>
        The <b>Random Forest Classifier</b> emerged as the champion model, achieving an outstanding <b>Macro F1-score of 0.903</b> and an <b>Overall Accuracy of 94.5%</b>. 
        We explicitly relied on the Macro F1-score as our primary evaluation metric rather than accuracy alone, ensuring that the model performs 
        equally well on the minority classes (Casual and Advanced) and is robust against data imbalance.
        <br><br>
        <b>3) Top Feature Importances:</b><br>
        The model's decisions are highly transparent and logical. Inline Feature Importance analysis indicates that the top 3 predictive drivers are: 
        <code>Total_Reels_Watched</code> &rarr; <code>Focus_Sessions_Count</code> &rarr; <code>Study_Hours</code>. 
        This perfectly validates our core hypothesis regarding digital distraction and academic focus.
        </p>

        <h3>Prevention of Data Leakage</h3>
        <p style='color:#CBD5E1; line-height:1.9;'>
        To guarantee genuine generalization, strict feature selection was conducted. Only <b>7 behavioral features</b> were allowed into training 
        (<i>Age, Total_Reels_Watched, Coffee_Consumed_Per_Day, Focus_Sessions_Count, Study_Hours, Is_Late_Night, Device_Type</i>). 
        Target-derived or highly correlated columns—such as <code>Brainrot_Exposure_Score</code>, <code>Wellbeing_Score</code>, <code>Attention_Span_Level</code>, 
        <code>Aura_Color_Code</code>, <code>Coffee_Level</code>, and <code>Smoking_Status</code>—were <b>deliberately excluded</b> from the training phase. 
        This prevents mathematical data leakage, ensuring that the dashboard's performance is realistic and not artificially inflated.
        </p>
        
        </div>
        """,
        unsafe_allow_html=True,
    )