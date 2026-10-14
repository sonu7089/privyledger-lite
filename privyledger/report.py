"""CSV + summary helpers (pandas, stdlib only)."""
import pandas as pd

def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    cols = ["filename", "vendor", "date", "amount", "invoice_no", "category", "confidence", "method"]
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
    out.rename(columns={"amount": "total"}, inplace=True)
    return out
