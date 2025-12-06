# Legal AI Backend Server

Flask-based API server for the AdvocaDabra Legal AI System.

## Features
- JWT Authentication with SQLite database
- File upload and processing (PDF, TXT, JSON, CSV, Excel, Word)
- Similar Case Retrieval (SCR) using FAISS vector search
- Precedent Case Retrieval (PCR) with authority scoring
- RESTful API endpoints

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python backend_server.py
```

Server runs on: http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - User login  
- `GET /api/auth/verify` - Verify JWT token

### File Operations
- `POST /api/upload` - Upload legal documents
- `GET /api/files` - List user files
- `POST /api/analyze-file` - Analyze uploaded file

### AI Analysis
- `POST /api/scr` - Similar Case Retrieval
- `POST /api/pcr` - Precedent Case Retrieval
- `GET /api/health` - System health check

## Data Files
- `di_prime_embeddings/` - Vector embeddings for 103,980+ legal cases
- `uploads/` - User uploaded files
- `users.db` - SQLite authentication database
