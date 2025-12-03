import os
import json
import re
import unicodedata
from tqdm import tqdm

RAW_ROOT = "/Users/uditkandi/Downloads/data_raw"
OUT_DIR = "/Users/uditkandi/myjava/Sliding window/c/Advocadabra/output"
OUT_FILE = os.path.join(OUT_DIR, "di_dataset.jsonl")



def clean_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_attorney_names(attorney_entries):
    clean_attorneys = []
    for entry in attorney_entries:
        entry = entry.split(", for")[0]
        entry = entry.split(", contra")[0]
        entry = entry.replace("Attorney General", "")
        entry = entry.strip()
        if entry:
            clean_attorneys.append(entry)
    return clean_attorneys

def extract_parties(parties_list):
    plaintiffs, defendants = [], []

    if not parties_list:
        return [], []

    for p in parties_list:
        p_clean = p.replace("v.", "vs").replace("V.", "vs").strip()
        if "vs" in p_clean:
            left, right = p_clean.split("vs", 1)
            plaintiffs.append(left.strip())
            defendants.append(right.strip())
    return plaintiffs, defendants

def extract_opinion_text(casebody):
    opinions = casebody.get("opinions", [])
    texts = [op.get("text", "") for op in opinions]
    return clean_text("\n\n".join(texts))

def extract_judge(casebody):
    judges = casebody.get("judges", [])
    if judges:
        return judges[0]

    for op in casebody.get("opinions", []):
        if op.get("author"):
            return op["author"]

    return ""



def extract_case(data, filename):
    case_id = data.get("id", filename)
    title = data.get("name") or data.get("name_abbreviation", "")

    court = data.get("court", {}).get("name", "")
    jurisdiction = data.get("jurisdiction", {}).get("name", "")
    date = data.get("decision_date", "")

    citations = [c["cite"] for c in data.get("citations", []) if "cite" in c]

    casebody = data.get("casebody", {})

    parties = casebody.get("parties", [])
    plaintiffs, defendants = extract_parties(parties)

    attorneys_raw = casebody.get("attorneys", [])
    attorneys = extract_attorney_names(attorneys_raw)

    judge = extract_judge(casebody)
    headnotes = clean_text(casebody.get("head_matter", ""))

    raw_text = extract_opinion_text(casebody)

    return {
        "case_id": case_id,
        "title": title,
        "court": court,
        "jurisdiction": jurisdiction,
        "date": date,
        "citations": citations,

        "plaintiffs": plaintiffs,
        "defendants": defendants,
        "parties": parties,
        "judge": judge,
        "attorneys": attorneys,

        "headnotes": headnotes,
        "raw_text": raw_text,

        "case_summary": "",
        "verdict": ""
    }


def build_DI_dataset():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk(RAW_ROOT):
            json_files = [f for f in files if f.lower().endswith(".json")]

            if len(json_files) > 0:
                print(f"[DEBUG] Folder: {root} | JSON files found: {len(json_files)}")

            for filename in tqdm(json_files, desc=f"Processing {root}", leave=False):
                path = os.path.join(root, filename)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        data = json.load(f)
                except Exception as e:
                    print("[WARN]", e)
                    continue

                case_entry = extract_case(data, filename)
                out.write(json.dumps(case_entry, ensure_ascii=False) + "\n")

    print(f"[DONE] DI dataset written to {OUT_FILE}")



if __name__ == "__main__":
    print("Starting DI build...")
    build_DI_dataset()