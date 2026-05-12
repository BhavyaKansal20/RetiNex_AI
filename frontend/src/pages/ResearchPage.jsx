import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FlaskConical, Cpu, Database, Layers, TrendingUp, Target, BarChart } from 'lucide-react';
import { researchAPI } from '../api';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Tooltip, Legend, Filler } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Tooltip, Legend, Filler);

const SEVERITY_COLORS = ['#22c55e', '#eab308', '#f97316', '#ef4444', '#dc2626'];
const CLASS_NAMES = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'];
const fadeUp = { hidden: { opacity: 0, y: 20 }, visible: (i = 0) => ({ opacity: 1, y: 0, transition: { delay: i * 0.08, duration: 0.5 } }) };

function MetricCard({ label, value, icon: Icon, color, index }) {
  return (
    <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={index} className="glass-card p-4 flex items-center gap-3">
      <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${color}18` }}>
        <Icon size={18} style={{ color }} />
      </div>
      <div>
        <p className="text-lg font-bold">{typeof value === 'number' ? (value * 100).toFixed(1) + '%' : value}</p>
        <p className="text-xs text-[var(--color-text-muted)]">{label}</p>
      </div>
    </motion.div>
  );
}

export default function ResearchPage() {
  const [metrics, setMetrics] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([researchAPI.getMetrics(), researchAPI.getModelInfo()])
      .then(([m, mi]) => { setMetrics(m.data); setModelInfo(mi.data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-64px)] px-4 py-10 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
          {[...Array(4)].map((_, i) => <div key={i} className="skeleton h-20 rounded-2xl" />)}
        </div>
        <div className="skeleton h-96 rounded-2xl" />
      </div>
    );
  }

  const report = metrics?.classification_report || {};
  const cm = metrics?.confusion_matrix || [];
  const history = metrics?.training_history;
  const perClass = metrics?.per_class_metrics;

  // Training curves data
  const hasCurves = history && history.loss && history.loss.length > 0;
  const trainingData = hasCurves ? {
    labels: history.loss.map((_, i) => `Epoch ${i + 1}`),
    datasets: [
      {
        label: 'Train Loss',
        data: history.loss,
        borderColor: '#00d4aa',
        backgroundColor: 'rgba(0, 212, 170, 0.1)',
        tension: 0.4,
        fill: true,
      },
      ...(history.val_loss ? [{
        label: 'Val Loss',
        data: history.val_loss,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
      }] : []),
    ],
  } : null;

  const accuracyData = hasCurves && history.accuracy ? {
    labels: history.accuracy.map((_, i) => `Epoch ${i + 1}`),
    datasets: [
      {
        label: 'Train Accuracy',
        data: history.accuracy,
        borderColor: '#8b5cf6',
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        tension: 0.4,
        fill: true,
      },
      ...(history.val_accuracy ? [{
        label: 'Val Accuracy',
        data: history.val_accuracy,
        borderColor: '#f97316',
        backgroundColor: 'rgba(249, 115, 22, 0.1)',
        tension: 0.4,
        fill: true,
      }] : []),
    ],
  } : null;

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: '#94a3b8', font: { size: 11, family: 'Inter' } } } },
    scales: {
      x: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(100,200,255,0.04)' } },
      y: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(100,200,255,0.04)' } },
    },
  };

  // Per-class F1 bar data
  const f1Data = perClass ? {
    labels: Object.keys(perClass),
    datasets: [{
      label: 'F1-Score',
      data: Object.values(perClass).map(v => v.f1_score || 0),
      backgroundColor: SEVERITY_COLORS.map(c => c + '80'),
      borderColor: SEVERITY_COLORS,
      borderWidth: 1,
      borderRadius: 6,
    }],
  } : null;

  return (
    <div className="min-h-[calc(100vh-64px)] bg-grid px-4 py-10">
      <div className="max-w-6xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-[var(--color-violet)]/20 flex items-center justify-center">
              <FlaskConical size={20} className="text-[var(--color-violet)]" />
            </div>
            <h1 className="text-3xl font-bold">Research Dashboard</h1>
          </div>
          <p className="text-[var(--color-text-secondary)] mb-8 ml-[52px]">Model evaluation metrics and training analysis</p>
        </motion.div>

        {/* Summary metrics */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard icon={Target} label="Accuracy" value={report.accuracy || 0} color="#00d4aa" index={0} />
          <MetricCard icon={TrendingUp} label="Macro F1" value={report.macro_avg?.['f1-score'] || report['macro avg']?.['f1-score'] || 0} color="#3b82f6" index={1} />
          <MetricCard icon={BarChart} label="W. Precision" value={report.weighted_avg?.precision || report['weighted avg']?.precision || 0} color="#8b5cf6" index={2} />
          <MetricCard icon={Layers} label="W. Recall" value={report.weighted_avg?.recall || report['weighted avg']?.recall || 0} color="#f97316" index={3} />
        </div>

        {/* Confusion matrix */}
        <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={4} className="glass-card-glow p-6 mb-8">
          <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Confusion Matrix</h3>
          {cm.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="mx-auto border-separate" style={{ borderSpacing: '3px' }}>
                <thead>
                  <tr>
                    <th className="p-2" />
                    {CLASS_NAMES.map((name, i) => (
                      <th key={i} className="p-2 text-xs text-[var(--color-text-muted)] font-medium whitespace-nowrap">{name}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {cm.map((row, i) => {
                    const rowMax = Math.max(...row.map(Number), 1);
                    return (
                      <tr key={i}>
                        <td className="p-2 text-xs text-[var(--color-text-muted)] font-medium whitespace-nowrap text-right">{CLASS_NAMES[i]}</td>
                        {row.map((val, j) => {
                          const intensity = Math.min(Number(val) / rowMax, 1);
                          const isDiag = i === j;
                          return (
                            <td key={j} className="w-14 h-14 text-center text-sm font-mono rounded-lg transition-all" style={{
                              background: isDiag
                                ? `rgba(0, 212, 170, ${0.15 + intensity * 0.5})`
                                : `rgba(239, 68, 68, ${intensity * 0.3})`,
                              color: intensity > 0.3 ? '#f0f4f8' : '#64748b',
                            }}>
                              {val}
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              <div className="flex justify-center gap-6 mt-4 text-xs text-[var(--color-text-muted)]">
                <span>← Predicted →</span>
                <span>↑ Actual ↓</span>
              </div>
            </div>
          ) : (
            <p className="text-sm text-[var(--color-text-muted)] text-center py-8">
              No evaluation data available. Run <code className="bg-white/5 px-2 py-0.5 rounded text-xs">training/export_metrics.py</code> to generate metrics.
            </p>
          )}
        </motion.div>

        {/* Training curves */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={5} className="glass-card-glow p-6">
            <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Training / Validation Loss</h3>
            <div className="h-[260px]">
              {trainingData ? <Line data={trainingData} options={lineOptions} /> : (
                <p className="text-sm text-[var(--color-text-muted)] flex items-center justify-center h-full">No training history available</p>
              )}
            </div>
          </motion.div>

          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={6} className="glass-card-glow p-6">
            <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Training / Validation Accuracy</h3>
            <div className="h-[260px]">
              {accuracyData ? <Line data={accuracyData} options={lineOptions} /> : (
                <p className="text-sm text-[var(--color-text-muted)] flex items-center justify-center h-full">No training history available</p>
              )}
            </div>
          </motion.div>
        </div>

        {/* Per-class F1 */}
        {f1Data && (
          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={7} className="glass-card-glow p-6 mb-8">
            <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Per-Class F1-Score</h3>
            <div className="h-[260px]">
              <Bar data={f1Data} options={{
                ...lineOptions,
                indexAxis: 'y',
                scales: {
                  ...lineOptions.scales,
                  x: { ...lineOptions.scales.x, max: 1 },
                },
              }} />
            </div>
          </motion.div>
        )}

        {/* Model info */}
        {modelInfo && (
          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={8} className="glass-card-glow p-6">
            <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)] flex items-center gap-2">
              <Cpu size={16} /> Model Architecture
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { label: 'Model', value: modelInfo.model_name },
                { label: 'Framework', value: modelInfo.framework },
                { label: 'Input Size', value: modelInfo.input_size },
                { label: 'Classes', value: modelInfo.num_classes },
                { label: 'Datasets', value: modelInfo.datasets?.join(', ') },
                { label: 'Explainability', value: modelInfo.explainability?.join(', ') },
              ].map((item) => (
                <div key={item.label} className="bg-white/[0.03] rounded-xl p-3">
                  <p className="text-xs text-[var(--color-text-muted)] mb-1">{item.label}</p>
                  <p className="text-sm font-medium">{item.value}</p>
                </div>
              ))}
            </div>
            {modelInfo.preprocessing && (
              <div className="mt-4">
                <p className="text-xs text-[var(--color-text-muted)] mb-2">Preprocessing Pipeline</p>
                <div className="flex flex-wrap gap-2">
                  {modelInfo.preprocessing.map((step) => (
                    <span key={step} className="px-3 py-1.5 rounded-lg bg-white/5 text-xs text-[var(--color-text-secondary)]">{step}</span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
