print("SERVER STARTING...")
from flask import Flask, request, jsonify
print("IMPORTING LIBRARIES...")
import pandas as pd
import sqlalchemy as sa
import os
import re
import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import traceback
import pyodbc
from google.genai import errors

from prompts import build_full_prompt, SCHEMA_METADATA, build_intent_prompt

load_dotenv()
app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# ── Engine singleton ──────────────────────────────────────────────────────────
# Created once at startup and reused across all requests.
# Previously get_engine() re-created a full connection pool on every request.
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        driver = os.getenv("SQL_DRIVER").replace(" ", "+")
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")
        _engine = sa.create_engine(
            f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes"
        )
    return _engine


# ── CORS ──────────────────────────────────────────────────────────────────────
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    # GET added for /dashboard endpoint
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response


# ── Helpers ───────────────────────────────────────────────────────────────────


def safe_ai_call(prompt):
    try:
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        )

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        return res.text or ""

    except Exception as e:
        print(f"AI failed: {e}")
        return ""

def detect_intent(user_message):
    try:
        prompt = build_intent_prompt(user_message)
        config = types.GenerateContentConfig(response_mime_type="application/json")
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        text = res.text
        if not text:
            return {"intent": "unsupported", "confidence": 0.0}

        data = json.loads(text)
        intent = data.get("intent")
        confidence = data.get("confidence")

        if confidence is not None:
            try:
                confidence = float(confidence)
            except (ValueError, TypeError):
                confidence = None

        if intent not in ["analytics", "unsupported"] or confidence is None:
            return {"intent": "unsupported", "confidence": 0.0}

        return {"intent": intent, "confidence": confidence}
    except Exception as e:
         print("Intent detection failed:", e)

    # لو Gemini وقع لا تمنع المستخدم من استخدام النظام
    return {
        "intent": "analytics",
        "confidence": 1.0,
    }


def is_safe_query(query):
    q = query.lower()
    if not q.startswith("select") or "from" not in q:
        return False
    forbidden = ["drop", "delete", "update", "insert", "alter", "truncate", "exec", "execute"]
    return not any(x in q for x in forbidden)


def validate_columns(query: str) -> tuple[bool, str]:
    allowed = {c["name"].lower() for c in SCHEMA_METADATA["columns"]}
    sql_reserved = {
        "select", "from", "where", "as", "avg", "sum", "count", "min", "max",
        "group", "by", "order", "desc", "asc", "and", "or", "not", "top",
        "datepart", "month", "year", "convert", "varchar", "int", "float",
        "cast", "is", "null", "like", "between", "having", "distinct", "on",
        "join", "inner", "left", "right", "full", "outer", "cross", "over",
        "partition", "with", "cte", "row_number", "rank", "dense_rank", "ntile",
        "case", "when", "then", "else", "end", "in", "exists", "all", "any",
        "some", "union", "intersect", "except", "offset", "fetch",
        "vw_user_activity", "val", "value",
    }
    # Ignore string literals to prevent matching values as column tokens
    query_clean = re.sub(r"'[^']*'", "", query)
    tokens = set(re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", query_clean.lower()))
    invalid = tokens - allowed - sql_reserved
    if invalid:
        return False, ", ".join(invalid)
    return True, ""


def select_chart_type(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "text"
    n_cols = df.shape[1]
    n_rows = len(df)
    if n_cols == 1:
        return "kpi"
    if n_cols == 2:
        col1, col2 = df.columns[0], df.columns[1]
        is_num1 = pd.api.types.is_numeric_dtype(df[col1])
        is_num2 = pd.api.types.is_numeric_dtype(df[col2])
        is_date1 = pd.api.types.is_datetime64_any_dtype(df[col1])
        if is_num1 and is_num2:
            return "scatter"
        if is_date1 or "date" in col1.lower() or "time" in col1.lower() or "month" in col1.lower():
            return "line"
        return "bar" if n_rows <= 15 else "table"
    return "table"


def clean_df(df):
    df = df.fillna(0)
    df = df.apply(lambda col: col.map(
        lambda x: float(x) if isinstance(x, (int, float)) else x
    ))
    return df


def parse_ai_response(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


# ── /chat ─────────────────────────────────────────────────────────────────────

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json() or {}
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    intent_res = detect_intent(user_msg)
    intent = intent_res.get("intent", "unsupported")
    confidence = intent_res.get("confidence", 0.0)

    print(f"Detected intent: {intent} (confidence: {confidence:.2f})")

    if intent == "unsupported" or confidence < 0.75:
        return jsonify({
            "type": "text",
            "message": "I am an AI analytics assistant for this project. I can only answer questions related to the wellbeing analytics data and dashboard.",
        })

    prompt = build_full_prompt(user_msg)

    try:
        ai_response = safe_ai_call(prompt)
        if not ai_response:
            return jsonify({
        "type": "text",
        "message":
            "The AI service is currently busy. Please try again in a few moments."
    })

        ai_output = parse_ai_response(ai_response)
        if not ai_output or not isinstance(ai_output, dict) or "sql" not in ai_output:
            raise Exception("Invalid AI response format")

        sql_query = ai_output["sql"]
        insight = ai_output.get("insight", "")

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({
            "type": "text",
            "message": "AI service is temporarily unavailable. Please try again later.",
        })

    print("SQL:", sql_query)

    if not is_safe_query(sql_query):
        return jsonify({"error": "Unsafe query"}), 400

    valid, reason = validate_columns(sql_query)
    if not valid:
        return jsonify({"error": f"Invalid columns: {reason}"}), 400

    try:
        df = pd.read_sql(sql_query, get_engine())
        df = clean_df(df)
        print(df.head())
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "SQL failed", "details": str(e)}), 500

    if df.empty:
        return jsonify({"type": "text", "message": "No data found for your query."})

    chart_type = select_chart_type(df)

    try:
        if chart_type == "kpi":
            return jsonify({
                "type": "kpi",
                "value": float(df.iloc[0, 0]),
                "message": insight,
            })

        elif chart_type == "scatter":
            scatter_data = []
            for x, y in zip(df.iloc[:, 0], df.iloc[:, 1]):
                try:
                    scatter_data.append({"x": float(x), "y": float(y)})
                except (ValueError, TypeError):
                    continue
            return jsonify({
                "type": "scatter",
                "scatterData": scatter_data,
                "message": insight,
            })

        elif chart_type == "line":
            return jsonify({
                "type": "line",
                "labels": df.iloc[:, 0].astype(str).tolist(),
                "values": df.iloc[:, 1].tolist(),
                "message": insight,
            })

        elif chart_type == "bar":
            return jsonify({
                "type": "bar_chart",
                "labels": df.iloc[:, 0].astype(str).tolist(),
                "values": df.iloc[:, 1].tolist(),
                "message": insight,
            })

        elif chart_type == "table":
            return jsonify({
                "type": "table",
                "data": df.to_dict(orient="records"),
                "message": insight,
            })

        return jsonify({"type": "text", "message": insight})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Response failed", "details": str(e)}), 500


# ── /dashboard ────────────────────────────────────────────────────────────────

def _fmt_month(ym: str) -> str:
    """Convert '2024-01' → 'Jan 24' for readable line chart x-axis labels."""
    try:
        dt = datetime.datetime.strptime(ym, "%Y-%m")
        return dt.strftime("%b %y")
    except Exception:
        return ym


def _generate_dashboard_insight(avg_wellbeing, active_users, avg_study_hours, total_reels):
    try:
        prompt = (
            f"Write a short, engaging, single-sentence Arabic insight explaining the user wellbeing data: "
            f"Average Wellbeing Score is {avg_wellbeing:.1f}/100, Active Users count is {active_users:,}, "
            f"Average Study Hours is {avg_study_hours:.1f}, and Total Reels Watched is {total_reels:,}. "
            f"Explain potential relationships or observations, e.g., high study hours or high short content exposure. "
            f"Keep it professional and return ONLY a JSON object with a single key 'insight'."
        )
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
        )

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        data = json.loads(res.text)
        return data.get("insight") or (
            f"Average wellbeing is {avg_wellbeing:.1f}/100 across {active_users:,} users."
        )

    except Exception as e:
        print("Insight failed:", e)

        # fallback سريع
        return (
            f"Average wellbeing is {avg_wellbeing:.1f}/100 across {active_users:,} users."
        )
