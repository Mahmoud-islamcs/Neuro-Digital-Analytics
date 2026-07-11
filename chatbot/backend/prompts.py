import json

SCHEMA_METADATA = {
    "table": "vw_user_activity",
    "columns": [
        {"name": "total_reels_watched", "type": "INT", "description": "Number of short videos watched", "aggregations": ["SUM", "AVG", "COUNT"]},
        {"name": "study_hours", "type": "FLOAT", "description": "Hours spent studying", "aggregations": ["SUM", "AVG", "MAX", "MIN"]},
        {"name": "wellbeing_score", "type": "FLOAT", "description": "Score 0-100", "aggregations": ["AVG", "MAX", "MIN", "SUM"]},
        {"name": "brainrot_exposure_score", "type": "FLOAT", "description": "Score 0-100", "aggregations": ["AVG", "MAX", "MIN", "SUM"]},
        {"name": "focus_sessions_count", "type": "INT", "description": "Number of focus sessions", "aggregations": ["SUM", "AVG", "COUNT"]},
        {"name": "peak_hour", "type": "INT", "description": "Peak activity hour (0-23)", "aggregations": ["AVG", "MAX", "MIN", "MODE"]},
        {"name": "brainrot_stage", "type": "VARCHAR", "description": "Cognitive stage", "allowed_values": ["Early", "Moderate", "Severe"], "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "age_group", "type": "VARCHAR", "description": "Age group", "allowed_values": ["18-24", "25-34", "35-44", "45+"], "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "region", "type": "VARCHAR", "description": "User region", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "device_type", "type": "VARCHAR", "description": "Device used", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "activity_id", "type": "INT", "description": "Primary key", "aggregations": ["COUNT"]},
        {"name": "short_content_percentage", "type": "FLOAT", "description": "Percentage of short content", "aggregations": ["AVG", "SUM"]},
        {"name": "coffee_consumed_per_day", "type": "INT", "description": "Cups per day", "aggregations": ["AVG", "SUM", "MAX"]},
        {"name": "smoking_breaks_count", "type": "INT", "description": "Breaks per day", "aggregations": ["AVG", "SUM", "MAX"]},
        {"name": "username", "type": "VARCHAR", "description": "User name", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "age", "type": "INT", "description": "User age", "aggregations": ["AVG", "MAX", "MIN", "COUNT"]},
        {"name": "is_smoker", "type": "BIT", "description": "0 or 1", "allowed_values": [0, 1], "aggregations": ["SUM", "AVG", "GROUP BY"]},
        {"name": "base_focus_level", "type": "FLOAT", "description": "Baseline focus (0-100)", "aggregations": ["AVG", "MAX", "MIN"]},
        {"name": "attention_span_level", "type": "VARCHAR", "description": "Categorical attention level", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "aura_color_code", "type": "VARCHAR", "description": "Color code", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "coffee_level", "type": "VARCHAR", "description": "Categorical coffee level", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "smoking_status", "type": "VARCHAR", "description": "Categorical smoking status", "aggregations": ["COUNT", "GROUP BY"]},
        {"name": "full_date", "type": "DATE", "description": "Activity date", "aggregations": ["MIN", "MAX", "COUNT", "GROUP BY"]},
        {"name": "is_late_night", "type": "BIT", "description": "0 or 1", "allowed_values": [0, 1], "aggregations": ["SUM", "AVG", "GROUP BY"]},
        {"name": "is_exam_season", "type": "BIT", "description": "0 or 1", "allowed_values": [0, 1], "aggregations": ["SUM", "AVG", "GROUP BY"]},
        {"name": "is_weekend", "type": "BIT", "description": "0 or 1", "allowed_values": [0, 1], "aggregations": ["SUM", "AVG", "GROUP BY"]},
    ]
}

FEW_SHOT_EXAMPLES = [
    {
        "question": "What is the average wellbeing score?",
        "sql": "SELECT AVG(wellbeing_score) AS val FROM vw_user_activity",
        "insight": "متوسط درجة الرفاهية للمستخدمين هو 72.5 من أصل 100."
    },
    {
        "question": "What is the total number of reels watched?",
        "sql": "SELECT SUM(total_reels_watched) AS val FROM vw_user_activity",
        "insight": "تم مشاهدة 1.2 مليون reel إجمالاً."
    },
    {
        "question": "Show average brainrot exposure by age group.",
        "sql": "SELECT age_group, AVG(brainrot_exposure_score) AS val FROM vw_user_activity GROUP BY age_group",
        "insight": "الفئة العمرية 18-24 تسجل أعلى متوسط تعرض بقيمة 85.3."
    },
    {
        "question": "Show average wellbeing score over months.",
        "sql": "SELECT DATEPART(month, full_date) AS month, AVG(wellbeing_score) AS val FROM vw_user_activity GROUP BY DATEPART(month, full_date) ORDER BY month",
        "insight": "انخفضت درجة الرفاهية خلال موسم الامتحانات (يونيو) إلى 58.2."
    },
    {
        "question": "What is the relationship between study hours and brainrot exposure?",
        "sql": "SELECT study_hours, brainrot_exposure_score FROM vw_user_activity",
        "insight": "يوجد علاقة عكسية بين ساعات المذاكرة ومؤشر التعرض للمحتوى القصير."
    },
    {
        "question": "Who are the top 5 users by reels watched?",
        "sql": "SELECT TOP 5 username, total_reels_watched AS val FROM vw_user_activity ORDER BY total_reels_watched DESC",
        "insight": "المستخدم Ahmed يتصدر بـ 4,200 reel."
    },
    {
        "question": "How many users are in each brainrot stage?",
        "sql": "SELECT brainrot_stage, COUNT(*) AS val FROM vw_user_activity GROUP BY brainrot_stage",
        "insight": "45% من المستخدمين في المرحلة المتوسطة من التعرض."
    },
    {
        "question": "What percentage of sessions are late night?",
        "sql": "SELECT 100.0 * SUM(CAST(is_late_night AS INT)) / COUNT(*) AS val FROM vw_user_activity",
        "insight": "32% من الجلسات تحدث في وقت متأخر من الليل."
    },
    {
        "question": "Compare average focus level between smokers and non-smokers.",
        "sql": "SELECT is_smoker, AVG(base_focus_level) AS val FROM vw_user_activity GROUP BY is_smoker",
        "insight": "المدخنون يسجلون تركيزاً أقل بنسبة 15% مقارنة بغير المدخنين."
    },
    {
        "question": "What is the average coffee consumption per region?",
        "sql": "SELECT region, AVG(coffee_consumed_per_day) AS val FROM vw_user_activity GROUP BY region",
        "insight": "منطقة الرياض تسجل أعلى متوسط استهلاك للقهوة (4.2 كوب/يوم)."
    }
]


