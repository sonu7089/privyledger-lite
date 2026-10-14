*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

## What I Built

I built **PrivyLedger Lite**. It is a simple invoice sorter for freelancers.

The problem is small but real. Freelancers get a lot of PDFs at month end. Invoices, Swiggy bills, electricity bills, client payments. All mixed in one folder. And most sorting tools ask you to upload these files to their server. Many people don't want to do that because these files have client names and money details.

So PrivyLedger works fully on your own laptop. You drop your PDFs in, and it pulls out vendor, date, amount, and invoice number. Then it puts each file in a category like Travel, Software, Utilities, or Client Income. In the end you get a clean table and a CSV file you can send to your CA.

Who would pay for this? Freelancers and small CAs who handle 100 to 500 bills a month. I think $5 a month is fair. It can work at that price only because it costs nothing to run.

## Demo

There is no live link because this app runs offline by design. Here is a video where I run it on my laptop:

[Paste your Loom / YouTube link here]

What you will see in the video:
1. I run `py -3.12 demo_cli.py`
2. It reads 6 sample bills and sorts them
3. I open the Streamlit app, upload the same files, and download the CSV

Sample run from my machine:
```
invoice_github.txt -> Software & SaaS | GitHub Inc | 48.0
receipt_swiggy.txt -> Travel & Food | Swiggy Foods | 1249.0
invoice_bescom.txt -> Utilities | BESCOM Electricity | 2310.5
```

## Code

https://github.com/sonu7089/privyledger-lite

It is plain Python. No API keys. The main parts are:

```
privyledger/
  extract.py     # reads PDF and finds fields with regex
  categorize.py  # rules first, then small local model
  report.py      # makes CSV and totals
app.py           # simple Streamlit UI
demo_cli.py      # runs without UI, good for testing
samples/         # 6 sample bills
```

To try it:
```bash
pip install -r requirements.txt
py -3.12 demo_cli.py
py -3.12 -m streamlit run app.py
```

## How I Built It

I kept it very light so it runs on a normal laptop with no GPU.

These are the open-source pieces I used:

- **Open-weight model:** `sentence-transformers/all-MiniLM-L6-v2`. It is small, about 80MB, and runs on CPU. I use it to match a bill to a category. For example, if the bill says "ink cartridges and A4 bundle", the rules miss it, but this model still puts it in Office Supplies.
- **Open-source tools:** `pdfplumber` and `pypdf` to read PDFs, `scikit-learn` for a TF-IDF fallback when there is no internet, `Streamlit` and `pandas` for the UI and CSV.
- **Local only:** First it tries simple keyword rules. They need zero RAM and got 6 out of 6 right in my test. If rules fail, it tries the small local model. If that is not downloaded, it uses TF-IDF. Nothing is sent to any server.

I also left an optional Ollama hook. If you have Ollama running with `qwen2.5:0.5b` or `llama3.2:1b`, it will write a one-line summary. But the app works fine without it. I did not want to force people to install a big model.

## Why Does Open Innovation Matter?

Open is the reason this idea works at all.

First, privacy. People told me they don't want to upload money files to some website. Since my code runs everything locally, I can show them there is no upload code at all. With a closed API, I could not make that promise.

Second, cost. A closed API charges per file, around 3 to 5 cents. If someone sorts 500 files, that is $15 to $25 just in API cost. I want to charge $5 a month. That math only works if running it costs zero. Mine does.

Third, control. Generic tools get Indian bills wrong. Swiggy, BESCOM, Razorpay fees — they often miss these. Since my code is open, I just added those words to a list and it worked. I did not need to wait for any company or pay for fine-tuning.

To be honest, a big closed model would read messy PDFs a bit better. But for this use case, trust and price matter more than that last bit of accuracy. That is where open wins for me.
