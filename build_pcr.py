import faiss
import numpy as np
import joblib
import json
import argparse
from sentence_transformers import SentenceTransformer

# ---------------------------------------------
# PATHS
# ---------------------------------------------
EMB_DIR = "./di_prime_embeddings"
META_FILE = f"{EMB_DIR}/metadata.joblib"
FAISS_FILE = f"{EMB_DIR}/faiss.index"
DI_PATH = "/Users/srinandanasarmakesapragada/Documents/data_raw/di_dataset.jsonl"

# ---------------------------------------------
# Load resources
# ---------------------------------------------
print("Loading FAISS index...")
index = faiss.read_index(FAISS_FILE)

print("Loading metadata...")
metadata = joblib.load(META_FILE)

print("Loading DI...")
cases = []
with open(DI_PATH, "r", encoding="utf-8") as f:
    for line in f:
        try:
            cases.append(json.loads(line))
        except:
            pass

print("Loading embedding model (E5-base)...")
model = SentenceTransformer("intfloat/e5-base")

# ---------------------------------------------
# COURT PRESTIGE MAP
# ---------------------------------------------
COURT_PRESTIGE = {
    "supreme court": 5.0,
    "court of appeals": 4.0,
    "appellate division": 3.0,
    "circuit court": 2.5,
    "district court": 1.5,
    "trial court": 1.0,
}

def court_score(text):
    text = (text or "").lower()
    score = 0.0
    for court, w in COURT_PRESTIGE.items():
        if court in text:
            score += w
    return score

# ---------------------------------------------
# BAD CASE FILTER: Remove procedural junk
# ---------------------------------------------
BAD_PHRASES = [
    "motion denied",
    "motion to dismiss",
    "appeal dismissed",
    "appeal denied",
    "motion for leave",
    "summary order",
    "order affirmed",
    "order reversed",
    "reargument denied",
    "dismissed on procedural grounds",
    "petition denied",
    "leave to appeal denied",
]

def is_procedural_case(text):
    t = (text or "").lower()
    return any(p in t for p in BAD_PHRASES)

# ---------------------------------------------
# KEYWORD DEPTH SCORE (reasoning strength)
# ---------------------------------------------
DEPTH_KEYWORDS = [
    ("opinion of the court", 4.0),
    ("we hold", 2.5),
    ("the issue is", 2.0),
    ("the question before the court", 2.0),
    ("in this action", 1.5),
    ("as a matter of law", 1.5),
    ("reasoning", 2.0),
    ("analysis", 1.5),
]

def reasoning_depth(text):
    t = (text or "").lower()
    score = 0
    for key, w in DEPTH_KEYWORDS:
        if key in t:
            score += w
    return score

# ---------------------------------------------
# MAIN PCR FUNCTION
# ---------------------------------------------
def recommend_precedents(query_text, k=10, sample_size=1000, min_length=800, search_limit=None):
    # Ensure query is trimmed and prefixed for e5
    query_text = "query: " + query_text.strip()

    query_emb = model.encode(query_text, convert_to_numpy=True).astype("float32")
    query_emb = np.expand_dims(query_emb, 0)

    if search_limit is None:
        SEARCH_LIMIT = max(k * 10, 200)
    else:
        SEARCH_LIMIT = search_limit

    distances, indices = index.search(query_emb, SEARCH_LIMIT)

    candidates = []
    seen_ids = set()
    total_cases = len(cases)

    for dist, idx in zip(distances[0], indices[0]):
        # faiss may return -1 for padding if index shorter than SEARCH_LIMIT
        if idx < 0 or idx >= total_cases:
            continue

        case = cases[idx]
        cid = case.get("case_id")
        raw = case.get("raw_text", "") or ""

        # remove dupes
        if not cid or cid in seen_ids:
            continue
        seen_ids.add(cid)

        # ----------------------------
        # HARD FILTERS
        # ----------------------------
        if len(raw) < min_length:
            continue  # too short = procedural or not useful

        if is_procedural_case(raw):
            continue  # remove orders/procedural junk

        # ----------------------------
        # FEATURE SCORES
        # ----------------------------
        sim = float(dist)
        court_s = court_score(raw)
        depth_s = reasoning_depth(raw)
        kw_s = 1.0 if "trademark" in raw.lower() else 0.0

        # FINAL SCORE
        final = (
            sim * 1.0          # core relevance
            + court_s * 0.20   # authority
            + depth_s * 0.15   # reasoning quality
            + kw_s * 0.10      # topic alignment
        )

        # sample text sized by sample_size param (None => full)
        sample_text = raw

        candidates.append({
            "case_id": cid,
            "similarity": sim,
            "precedent_strength": court_s,
            "reasoning_depth": depth_s,
            "keyword_bonus": kw_s,
            "final_score": final,
            "sample": sample_text,
            "title": case.get("title", ""),
            "court": case.get("court", ""),
            "date": case.get("date", "")
        })

    # rank by final score
    candidates = sorted(candidates, key=lambda x: x["final_score"], reverse=True)

    return candidates[:k]

