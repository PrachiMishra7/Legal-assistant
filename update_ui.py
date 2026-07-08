import re
with open('frontend.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_css = """
:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --primary-light: #818cf8;
  --secondary: #ec4899;
  --accent: #10b981;
  --bg-main: #09090b;
  --bg-card: rgba(24, 24, 27, 0.6);
  --bg-card-hover: rgba(39, 39, 42, 0.8);
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --border: rgba(255, 255, 255, 0.1);
  --glow-primary: rgba(99, 102, 241, 0.5);
  --glow-secondary: rgba(236, 72, 153, 0.5);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Poppins', sans-serif;
  background: var(--bg-main);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Dynamic animated mesh gradient background */
body::before {
  content: '';
  position: fixed;
  top: -50%; left: -50%; width: 200%; height: 200%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(236, 72, 153, 0.1) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.05) 0%, transparent 40%);
  pointer-events: none;
  z-index: -1;
  animation: mesh 20s ease-in-out infinite alternate;
}

@keyframes mesh {
  0% { transform: rotate(0deg) scale(1); }
  100% { transform: rotate(15deg) scale(1.1); }
}

header {
  padding: 4rem 2rem;
  text-align: center;
  background: radial-gradient(ellipse at top, rgba(99, 102, 241, 0.15), transparent 70%);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(10px);
  margin-bottom: 2rem;
}

header h1 {
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
  letter-spacing: -1.5px;
}

header p {
  font-size: 1.25rem;
  color: var(--text-secondary);
  font-weight: 300;
}

.badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-size: 0.9rem;
  margin-top: 1.5rem;
  backdrop-filter: blur(5px);
  color: var(--primary-light);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 4rem;
}

/* Glassmorphism Cards */
.hero-section, .card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid var(--border);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  padding: 2.5rem;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
}

.hero-section {
  margin-bottom: 3rem;
  padding: 3.5rem;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 60px -12px rgba(99, 102, 241, 0.3);
  background: var(--bg-card-hover);
  border-color: rgba(99, 102, 241, 0.3);
}

.input-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

textarea {
  width: 100%;
  height: 220px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  color: #fff;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
  background: rgba(0, 0, 0, 0.5);
}

button {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  border: none;
  padding: 1.25rem 2.5rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: auto;
  box-shadow: 0 10px 25px -5px var(--glow-primary);
  position: relative;
  overflow: hidden;
}

button::after {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
  transform: translateX(-100%);
}

button:hover::after {
  transform: translateX(100%);
  transition: transform 0.6s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px -5px var(--glow-secondary);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.upload-zone {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.02);
  transition: all 0.3s ease;
}

.upload-zone:hover {
  border-color: var(--primary);
  background: rgba(99, 102, 241, 0.05);
}

.file-upload-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--border);
  padding: 1rem 2rem;
  border-radius: 50px;
  cursor: pointer;
  display: inline-block;
  color: #fff;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.file-upload-btn:hover {
  background: #fff;
  color: #000;
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem;
}

.full-width { grid-column: 1 / -1; }

.summary-box {
  background: linear-gradient(to right, rgba(99,102,241,0.1), rgba(236,72,153,0.05));
  border-left: 4px solid var(--primary);
  padding: 2rem;
  border-radius: 0 16px 16px 0;
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--text-primary);
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  padding: 2rem 1rem;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s ease;
}

.metric:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--primary-light);
  transform: translateY(-3px);
}

.metric strong {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.metric h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin-top: 0.5rem;
  background: linear-gradient(to bottom right, #fff, #a5b4fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  padding-bottom: 0.1em;
  line-height: 1.1;
}

.section {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}

.section::before {
  content: '';
  position: absolute;
  left: 0; top: 0; height: 100%; width: 4px;
  background: var(--primary);
}

.section-title {
  font-weight: 700;
  font-size: 1.2rem;
  color: #fff;
  margin-bottom: 1rem;
}

.confidence {
  display: inline-block;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.progress {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  margin: 1rem 0;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 50px;
}

pre {
  background: rgba(0, 0, 0, 0.5);
  padding: 1.5rem;
  border-radius: 12px;
  color: var(--text-secondary);
  font-family: monospace;
  font-size: 0.9rem;
  white-space: pre-wrap;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.toggle {
  display: inline-block;
  margin-top: 1rem;
  color: var(--primary-light);
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: color 0.2s ease;
}

.toggle:hover { color: #fff; }

.details {
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transition: all 0.4s ease;
}

.details.open {
  max-height: 2000px;
  opacity: 1;
  margin-top: 1rem;
}

canvas {
  margin-top: 1rem;
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
}

#uploadStatus {
  margin-top: 1.5rem;
  text-align: center;
  font-weight: 500;
  color: var(--accent);
}

::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--bg-main); }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

/* Responsive */
@media (max-width: 1024px) {
  .input-grid, .results-grid { grid-template-columns: 1fr; }
  .metrics { grid-template-columns: 1fr; }
}

@media (max-width: 767px) {
  header h1 { font-size: 2.2rem; }
  .hero-section { padding: 2rem; }
  .card { padding: 1.5rem; }
  .metric h1 { font-size: 2.5rem; }
}

/* Entrance animations */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-section { animation: slideUp 0.8s ease forwards; }
.card { animation: slideUp 0.8s ease forwards; opacity: 0; }
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }

/* Floating legal icons */
.floating-icon {
  position: fixed; font-size: 3rem; opacity: 0.05; pointer-events: none; z-index: -1; animation: float 20s ease-in-out infinite;
}
.floating-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.floating-icon:nth-child(2) { top: 60%; right: 15%; animation-delay: 5s; }
.floating-icon:nth-child(3) { bottom: 20%; left: 20%; animation-delay: 10s; }
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-20px) rotate(5deg); }
  50% { transform: translateY(0) rotate(0deg); }
  75% { transform: translateY(20px) rotate(-5deg); }
}
"""

html = re.sub(r'<style>.*?</style>', f'<style>\n{new_css}\n</style>', html, flags=re.DOTALL)
with open('frontend.html', 'w', encoding='utf-8') as f:
    f.write(html)
