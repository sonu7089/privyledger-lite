"""PrivyLedger Lite — Streamlit UI. 100% local, tiny RAM."""
import streamlit as st
from pathlib import Path
import tempfile

from privyledger.extract import extract_text, extract_fields
from privyledger.categorize import categorize, ollama_polish
from privyledger.report import to_dataframe, monthly_summary

st.set_page_config(page_title="PrivyLedger Lite", page_icon="🧾", layout="wide")
st.title("🧾 PrivyLedger Lite — local invoice sorter")
st.caption("Open-weights + rules, runs on your laptop. No data leaves the machine. ~80MB model, CPU-only.")

uploaded = st.file_uploader("Drop invoices/receipts (PDF/TXT)", type=["pdf", "txt"], accept_multiple_files=True)

if uploaded:
    rows = []
    for f in uploaded:
        suffix = Path(f.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(f.read())
            tmp_path = tmp.name
        text = extract_text(tmp_path)
        fields = extract_fields(text)
        cat = categorize(text)
        polish = ollama_polish(text, cat["category"]) if st.checkbox(f"AI summary for {f.name}? (needs local Ollama tiny model)", value=False, key=f.name) else None
        rows.append({
            "filename": f.name,
            "vendor": fields["vendor"],
            "date": fields["date"],
            "amount": fields["amount"],
            "invoice_no": fields["invoice_no"],
            "category": cat["category"],
            "confidence": cat["confidence"],
            "method": cat["method"] + ("+ollama" if polish else ""),
            "summary": polish or "",
            "preview": text[:500],
        })
    df = to_dataframe(rows)
    st.subheader("Sorted")
    st.dataframe(df.drop(columns=[c for c in ["preview"] if c in df.columns]), use_container_width=True)
    st.subheader("Totals by category")
    st.bar_chart(monthly_summary(df).set_index("category"))
    st.download_button("Download CSV", df.to_csv(index=False), "privyledger.csv", "text/csv")
    with st.expander("Why open?"):
        st.markdown("- **Private:** MiniLM + regex run locally, nothing uploaded.\n- **$0 cost:** no per-doc API fee.\n- **Swappable:** change `CATEGORY_DESCRIPTIONS` or plug `qwen2.5:0.5b` via Ollama.\n- **Offline:** TF-IDF fallback works with no internet.")
else:
    st.info("Upload files to try. Or run: `python demo_cli.py` for an offline demo with samples.")
