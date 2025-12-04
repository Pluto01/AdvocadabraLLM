import os
import json
import time
import joblib
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


DI_PATH = "/Users/uditkandi/project 3-1/di_dataset2.jsonl"  
EMBED_DIR = "./di_prime_embeddings"
os.makedirs(EMBED_DIR, exist_ok=True)

EMB_FILE = os.path.join(EMBED_DIR, "embeddings.npy")
META_FILE = os.path.join(EMBED_DIR, "metadata.joblib")
CHECKPOINT_FILE = os.path.join(EMBED_DIR, "checkpoint.json")
MODEL_NAME = "intfloat/e5-base"
BATCH_SIZE = 64  


def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return {"done": 0}
    try:
        return json.load(open(CHECKPOINT_FILE))
    except:
        return {"done": 0}


def save_checkpoint(state):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(state, f)



def make_text(case):
    for field in ["summary", "case_summary", "facts", "raw_text"]:
        if field in case and case[field]:
            return " ".join(case[field].split())[:10000]
    return ""



def build_embeddings():
    print("Loading DI...")
    cases = []
    with open(DI_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                cases.append(json.loads(line))
            except:
                pass

    total = len(cases)
    print(f"Total cases: {total}")

    cp = load_checkpoint()
    start_idx = cp.get("done", 0)
    print(f"[RESUME] Starting from index {start_idx}")

    # Load or init memory arrays
    if os.path.exists(EMB_FILE):
        embeddings = np.load(EMB_FILE)
        print(f"[LOAD] Loaded existing embeddings: {embeddings.shape}")
    else:
        embeddings = np.zeros((total, 768), dtype="float32")

    if os.path.exists(META_FILE):
        metadata = joblib.load(META_FILE)
    else:
        metadata = [{} for _ in range(total)]

    model = SentenceTransformer(MODEL_NAME)

    t0 = time.time()
    processed = start_idx

    for i in tqdm(range(start_idx, total), desc="Embedding DI"):
        case = cases[i]
        text = make_text(case)

        emb = model.encode(text, convert_to_numpy=True)
        embeddings[i] = emb
        metadata[i] = {"case_id": case.get("case_id"), "text_len": len(text)}

        processed += 1

        if processed % 100 == 0:  # checkpoint every 100 cases
            np.save(EMB_FILE, embeddings)
            joblib.dump(metadata, META_FILE)
            save_checkpoint({"done": processed})

            elapsed = time.time() - t0
            rate = processed / elapsed
            eta = (total - processed) / rate if rate > 0 else 99999

            print(f"\n[CHECKPOINT] Saved at {processed}/{total}. ETA {int(eta/60)} min\n")

    # Final save
    np.save(EMB_FILE, embeddings)
    joblib.dump(metadata, META_FILE)
    save_checkpoint({"done": total})

    print("\nDONE.")
    print("Embeddings shape:", embeddings.shape)
    print("Metadata saved:", META_FILE)
    print("Embeddings saved:", EMB_FILE)



if __name__ == "__main__":
    build_embeddings()