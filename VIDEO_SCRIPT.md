# Video Script — PrivyLedger Lite (60-75 sec)

Read this as-is. Keep your screen on terminal + app. No need to show your face.

---

**[0-10s] Start with problem. Show messy folder.**
> "If you are a freelancer, your downloads folder looks like this. Invoices, Swiggy bills, electricity bills. All mixed. And you don't want to upload them to some random website just to sort them."

**[10-25s] Show what you built. Open terminal.**
> "So I built PrivyLedger Lite. It runs fully on your laptop. No upload, no API key. Let me run it."
> *Run: `py -3.12 demo_cli.py`*
> "See, it reads six bills, finds vendor, date, amount, and puts each in a category. And it saves a CSV."

**[25-45s] Open Streamlit UI.**
> *Run: `py -3.12 -m streamlit run app.py`, upload 2-3 files*
> "Same thing in a simple UI. I drop files here, I get a table, totals by category, and I can download the CSV for my CA."

**[45-60s] Why open. Show categorize.py quickly.**
> "Why open source? First, privacy — everything runs here, nothing leaves my laptop. Second, cost — a closed API would charge per file, so a five dollar plan would lose money. Mine costs zero to run. It uses a small open model, MiniLM, about 80 MB, plus simple rules. That's it."
> "Link to code is in the post. Thanks."

---

### Recording tips
- Zoom terminal to 150%
- Keep `samples/` folder open to show inputs
- End screen: freeze 3 sec on `out/privyledger.csv` open in Excel
- Upload to Loom/YouTube unlisted, paste link in Demo section
