import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { Eye, Mail, Lock, AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/predict');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-12 bg-grid">
      <div className="absolute top-[20%] left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[radial-gradient(circle,rgba(0,212,170,0.06),transparent_60%)] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="glass-card-glow w-full max-w-md p-8 relative z-10"
      >
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--color-teal)] to-[var(--color-blue)] flex items-center justify-center mx-auto mb-4 animate-pulse-glow">
            <Eye size={28} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold mb-1">Welcome Back</h1>
          <p className="text-sm text-[var(--color-text-secondary)]">Sign in to RetiNex AI</p>
        </div>

        {error && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
            className="flex items-center gap-2 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 mb-6 text-sm text-red-400"
          >
            <AlertCircle size={16} />
            {error}
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-[var(--color-text-secondary)] mb-2 font-medium">Email</label>
            <div className="relative">
              <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)]" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field !pl-11"
                placeholder="you@example.com"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-[var(--color-text-secondary)] mb-2 font-medium">Password</label>
            <div className="relative">
              <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)]" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field !pl-11"
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2">
            {loading ? (
              <div className="w-5 h-5 border-2 border-[var(--color-bg-primary)]/30 border-t-[var(--color-bg-primary)] rounded-full animate-spin" />
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <p className="text-center text-sm text-[var(--color-text-muted)] mt-6">
          Don&apos;t have an account?{' '}
          <Link to="/register" className="text-[var(--color-teal)] hover:underline no-underline font-medium">Create one</Link>
        </p>
      </motion.div>
    </div>
  );
}
