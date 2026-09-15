import pandas as pd
from pathlib import Path

# ==========================================
# 1. PATHS
# ==========================================

project_dir = Path(__file__).resolve().parent.parent

input_file = project_dir / "data" / "raw" / "incident_event_log.csv"
output_dir = project_dir / "data" / "processed"

output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "incidents_cleaned.csv"


# ==========================================
# 2. LOAD RAW DATA
# ==========================================

print("Loading dataset...")

df = pd.read_csv(input_file)

print("Raw event records:", len(df))
print("Unique incidents:", df["number"].nunique())


# ==========================================
# 3. REPLACE '?' WITH MISSING VALUES
# ==========================================

df = df.replace("?", pd.NA)


# ==========================================
# 4. CONVERT DATE COLUMNS
# ==========================================

date_columns = [
    "opened_at",
    "sys_created_at",
    "sys_updated_at",
    "resolved_at",
    "closed_at"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )


# ==========================================
# 5. SORT EVENT HISTORY
# ==========================================

df = df.sort_values(
    ["number", "sys_updated_at"]
).reset_index(drop=True)


# ==========================================
# 6. HELPER FUNCTIONS
# ==========================================

def first_non_null(series):
    series = series.dropna()

    if len(series) == 0:
        return pd.NA

    return series.iloc[0]


def last_non_null(series):
    series = series.dropna()

    if len(series) == 0:
        return pd.NA

    return series.iloc[-1]


# ==========================================
# 7. CREATE INCIDENT-LEVEL DATASET
# ==========================================

print("\nCreating incident-level dataset...")

first_value_columns = [
    "opened_at",
    "sys_created_at",
    "caller_id",
    "opened_by",
    "contact_type",
    "location",
    "category",
    "subcategory",
    "u_symptom",
    "cmdb_ci",
    "impact",
    "urgency",
    "priority",
    "assignment_group",
    "knowledge",
    "u_priority_confirmation",
    "notify",
    "problem_id",
    "rfc",
    "vendor",
    "caused_by"
]


last_value_columns = [
    "incident_state",
    "active",
    "reassignment_count",
    "reopen_count",
    "sys_mod_count",
    "made_sla",
    "assigned_to",
    "closed_code",
    "resolved_by",
    "resolved_at",
    "closed_at"
]


aggregations = {}

for column in first_value_columns:
    aggregations[column] = first_non_null

for column in last_value_columns:
    aggregations[column] = last_non_null


incident_df = (
    df.groupby("number", sort=False)
      .agg(aggregations)
      .reset_index()
)


# ==========================================
# 8. FIX DATE TYPES AFTER GROUPBY
# ==========================================

for column in [
    "opened_at",
    "sys_created_at",
    "resolved_at",
    "closed_at"
]:
    incident_df[column] = pd.to_datetime(
        incident_df[column],
        errors="coerce"
    )


# ==========================================
# 9. CALCULATE RESOLUTION TIME
# ==========================================

print("Calculating analytical metrics...")

incident_df["resolution_hours"] = (
    incident_df["resolved_at"] -
    incident_df["opened_at"]
).dt.total_seconds() / 3600


# ==========================================
# 10. CALCULATE CLOSURE TIME
# ==========================================

incident_df["closure_hours"] = (
    incident_df["closed_at"] -
    incident_df["opened_at"]
).dt.total_seconds() / 3600


# ==========================================
# 11. DAYS TO RESOLUTION
# ==========================================

incident_df["resolution_days"] = (
    incident_df["resolution_hours"] / 24
)


# ==========================================
# 12. DAYS TO CLOSURE
# ==========================================

incident_df["closure_days"] = (
    incident_df["closure_hours"] / 24
)


# ==========================================
# 13. DATE ANALYTICS
# ==========================================

incident_df["opened_date"] = (
    incident_df["opened_at"].dt.date
)

incident_df["opened_year"] = (
    incident_df["opened_at"].dt.year
)

incident_df["opened_month"] = (
    incident_df["opened_at"].dt.month
)

incident_df["opened_month_name"] = (
    incident_df["opened_at"].dt.strftime("%B")
)

incident_df["opened_day_name"] = (
    incident_df["opened_at"].dt.strftime("%A")
)


# ==========================================
# 14. SLA STATUS
# ==========================================

incident_df["sla_status"] = incident_df["made_sla"].map({
    True: "Met SLA",
    False: "Breached SLA"
})


# ==========================================
# 15. REOPEN FLAG
# ==========================================

incident_df["was_reopened"] = (
    incident_df["reopen_count"] > 0
)


# ==========================================
# 16. HIGH REASSIGNMENT FLAG
# ==========================================

incident_df["high_reassignment"] = (
    incident_df["reassignment_count"] >= 3
)


# ==========================================
# 17. SAVE
# ==========================================

incident_df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 18. VALIDATION
# ==========================================

print("\n========== CLEANING COMPLETE ==========")

print("Incident-level records:", len(incident_df))
print("Columns:", len(incident_df.columns))

print("\nOutput file:")
print(output_file)

print("\nSLA status:")
print(incident_df["sla_status"].value_counts())

print("\nReopened incidents:")
print(incident_df["was_reopened"].value_counts())

print("\nFinal incident states:")
print(incident_df["incident_state"].value_counts())

print("\nResolution time summary:")
print(
    incident_df["resolution_hours"].describe()
)

print("\nClosure time summary:")
print(
    incident_df["closure_hours"].describe()
)

print("\n========== FIRST 5 INCIDENTS ==========")

print(
    incident_df[
        [
            "number",
            "opened_at",
            "resolved_at",
            "closed_at",
            "priority",
            "assignment_group",
            "made_sla",
            "resolution_hours",
            "closure_hours"
        ]
    ].head().to_string(index=False)
)

print("\n========== SUCCESS ==========")