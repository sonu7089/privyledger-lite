# I built a side hustle that sorts invoices without the cloud — here's why open won

**TL;DR:** PrivyLedger Lite sorts freelancer invoices locally. Open weights + rules, ~80MB, CPU-only, $0/doc. A closed API would have killed the business on cost and trust.

## The problem (real person)
My friend freelances and dreads month-end: 200 PDFs in Downloads, client names + amounts she refuses to upload to random AI tools. She'd pay for a sorter that *doesn't* send data anywhere.

## What I built
Drop PDFs/TXTs → vendor/date/amount auto-extracted → category → CSV + totals bar chart.
Stack, all open:
- `pdfplumber` / `pypdf` for extraction
- `sentence-transformers/all-MiniLM-L6-v2` (open weights) for zero-shot categorization
- `scikit-learn` TF-IDF fallback when offline
- Streamlit UI, optional `qwen2.5:0.5b` / `llama3.2:1b` via Ollama for summaries

No internet after first model cache. Tested 6/6 correct; ambiguous receipt fell through to MiniLM and still got it right.

## Why open innovation matters here
1. **Privacy kept data local:** Invoices stay on her laptop. With a closed API I'd have to say "trust my server" — instant no.
2. **Cost made the hustle viable:** Closed would be ~$15/mo in API fees for 500 docs. I charge $5/mo. Only $0 marginal cost works.
3. **Swappable + tunable:** She does Indian GST + Swiggy/Uber receipts a generic tool mislabels. I just edited keyword lists + category descriptions — no waiting on a vendor.
4. **Runs on crap hardware:** Rules first (0 RAM), MiniLM only when needed. Works on her 4GB old laptop.

Closed would be more accurate on weird PDFs, honestly. But she'd never use it. Open won on trust + economics, not benchmarks.

## First user?
Sent her `demo_cli.py` + 6 samples. She ran it, asked: "can it flag unpaid client invoices next?" That's v2 — and yes, she'd pay ₹199/mo if it does GST totals.

Repo: local-first, MIT. Try `py -3.12 demo_cli.py`.

#hacktoberfest #openweight #sidehustle #localai
