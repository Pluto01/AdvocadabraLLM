

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import json
import gc
import re
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
import faiss
from tqdm import tqdm

from sentence_transformers import SentenceTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

DATA_ROOT = "/Users/uditkandi/project 3-1/di_prime_embeddings/data_raw"
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
CONF_THRESHOLD = 0.90
DROP_LABEL = "settlement"

LABEL_PATTERNS = [
    (r"judgment.*for the plaintiff", "plaintiff"),
    (r"judgment.*for the defendant", "defendant"),
    (r"plaintiff cannot recover", "defendant"),
    (r"bill.*dismissed", "dismissal"),
    (r"demurrer.*sustained", "defendant"),
    (r"demurrer.*overruled", "plaintiff"),
    (r"appeal.*denied", "defendant"),
    (r"affirm(ed|s)", "defendant"),
    (r"revers(ed|es)", "plaintiff"),
    (r"settlement|settled", "settlement"),
]

def guess_label(text):
    t = text.lower()
    for pat, lab in LABEL_PATTERNS:
        if re.search(pat, t):
            return lab
    return None

def extract_text(j):
    try:
        ops = j.get("casebody", {}).get("opinions", [])
        parts = []
        for op in ops:
            t = op.get("text", "")
            if isinstance(t, str) and len(t) > 50:
                parts.append(t)
        return "\n".join(parts) if parts else None
    except:
        return None

print("\n[1] Loading DataFrame...")

if os.path.exists("cases_df.pkl"):
    df = pd.read_pickle("cases_df.pkl")
    print("[1] Loaded cached DataFrame.\n")
else:
    print("[1] cases_df.pkl not found → rebuilding from JSON files...")

    records = []
    files = list(Path(DATA_ROOT).rglob("*.json"))

    for p in tqdm(files, desc="Reading JSON files"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                j = json.load(f)

            text = extract_text(j)
            if not text:
                continue

            records.append({
                "text": text,
                "summary_short": text.replace("\n", " ")[:700],
                "summary_long": text.replace("\n", " ")[:3000],
                "verdict": guess_label(text[:3000]),
                "path": str(p)
            })
        except:
            continue

    df = pd.DataFrame(records)
    df.to_pickle("cases_df.pkl")
    print(f"[1] Built DataFrame with {len(df)} cases and saved cases_df.pkl\n")

print("[2] Loading embeddings, FAISS, weak model...")

embeddings = np.load("embeddings.npy")
index = faiss.read_index("faiss_index.bin")

bundle = joblib.load("ljp_model.joblib")
clf_weak = bundle["clf"]
le_weak = bundle["label_enc"]

embed_model = SentenceTransformer(MODEL_NAME)

def build_feature(idx, summary, k=6):
    own = embeddings[idx]

    q = embed_model.encode([summary], convert_to_numpy=True)
    faiss.normalize_L2(q)

    D, I = index.search(q, k)
    nbrs = [i for i in I[0] if i != idx][:3]

    if nbrs:
        neigh = np.mean(embeddings[nbrs], axis=0)
        sim = float(np.mean(D[0][1:len(nbrs)+1]))
    else:
        neigh = np.zeros_like(own)
        sim = 0.0

    return np.concatenate([own, neigh, [sim]])

print("[3] High-confidence self-training...")

unlabeled = df[df["verdict"].isnull()].reset_index()
X_pseudo, y_pseudo = [], []

for _, row in tqdm(unlabeled.iterrows(), total=len(unlabeled)):
    idx = row["index"]
    feat = build_feature(idx, row["summary_short"])

    probs = clf_weak.predict_proba([feat])[0]
    p = np.argmax(probs)
    conf = probs[p]
    label = le_weak.inverse_transform([p])[0]

    if conf >= CONF_THRESHOLD and label != DROP_LABEL:
        X_pseudo.append(feat)
        y_pseudo.append(label)

print(f"[3] Accepted pseudo-labels: {len(y_pseudo)}\n")

orig = df[df["verdict"].notnull()]
orig = orig[orig["verdict"] != DROP_LABEL]

X_orig, y_orig = [], []

for i, row in tqdm(orig.iterrows(), total=len(orig)):
    X_orig.append(build_feature(i, row["summary_short"]))
    y_orig.append(row["verdict"])

X = np.vstack(X_orig + X_pseudo)
y = np.array(y_orig + y_pseudo)

print(f"[4] Final training size: {len(y)}\n")

le = LabelEncoder()
y_enc = le.fit_transform(y)

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y_enc, test_size=0.15, stratify=y_enc, random_state=42
)

clf = MLPClassifier(
    hidden_layer_sizes=(512,256),
    max_iter=30,
    batch_size=256,
    activation="relu",
    learning_rate="adaptive"
)

print("[5] Training final model...")
clf.fit(X_tr, y_tr)

pred = clf.predict(X_te)

print("\nFINAL ACCURACY:", accuracy_score(y_te, pred))
print(classification_report(y_te, pred, target_names=le.classes_))

joblib.dump({"clf": clf, "label_enc": le}, "ljp_model_final.joblib")
print("\n[5] Saved ljp_model_final.joblib")

def explain_case(text, top_k=5):
    text = text.replace("\n"," ")[:700]

    q = embed_model.encode([text], convert_to_numpy=True)
    faiss.normalize_L2(q)

    D, I = index.search(q, top_k + 1)
    nbrs = I[0][1:top_k+1]
    sims = D[0][1:top_k+1]

    own = q[0]
    neigh = np.mean(embeddings[nbrs], axis=0) if len(nbrs) else np.zeros_like(own)
    sim = float(np.mean(sims)) if len(nbrs) else 0.0

    feat = np.concatenate([own, neigh, [sim]])
    probs = clf.predict_proba([feat])[0]
    p = np.argmax(probs)

    feat_no = np.concatenate([own, np.zeros_like(neigh), [0.0]])
    probs_no = clf.predict_proba([feat_no])[0]

    return {
        "prediction": le.inverse_transform([p])[0],
        "probability": float(probs[p]),
        "prob_without_neighbors": float(probs_no[p]),
        "neighbor_influence_delta": float(probs[p] - probs_no[p]),
        "evidence": [
            {
                "similarity": float(s),
                "snippet": df.at[i, "summary_short"][:300],
                "path": df.at[i, "path"]
            } for i, s in zip(nbrs, sims)
        ]
    }

print("\n[TEST] XAI example:\n")
print(json.dumps(
    explain_case("The court holds that the defendant is entitled to judgment as a matter of law."),
    indent=2
))

print("\nDONE")