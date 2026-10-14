"""Lightweight text + field extraction. No heavy OCR by default."""
import re
from pathlib import Path

DATE_PATTERNS = [
    r"(\d{4}-\d{2}-\d{2})",
    r"(\d{2}[/-]\d{2}[/-]\d{4})",
    r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})",
]

AMOUNT_PATTERNS = [
    r"(?:Total|Amount|Grand Total|Balance|INR|Rs\.?|₹|\$)\s*[:\-]?\s*([₹$]?\s?[\d,]+\.\d{2})",
    r"([₹$]\s?[\d,]+\.\d{2})",
    r"((?:INR|Rs\.?)\s?[\d,]+\.?\d*)",
]

INVOICE_PATTERNS = [
    r"(?:Invoice\s*(?:No|Number|#|ID)\s*[:\-]?\s*([A-Za-z0-9\-\/]+))",
    r"(?:Receipt\s*(?:No|#)\s*[:\-]?\s*([A-Za-z0-9\-\/]+))",
]


def extract_text(file_path: str | Path) -> str:
    p = Path(file_path)
    suffix = p.suffix.lower()
    if suffix == ".txt":
        return p.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        # Try pdfplumber first (better tables), fall back to pypdf
        try:
            import pdfplumber
            texts = []
            with pdfplumber.open(str(p)) as pdf:
                for page in pdf.pages:
                    texts.append(page.extract_text() or "")
            joined = "\n".join(texts).strip()
            if len(joined) > 10:
                return joined
        except Exception:
            pass
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(p))
            return "\n".join([(pg.extract_text() or "") for pg in reader.pages])
        except Exception as e:
            return f"[PDF parse failed: {e}]"
    # csv, etc: read as text
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def extract_fields(text: str) -> dict:
    text = text or ""
    vendor = ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Vendor = first meaningful line under 60 chars, not containing invoice/total
    for ln in lines[:5]:
        if len(ln) < 3:
            continue
        low = ln.lower()
        if any(k in low for k in ("invoice", "receipt", "total", "gst", "tax")):
            continue
        vendor = ln[:60]
        break
    if not vendor and lines:
        vendor = lines[0][:60]

    date = ""
    for pat in DATE_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            date = m.group(1)
            break

    amount = ""
    # Prefer "Total" line
    for line in text.splitlines():
        if re.search(r"total|amount|balance", line, re.I):
            m = re.search(r"[\d,]+\.\d{2}|[\d,]+", line)
            if m:
                amount = m.group(0)
                break
    if not amount:
        for pat in AMOUNT_PATTERNS:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                amount = re.search(r"[\d,]+\.?\d*", m.group(1))
                amount = amount.group(0) if amount else m.group(1)
                break

    inv_no = ""
    for pat in INVOICE_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            inv_no = m.group(1).strip()
            break

    amount_clean = re.sub(r"[^\d.]", "", amount or "").strip(".")
    try:
        amount_val = float(amount_clean.replace(",", "")) if amount_clean else 0.0
    except ValueError:
        amount_val = 0.0

    return {
        "vendor": vendor or "Unknown",
        "date": date or "Unknown",
        "amount_str": amount or "",
        "amount": amount_val,
        "invoice_no": inv_no or "Unknown",
    }