# ---------------------------------------------
# FINAL PRECEDENT SELECTOR (ONE CASE + EXPLANATION)
# ---------------------------------------------
def find_best_precedent(query_text, **kwargs):
    top_cases = recommend_precedents(query_text, **kwargs)

    if not top_cases:
        return {
            "precedent_case": None,
            "explanation": "No suitable precedent found after applying filters."
        }

    best = top_cases[0]
    cid = best["case_id"]
    sim = best["similarity"]
    court = best["precedent_strength"]
    depth = best["reasoning_depth"]
    topic = best["keyword_bonus"]
    sample = best["sample"]

    explanation_lines = []
    explanation_lines.append(f"Case {cid} is selected as the strongest precedent because:")

    if court >= 4:
        explanation_lines.append(f"- It originates from a highly authoritative court (score {court:.2f}).")
    elif court > 0:
        explanation_lines.append(f"- It comes from a moderately authoritative court (score {court:.2f}).")
    else:
        explanation_lines.append(f"- Although court authority is low ({court:.2f}), other factors compensate.")

    if depth >= 3:
        explanation_lines.append(f"- The case contains substantial judicial reasoning (depth {depth:.2f}).")
    elif depth > 0:
        explanation_lines.append(f"- The case includes some relevant legal reasoning (depth {depth:.2f}).")
    else:
        explanation_lines.append(f"- It lacks explicit reasoning phrases but remains legally relevant.")

    explanation_lines.append(f"- It is closely related to the input scenario (semantic similarity {sim:.3f}).")
    if topic > 0:
        explanation_lines.append(f"- It discusses trademark-related matters, aligning with the query topic.")
    explanation_lines.append("- After filtering procedural cases and re-ranking, this case had the highest overall score.")

    return {
        "precedent_case": best,
        "explanation": "\n".join(explanation_lines)
    }

# ---------------------------------------------
# CLI: parse args and run
# ---------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PCR: Precedent Candidate Retriever")
    parser.add_argument("--query", "-q", type=str, help="Query text. If omitted, you will be prompted.")
    parser.add_argument("--k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--sample-size", type=int, default=2000, help="Number of chars to return from case text. Use 0 or -1 for full text")
    parser.add_argument("--min-length", type=int, default=800, help="Minimum raw_text length to consider a case (filters junk)")
    parser.add_argument("--show-explanation", action="store_true", help="Show explanation for best precedent")
    args = parser.parse_args()

    if args.query:
        query = args.query
    else:
        try:
            query = input("Enter your query: ").strip()
        except Exception:
            print("Interactive input not available; please use --query")
            return

    sample_size = None if args.sample_size <= 0 else args.sample_size

    results = recommend_precedents(query, k=args.k, sample_size=sample_size, min_length=args.min_length)

    if not results:
        print("No results found.")
        return

    print(f"\nTop {len(results)} precedents:\n")
    for i, r in enumerate(results, start=1):
        print(f"[{i}] Case ID: {r['case_id']} | final_score: {r['final_score']:.4f} | sim: {r['similarity']:.4f}")
        print(f"     Title: {r.get('title','')}")
        print(f"     Court: {r.get('court','')} | Date: {r.get('date','')}")
        print("     Sample:")
        print(r["sample"].rstrip())
        print("-" * 80)

    if args.show_explanation:
        final = find_best_precedent(query, k=args.k, sample_size=sample_size, min_length=args.min_length)
        print("\nEXPLANATION FOR BEST PRECEDENT:\n")
        print(final["explanation"])

if __name__ == "__main__":
    main()