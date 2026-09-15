import pandas as pd
from pathlib import Path

# ==========================================
# 1. PATHS
# ==========================================

project_dir = Path(__file__).resolve().parent.parent

input_file = (
    project_dir
    / "data"
    / "processed"
    / "incidents_cleaned.csv"
)

output_file = (
    project_dir
    / "data"
    / "processed"
    / "incidents_analytics.csv"
)


# ==========================================
# 2. LOAD CLEANED DATA
# ==========================================

print("Loading cleaned incident dataset...")

df = pd.read_csv(input_file)

print("Records:", len(df))


# ==========================================
# 3. CONVERT DATE COLUMNS
# ==========================================

date_columns = [
    "opened_at",
    "sys_created_at",
    "resolved_at",
    "closed_at"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )


# ==========================================
# 4. SELECT BUSINESS-RELEVANT COLUMNS
# ==========================================

analytics_columns = [
    # Identification
    "number",

    # Incident information
    "incident_state",
    "active",
    "contact_type",

    # Classification
    "category",
    "subcategory",
    "u_symptom",

    # Business impact
    "impact",
    "urgency",
    "priority",

    # Assignment
    "assignment_group",
    "assigned_to",

    # Location / caller
    "location",
    "caller_id",

    # Incident handling
    "reassignment_count",
    "reopen_count",
    "sys_mod_count",

    # SLA
    "made_sla",
    "sla_status",

    # Resolution
    "resolved_by",
    "resolved_at",
    "closed_code",
    "closed_at",

    # Dates
    "opened_at",

    # Derived metrics
    "resolution_hours",
    "resolution_days",
    "closure_hours",
    "closure_days",
    "was_reopened",
    "high_reassignment",

    # Date analytics
    "opened_date",
    "opened_year",
    "opened_month",
    "opened_month_name",
    "opened_day_name"
]


analytics_df = df[analytics_columns].copy()


# ==========================================
# 5. CLEAN TEXT COLUMNS
# ==========================================

text_columns = [
    "category",
    "subcategory",
    "u_symptom",
    "assignment_group",
    "assigned_to",
    "location",
    "caller_id",
    "resolved_by",
    "closed_code"
]

for column in text_columns:

    analytics_df[column] = (
        analytics_df[column]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )


# ==========================================
# 6. CREATE PRIORITY LEVEL
# ==========================================

analytics_df["priority_level"] = (
    analytics_df["priority"]
    .str.extract(r"(\d+)")
    .astype("Int64")
)


# ==========================================
# 7. CREATE PRIORITY LABEL
# ==========================================

analytics_df["priority_label"] = (
    analytics_df["priority"]
    .str.replace(
        r"^\d+\s*-\s*",
        "",
        regex=True
    )
)


# ==========================================
# 8. CREATE IMPACT LEVEL
# ==========================================

analytics_df["impact_level"] = (
    analytics_df["impact"]
    .str.extract(r"(\d+)")
    .astype("Int64")
)


# ==========================================
# 9. CREATE URGENCY LEVEL
# ==========================================

analytics_df["urgency_level"] = (
    analytics_df["urgency"]
    .str.extract(r"(\d+)")
    .astype("Int64")
)


# ==========================================
# 10. CREATE MONTH-YEAR
# ==========================================

analytics_df["opened_month_year"] = (
    analytics_df["opened_at"]
    .dt.to_period("M")
    .astype(str)
)


# ==========================================
# 11. CREATE SLA NUMERIC FLAG
# ==========================================

analytics_df["sla_breached"] = (
    analytics_df["made_sla"] == False
).astype(int)


# ==========================================
# 12. CREATE REOPEN NUMERIC FLAG
# ==========================================

analytics_df["reopened_flag"] = (
    analytics_df["was_reopened"] == True
).astype(int)


# ==========================================
# 13. CREATE HIGH REASSIGNMENT FLAG
# ==========================================

analytics_df["high_reassignment_flag"] = (
    analytics_df["reassignment_count"] >= 3
).astype(int)


# ==========================================
# 14. CREATE RESOLUTION BUCKET
# ==========================================

def resolution_bucket(hours):

    if pd.isna(hours):
        return "Not Resolved"

    if hours <= 4:
        return "0-4 Hours"

    elif hours <= 24:
        return "4-24 Hours"

    elif hours <= 72:
        return "1-3 Days"

    elif hours <= 168:
        return "3-7 Days"

    elif hours <= 720:
        return "7-30 Days"

    else:
        return "30+ Days"


analytics_df["resolution_bucket"] = (
    analytics_df["resolution_hours"]
    .apply(resolution_bucket)
)


# ==========================================
# 15. CREATE PRIORITY SORT ORDER
# ==========================================

analytics_df = analytics_df.sort_values(
    "opened_at"
).reset_index(drop=True)


# ==========================================
# 16. SAVE
# ==========================================

analytics_df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 17. VALIDATION
# ==========================================

print("\n========== ANALYTICS TABLE CREATED ==========")

print("Rows:", len(analytics_df))
print("Columns:", len(analytics_df.columns))

print("\nOutput:")
print(output_file)

print("\nPriority distribution:")
print(
    analytics_df["priority_label"]
    .value_counts()
)

print("\nResolution buckets:")
print(
    analytics_df["resolution_bucket"]
    .value_counts()
)

print("\nSLA distribution:")
print(
    analytics_df["sla_status"]
    .value_counts()
)

print("\nTop assignment groups:")
print(
    analytics_df["assignment_group"]
    .value_counts()
    .head(10)
)

print("\n========== SAMPLE RECORDS ==========")

print(
    analytics_df[
        [
            "number",
            "priority",
            "priority_label",
            "category",
            "assignment_group",
            "sla_status",
            "resolution_hours",
            "resolution_bucket"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\n========== SUCCESS ==========")