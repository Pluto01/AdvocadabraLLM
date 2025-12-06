import os
import json
import time
import joblib
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


DI_PATH = "/Users/srinandanasarmakesapragada/Documents/data_raw/di_dataset.jsonl"  
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

    # initialize model early so we know embedding dim
    model = SentenceTransformer(MODEL_NAME)
    embedding_dim = model.get_sentence_embedding_dimension()

    # Load or init embeddings safely
    if os.path.exists(EMB_FILE):
        loaded = np.load(EMB_FILE)
        print(f"[LOAD] Loaded existing embeddings: {loaded.shape}")

        # ensure 2D shape and copy data
        if loaded.size == 0 or loaded.shape[0] == 0:
            # file exists but empty -> create full array
            embeddings = np.zeros((total, embedding_dim), dtype="float32")
            actual_embedded = 0
        else:
            # loaded has some rows; handle possible mismatch in dim/rows
            if loaded.ndim == 1:
                loaded = loaded.reshape(-1, embedding_dim)
            if loaded.shape[1] != embedding_dim:
                raise ValueError(f"Loaded embeddings dim {loaded.shape[1]} != model dim {embedding_dim}")
            
            # Count actual non-zero embeddings
            non_zero_mask = np.sum(np.abs(loaded), axis=1) > 0
            actual_embedded = np.sum(non_zero_mask)
            
            # Always create new array and copy existing data
            embeddings = np.zeros((total, embedding_dim), dtype="float32")
            if loaded.shape[0] > 0:
                copy_rows = min(loaded.shape[0], total)
                embeddings[:copy_rows] = loaded[:copy_rows]
    else:
        embeddings = np.zeros((total, embedding_dim), dtype="float32")
        actual_embedded = 0

    # Use checkpoint start_idx, but validate against actual embeddings
    print(f"[INFO] Checkpoint start index: {start_idx}")
    print(f"[INFO] Actual embedded cases: {actual_embedded}")
    
    # If checkpoint is ahead of actual embeddings, use actual count
    if start_idx > actual_embedded:
        print(f"[WARNING] Checkpoint ({start_idx}) > actual embeddings ({actual_embedded}). Using actual count.")
        start_idx = actual_embedded
    
    print(f"[INFO] Starting embedding from index {start_idx}")

    # metadata handling
    if os.path.exists(META_FILE):
        metadata = joblib.load(META_FILE)
        # ensure metadata length == total
        if len(metadata) < total:
            metadata.extend([{} for _ in range(total - len(metadata))])
    else:
        metadata = [{} for _ in range(total)]

    t0 = time.time()
    processed = start_idx

    for i in tqdm(range(start_idx, total), desc="Embedding DI"):
        case = cases[i]
        text = make_text(case)

        emb = model.encode(text, convert_to_numpy=True)
        if emb.shape[0] != embedding_dim:
            raise ValueError(f"embedding dim mismatch at index {i}: got {emb.shape[0]} expected {embedding_dim}")

        embeddings[i] = emb
        metadata[i] = {"case_id": case.get("case_id"), "text_len": len(text)}

        processed += 1

        if processed % 100 == 0:  # checkpoint every 100 cases
            np.save(EMB_FILE, embeddings)
            joblib.dump(metadata, META_FILE)
            save_checkpoint({"done": processed})

            elapsed = time.time() - t0
            rate = processed / elapsed if elapsed > 0 else 0
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