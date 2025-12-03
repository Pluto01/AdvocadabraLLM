import faiss
import numpy as np
import joblib
import json
from sentence_transformers import SentenceTransformer

EMB_DIR = "/Users/uditkandi/project 3-1/di_prime_embeddings"
EMB_FILE = f"{EMB_DIR}/embeddings.npy"
META_FILE = f"{EMB_DIR}/metadata.joblib"
FAISS_FILE = f"{EMB_DIR}/faiss.index"

DI_PATH = "/Users/uditkandi/project 3-1/di_dataset2.jsonl"


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

print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def retrieve_similar_cases(query_text, k=10):
    """Return top-k UNIQUE similar cases (no duplicate case_ids)."""

    query_emb = model.encode(query_text, convert_to_numpy=True).astype("float32")
    query_emb = np.expand_dims(query_emb, axis=0)

    # Fetch extra neighbors to ensure we get k unique case_ids
    SEARCH_LIMIT = max(k * 5, 50)

    distances, indices = index.search(query_emb, SEARCH_LIMIT)

    results = []
    seen_ids = set()

    for dist, idx in zip(distances[0], indices[0]):
        cid = metadata[idx]["case_id"]

        # skip duplicates
        if cid in seen_ids:
            continue

        seen_ids.add(cid)

        # get text
        case = cases[idx]
        sample = case.get("summary") or case.get("raw_text", "")[:200]

        results.append({
            "case_id": cid,
            "score": float(dist),
            "text_sample": sample
        })

        if len(results) == k:
            break

    return results


if __name__ == "__main__":
    print("Testing SCR...\n")

    query = """
    Patent infringement involving mechanical coupling design.
    Plaintiff claims defendant copied a patented mechanism.
    """

    results = retrieve_similar_cases(query, k=10)

    print("\nTop 10 UNIQUE similar cases:\n")
    for r in results:
        print(f"Case ID: {r['case_id']} | Score: {r['score']}")
        print(f"Text sample: {r['text_sample']}\n")