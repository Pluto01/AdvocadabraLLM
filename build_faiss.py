import os
import faiss
import numpy as np
import joblib

EMB_DIR = "./di_prime_embeddings"
EMB_FILE = os.path.join(EMB_DIR,"embeddings.npy")
META_FILE = os.path.join(EMB_DIR,"metadata.joblib")

INDEX_FILE = os.path.join(EMB_DIR,"faiss.index")

def build_faiss_index():
    print("Loading embeddings...")
    embeddings = np.load(EMB_FILE).astype("float32")
    total, dim = embeddings.shape
    print(f"Embeddings loaded: {embeddings.shape}")

    faiss.normalize_L2(embeddings)

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)
    print(f"Index built with {index.ntotal} vectors")

    print(f"Saving index to: {INDEX_FILE}")
    faiss.write_index(index, INDEX_FILE)

    print("FAISS index saved successfully.")

if __name__=="__main__":
    build_faiss_index()
