import React, { useState, useEffect, useCallback } from "react";
import { useAuth } from "../hooks/useAuth.jsx";
import { fileAPI, aiAPI } from "../lib/api.js";

// File upload is now integrated into IntegratedAnalysis component

// Integrated Analysis Component with File Upload
function IntegratedAnalysis({ analysisType, files, onFileUploaded, selectedFile, setSelectedFile }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [expandedCases, setExpandedCases] = useState(new Set());

  // File Upload Handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      uploadFiles(e.dataTransfer.files);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      uploadFiles(e.target.files);
    }
  };

  const uploadFiles = async (fileList) => {
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      setUploading(true);
      setUploadProgress(0);

      try {        const response = await fileAPI.upload(file, (progressEvent) => {
          const progress = (progressEvent.loaded / progressEvent.total) * 100;
          setUploadProgress(progress);
        });
        
        if (response.success) {
          setUploadSuccess(`✓ ${file.name} uploaded successfully!`);
          setTimeout(() => setUploadSuccess(''), 3000);
        }
        if (onFileUploaded) onFileUploaded();
      } catch (error) {
        setError(`Upload failed for ${file.name}: ${error.response?.data?.error || error.message}`);
        setTimeout(() => setError(''), 5000);
      }
    }
    setUploading(false);
    setUploadProgress(0);
  };

  // Analysis Handlers
  const handleTextAnalysis = async () => {
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      let response;
      if (analysisType === 'scr') {
        response = await aiAPI.scr(query, 10);
      } else if (analysisType === 'pcr') {
        response = await aiAPI.pcr(query, 5, false);
      }
      
      setResults(response);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFileAnalysis = async () => {
    if (!selectedFile) {
      setError('Please select a file to analyze');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fileAPI.analyze(selectedFile.id, analysisType, 10);
      setResults(response);
    } catch (err) {
      setError(err.response?.data?.error || 'File analysis failed');
    } finally {
      setLoading(false);
    }
  };
  const toggleCaseExpansion = (index) => {
    setExpandedCases(prev => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  const analysisTypeInfo = {
    scr: {
      title: 'Similar Case Retrieval',
      description: 'Find cases similar to your query using AI-powered semantic search',
      color: 'blue',
      placeholder: 'Describe your case or legal issue here...'
    },
    pcr: {
      title: 'Precedent Case Retrieval',
      description: 'Discover relevant legal precedents with authority scoring and reasoning analysis',
      color: 'purple',
      placeholder: 'Enter your legal query or precedent search criteria...'
    }
  };

  const info = analysisTypeInfo[analysisType];
  return (
    <div className="max-w-4xl mx-auto space-y-12">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 mb-4">
          {info.title}
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          {info.description}
        </p>
      </div>

      {/* Notifications */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-2xl">
          {error}
        </div>
      )}

      {uploadSuccess && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-6 py-4 rounded-2xl">
          {uploadSuccess}
        </div>
      )}

      {/* Analysis Input */}
      <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8">        <div className="space-y-6">
          {/* Text Input with File Upload */}
          <div className="relative">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={info.placeholder}
              className="w-full h-32 px-6 py-4 pr-16 border border-gray-200 rounded-2xl bg-gray-50 text-gray-900 focus:bg-white focus:border-gray-400 focus:outline-none resize-none text-lg placeholder:text-gray-500"
              disabled={loading}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            />
            
            {/* File Upload Button (Paperclip) */}
            <div className="absolute bottom-4 right-4">
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                accept=".pdf,.txt,.json,.csv,.xlsx,.xls,.docx"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                disabled={uploading}
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className={`flex items-center justify-center w-10 h-10 rounded-full transition-colors cursor-pointer ${
                  dragActive ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                }`}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66L9.64 16.2a2 2 0 0 1-2.83-2.83l8.49-8.49"/>
                </svg>
              </label>
            </div>
          </div>

          {/* Upload Progress */}
          {uploading && (
            <div className="bg-blue-50 rounded-2xl p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-blue-800 font-medium">Uploading files...</span>
                <span className="text-blue-600 text-sm">{Math.round(uploadProgress)}%</span>
              </div>
              <div className="w-full bg-blue-100 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          )}

          {/* Selected Files */}
          {files.length > 0 && (
            <div className="bg-gray-50 rounded-2xl p-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-3">Uploaded Files</h4>
              <div className="space-y-2 max-h-24 overflow-y-auto">
                {files.slice(0, 3).map((file) => (
                  <div
                    key={file.id}
                    className={`flex items-center justify-between p-2 rounded-xl cursor-pointer transition ${
                      selectedFile?.id === file.id
                        ? 'bg-blue-100 border border-blue-200'
                        : 'bg-white hover:bg-gray-100'
                    }`}
                    onClick={() => setSelectedFile(file)}
                  >
                    <span className="text-sm truncate text-gray-800">{file.original_name}</span>
                    {selectedFile?.id === file.id && (
                      <svg className="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                ))}
                {files.length > 3 && (
                  <div className="text-xs text-gray-500 text-center py-1">
                    +{files.length - 3} more files
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Analyze Button */}
          <button
            onClick={selectedFile ? handleFileAnalysis : handleTextAnalysis}
            disabled={loading || (!query.trim() && !selectedFile)}
            className="w-full bg-black text-white py-4 px-8 rounded-2xl font-semibold text-lg hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            ) : selectedFile ? (
              `Analyze "${selectedFile.original_name}"`
            ) : (
              `Run ${analysisType.toUpperCase()} Analysis`
            )}
          </button>
        </div>
      </div>      {/* Results */}
      {results && (
        <div className="mt-12">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-semibold text-gray-900 mb-2">Analysis Results</h2>
            <p className="text-gray-600">Found {results.results?.length || 0} relevant cases</p>
          </div>
          
          <div className="space-y-6">
            {results.results?.map((result, index) => {
              const isExpanded = expandedCases.has(index);
              return (
                <div 
                  key={index} 
                  className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden transition-all duration-300 hover:shadow-xl"
                >
                  {/* Case Header - Always Visible */}
                  <div 
                    className="p-6 cursor-pointer"
                    onClick={() => toggleCaseExpansion(index)}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="text-xl font-semibold text-gray-900">
                            Case ID: {result.case_id}
                          </h3>
                          <div className="flex items-center space-x-4">                            <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                              Score: {result.score?.toFixed(4) || result.final_score?.toFixed(4)}
                            </span>
                            <svg 
                              className={`w-5 h-5 text-gray-500 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
                              fill="none" 
                              stroke="currentColor" 
                              viewBox="0 0 24 24"
                            >
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </div>
                        </div>
                        
                        {result.title && (
                          <p className="text-lg text-gray-700 font-medium mb-2">
                            {result.title}
                          </p>
                        )}
                        
                        {result.court && (
                          <p className="text-gray-600 mb-3">
                            <span className="font-medium">Court:</span> {result.court}
                          </p>
                        )}
                          {/* Preview Text */}
                        <div className="text-gray-700 leading-relaxed">
                          {isExpanded ? (
                            <div className="prose max-w-none">
                              <div className="bg-gray-50 rounded-2xl p-6 border-l-4 border-blue-400">
                                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                                  {result.text_sample || result.sample || result.text || 'No content available'}
                                </div>
                              </div>
                            </div>
                          ) : (
                            <p className="text-gray-600">
                              {(result.text_sample || result.sample || result.text || '').substring(0, 200)}
                              {(result.text_sample || result.sample || result.text || '').length > 200 && '...'}
                              <span className="ml-2 text-blue-600 font-medium">Click to expand</span>
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Expandable Content */}
                  {isExpanded && (
                    <div className="border-t border-gray-100 bg-gray-50 p-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {result.date && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Date</h4>
                            <p className="text-gray-700">{result.date}</p>
                          </div>
                        )}
                        
                        {result.judges && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Judges</h4>
                            <p className="text-gray-700">{result.judges}</p>
                          </div>
                        )}
                        
                        {result.parties && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Parties</h4>
                            <p className="text-gray-700">{result.parties}</p>
                          </div>
                        )}
                        
                        {result.keywords && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Keywords</h4>
                            <div className="flex flex-wrap gap-2">
                              {result.keywords.split(',').map((keyword, i) => (
                                <span key={i} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                                  {keyword.trim()}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [activeTab, setActiveTab] = useState('scr');

  const loadFiles = useCallback(async () => {
    try {
      const response = await fileAPI.list();
      if (response.success) {
        setFiles(response.files);
      }
    } catch (error) {
      console.error('Failed to load files:', error);
    }
  }, []);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-6">          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <img 
                src="/assets/advoca-dabra.jpeg" 
                alt="AdvocaDabra" 
                className="h-10 w-auto"
              />
              <div>
                <h1 className="text-2xl font-semibold text-gray-900">
                  AdvocaDabra
                </h1>
                <p className="text-gray-600 mt-1">
                  Welcome back, {user?.name || user?.email}
                </p>
              </div>
            </div>
            <button
              onClick={logout}
              className="text-gray-600 hover:text-gray-900 transition-colors font-medium"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
      
      {/* Navigation Tabs */}
      <div className="border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6">
          <nav className="flex space-x-12">            <button
              onClick={() => setActiveTab('scr')}
              className={`py-6 px-2 border-b-2 font-medium transition-colors ${
                activeTab === 'scr'
                  ? 'border-black text-black'
                  : 'border-transparent text-gray-500 hover:text-gray-900'
              }`}
            >
              Similar Case Retrieval
            </button>
            <button
              onClick={() => setActiveTab('pcr')}
              className={`py-6 px-2 border-b-2 font-medium transition-colors ${
                activeTab === 'pcr'
                  ? 'border-black text-black'
                  : 'border-transparent text-gray-500 hover:text-gray-900'
              }`}
            >
              Precedent Case Retrieval
            </button>            <button
              onClick={() => setActiveTab('ljp')}
              className={`py-6 px-2 border-b-2 font-medium transition-colors ${
                activeTab === 'ljp'
                  ? 'border-black text-black'
                  : 'border-transparent text-gray-500 hover:text-gray-900'
              }`}
            >
              Legal Judgement Prediction
            </button>
          </nav>
        </div>
      </div>      
      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {activeTab === 'scr' && (
          <IntegratedAnalysis 
            analysisType="scr"
            files={files}
            onFileUploaded={loadFiles}
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
          />
        )}

        {activeTab === 'pcr' && (
          <IntegratedAnalysis 
            analysisType="pcr"
            files={files}
            onFileUploaded={loadFiles}
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
          />
        )}        {activeTab === 'ljp' && (
          <div className="max-w-4xl mx-auto space-y-12">
            {/* Header */}
            <div className="text-center py-8">
              <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 mb-4">
                Legal Judgement Prediction
              </h1>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
                Predict legal case outcomes using AI-powered analysis of case facts and legal precedents
              </p>
            </div>

            {/* Coming Soon Content */}
            <div className="text-center py-16">
              <div className="text-8xl mb-8">⚖️</div>
              <h3 className="text-3xl font-semibold text-gray-900 mb-4">Coming Soon</h3>
              <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
                Legal Judgement Prediction is currently under development. This powerful feature will analyze case details 
                and predict potential outcomes based on historical legal data and AI models.
              </p>
              
              {/* Feature Preview Cards */}
              <div className="grid md:grid-cols-3 gap-6 mt-12">
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
                  <div className="text-3xl mb-4">🎯</div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">Outcome Prediction</h4>
                  <p className="text-gray-600 text-sm">
                    Predict case outcomes with confidence scores based on similar historical cases
                  </p>
                </div>
                
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-100">
                  <div className="text-3xl mb-4">📊</div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">Success Probability</h4>
                  <p className="text-gray-600 text-sm">
                    Calculate win/loss probabilities for different legal strategies
                  </p>
                </div>
                
                <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-100">
                  <div className="text-3xl mb-4">🔍</div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">Risk Assessment</h4>
                  <p className="text-gray-600 text-sm">
                    Identify potential risks and opportunities in your legal cases
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
