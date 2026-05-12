import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ScanEye, Shield, FileText, BarChart3, Brain, Zap, ArrowRight, Eye } from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1, y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] },
  }),
};

const features = [
  { icon: ScanEye, title: 'AI-Powered Detection', desc: 'EfficientNetV2 deep learning model trained on 5,000+ retinal images for accurate DR classification.' },
  { icon: Brain, title: 'Explainable AI', desc: 'GradCAM heatmaps reveal exactly where the model focuses, building clinician trust.' },
  { icon: FileText, title: 'Clinical Reports', desc: 'Instant downloadable PDF reports with predictions, heatmaps, and recommendations.' },
  { icon: BarChart3, title: 'Analytics Dashboard', desc: 'Track predictions, view disease distributions, and monitor screening activity.' },
  { icon: Shield, title: 'Research Grade', desc: 'Confusion matrices, F1-scores, and cross-dataset evaluation for publication-ready results.' },
  { icon: Zap, title: 'Fast Inference', desc: 'Optimized pipeline delivers results in seconds with Test-Time Augmentation support.' },
];

const stages = [
  { grade: 0, label: 'No DR', color: '#22c55e', desc: 'Healthy retina' },
  { grade: 1, label: 'Mild', color: '#eab308', desc: 'Microaneurysms' },
  { grade: 2, label: 'Moderate', color: '#f97316', desc: 'Dot hemorrhages' },
  { grade: 3, label: 'Severe', color: '#ef4444', desc: 'Extensive lesions' },
  { grade: 4, label: 'Proliferative', color: '#dc2626', desc: 'Neovascularization' },
];

export default function LandingPage() {
  return (
    <div className="bg-grid min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden pt-20 pb-28 px-4">
        <div className="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-[radial-gradient(circle,rgba(0,212,170,0.08),transparent_60%)] pointer-events-none" />
        <div className="absolute top-[100px] right-[-100px] w-[400px] h-[400px] bg-[radial-gradient(circle,rgba(59,130,246,0.06),transparent_60%)] pointer-events-none" />

        <div className="max-w-5xl mx-auto text-center relative z-10">
          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={0}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--color-border-glow)] bg-[var(--color-teal-dim)] text-sm text-[var(--color-teal)] font-medium mb-6"
          >
            <Eye size={14} />
            Powered by EfficientNetV2 + GradCAM
          </motion.div>

          <motion.h1 initial="hidden" animate="visible" variants={fadeUp} custom={1}
            className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6"
          >
            <span className="text-gradient">Diabetic Retinopathy</span>
            <br />
            <span className="text-[var(--color-text-primary)]">Detection with AI</span>
          </motion.h1>

          <motion.p initial="hidden" animate="visible" variants={fadeUp} custom={2}
            className="text-lg sm:text-xl text-[var(--color-text-secondary)] max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Research-grade explainable AI for retinal screening. Upload a fundus image and receive
            instant classification with visual explanations and clinical reports.
          </motion.p>

          <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={3}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link to="/register" className="btn-primary text-base !py-3.5 !px-8 flex items-center gap-2 no-underline">
              Start Screening <ArrowRight size={18} />
            </Link>
            <Link to="/research" className="btn-outline text-base !py-3.5 !px-8 no-underline">
              View Research
            </Link>
          </motion.div>
        </div>
      </section>

      {/* DR Stages */}
      <section className="py-16 px-4">
        <div className="max-w-5xl mx-auto">
          <motion.h2 initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}
            className="text-2xl sm:text-3xl font-bold text-center mb-12"
          >
            5-Class DR Severity Classification
          </motion.h2>
          <div className="flex flex-wrap justify-center gap-4">
            {stages.map((s, i) => (
              <motion.div key={s.grade} initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={i}
                className="glass-card px-6 py-4 flex flex-col items-center min-w-[140px] hover:scale-105 transition-transform duration-300"
              >
                <div className="w-3 h-3 rounded-full mb-2" style={{ background: s.color, boxShadow: `0 0 12px ${s.color}50` }} />
                <span className="text-sm font-bold mb-1" style={{ color: s.color }}>Grade {s.grade}</span>
                <span className="text-sm font-semibold text-[var(--color-text-primary)]">{s.label}</span>
                <span className="text-xs text-[var(--color-text-muted)] mt-1">{s.desc}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.h2 initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}
            className="text-2xl sm:text-3xl font-bold text-center mb-4"
          >
            Platform Features
          </motion.h2>
          <motion.p initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={1}
            className="text-[var(--color-text-secondary)] text-center mb-14 max-w-xl mx-auto"
          >
            A complete clinical-grade AI screening pipeline from image upload to PDF report.
          </motion.p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((f, i) => {
              const Icon = f.icon;
              return (
                <motion.div key={f.title} initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={i}
                  className="glass-card-glow p-6 hover:translate-y-[-4px] transition-all duration-300 group"
                >
                  <div className="w-11 h-11 rounded-xl bg-[var(--color-teal-dim)] flex items-center justify-center mb-4 group-hover:bg-[var(--color-teal)] transition-colors duration-300">
                    <Icon size={20} className="text-[var(--color-teal)] group-hover:text-[var(--color-bg-primary)] transition-colors duration-300" />
                  </div>
                  <h3 className="text-base font-semibold mb-2">{f.title}</h3>
                  <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{f.desc}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Tech stack */}
      <section className="py-16 px-4 border-t border-[var(--color-border-glass)]">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-[var(--color-text-muted)] text-sm mb-6">Built with</p>
          <div className="flex flex-wrap items-center justify-center gap-6 text-[var(--color-text-secondary)] text-sm font-medium">
            {['TensorFlow', 'Keras', 'EfficientNetV2', 'GradCAM', 'FastAPI', 'React', 'Google Sheets API'].map((t) => (
              <span key={t} className="px-4 py-2 glass-card">{t}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-[var(--color-border-glass)]">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm text-[var(--color-text-muted)]">
            <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-[var(--color-teal)] to-[var(--color-blue)] flex items-center justify-center">
              <Eye size={12} className="text-white" />
            </div>
            RetiNex AI © {new Date().getFullYear()}
          </div>
          <p className="text-xs text-[var(--color-text-muted)]">
            Research-grade medical AI platform • Not for clinical diagnosis
          </p>
        </div>
      </footer>
    </div>
  );
}
