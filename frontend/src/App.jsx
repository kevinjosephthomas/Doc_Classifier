import { useState, useRef } from 'react'
import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

export default function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const inputRef = useRef(null)

  const handleFile = (chosen) => {
    if (!chosen) return
    const allowed = ['application/pdf', 'text/plain', 'text/markdown', 'text/csv']
    const ext = chosen.name.split('.').pop().toLowerCase()
    const allowedExts = ['pdf', 'txt', 'md', 'csv']
    if (!allowedExts.includes(ext)) {
      setError('Unsupported file type. Please upload a PDF or text file.')
      return
    }
    setFile(chosen)
    setResult(null)
    setError(null)

    if (ext !== 'pdf') {
      const reader = new FileReader()
      reader.onload = (e) => setPreview(e.target.result.slice(0, 600))
      reader.readAsText(chosen)
    } else {
      setPreview('')
    }
  }

  const onInputChange = (e) => handleFile(e.target.files[0])
  const onDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    handleFile(e.dataTransfer.files[0])
  }

  const onClassify = async () => {
    if (!file) return
    setLoading(true)
    setResult(null)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await fetch(`${API_URL}/classify`, { method: 'POST', body: formData })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Classification failed.')
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const onRemove = () => {
    setFile(null)
    setPreview('')
    setResult(null)
    setError(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  // --- Visualization Helpers ---
  const renderConfidenceChart = (confidence) => {
    const data = [
      { name: 'Confidence', value: confidence },
      { name: 'Uncertainty', value: 100 - confidence }
    ]
    const COLORS = ['#10b981', '#1e2d45'] // Success green vs muted background

    return (
      <div className="chart-container">
        <h4>AI Confidence Score</h4>
        <div className="gauge-chart">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="100%"
                startAngle={180}
                endAngle={0}
                innerRadius={60}
                outerRadius={80}
                paddingAngle={0}
                dataKey="value"
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <RechartsTooltip cursor={false} contentStyle={{ background: '#1a2236', border: '1px solid #1e2d45', color: '#fff' }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="gauge-value">{confidence}%</div>
        </div>
      </div>
    )
  }

  const renderStatsChart = (wordCount, fileSize) => {
    // A simple mock chart comparing typical lengths
    const data = [
      { name: 'This Doc', Words: wordCount },
      { name: 'Avg Doc', Words: 1500 }
    ]

    return (
      <div className="chart-container">
        <h4>Document Size (Words)</h4>
        <div style={{ height: 180, marginTop: '20px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e2d45" />
              <XAxis dataKey="name" stroke="#64748b" tick={{ fill: '#64748b' }} />
              <YAxis stroke="#64748b" tick={{ fill: '#64748b' }} />
              <RechartsTooltip cursor={{ fill: '#1a2236' }} contentStyle={{ background: '#111827', border: '1px solid #1e2d45', color: '#fff' }} />
              <Bar dataKey="Words" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-badge">⚡ Powered by Groq + Recharts</div>
        <h1>AI Document Classifier</h1>
        <p>Upload a document to extract visual classification metrics instantly.</p>
      </header>

      <div className="card">
        {/* Drop Zone */}
        <div
          className={`drop-zone${dragOver ? ' drag-over' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
          onClick={() => inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.txt,.md,.csv"
            onChange={onInputChange}
            onClick={(e) => e.stopPropagation()}
          />
          <span className="drop-icon">📂</span>
          <h3>Drag & drop your document here</h3>
          <p>Supports PDF and text files (.txt, .md, .csv)</p>
          <span className="browse-btn">Browse File</span>
        </div>

        {/* File Pill */}
        {file && (
          <div className="file-pill">
            <span className="file-pill-icon">
              {file.name.endsWith('.pdf') ? '🗂️' : '📄'}
            </span>
            <div className="file-pill-info">
              <div className="name">{file.name}</div>
              <div className="size">{formatBytes(file.size)}</div>
            </div>
            <button className="file-pill-remove" onClick={onRemove} title="Remove">✕</button>
          </div>
        )}

        {/* Preview */}
        {preview && (
          <div>
            <div className="preview-label">Text Preview</div>
            <div className="preview-box">{preview}{preview.length >= 600 ? '…' : ''}</div>
          </div>
        )}

        {/* Classify Button */}
        <button
          className="classify-btn"
          onClick={onClassify}
          disabled={!file || loading}
        >
          {loading ? <><span className="spinner" /> Analyzing…</> : <>🔍 Classify Document</>}
        </button>

        {/* Result & Visualizations */}
        {result && result.result && (
          <div className="result-card">
            <div className="result-header">
              <div className="result-badge">✓ {result.result.type}</div>
              <div className="result-filename">{result.filename}</div>
            </div>
            
            <div className="result-body" style={{ marginBottom: '25px', padding: '15px', background: 'rgba(99, 102, 241, 0.05)', borderRadius: '8px', borderLeft: '3px solid #6366f1' }}>
              <strong>AI Reasoning:</strong> {result.result.reason}
            </div>

            <div className="charts-wrapper" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              {renderConfidenceChart(result.result.confidence)}
              {renderStatsChart(result.result.word_count || 0, file?.size)}
            </div>
          </div>
        )}

        {/* Error */}
        {error && <div className="error-box">⚠️ {error}</div>}
      </div>

      <footer className="footer">
        Document Classifier · Interactive Dashboards Powered by Recharts
      </footer>
    </div>
  )
}
