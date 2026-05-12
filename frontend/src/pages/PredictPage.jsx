import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, ScanEye, Download, Image as ImageIcon, AlertCircle, CheckCircle2, Loader2, X, Eye, Layers, Blend } from 'lucide-react';
import { predictionAPI, reportAPI } from '../api';

const SEVERITY_COLORS = { 0: '#22c55e', 1: '#eab308', 2: '#f97316', 3: '#ef4444', 4: '#dc2626' };
const CLASS_NAMES = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'];

export default function PredictPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [useTTA, setUseTTA] = useState(false);
  const [activeTab, setActiveTab] = useState('original');
  const [reportLoading, setReportLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFile = useCallback((f) => {
    if (f && f.type.startsWith('image/')) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResult(null);
      setError('');
    } else {
      setError('Please upload a valid image file.');
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragActive(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }, [handleFile]);

  const handlePredict = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await predictionAPI.predict(formData, useTTA);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!result?.prediction_id) return;
    setReportLoading(true);
    try {
      const genRes = await reportAPI.generate({ prediction_id: result.prediction_id });
      const dlRes = await reportAPI.download(genRes.data.report_id);
      const url = URL.createObjectURL(dlRes.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = `retinex_report_${genRes.data.patient_id}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError('Failed to generate report.');
    } finally {
      setReportLoading(false);
    }
  };

  const clearAll = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError('');
  };

  const gradcamTabs = [
    { key: 'original', label: 'Original', icon: Eye },
    { key: 'heatmap', label: 'GradCAM', icon: Layers },
    { key: 'overlay', label: 'Overlay', icon: Blend },
  ];

  return (
    <div className="min-h-[calc(100vh-64px)] bg-grid px-4 py-10">
      <div className="max-w-6xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <h1 className="text-3xl font-bold mb-2">AI Prediction</h1>
          <p className="text-[var(--color-text-secondary)] mb-8">Upload a retinal fundus image for diabetic retinopathy screening</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Upload + Controls */}
          <div className="space-y-5">
            {/* Upload zone */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
              className={`glass-card-glow p-6 ${dragActive ? 'border-[var(--color-teal)] bg-[var(--color-teal-dim)]' : ''}`}
              onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
              onDragLeave={() => setDragActive(false)}
              onDrop={handleDrop}
            >
              {!preview ? (
                <label className="flex flex-col items-center justify-center py-14 cursor-pointer">
                  <div className="w-16 h-16 rounded-2xl bg-[var(--color-teal-dim)] flex items-center justify-center mb-4">
                    <Upload size={28} className="text-[var(--color-teal)]" />
                  </div>
                  <p className="text-sm font-medium mb-1">Drag & drop or click to upload</p>
                  <p className="text-xs text-[var(--color-text-muted)]">PNG, JPG, JPEG • Max 10MB</p>
                  <input type="file" accept="image/*" className="hidden" onChange={(e) => handleFile(e.target.files[0])} />
                </label>
              ) : (
                <div className="relative">
                  <button onClick={clearAll}
                    className="absolute top-2 right-2 z-10 w-8 h-8 rounded-full bg-black/60 flex items-center justify-center text-white hover:bg-black/80 cursor-pointer border-none transition-colors"
                  >
                    <X size={16} />
                  </button>
                  <img src={preview} alt="Preview" className="w-full rounded-xl object-contain max-h-[320px] mx-auto block" />
                  <p className="text-xs text-[var(--color-text-muted)] mt-3 truncate">{file?.name}</p>
                </div>
              )}
            </motion.div>

            {/* Controls */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
              className="glass-card p-5 flex flex-col sm:flex-row items-center gap-4"
            >
              <label className="flex items-center gap-2 text-sm cursor-pointer select-none">
                <input type="checkbox" checked={useTTA} onChange={(e) => setUseTTA(e.target.checked)}
                  className="w-4 h-4 rounded accent-[var(--color-teal)]"
                />
                <span className="text-[var(--color-text-secondary)]">Test-Time Augmentation</span>
              </label>
              <div className="flex-1" />
              <button onClick={handlePredict} disabled={!file || loading}
                className="btn-primary flex items-center gap-2 min-w-[160px] justify-center"
              >
                {loading ? (
                  <><Loader2 size={18} className="animate-spin" /> Analyzing...</>
                ) : (
                  <><ScanEye size={18} /> Run Detection</>
                )}
              </button>
            </motion.div>

            {/* Error */}
            <AnimatePresence>
              {error && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                  className="flex items-center gap-2 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 text-sm text-red-400"
                >
                  <AlertCircle size={16} /> {error}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Right: Results */}
          <div className="space-y-5">
            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="glass-card-glow p-8 flex flex-col items-center justify-center min-h-[420px]"
                >
                  <div className="w-20 h-20 rounded-full border-4 border-[var(--color-teal-dim)] border-t-[var(--color-teal)] animate-spin mb-6" />
                  <p className="text-sm text-[var(--color-text-secondary)] animate-pulse">Processing retinal image...</p>
                </motion.div>
              ) : result ? (
                <motion.div key="result" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                  {/* Prediction card */}
                  <div className="glass-card-glow p-6 mb-5">
                    <div className="flex items-center gap-3 mb-5">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center"
                        style={{ background: `${SEVERITY_COLORS[result.result.predicted_class]}20` }}
                      >
                        <CheckCircle2 size={22} style={{ color: SEVERITY_COLORS[result.result.predicted_class] }} />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold" style={{ color: SEVERITY_COLORS[result.result.predicted_class] }}>
                          {result.result.predicted_label}
                        </h3>
                        <p className="text-xs text-[var(--color-text-muted)]">Grade {result.result.predicted_class}</p>
                      </div>
                      <div className="ml-auto text-right">
                        <p className="text-2xl font-bold" style={{ color: SEVERITY_COLORS[result.result.predicted_class] }}>
                          {(result.result.confidence * 100).toFixed(1)}%
                        </p>
                        <p className="text-xs text-[var(--color-text-muted)]">Confidence</p>
                      </div>
                    </div>

                    {/* Confidence bars */}
                    <div className="space-y-2.5">
                      {CLASS_NAMES.map((name, i) => {
                        const prob = result.result.probabilities_list?.[i] ?? result.result.probabilities?.[name] ?? 0;
                        return (
                          <div key={name} className="flex items-center gap-3">
                            <span className="text-xs w-24 text-[var(--color-text-secondary)] truncate">{name}</span>
                            <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${prob * 100}%` }}
                                transition={{ duration: 0.8, delay: i * 0.1 }}
                                className="h-full rounded-full"
                                style={{ background: SEVERITY_COLORS[i] }}
                              />
                            </div>
                            <span className="text-xs w-12 text-right font-mono text-[var(--color-text-muted)]">
                              {(prob * 100).toFixed(1)}%
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Severity description */}
                  <div className="glass-card p-5 mb-5">
                    <h4 className="text-sm font-semibold mb-2 text-[var(--color-text-secondary)]">Clinical Assessment</h4>
                    <p className="text-sm text-[var(--color-text-primary)] leading-relaxed">{result.severity_description}</p>
                  </div>

                  {/* GradCAM viewer */}
                  {result.gradcam && (
                    <div className="glass-card-glow p-5 mb-5">
                      <h4 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Explainable AI — GradCAM</h4>
                      <div className="flex gap-1 mb-4">
                        {gradcamTabs.map((tab) => {
                          const Icon = tab.icon;
                          return (
                            <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                              className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-medium transition-all cursor-pointer border-none ${
                                activeTab === tab.key
                                  ? 'bg-[var(--color-teal)] text-[var(--color-bg-primary)]'
                                  : 'bg-white/5 text-[var(--color-text-secondary)] hover:bg-white/10'
                              }`}
                            >
                              <Icon size={14} /> {tab.label}
                            </button>
                          );
                        })}
                      </div>
                      <AnimatePresence mode="wait">
                        <motion.img
                          key={activeTab}
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          transition={{ duration: 0.3 }}
                          src={`data:image/png;base64,${result.gradcam[activeTab]}`}
                          alt={activeTab}
                          className="w-full max-h-[300px] rounded-xl object-contain mx-auto block"
                        />
                      </AnimatePresence>
                    </div>
                  )}

                  {/* Download report */}
                  <button onClick={handleDownloadReport} disabled={reportLoading}
                    className="btn-outline w-full flex items-center justify-center gap-2"
                  >
                    {reportLoading ? (
                      <><Loader2 size={16} className="animate-spin" /> Generating Report...</>
                    ) : (
                      <><Download size={16} /> Download PDF Report</>
                    )}
                  </button>
                </motion.div>
              ) : (
                <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                  className="glass-card p-8 flex flex-col items-center justify-center min-h-[420px] text-center"
                >
                  <div className="w-16 h-16 rounded-2xl bg-[var(--color-blue-dim)] flex items-center justify-center mb-4">
                    <ImageIcon size={28} className="text-[var(--color-blue)]" />
                  </div>
                  <p className="text-sm text-[var(--color-text-secondary)] mb-1">No results yet</p>
                  <p className="text-xs text-[var(--color-text-muted)]">Upload an image and run detection to see predictions here</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
