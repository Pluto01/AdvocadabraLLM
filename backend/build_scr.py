import faiss
import numpy as np
import joblib
import json
from sentence_transformers import SentenceTransformer

EMB_DIR = "./di_prime_embeddings"
EMB_FILE = f"{EMB_DIR}/embeddings.npy"
META_FILE = f"{EMB_DIR}/metadata.joblib"
FAISS_FILE = f"{EMB_DIR}/faiss.index"

# Use local mock dataset for development
DI_PATH = f"{EMB_DIR}/mock_dataset.jsonl"

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

print("Loading embedding model (e5-base)...")
model = SentenceTransformer("intfloat/e5-base")   # <-- FIXED


def retrieve_similar_cases(query_text, k=10):
    """Return top-k UNIQUE similar cases (no duplicate case_ids)."""

    # e5 recommends using "query: " prefix
    query_text = "query: " + query_text

    # Encode and normalize
    query_emb = model.encode(query_text, convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_emb.reshape(1, -1))

    # Fetch extra neighbors to ensure we get k unique case_ids
    SEARCH_LIMIT = max(k * 5, 50)

    distances, indices = index.search(query_emb.reshape(1, -1), SEARCH_LIMIT)

    results = []
    seen_ids = set()

    for dist, idx in zip(distances[0], indices[0]):
        cid = metadata[idx]["case_id"]

        # skip duplicates
        if cid in seen_ids:
            continue

        seen_ids.add(cid)

        case = cases[idx]
        sample = case.get("summary") or case.get("raw_text", "")[:20000]

        results.append({
            "case_id": cid,
            "score": float(dist),   # cosine similarity (because of IP index + L2 norm)
            "text_sample": sample
        })

        if len(results) == k:
            break

    return results


if __name__ == "__main__":
    
    print("Enter your query:")
    query = input("> ")

    k = 10
    results = retrieve_similar_cases(query, k=k)

    print(f"\nTop {k} UNIQUE similar cases:\n")
    for r in results:
        print(f"Case ID: {r['case_id']} | Score: {r['score']}")
        print(f"Text sample:\n{r['text_sample']}\n")