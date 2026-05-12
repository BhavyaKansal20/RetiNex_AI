import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Users, Activity, TrendingUp, Clock } from 'lucide-react';
import { analyticsAPI } from '../api';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const SEVERITY_COLORS = ['#22c55e', '#eab308', '#f97316', '#ef4444', '#dc2626'];
const fadeUp = { hidden: { opacity: 0, y: 20 }, visible: (i = 0) => ({ opacity: 1, y: 0, transition: { delay: i * 0.08, duration: 0.5 } }) };

function StatCard({ icon: Icon, label, value, color, index }) {
  return (
    <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={index} className="glass-card-glow p-5 flex items-center gap-4">
      <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ background: `${color}18` }}>
        <Icon size={22} style={{ color }} />
      </div>
      <div>
        <p className="text-2xl font-bold">{value}</p>
        <p className="text-xs text-[var(--color-text-muted)]">{label}</p>
      </div>
    </motion.div>
  );
}

export default function DashboardPage() {
  const [overview, setOverview] = useState(null);
  const [userStats, setUserStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([analyticsAPI.getOverview(), analyticsAPI.getUserStats()])
      .then(([ov, us]) => { setOverview(ov.data); setUserStats(us.data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-64px)] px-4 py-10 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
          {[...Array(4)].map((_, i) => <div key={i} className="skeleton h-24 rounded-2xl" />)}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="skeleton h-80 rounded-2xl" />
          <div className="skeleton h-80 rounded-2xl" />
        </div>
      </div>
    );
  }

  const distLabels = overview?.disease_distribution ? Object.keys(overview.disease_distribution) : [];
  const distValues = overview?.disease_distribution ? Object.values(overview.disease_distribution) : [];

  const doughnutData = {
    labels: distLabels,
    datasets: [{
      data: distValues,
      backgroundColor: SEVERITY_COLORS.slice(0, distLabels.length),
      borderWidth: 0,
      hoverOffset: 8,
    }],
  };

  const barData = {
    labels: distLabels,
    datasets: [{
      label: 'Predictions',
      data: distValues,
      backgroundColor: SEVERITY_COLORS.slice(0, distLabels.length).map(c => c + '80'),
      borderColor: SEVERITY_COLORS.slice(0, distLabels.length),
      borderWidth: 1,
      borderRadius: 6,
    }],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#94a3b8', font: { size: 11, family: 'Inter' } } },
    },
    scales: {
      x: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(100,200,255,0.04)' } },
      y: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(100,200,255,0.04)' } },
    },
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-grid px-4 py-10">
      <div className="max-w-6xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold mb-2">Analytics Dashboard</h1>
          <p className="text-[var(--color-text-secondary)] mb-8">Platform-wide statistics and prediction analytics</p>
        </motion.div>

        {/* Stat cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
          <StatCard icon={Activity} label="Total Predictions" value={overview?.total_predictions ?? 0} color="#00d4aa" index={0} />
          <StatCard icon={Users} label="Total Users" value={overview?.total_users ?? 0} color="#3b82f6" index={1} />
          <StatCard icon={BarChart3} label="Your Predictions" value={userStats?.total_predictions ?? 0} color="#8b5cf6" index={2} />
          <StatCard icon={TrendingUp} label="Your Reports" value={userStats?.total_reports ?? 0} color="#f97316" index={3} />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={4} className="glass-card-glow p-6">
            <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Disease Distribution</h3>
            <div className="h-[280px] flex items-center justify-center">
              <Doughnut data={doughnutData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 11, family: 'Inter' }, padding: 16 } } } }} />
            </div>
          </motion.div>

          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={5} className="glass-card-glow p-6">
            <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)]">Predictions by Class</h3>
            <div className="h-[280px]">
              <Bar data={barData} options={chartOptions} />
            </div>
          </motion.div>
        </div>

        {/* Recent predictions */}
        <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={6} className="glass-card-glow p-6">
          <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)] flex items-center gap-2">
            <Clock size={16} /> Recent Predictions
          </h3>
          {overview?.recent_predictions?.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-[var(--color-text-muted)] border-b border-white/5">
                    <th className="pb-3 font-medium">Date</th>
                    <th className="pb-3 font-medium">Prediction</th>
                    <th className="pb-3 font-medium">Confidence</th>
                    <th className="pb-3 font-medium">Image</th>
                  </tr>
                </thead>
                <tbody>
                  {overview.recent_predictions.map((p, i) => (
                    <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                      <td className="py-3 text-[var(--color-text-muted)] text-xs">
                        {p.created_at ? new Date(p.created_at).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="py-3">
                        <span className="px-2.5 py-1 rounded-lg text-xs font-medium" style={{
                          background: `${SEVERITY_COLORS[p.predicted_class] || '#6b7280'}18`,
                          color: SEVERITY_COLORS[p.predicted_class] || '#6b7280',
                        }}>
                          {p.predicted_label || 'N/A'}
                        </span>
                      </td>
                      <td className="py-3 font-mono text-xs text-[var(--color-text-secondary)]">
                        {p.confidence ? `${(parseFloat(p.confidence) * 100).toFixed(1)}%` : 'N/A'}
                      </td>
                      <td className="py-3 text-xs text-[var(--color-text-muted)] truncate max-w-[120px]">{p.image_filename || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-sm text-[var(--color-text-muted)] py-8 text-center">No predictions yet</p>
          )}
        </motion.div>
      </div>
    </div>
  );
}
