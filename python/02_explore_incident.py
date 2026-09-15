import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw" / "incident_event_log.csv"

df = pd.read_csv(file_path)

# Select one incident that appears multiple times
incident_id = "INC0000045"

incident = df[df["number"] == incident_id].copy()

print("\n========== INCIDENT HISTORY ==========")
print("Incident:", incident_id)
print("Number of event records:", len(incident))

print("\n========== EVENT HISTORY ==========")

columns_to_show = [
    "number",
    "incident_state",
    "active",
    "reassignment_count",
    "reopen_count",
    "sys_mod_count",
    "made_sla",
    "opened_at",
    "sys_updated_at",
    "resolved_at",
    "closed_at"
]

print(incident[columns_to_show].to_string(index=False))

print("\n========== STATES ==========")
print(incident["incident_state"].value_counts())

print("\n========== FIRST RECORD ==========")
print(incident.iloc[0].to_string())

print("\n========== LAST RECORD ==========")
print(incident.iloc[-1].to_string())