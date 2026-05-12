import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { Eye, BarChart3, FlaskConical, User, LogOut, Menu, X, ScanEye } from 'lucide-react';

const navLinks = [
  { to: '/predict', label: 'AI Predict', icon: ScanEye },
  { to: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { to: '/research', label: 'Research', icon: FlaskConical },
];

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-[var(--color-bg-primary)]/80 backdrop-blur-xl border-b border-[var(--color-border-glass)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 no-underline">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[var(--color-teal)] to-[var(--color-blue)] flex items-center justify-center">
              <Eye size={20} className="text-white" />
            </div>
            <span className="text-lg font-bold text-gradient tracking-tight">RetiNex AI</span>
          </Link>

          {/* Desktop links */}
          <div className="hidden md:flex items-center gap-1">
            {user && navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`relative flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium no-underline transition-all duration-200 ${
                    isActive
                      ? 'text-[var(--color-teal)] bg-[var(--color-teal-dim)]'
                      : 'text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-white/5'
                  }`}
                >
                  <Icon size={16} />
                  {link.label}
                  {isActive && (
                    <motion.div
                      layoutId="nav-indicator"
                      className="absolute bottom-0 left-2 right-2 h-0.5 bg-[var(--color-teal)] rounded-full"
                      transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>

          {/* Right side */}
          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <>
                <Link
                  to="/profile"
                  className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-white/5 no-underline transition-all"
                >
                  <User size={16} />
                  {user.username}
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm text-[var(--color-text-muted)] hover:text-red-400 hover:bg-red-400/10 transition-all cursor-pointer bg-transparent border-none"
                >
                  <LogOut size={16} />
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] no-underline transition-colors px-4 py-2">
                  Login
                </Link>
                <Link to="/register" className="btn-primary text-sm !py-2.5 !px-5 no-underline">
                  Get Started
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 rounded-xl text-[var(--color-text-secondary)] hover:bg-white/5 bg-transparent border-none cursor-pointer"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-[var(--color-border-glass)] bg-[var(--color-bg-primary)]/95 backdrop-blur-xl overflow-hidden"
          >
            <div className="px-4 py-4 space-y-2">
              {user && navLinks.map((link) => {
                const Icon = link.icon;
                return (
                  <Link
                    key={link.to}
                    to={link.to}
                    onClick={() => setMobileOpen(false)}
                    className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium no-underline transition-all ${
                      location.pathname === link.to
                        ? 'text-[var(--color-teal)] bg-[var(--color-teal-dim)]'
                        : 'text-[var(--color-text-secondary)]'
                    }`}
                  >
                    <Icon size={18} />
                    {link.label}
                  </Link>
                );
              })}
              {user ? (
                <button
                  onClick={() => { logout(); setMobileOpen(false); }}
                  className="flex items-center gap-3 px-4 py-3 rounded-xl text-sm text-red-400 bg-transparent border-none w-full cursor-pointer"
                >
                  <LogOut size={18} />
                  Logout
                </button>
              ) : (
                <div className="flex flex-col gap-2 pt-2">
                  <Link to="/login" onClick={() => setMobileOpen(false)} className="btn-outline text-center no-underline">Login</Link>
                  <Link to="/register" onClick={() => setMobileOpen(false)} className="btn-primary text-center no-underline">Get Started</Link>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
