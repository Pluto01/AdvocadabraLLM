# AdvocaDabra Legal AI System

A comprehensive legal AI assistant that combines Similar Case Retrieval (SCR) and Precedent Case Retrieval (PCR) with a modern React frontend and real authentication system.

## Features

- **Similar Case Retrieval (SCR)**: Find cases similar to your query using AI-powered semantic search
- **Precedent Case Retrieval (PCR)**: Discover relevant legal precedents with authority scoring
- **File Upload Support**: Upload and analyze PDF, TXT, JSON, CSV, Excel, and Word documents
- **Real Authentication**: JWT-based authentication with SQLite database
- **Modern UI**: Clean, responsive React interface with Tailwind CSS
- **Fast Search**: FAISS-powered vector search through 103,980+ legal cases
- **Analysis Dashboard**: Integrated interface for text and file analysis

## Architecture

### Backend (`/backend`)
- **Flask API Server**: JWT authentication, file handling, AI analysis
- **SCR/PCR Modules**: Similar Case Retrieval and Precedent Case Retrieval
- **Vector Embeddings**: FAISS-indexed legal case embeddings
- **Data Storage**: SQLite database and file upload system

### Frontend (`/frontend/legal-ai-client`)
- **React + Vite**: Modern web application with TypeScript support
- **Dashboard**: Integrated SCR/PCR analysis with drag-drop file upload
- **Authentication**: JWT-based login/signup with persistent sessions
- **Responsive UI**: Tailwind CSS with mobile-friendly design

### Data & External Dependencies
- **103,980 Legal Cases** from the DI dataset (stored in `~/Documents/data_raw/`)
- **58,200+ Embeddings** generated (ongoing process)
- **FAISS Index** for fast similarity search
- **Node Modules** managed automatically by npm (no duplicate installations)

## Project Structure

```
AdvocadabraLLM/
├── README.md                 # Main project documentation
├── start_system.sh          # One-command system startup
├── test_system.py           # Comprehensive system tests
├── cleanup.py               # Project maintenance script
├── backend/                 # Flask API Server
│   ├── backend_server.py    # Main API server
│   ├── build_scr.py        # Similar Case Retrieval
│   ├── build_pcr.py        # Precedent Case Retrieval
│   ├── Embeddings.py       # Vector embedding generation
│   ├── requirements.txt    # Python dependencies
│   ├── users.db           # SQLite authentication database
│   ├── di_prime_embeddings/   # Vector embeddings storage
│   └── uploads/           # User uploaded files
└── frontend/              # React Web Application  
    └── legal-ai-client/   # Main frontend application
        ├── package.json   # Node.js dependencies
        ├── vite.config.js # Build configuration
        ├── src/          # React source code
        │   ├── routes/   # Page components
        │   ├── components/ # Reusable UI components
        │   ├── hooks/    # React custom hooks
        │   └── lib/      # API client library
        └── public/       # Static assets
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- 8GB+ RAM (for embeddings)

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Generate required data files for SCR/PCR services
python3 setup_dev_environment.py

# Start backend server
python backend_server.py
```
Backend runs on: http://localhost:8000

### 2. Frontend Setup
```bash
cd frontend/legal-ai-client
npm install
npm run dev
```
Frontend runs on: http://localhost:5173

### 3. Test Login
- Email: `test@example.com`
- Password: `test123`

### 3. Access the Application
Open http://localhost:5173 and create an account to start using the legal AI system.

## Usage

### Text Analysis
1. Navigate to SCR or PCR tab
2. Enter your legal query in the text area
3. Click "Run Analysis" to get similar cases or precedents

### File Analysis
1. Upload legal documents via drag-drop or file browser
2. Select an uploaded file from your file list
3. Click "Analyze File" to process the document content

### Supported File Types
- **PDF**: Legal documents, case files
- **TXT**: Plain text legal content
- **JSON**: Structured legal data
- **CSV**: Case databases, legal datasets
- **Excel**: Legal spreadsheets, case lists
- **Word**: Legal documents, briefs

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

## Testing

Run the comprehensive test suite:
```bash
python3 test_system.py
```

Tests include:
- API Health Check
- Authentication (Signup/Login)
- SCR Text Analysis
- PCR Text Analysis
- File Upload
- File Analysis

## System Status

- **Backend**: Running (Port 8000)
- **Frontend**: Running (Port 5173)
- **Database**: SQLite initialized
- **AI Models**: SCR & PCR operational
- **Embeddings**: 58,200/103,980 (56% complete)
- **File Storage**: Upload system active

## Configuration

### Environment Variables
```bash
FLASK_SECRET_KEY=your-secret-key-change-in-production
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=50MB
```

### Data Paths
- **Legal Cases**: `~/Documents/data_raw/di_dataset.jsonl` (external data source)
- **Embeddings**: `backend/di_prime_embeddings/` (vector storage)
- **Uploads**: `backend/uploads/` (user files)
- **Database**: `backend/users.db` (authentication)

## Production Ready Features

- **Real Authentication**: JWT tokens with secure password hashing
- **File Processing**: Multi-format support with error handling
- **Error Management**: Graceful fallbacks and user feedback
- **Progress Tracking**: Upload progress and analysis status
- **Responsive Design**: Mobile-friendly interface
- **Security**: CORS enabled, input validation
- **Performance**: FAISS indexing for fast search

## Future Enhancements

- **LJP Integration**: Legal Judgment Prediction
- **Advanced Analytics**: Case outcome prediction
- **Document Generation**: AI-powered legal document creation
- **Collaborative Features**: Team workspaces
- **Export Options**: PDF reports, case summaries

## License

This project is for educational and research purposes in legal AI technology.

---

## Quick Reference

| Component | Command | URL |
|-----------|---------|-----|
| **Full System** | `./start_system.sh` | Frontend: http://localhost:5173 |
| **Backend Only** | `cd backend && python backend_server.py` | API: http://localhost:8000 |
| **Frontend Only** | `cd frontend/legal-ai-client && npm run dev` | App: http://localhost:5173 |
| **Run Tests** | `python3 test_system.py` | All endpoints tested |
| **Clean Project** | `python3 cleanup.py` | Maintenance & stats |

## Development Workflow

1. **Start Development**: `./start_system.sh`
2. **Make Changes**: Edit files in `backend/` or `frontend/legal-ai-client/`
3. **Test Changes**: `python3 test_system.py`
4. **Clean Up**: `python3 cleanup.py`

---

** AdvocaDabra Legal AI System - Professional Architecture Ready for Production!**

*See `REORGANIZATION_SUMMARY.md` for complete details on the new project structure.*