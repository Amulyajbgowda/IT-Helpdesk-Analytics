import pandas as pd
from pathlib import Path

# ==========================================
# 1. PATH
# ==========================================

project_dir = Path(__file__).resolve().parent.parent

file_path = (
    project_dir
    / "data"
    / "processed"
    / "incidents_cleaned.csv"
)

df = pd.read_csv(file_path)


# ==========================================
# 2. BASIC INFORMATION
# ==========================================

print("\n========== DATASET VALIDATION ==========")

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==========================================
# 3. DUPLICATE INCIDENTS
# ==========================================

print("\n========== DUPLICATE INCIDENT IDs ==========")

duplicate_ids = df["number"].duplicated().sum()

print("Duplicate incident IDs:", duplicate_ids)


# ==========================================
# 4. MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")

missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)

print(missing)


# ==========================================
# 5. NEGATIVE RESOLUTION TIMES
# ==========================================

print("\n========== NEGATIVE RESOLUTION TIMES ==========")

negative_resolution = (
    df["resolution_hours"] < 0
).sum()

print("Negative resolution times:", negative_resolution)


# ==========================================
# 6. NEGATIVE CLOSURE TIMES
# ==========================================

print("\n========== NEGATIVE CLOSURE TIMES ==========")

negative_closure = (
    df["closure_hours"] < 0
).sum()

print("Negative closure times:", negative_closure)


# ==========================================
# 7. EXTREME RESOLUTION TIMES
# ==========================================

print("\n========== EXTREME RESOLUTION TIMES ==========")

print(
    "Resolution > 30 days:",
    (df["resolution_hours"] > 30 * 24).sum()
)

print(
    "Resolution > 60 days:",
    (df["resolution_hours"] > 60 * 24).sum()
)

print(
    "Resolution > 90 days:",
    (df["resolution_hours"] > 90 * 24).sum()
)


# ==========================================
# 8. PRIORITY DISTRIBUTION
# ==========================================

print("\n========== PRIORITY DISTRIBUTION ==========")

print(
    df["priority"]
    .value_counts(dropna=False)
)


# ==========================================
# 9. SLA DISTRIBUTION
# ==========================================

print("\n========== SLA DISTRIBUTION ==========")

print(
    df["sla_status"]
    .value_counts()
)


# ==========================================
# 10. CATEGORY DISTRIBUTION
# ==========================================

print("\n========== TOP 15 CATEGORIES ==========")

print(
    df["category"]
    .value_counts(dropna=False)
    .head(15)
)


# ==========================================
# 11. ASSIGNMENT GROUP DISTRIBUTION
# ==========================================

print("\n========== TOP 15 ASSIGNMENT GROUPS ==========")

print(
    df["assignment_group"]
    .value_counts(dropna=False)
    .head(15)
)


# ==========================================
# 12. REOPEN ANALYSIS
# ==========================================

print("\n========== REOPEN ANALYSIS ==========")

print(
    df["was_reopened"]
    .value_counts()
)


# ==========================================
# 13. REASSIGNMENT ANALYSIS
# ==========================================

print("\n========== REASSIGNMENT SUMMARY ==========")

print(
    df["reassignment_count"]
    .describe()
)


# ==========================================
# 14. RESOLUTION SUMMARY
# ==========================================

print("\n========== RESOLUTION SUMMARY ==========")

print(
    df["resolution_hours"]
    .describe()
)


# ==========================================
# 15. CLOSURE SUMMARY
# ==========================================

print("\n========== CLOSURE SUMMARY ==========")

print(
    df["closure_hours"]
    .describe()
)


# ==========================================
# 16. DATE RANGE
# ==========================================

print("\n========== DATE RANGE ==========")

print(
    "First incident opened:",
    df["opened_at"].min()
)

print(
    "Last incident opened:",
    df["opened_at"].max()
)


# ==========================================
# 17. FINAL CHECK
# ==========================================

print("\n========== VALIDATION COMPLETE ==========")

if duplicate_ids == 0:
    print("✓ Incident IDs are unique")
else:
    print("⚠ Duplicate incident IDs found")

if negative_resolution == 0:
    print("✓ No negative resolution times")
else:
    print("⚠ Negative resolution times found")

if negative_closure == 0:
    print("✓ No negative closure times")
else:
    print("⚠ Negative closure times found")

print("\nDataset is ready for the next validation stage.")