@app.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        engine = get_engine()

        # ── KPIs ─────────────────────────────────────────────────────────────

        avg_wellbeing = float(pd.read_sql(
            "SELECT AVG(wellbeing_score) AS value FROM vw_user_activity",
            engine,
        ).iloc[0]["value"])

        active_users = int(pd.read_sql(
            "SELECT COUNT(DISTINCT username) AS value FROM vw_user_activity",
            engine,
        ).iloc[0]["value"])

        avg_study_hours = float(pd.read_sql(
            "SELECT AVG(study_hours) AS value FROM vw_user_activity",
            engine,
        ).iloc[0]["value"])

        total_reels = float(pd.read_sql(
            "SELECT SUM(total_reels_watched) AS value FROM vw_user_activity",
            engine,
        ).iloc[0]["value"])

        # ── Bar Chart — Wellbeing by Age Group ───────────────────────────────
        

        bar_df = pd.read_sql("""
            SELECT
                age_group,
                ROUND(AVG(wellbeing_score), 2) AS value
            FROM vw_user_activity
            GROUP BY age_group
            ORDER BY age_group
        """, engine)

        # ── Line Chart — Monthly Wellbeing Trend ─────────────────────────────
     

        line_df = pd.read_sql("""
            SELECT
    age_group AS label,
    ROUND(AVG(study_hours),2) AS value
FROM vw_user_activity
GROUP BY age_group
ORDER BY age_group
        """, engine)

        line_labels = [_fmt_month(str(v)) for v in line_df["label"].tolist()]
        line_values = [round(float(v), 2) for v in line_df["value"].tolist()]

        # ── AI Insight ───────────────────────────────────────────────────────

        insight = _generate_dashboard_insight(
            avg_wellbeing, active_users, avg_study_hours, total_reels
        )
        

        return jsonify({
            "kpis": [
                {"label": "Average Wellbeing", "value": avg_wellbeing},
                {"label": "Active Users",      "value": active_users},
                {"label": "Study Hours",       "value": avg_study_hours},
                {"label": "Reels Watched",     "value": total_reels},
            ],
            "bar_chart": {
                "title": "Wellbeing by Age Group",
                "labels": bar_df["age_group"].astype(str).tolist(),
                "values": [round(float(v), 2) for v in bar_df["value"].tolist()],
            },
            "line_chart": {
                "title": "Wellbeing Trend",
                "labels": line_labels,
                "values": line_values,
            },
            "insight": insight,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
