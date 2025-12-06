#!/usr/bin/env python3
"""
Development Setup Script for AdvocaDabra SCR/PCR Systems
Creates mock data files for development when real dataset is not available
"""
import os
import json
import faiss
import numpy as np
import joblib
from datetime import datetime

EMB_DIR = "./di_prime_embeddings"
EMB_FILE = f"{EMB_DIR}/embeddings.npy"
META_FILE = f"{EMB_DIR}/metadata.joblib"
FAISS_FILE = f"{EMB_DIR}/faiss.index"
MOCK_DATASET = f"{EMB_DIR}/mock_dataset.jsonl"

def create_mock_data():
    """Create mock legal case data for development"""
    print("🔧 Creating mock legal case data for development...")
    
    # Ensure directory exists
    os.makedirs(EMB_DIR, exist_ok=True)
    
    # Sample legal cases for development
    mock_cases = [
        {
            "id": "case_001",
            "title": "Contract Breach in Commercial Real Estate",
            "summary": "Plaintiff sued for breach of commercial lease agreement involving failure to maintain property standards.",
            "court": "Superior Court",
            "year": 2023,
            "outcome": "Plaintiff awarded damages",
            "legal_area": "Contract Law"
        },
        {
            "id": "case_002", 
            "title": "Employment Discrimination Case",
            "summary": "Employee filed discrimination lawsuit alleging wrongful termination based on age discrimination.",
            "court": "Federal District Court",
            "year": 2022,
            "outcome": "Settlement reached",
            "legal_area": "Employment Law"
        },
        {
            "id": "case_003",
            "title": "Intellectual Property Infringement",
            "summary": "Patent holder sued competitor for unauthorized use of patented technology in manufacturing process.",
            "court": "Court of Appeals",
            "year": 2023,
            "outcome": "Injunction granted",
            "legal_area": "Intellectual Property"
        },
        {
            "id": "case_004",
            "title": "Personal Injury - Medical Malpractice",
            "summary": "Patient sued hospital for negligence during surgical procedure resulting in permanent injury.",
            "court": "State Supreme Court",
            "year": 2021,
            "outcome": "Jury verdict for plaintiff",
            "legal_area": "Medical Malpractice"
        },
        {
            "id": "case_005",
            "title": "Corporate Merger Dispute",
            "summary": "Shareholders challenged merger terms alleging inadequate consideration and breach of fiduciary duty.",
            "court": "Delaware Chancery Court",
            "year": 2023,
            "outcome": "Merger blocked pending review",
            "legal_area": "Corporate Law"
        }
    ]
    
    # Create mock dataset file
    with open(MOCK_DATASET, 'w') as f:
        for case in mock_cases:
            f.write(json.dumps(case) + '\n')
    
    print(f"✅ Created mock dataset with {len(mock_cases)} cases")
    return mock_cases

def create_mock_embeddings(cases):
    """Create mock embeddings for the cases"""
    print("🔧 Creating mock embeddings...")
    
    # Create random embeddings (768 dimensions for sentence transformers)
    n_cases = len(cases)
    embedding_dim = 768
    
    # Generate random but consistent embeddings
    np.random.seed(42)  # For reproducible results
    embeddings = np.random.randn(n_cases, embedding_dim).astype(np.float32)
    
    # Normalize embeddings
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms
    
    # Save embeddings
    np.save(EMB_FILE, embeddings)
    print(f"✅ Created embeddings file: {EMB_FILE}")
    
    return embeddings

def create_mock_metadata(cases):
    """Create metadata for the cases"""
    print("🔧 Creating mock metadata...")
    
    metadata = []
    for i, case in enumerate(cases):
        metadata.append({
            'index': i,
            'case_id': case['id'],
            'title': case['title'],
            'summary': case['summary'],
            'court': case['court'],
            'year': case['year'],
            'outcome': case['outcome'],
            'legal_area': case['legal_area']
        })
    
    # Save metadata
    joblib.dump(metadata, META_FILE)
    print(f"✅ Created metadata file: {META_FILE}")
    
    return metadata

def create_faiss_index(embeddings):
    """Create FAISS index from embeddings"""
    print("🔧 Creating FAISS index...")
    
    # Create index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner product similarity
    
    # Add embeddings to index
    index.add(embeddings)
    
    # Save index
    faiss.write_index(index, FAISS_FILE)
    print(f"✅ Created FAISS index: {FAISS_FILE}")
    
    return index

def setup_development_environment():
    """Set up complete development environment"""
    print("🚀 Setting up AdvocaDabra Development Environment")
    print("=" * 50)
    
    # Check if files already exist
    if (os.path.exists(EMB_FILE) and 
        os.path.exists(META_FILE) and 
        os.path.exists(FAISS_FILE)):
        print("✅ Development files already exist!")
        print("   Use --force to recreate them")
        return
    
    # Create mock data
    cases = create_mock_data()
    embeddings = create_mock_embeddings(cases)
    metadata = create_mock_metadata(cases)
    index = create_faiss_index(embeddings)
    
    print("\n🎉 Development environment setup complete!")
    print("=" * 50)
    print(f"📁 Files created in: {EMB_DIR}/")
    print(f"   - {len(cases)} mock legal cases")
    print(f"   - {embeddings.shape[0]} embeddings ({embeddings.shape[1]} dimensions)")
    print(f"   - FAISS index with {index.ntotal} vectors")
    print("\n🚀 You can now start the backend server!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Setup AdvocaDabra development environment")
    parser.add_argument("--force", action="store_true", help="Force recreate files even if they exist")
    args = parser.parse_args()
    
    if args.force:
        # Remove existing files
        for file in [EMB_FILE, META_FILE, FAISS_FILE, MOCK_DATASET]:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  Removed existing file: {file}")
    
    setup_development_environment()
