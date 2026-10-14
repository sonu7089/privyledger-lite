"""Light categorizer: rules -> MiniLM open-weights -> TF-IDF fallback.
Optional Ollama polish if a tiny model server is running (qwen2.5:0.5b / llama3.2:1b).
All local, $0 cost.
"""
from __future__ import annotations
import os
import re

CATEGORIES = [
    "Software & SaaS",
    "Travel & Food",
    "Office Supplies",
    "Client Income",
    "Utilities",
    "Freelance Services",
    "Tax & Fees",
    "Other",
]

CATEGORY_DESCRIPTIONS = {
    "Software & SaaS": "software subscription saas github vercel figma notion cloud hosting domain",
    "Travel & Food": "travel flight hotel uber swiggy zomato restaurant food taxi trip",
    "Office Supplies": "office stationery amazon flipkart printer paper supplies equipment",
    "Client Income": "payment received client invoice paid income project milestone",
    "Utilities": "electricity wifi internet phone rent utility bill broadband mobile",
    "Freelance Services": "freelance design development writing consulting contractor service fee",
    "Tax & Fees": "tax gst income tax ca fee penalty bank charge gateway fee",
    "Other": "miscellaneous general receipt",
}

KEYWORD_RULES: list[tuple[str, list[str]]] = [
    ("Software & SaaS", ["github", "vercel", "figma", "notion", "saas", "subscription", "openai", "domain", "hosting", "adobe"]),
    ("Travel & Food", ["uber", "ola", "swiggy", "zomato", "flight", "hotel", "indigo", "restaurant", "food", "travel"]),
    ("Office Supplies", ["amazon", "flipkart", "stationery", "printer", "office", "supplies"]),
    ("Client Income", ["payment received", "paid to you", "client payment", "project income", "milestone paid"]),
    ("Utilities", ["electricity", "bescom", "airtel", "jio", "wifi", "broadband", "utility", "rent", "phone bill"]),
    ("Tax & Fees", ["gst", "income tax", "tds", "ca fee", "penalty", "bank charge", "razorpay fee", "stripe fee"]),
    ("Freelance Services", ["freelance", "design", "development", "consulting", "contractor", "service charge"]),
]

_model = None

def _rules_match(text: str) -> str | None:
    low = text.lower()
    for cat, kws in KEYWORD_RULES:
        for kw in kws:
            if kw in low:
                return cat
    return None


def _embedding_match(text: str) -> tuple[str, float] | None:
    """Zero-shot via all-MiniLM-L6-v2 (open weights, ~80MB, CPU). Returns None if unavailable."""
    global _model
    try:
        from sentence_transformers import SentenceTransformer, util
    except Exception:
        return None
    try:
        if _model is None:
            # Smallest practical open embedding model. Cached after first download.
            _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        import torch
        texts = [text[:1000]] + [CATEGORY_DESCRIPTIONS[c] for c in CATEGORIES]
        with torch.no_grad():
            embs = _model.encode(texts, convert_to_tensor=True, show_progress_bar=False)
        scores = util.cos_sim(embs[0], embs[1:])[0].tolist()
        best_i = max(range(len(scores)), key=lambda i: scores[i])
        return CATEGORIES[best_i], round(float(scores[best_i]), 3)
    except Exception:
        return None  # offline / no cache -> fallback


def _tfidf_match(text: str) -> tuple[str, float]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    docs = [text] + [CATEGORY_DESCRIPTIONS[c] for c in CATEGORIES]
    vec = TfidfVectorizer().fit_transform(docs)
    sims = cosine_similarity(vec[0], vec[1:])[0]
    best_i = int(sims.argmax())
    if sims[best_i] <= 0.01:
        return "Other", 0.1
    return CATEGORIES[best_i], round(float(sims[best_i]), 3)


def categorize(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {"category": "Other", "confidence": 0.0, "method": "empty"}
    hit = _rules_match(text)
    if hit:
        return {"category": hit, "confidence": 0.95, "method": "rules"}
    emb = _embedding_match(text)
    if emb:
        cat, conf = emb
        # Low similarity -> Other
        if conf < 0.15:
            return {"category": "Other", "confidence": conf, "method": "minilm-open-weights"}
        return {"category": cat, "confidence": conf, "method": "minilm-open-weights"}
    cat, conf = _tfidf_match(text)
    return {"category": cat, "confidence": conf, "method": "tfidf-fallback"}


def ollama_polish(text: str, category: str) -> str | None:
    """Optional one-line summary via local tiny open-weight chat model. None if no server."""
    host = os.getenv("OLLAMA_HOST", "")
    # Only try if host set or localhost likely running; fail fast otherwise
    try:
        import ollama
        client = ollama.Client(host=host or "http://localhost:11434", timeout=8)
        # Prefer smallest models first (low RAM)
        for model in ("qwen2.5:0.5b", "llama3.2:1b", "phi3:mini"):
            try:
                r = client.chat(
                    model=model,
                    messages=[{"role": "user", "content": f"In 10 words, summarize this receipt for category {category}: {text[:600]}"}],
                )
                return r["message"]["content"].strip()
            except Exception:
                continue
        return None
    except Exception:
        return None