def _build_schema_block() -> str:
    lines = []
    for col in SCHEMA_METADATA["columns"]:
        line = f"- {col['name']} ({col['type']}): {col['description']}"
        if "allowed_values" in col:
            line += f" | Allowed values: {col['allowed_values']}"
        if "aggregations" in col:
            line += f" | Valid aggregations: {', '.join(col['aggregations'])}"
        lines.append(line)
    return "\n".join(lines)


def _build_examples_block() -> str:
    blocks = []
    for ex in FEW_SHOT_EXAMPLES:
        blocks.append(
            f"""Question: {ex['question']}
SQL: {ex['sql']}
Insight: {ex['insight']}"""
        )
    return "\n\n".join(blocks)


def build_system_prompt() -> str:
    schema = _build_schema_block()
    examples = _build_examples_block()
    return f"""You are BrainRot Analytics AI, a senior data analyst operating on a SQL Server data warehouse.
Your task is to convert the user's natural language question into a valid SQL Server query and a brief, insightful Arabic summary.

# DATABASE SCHEMA
You are ONLY allowed to query the table: `{SCHEMA_METADATA['table']}`.
Allowed columns and their properties:
{schema}

# RULES
1. ONLY use columns listed above. NEVER invent new columns or tables.
2. Use SQL Server T-SQL syntax ONLY.
3. Use `TOP N` instead of `LIMIT`. NEVER use `LIMIT` or `OFFSET`.
4. Use `CONVERT(VARCHAR, full_date, 23)` for date formatting if needed.
5. For KPIs (single value), alias the aggregated column as `val` or `value`.
6. For group-by queries, the first column should be the dimension, the second should be the metric.
7. For time-series, group by `full_date` or `DATEPART(month, full_date)` or `DATEPART(year, full_date)`.
8. Return ONLY valid JSON. No markdown, no explanations, no code blocks outside the JSON.

# OUTPUT FORMAT
Return ONLY a raw JSON object with exactly these keys:
{{
  "sql": "SELECT ...",
  "insight": "نص تحليلي بالعربية يشرح النتيجة ..."
}}

# FEW-SHOT EXAMPLES
{examples}

# USER QUESTION
"""


def build_full_prompt(user_question: str) -> str:
    return build_system_prompt() + user_question.strip()


CLASSIFIER_SYSTEM_PROMPT = """You are an AI Analytics Intent Classifier for a wellbeing analytics database.
Your sole job is to classify the user's message into one of two intents: "analytics" or "unsupported".

Intents:
1. "analytics": The user is asking for analytics, metrics, aggregations, trends, statistics, or records from the wellbeing analytics database.
Typical database attributes include:
- wellbeing score
- study hours
- reels watched / short content percentage
- brainrot exposure score / brainrot stage
- coffee consumption / level
- smoking breaks / status
- age / age group
- region / location
- device type
- focus level / focus sessions
- date / time / weekend / exam season
Even if the query is in Arabic, English, or mixed, if it asks for database analytics, return "analytics".

2. "unsupported": Everything else, including:
- Greetings and pleasantries ("hello", "hi", "how are you", "صباح الخير", "اخبارك", etc.)
- Thanks and appreciation ("thank you", "شكرا", etc.)
- General chatbot conversations, jokes, questions about Python, translate requests, general world knowledge, etc.

Rules:
- You must output ONLY a JSON object with the keys "intent" and "confidence".
- "intent" must be exactly "analytics" or "unsupported".
- "confidence" must be a float between 0.0 and 1.0 indicating your confidence in the classification.

Examples:
- User: "What is the average wellbeing score?"
  Output: {"intent": "analytics", "confidence": 0.98}
- User: "Show users by brainrot stage."
  Output: {"intent": "analytics", "confidence": 0.99}
- User: "Compare study hours by region."
  Output: {"intent": "analytics", "confidence": 0.97}
- User: "How are you?"
  Output: {"intent": "unsupported", "confidence": 0.99}
- User: "Tell me a joke"
  Output: {"intent": "unsupported", "confidence": 0.98}
- User: "Translate this sentence to Arabic"
  Output: {"intent": "unsupported", "confidence": 0.99}
- User: "اخبارك"
  Output: {"intent": "unsupported", "confidence": 0.97}
- User: "صباح الخير"
  Output: {"intent": "unsupported", "confidence": 0.98}
- User: "اعطيني average sleep hours"
  Output: {"intent": "analytics", "confidence": 0.95}
- User: "من فاز بكأس العالم؟"
  Output: {"intent": "unsupported", "confidence": 0.99}
"""


def build_intent_prompt(user_message: str) -> str:
    return CLASSIFIER_SYSTEM_PROMPT + f"\nUser Message: {user_message.strip()}\nOutput JSON:"

