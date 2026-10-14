"""Offline CLI demo — no Streamlit, no internet needed."""
from pathlib import Path
from privyledger.extract import extract_text, extract_fields
from privyledger.categorize import categorize
from privyledger.report import to_dataframe, monthly_summary

samples = sorted(Path("samples").glob("*.*"))
rows = []
for p in samples:
    text = extract_text(p)
    f = extract_fields(text)
    c = categorize(text)
    rows.append({"filename": p.name, **f, "category": c["category"], "confidence": c["confidence"], "method": c["method"]})
    print(f"{p.name} -> {c['category']} ({c['method']}, {c['confidence']}) | {f['vendor']} | {f['amount']} | {f['date']}")

df = to_dataframe(rows)
print("\n--- Totals ---")
print(monthly_summary(df).to_string(index=False))
Path("out").mkdir(exist_ok=True)
df.to_csv("out/privyledger.csv", index=False)
print("\nSaved out/privyledger.csv")
