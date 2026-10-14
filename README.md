# 🧾 PrivyLedger Lite — local invoice sorter for freelancers

Side Hustle for Hacktoberfest Week 2. 100% local, tiny RAM, $0 to run.

## Why this?
Freelancers won't upload client invoices to a closed SaaS. PrivyLedger sorts PDFs/TXTs on their laptop: vendor, date, amount, category, CSV + totals.

## Open core (what makes it work)
- **Open weights:** `sentence-transformers/all-MiniLM-L6-v2` (~80MB, CPU) for zero-shot categorization. No API key.
- **Open harness:** pdfplumber/pypdf + scikit-learn + Streamlit + optional `ollama` client for tiny models (`qwen2.5:0.5b`, `llama3.2:1b`).
- **Local inference:** 3-tier — 1) keyword rules (0 RAM) → 2) MiniLM → 3) TF-IDF fallback (offline, no download).

Verified: 6/6 samples correct via rules, ambiguous case (`Ink cartridges...`) correctly → `Office Supplies` via `minilm-open-weights`.

## Why open beats closed here
1. **Privacy:** client financials never leave laptop — dealbreaker for CAs/freelancers.
2. **Cost:** closed OCR+LLM ≈ $0.03–0.05/doc. At 500 docs/mo that kills a $5/mo side hustle. Ours = $0.
3. **Offline + swappable:** works in a CA's office with bad wifi; edit `CATEGORY_DESCRIPTIONS` or swap model, no vendor lock.

## Run (light)
```bash
# CLI demo, no server needed — use Python 3.12 that has deps
py -3.12 demo_cli.py
# out/privyledger.csv created

# UI
py -3.12 -m streamlit run app.py
```

Optional: set `OLLAMA_HOST=http://localhost:11434` + `ollama pull qwen2.5:0.5b` for one-line AI summaries. App works without it.

## Side hustle plan
Target: 1 freelancer/CA. Price: $5/mo or ₹199/mo for CSV + monthly totals. First user ask: "Would you pay to never upload invoices again?"
