import pandas as pd
from pathlib import Path

# ==========================================
# 1. LOAD DATA
# ==========================================

project_dir = Path(__file__).resolve().parent.parent

file_path = (
    project_dir
    / "data"
    / "processed"
    / "incidents_analytics.csv"
)

df = pd.read_csv(file_path)

print("\n========== INITIAL BUSINESS ANALYSIS ==========")

print("Total incidents:", len(df))


# ==========================================
# 2. SLA PERFORMANCE
# ==========================================

print("\n========== SLA PERFORMANCE ==========")

sla_summary = (
    df.groupby("sla_status")
      .agg(
          incidents=("number", "count"),
          avg_resolution_hours=("resolution_hours", "mean")
      )
      .sort_values("incidents", ascending=False)
)

sla_summary["percentage"] = (
    sla_summary["incidents"]
    / len(df)
    * 100
)

print(sla_summary)


# ==========================================
# 3. SLA BY PRIORITY
# ==========================================

print("\n========== SLA BY PRIORITY ==========")

priority_sla = (
    df.groupby("priority_label")
      .agg(
          incidents=("number", "count"),
          sla_breaches=("sla_breached", "sum"),
          avg_resolution_hours=("resolution_hours", "mean")
      )
)

priority_sla["sla_breach_rate"] = (
    priority_sla["sla_breaches"]
    / priority_sla["incidents"]
    * 100
)

print(
    priority_sla
    .sort_values("sla_breach_rate", ascending=False)
)


# ==========================================
# 4. SLA BY ASSIGNMENT GROUP
# ==========================================

print("\n========== TOP GROUPS BY SLA BREACH RATE ==========")

group_sla = (
    df.groupby("assignment_group")
      .agg(
          incidents=("number", "count"),
          sla_breaches=("sla_breached", "sum"),
          avg_resolution_hours=("resolution_hours", "mean")
      )
)

group_sla["sla_breach_rate"] = (
    group_sla["sla_breaches"]
    / group_sla["incidents"]
    * 100
)

# Only consider groups with at least 100 incidents
group_sla_filtered = (
    group_sla[group_sla["incidents"] >= 100]
    .sort_values("sla_breach_rate", ascending=False)
)

print(
    group_sla_filtered.head(15)
)


# ==========================================
# 5. CATEGORY PERFORMANCE
# ==========================================

print("\n========== TOP CATEGORIES BY SLA BREACH RATE ==========")

category_sla = (
    df.groupby("category")
      .agg(
          incidents=("number", "count"),
          sla_breaches=("sla_breached", "sum"),
          avg_resolution_hours=("resolution_hours", "mean")
      )
)

category_sla["sla_breach_rate"] = (
    category_sla["sla_breaches"]
    / category_sla["incidents"]
    * 100
)

category_sla_filtered = (
    category_sla[category_sla["incidents"] >= 100]
    .sort_values("sla_breach_rate", ascending=False)
)

print(
    category_sla_filtered.head(15)
)


# ==========================================
# 6. PRIORITY VS RESOLUTION TIME
# ==========================================

print("\n========== RESOLUTION TIME BY PRIORITY ==========")

resolution_priority = (
    df.groupby("priority_label")
      .agg(
          incidents=("number", "count"),
          average_resolution_hours=("resolution_hours", "mean"),
          median_resolution_hours=("resolution_hours", "median"),
          average_closure_hours=("closure_hours", "mean")
      )
      .sort_values("median_resolution_hours")
)

print(resolution_priority)


# ==========================================
# 7. REASSIGNMENT IMPACT
# ==========================================

print("\n========== REASSIGNMENT IMPACT ==========")

reassignment_analysis = (
    df.groupby("high_reassignment_flag")
      .agg(
          incidents=("number", "count"),
          avg_resolution_hours=("resolution_hours", "mean"),
          sla_breaches=("sla_breached", "sum")
      )
)

reassignment_analysis["sla_breach_rate"] = (
    reassignment_analysis["sla_breaches"]
    / reassignment_analysis["incidents"]
    * 100
)

print(reassignment_analysis)


# ==========================================
# 8. REOPEN IMPACT
# ==========================================

print("\n========== REOPEN IMPACT ==========")

reopen_analysis = (
    df.groupby("reopened_flag")
      .agg(
          incidents=("number", "count"),
          avg_resolution_hours=("resolution_hours", "mean"),
          sla_breaches=("sla_breached", "sum")
      )
)

reopen_analysis["sla_breach_rate"] = (
    reopen_analysis["sla_breaches"]
    / reopen_analysis["incidents"]
    * 100
)

print(reopen_analysis)


# ==========================================
# 9. MONTHLY INCIDENT TREND
# ==========================================

print("\n========== MONTHLY INCIDENT VOLUME ==========")

monthly = (
    df.groupby("opened_month_year")
      .agg(
          incidents=("number", "count"),
          sla_breaches=("sla_breached", "sum")
      )
)

monthly["sla_breach_rate"] = (
    monthly["sla_breaches"]
    / monthly["incidents"]
    * 100
)

print(monthly.to_string())


# ==========================================
# 10. FINAL SUMMARY
# ==========================================

print("\n========== KEY DATASET METRICS ==========")

print("Total incidents:", len(df))

print(
    "SLA breach rate:",
    round(df["sla_breached"].mean() * 100, 2),
    "%"
)

print(
    "Average resolution:",
    round(df["resolution_hours"].mean(), 2),
    "hours"
)

print(
    "Median resolution:",
    round(df["resolution_hours"].median(), 2),
    "hours"
)

print(
    "Average closure:",
    round(df["closure_hours"].mean(), 2),
    "hours"
)

print(
    "Reopened incidents:",
    df["reopened_flag"].sum()
)

print(
    "High-reassignment incidents:",
    df["high_reassignment_flag"].sum()
)

print("\n========== ANALYSIS COMPLETE ==========")