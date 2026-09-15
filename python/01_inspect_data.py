import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Locate the dataset
# -----------------------------
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw" / "incident_event_log.csv"

# -----------------------------
# 2. Load dataset
# -----------------------------
df = pd.read_csv(file_path)

# -----------------------------
# 3. Basic information
# -----------------------------
print("\n========== DATASET OVERVIEW ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
for column in df.columns:
    print(column)

# -----------------------------
# 4. Data types
# -----------------------------
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# -----------------------------
# 5. Missing values
# -----------------------------
print("\n========== MISSING VALUES ==========")
missing = df.isnull().sum()

missing = missing[missing > 0].sort_values(ascending=False)

if len(missing) == 0:
    print("No missing values found.")
else:
    print(missing)

# -----------------------------
# 6. Duplicate rows
# -----------------------------
print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())

# -----------------------------
# 7. Unique incidents
# -----------------------------
print("\n========== UNIQUE INCIDENTS ==========")

if "number" in df.columns:
    print("Unique incidents:", df["number"].nunique())

# -----------------------------
# 8. Sample records
# -----------------------------
print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

# -----------------------------
# 9. Basic statistics
# -----------------------------
print("\n========== NUMERICAL SUMMARY ==========")
print(df.describe(include="all").T)

print("\n========== INSPECTION COMPLETE ==========")