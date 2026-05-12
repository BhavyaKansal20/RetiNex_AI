import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Calendar, Activity, FileText, Clock, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { analyticsAPI, predictionAPI } from '../api';

const SEVERITY_COLORS = { 0: '#22c55e', 1: '#eab308', 2: '#f97316', 3: '#ef4444', 4: '#dc2626' };
const fadeUp = { hidden: { opacity: 0, y: 20 }, visible: (i = 0) => ({ opacity: 1, y: 0, transition: { delay: i * 0.08, duration: 0.5 } }) };

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([analyticsAPI.getUserStats(), predictionAPI.getAll()])
      .then(([s, p]) => { setStats(s.data); setPredictions(p.data.predictions || []); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-[calc(100vh-64px)] bg-grid px-4 py-10">
      <div className="max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold mb-8">Profile</h1>
        </motion.div>

        {/* Profile card */}
        <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={0} className="glass-card-glow p-6 mb-6">
          <div className="flex items-center gap-5">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[var(--color-teal)] to-[var(--color-blue)] flex items-center justify-center text-white text-2xl font-bold">
              {user?.username?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold flex items-center gap-2"><User size={18} className="text-[var(--color-text-muted)]" /> {user?.username}</h2>
              <p className="text-sm text-[var(--color-text-secondary)] flex items-center gap-2 mt-1"><Mail size={14} /> {user?.email}</p>
            </div>
            <button onClick={logout} className="btn-outline !py-2.5 !px-4 flex items-center gap-2 text-sm text-red-400 border-red-400/30 hover:bg-red-400/10">
              <LogOut size={16} /> Logout
            </button>
          </div>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          {[
            { icon: Activity, label: 'Predictions', value: stats?.total_predictions ?? '—', color: '#00d4aa' },
            { icon: FileText, label: 'Reports', value: stats?.total_reports ?? '—', color: '#3b82f6' },
            { icon: Calendar, label: 'Joined', value: user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A', color: '#8b5cf6' },
          ].map((s, i) => {
            const Icon = s.icon;
            return (
              <motion.div key={s.label} initial="hidden" animate="visible" variants={fadeUp} custom={i + 1} className="glass-card p-4 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${s.color}18` }}>
                  <Icon size={18} style={{ color: s.color }} />
                </div>
                <div>
                  <p className="text-lg font-bold">{s.value}</p>
                  <p className="text-xs text-[var(--color-text-muted)]">{s.label}</p>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Prediction history */}
        <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={4} className="glass-card-glow p-6">
          <h3 className="text-sm font-semibold mb-4 text-[var(--color-text-secondary)] flex items-center gap-2">
            <Clock size={16} /> Your Prediction History
          </h3>
          {loading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => <div key={i} className="skeleton h-14 rounded-xl" />)}
            </div>
          ) : predictions.length > 0 ? (
            <div className="space-y-2.5">
              {predictions.slice(0, 15).map((p, i) => (
                <div key={i} className="flex items-center gap-4 p-3 rounded-xl bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
                  <div className="w-2 h-2 rounded-full" style={{ background: SEVERITY_COLORS[p.predicted_class] || '#6b7280' }} />
                  <span className="text-sm font-medium flex-1">{p.predicted_label}</span>
                  <span className="text-xs font-mono text-[var(--color-text-muted)]">
                    {p.confidence ? `${(parseFloat(p.confidence) * 100).toFixed(1)}%` : '—'}
                  </span>
                  <span className="text-xs text-[var(--color-text-muted)]">
                    {p.created_at ? new Date(p.created_at).toLocaleDateString() : ''}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-[var(--color-text-muted)] py-8 text-center">No predictions yet. Upload a retinal image to get started.</p>
          )}
        </motion.div>
      </div>
    </div>
  );
}
