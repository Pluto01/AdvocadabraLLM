#!/usr/bin/env python3
"""
AdvocaDabra Backend API Server
Integrates SCR (Similar Case Retrieval) and PCR (Precedent Case Retrieval)
with file upload and real authentication
"""
import os
import json
import jwt
import hashlib
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import fitz  # PyMuPDF for PDF processing

# Import our AI modules
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# We'll import these when needed to avoid startup errors
scr_model = None
def get_scr_functions():
    global scr_model
    try:
        from build_scr import retrieve_similar_cases
        return retrieve_similar_cases
    except Exception as e:
        print(f"Warning: SCR not available: {e}")
        return None

def get_pcr_functions():
    try:
        from build_pcr import recommend_precedents, find_best_precedent
        return recommend_precedents, find_best_precedent
    except Exception as e:
        print(f"Warning: PCR not available: {e}")
        return None, None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

CORS(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'json', 'csv', 'xlsx', 'xls', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database setup
DB_PATH = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def generate_token(user_id: int, email: str) -> str:
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication"""
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        user = verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.user = user
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated

# File processing utilities
def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def process_uploaded_file(file_path: str, file_type: str) -> Dict[str, Any]:
    """Process uploaded file and extract relevant text/data"""
    try:
        if file_type == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                'success': True,
                'text': content,
                'type': 'text'
            }
        
        elif file_type == 'pdf':
            text = extract_text_from_pdf(file_path)
            return {
                'success': True,
                'text': text,
                'type': 'pdf_text'
            }
        
        elif file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {
                'success': True,
                'data': data,
                'type': 'json'
            }
        
        elif file_type in ['csv']:
            df = pd.read_csv(file_path)
            return {
                'success': True,
                'data': df.to_dict('records'),
                'columns': df.columns.tolist(),
                'type': 'csv'
            }
        
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
            return {
                'success': True,
                'data': df.to_dict('records'),
                'columns': df.columns.tolist(),
                'type': 'excel'
            }
        
        else:
            return {
                'success': False,
                'error': f'Unsupported file type: {file_type}'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing file: {str(e)}'
        }

# Authentication Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        # Check if user already exists
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'User already exists'}), 409
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)',
            (email, password_hash, name)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Generate token
        token = generate_token(user_id, email)
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'name': name
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash, name FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not check_password_hash(user[1], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = generate_token(user[0], email)
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user[0],
                'email': email,
                'name': user[2]
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@app.route('/api/auth/verify', methods=['GET'])
@require_auth
def verify():
    return jsonify({
        'success': True,
        'user': {
            'id': request.user['user_id'],
            'email': request.user['email']
        }
    })

# File Upload Routes
@app.route('/api/upload', methods=['POST'])
@require_auth
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Supported: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user_files (user_id, filename, original_name, file_type) VALUES (?, ?, ?, ?)',
            (request.user['user_id'], unique_filename, filename, file_ext)
        )
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Process the file
        processed = process_uploaded_file(file_path, file_ext)
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': unique_filename,
            'original_name': filename,
            'file_type': file_ext,
            'processed': processed
        })
    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/files', methods=['GET'])
@require_auth
def list_files():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, filename, original_name, file_type, upload_time, processed 
            FROM user_files 
            WHERE user_id = ? 
            ORDER BY upload_time DESC
        ''', (request.user['user_id'],))
        
        files = []
        for row in cursor.fetchall():
            files.append({
                'id': row[0],
                'filename': row[1],
                'original_name': row[2],
                'file_type': row[3],
                'upload_time': row[4],
                'processed': bool(row[5])
            })
        
        conn.close()
        return jsonify({'success': True, 'files': files})
    
    except Exception as e:
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

# AI Analysis Routes
@app.route('/api/scr', methods=['POST'])
@require_auth
def similar_case_retrieval():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        k = data.get('k', 10)
        
        if not query:
            return jsonify({'error': 'Query text is required'}), 400
        
        retrieve_similar_cases = get_scr_functions()
        if not retrieve_similar_cases:
            return jsonify({'error': 'SCR service not available'}), 503
        
        results = retrieve_similar_cases(query, k=k)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': f'SCR analysis failed: {str(e)}'}), 500

@app.route('/api/pcr', methods=['POST'])
@require_auth
def precedent_case_retrieval():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        k = data.get('k', 5)
        get_explanation = data.get('explanation', False)
        
        if not query:
            return jsonify({'error': 'Query text is required'}), 400
        
        recommend_precedents, find_best_precedent = get_pcr_functions()
        if not recommend_precedents:
            return jsonify({'error': 'PCR service not available'}), 503
        
        if get_explanation:
            result = find_best_precedent(query, k=k)
            return jsonify({
                'success': True,
                'query': query,
                'best_precedent': result['precedent_case'],
                'explanation': result['explanation']
            })
        else:
            results = recommend_precedents(query, k=k)
            return jsonify({
                'success': True,
                'query': query,
                'results': results,
                'count': len(results)
            })
    
    except Exception as e:
        return jsonify({'error': f'PCR analysis failed: {str(e)}'}), 500

@app.route('/api/analyze-file', methods=['POST'])
@require_auth
def analyze_file():
    """Analyze uploaded file with SCR or PCR"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        analysis_type = data.get('type', 'scr')  # 'scr' or 'pcr'
        k = data.get('k', 10)
        
        if not file_id:
            return jsonify({'error': 'File ID is required'}), 400
        
        # Get file info
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT filename, file_type FROM user_files WHERE id = ? AND user_id = ?',
            (file_id, request.user['user_id'])
        )
        file_info = cursor.fetchone()
        conn.close()
        
        if not file_info:
            return jsonify({'error': 'File not found'}), 404
        
        filename, file_type = file_info
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Process file to extract text
        processed = process_uploaded_file(file_path, file_type)
        if not processed['success']:
            return jsonify({'error': processed['error']}), 400
        
        # Extract text for analysis
        query_text = ""
        if processed['type'] in ['text', 'pdf_text']:
            query_text = processed['text']
        elif processed['type'] in ['json']:
            # Try to extract text from JSON structure
            json_data = processed['data']
            if isinstance(json_data, dict):
                # Look for common text fields
                for field in ['text', 'content', 'description', 'summary', 'raw_text']:
                    if field in json_data:
                        query_text = str(json_data[field])
                        break
                if not query_text:
                    query_text = json.dumps(json_data)[:5000]  # Use first 5000 chars
        elif processed['type'] in ['csv', 'excel']:
            # Convert structured data to text for analysis
            if processed['data']:
                query_text = str(processed['data'][:5])  # First 5 rows as text
        
        if not query_text:
            return jsonify({'error': 'Could not extract analyzable text from file'}), 400
        
        # Limit text length for analysis
        query_text = query_text[:10000]  # First 10k characters
        
        # Perform analysis
        if analysis_type == 'scr':
            retrieve_similar_cases = get_scr_functions()
            if not retrieve_similar_cases:
                return jsonify({'error': 'SCR service not available'}), 503
            results = retrieve_similar_cases(query_text, k=k)
            return jsonify({
                'success': True,
                'analysis_type': 'scr',
                'file_id': file_id,
                'query_preview': query_text[:500] + "..." if len(query_text) > 500 else query_text,
                'results': results,
                'count': len(results)
            })
        elif analysis_type == 'pcr':
            recommend_precedents, _ = get_pcr_functions()
            if not recommend_precedents:
                return jsonify({'error': 'PCR service not available'}), 503
            results = recommend_precedents(query_text, k=k)
            return jsonify({
                'success': True,
                'analysis_type': 'pcr',
                'file_id': file_id,
                'query_preview': query_text[:500] + "..." if len(query_text) > 500 else query_text,
                'results': results,
                'count': len(results)
            })
        else:
            return jsonify({'error': 'Invalid analysis type. Use "scr" or "pcr"'}), 400
    
    except Exception as e:
        return jsonify({'error': f'File analysis failed: {str(e)}'}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    print("Starting AdvocaDabra Backend Server...")
    print("SCR (Similar Case Retrieval) - Ready")
    print("PCR (Precedent Case Retrieval) - Ready")
    print("Authentication System - Ready")
    print("File Upload System - Ready")
    print("\nServer running on http://localhost:8000")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
