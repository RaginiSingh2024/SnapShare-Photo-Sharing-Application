"""
themes.py — Premium SnapShare Design System
CSS-variable-based theming: one palette swap = entire UI switches.
"""

# ─────────────────────────────────────────────────────────────────────────────
# ANIMATIONS
# ─────────────────────────────────────────────────────────────────────────────
_ANIMATIONS = """
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-18px); }
    to   { opacity: 1; transform: translateX(0);     }
}
@keyframes gradientShift {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0   rgba(139, 92, 246, 0.45); }
    50%       { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0);   }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px);  }
    50%       { transform: translateY(-6px); }
}
@keyframes spin-slow {
    from { transform: rotate(0deg);   }
    to   { transform: rotate(360deg); }
}
"""

# ─────────────────────────────────────────────────────────────────────────────
# SHARED CSS  (uses only CSS variables — works for both themes)
# ─────────────────────────────────────────────────────────────────────────────
_SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* ══ Global reset & font ══════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* ══ App background ══════════════════════════════════════════════ */
.stApp,
[data-testid="stAppViewContainer"] {
    background: var(--ss-bg) !important;
    color: var(--ss-text-1) !important;
    min-height: 100vh;
}

/* Ambient gradient orb behind content */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -20vh;
    left: -10vw;
    width: 60vw;
    height: 60vh;
    background: radial-gradient(ellipse, rgba(139,92,246,0.10) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -15vh;
    right: -10vw;
    width: 50vw;
    height: 50vh;
    background: radial-gradient(ellipse, rgba(236,72,153,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ══ Sidebar ══════════════════════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: var(--ss-sidebar) !important;
    border-right: 1px solid var(--ss-border) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
}
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
    padding-top: 0 !important;
}
[data-testid="stSidebarCollapseButton"] {
    background: var(--ss-collapse-bg) !important;
    border: 1px solid var(--ss-collapse-border) !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 20px rgba(91,95,214,0.18) !important;
    overflow: visible !important;
}
[data-testid="stSidebarCollapseButton"] button {
    background: var(--ss-collapse-bg) !important;
    color: var(--ss-collapse-fg) !important;
    border: 1px solid var(--ss-collapse-border) !important;
    border-radius: 14px !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    padding: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 8px 20px rgba(91,95,214,0.18) !important;
}
[data-testid="stSidebarCollapseButton"] button[data-testid="stBaseButton-headerNoPadding"] {
    background: var(--ss-collapse-bg) !important;
    color: var(--ss-collapse-fg) !important;
    border: 1px solid var(--ss-collapse-border) !important;
    border-radius: 14px !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    padding: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] button[data-testid="stBaseButton-headerNoPadding"] span,
[data-testid="stSidebarCollapseButton"] button[data-testid="stBaseButton-headerNoPadding"] svg,
[data-testid="stSidebarCollapseButton"] button[data-testid="stBaseButton-headerNoPadding"] [data-testid="stIconMaterial"] {
    color: var(--ss-collapse-fg) !important;
    fill: var(--ss-collapse-fg) !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] button span {
    color: var(--ss-collapse-fg) !important;
    fill: var(--ss-collapse-fg) !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] button:hover {
    background: var(--ss-collapse-hover) !important;
}
[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
    color: var(--ss-collapse-fg) !important;
    fill: var(--ss-collapse-fg) !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] svg {
    fill: var(--ss-collapse-fg) !important;
    color: var(--ss-collapse-fg) !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stSidebarCollapsedControl"] button:hover,
[data-testid="stSidebarExpandedControl"] button:hover {
    background: var(--ss-collapse-hover) !important;
    border-color: var(--ss-collapse-border) !important;
}
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarExpandedControl"],
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarExpandedControl"] button,
[data-testid="stSidebarCollapsedControl"] button[data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebarExpandedControl"] button[data-testid="stBaseButton-headerNoPadding"] {
    background: var(--ss-collapse-bg) !important;
    color: var(--ss-collapse-fg) !important;
    border: 1px solid var(--ss-collapse-border) !important;
    border-radius: 14px !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    box-shadow: 0 8px 20px rgba(91,95,214,0.18) !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarExpandedControl"] svg,
[data-testid="stSidebarCollapsedControl"] span,
[data-testid="stSidebarExpandedControl"] span,
[data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"],
[data-testid="stSidebarExpandedControl"] [data-testid="stIconMaterial"] {
    color: var(--ss-collapse-fg) !important;
    fill: var(--ss-collapse-fg) !important;
    opacity: 1 !important;
}

/* ══ Header bar ══════════════════════════════════════════════════ */
[data-testid="stHeader"] {
    background: var(--ss-sidebar) !important;
    border-bottom: 1px solid var(--ss-border) !important;
}
[data-testid="stHeader"] button {
    color: var(--ss-text-1) !important;
}

/* ══ Scrollbar ═══════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--ss-border-strong);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #8b5cf6, #ec4899);
}

/* ══ Typography ══════════════════════════════════════════════════ */
.stApp {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}
h1, h2, h3, h4, h5, h6 { color: var(--ss-text-1) !important; }
p, li, span             { color: var(--ss-text-2); }

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--ss-text-1) !important;
    letter-spacing: -0.02em;
}
.stMarkdown p, .stMarkdown li { color: var(--ss-text-2) !important; }
.stCaption, [data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] {
    color: var(--ss-text-3) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
label[data-testid="stWidgetLabel"] {
    color: var(--ss-text-2) !important;
    font-weight: 600 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p {
    color: var(--ss-text-2) !important;
}

/* ══ Gradient text (brand) ═══════════════════════════════════════ */
.gradient-text {
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb923c 100%);
    background-size: 200% 200%;
    animation: gradientShift 4s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
    letter-spacing: -0.03em;
}

/* ══ Glassmorphism card ══════════════════════════════════════════ */
.glass-card {
    background: var(--ss-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--ss-border);
    border-radius: 24px;
    padding: 28px 32px;
    box-shadow: var(--ss-shadow-lg), inset 0 1px 0 rgba(255,255,255,0.06);
    margin-bottom: 20px;
    animation: fadeInUp 0.4s ease both;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--ss-shadow-xl), inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ══ Post card ════════════════════════════════════════════════════ */
.post-card {
    background: var(--ss-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--ss-border);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: var(--ss-shadow-md);
    animation: fadeInUp 0.35s ease both;
    transition: transform 0.2s ease;
}
.post-card:hover { transform: translateY(-1px); }

/* ══ Hero sections ═══════════════════════════════════════════════ */
.hero-section {
    text-align: center;
    padding: 60px 20px 48px;
    animation: fadeIn 0.5s ease both;
}
.hero-badge {
    display: inline-block;
    background: var(--ss-badge-bg);
    color: #a78bfa;
    border: 1px solid rgba(139,92,246,0.35);
    border-radius: 100px;
    padding: 5px 16px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-size: clamp(3rem, 8vw, 5.5rem);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.04em;
    margin-bottom: 18px;
}
.hero-sub {
    font-size: 1.15rem;
    color: var(--ss-text-2);
    max-width: 560px;
    margin: 0 auto 36px;
    line-height: 1.65;
}

/* ══ Stat chip ═══════════════════════════════════════════════════ */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--ss-badge-bg);
    border: 1px solid var(--ss-border);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--ss-text-1);
}
.stat-chip .stat-num {
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    font-size: 1rem;
}

/* ══ Feature card (grid items) ════════════════════════════════════ */
.feature-card {
    background: var(--ss-card);
    border: 1px solid var(--ss-border);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    animation: fadeInUp 0.4s ease both;
    height: 100%;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(139,92,246,0.18);
    border-color: rgba(139,92,246,0.4);
}
.feature-icon {
    font-size: 2.2rem;
    margin-bottom: 12px;
    display: block;
    animation: float 3s ease-in-out infinite;
}
.feature-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--ss-text-1);
    margin-bottom: 6px;
}
.feature-desc {
    font-size: 0.82rem;
    color: var(--ss-text-3);
    line-height: 1.55;
}

/* ══ Auth card ════════════════════════════════════════════════════ */
.auth-card {
    background: var(--ss-card);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--ss-border);
    border-radius: 28px;
    padding: 40px 44px;
    box-shadow: var(--ss-shadow-xl), 0 0 0 1px rgba(139,92,246,0.06) inset;
    animation: fadeInUp 0.45s ease both;
    position: relative;
    overflow: hidden;
}
.auth-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(139,92,246,0.12), transparent 70%);
    pointer-events: none;
}
.auth-logo {
    text-align: center;
    margin-bottom: 28px;
}
.auth-logo span {
    font-size: 2.4rem;
    font-weight: 900;
}

/* ══ Sidebar navigation pills ════════════════════════════════════ */
[data-testid="stSidebar"] .stRadio > label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: var(--ss-text-3) !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 4px;
    padding-left: 4px;
}
[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebar"] .stRadio > div > label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    color: var(--ss-text-2) !important;
    transition: all 0.18s ease !important;
    border: 1px solid transparent !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--ss-nav-hover) !important;
    color: var(--ss-text-1) !important;
    border-color: var(--ss-border) !important;
}
[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] {
    background: var(--ss-nav-active) !important;
    color: #ffffff !important;
    border-color: rgba(139,92,246,0.4) !important;
    box-shadow: 0 4px 14px rgba(139,92,246,0.20) !important;
}

/* ══ Buttons ══════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 40%, #ec4899 100%) !important;
    background-size: 200% 200% !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em !important;
    padding: 10px 20px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 16px rgba(139,92,246,0.30) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button p,
.stButton > button span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.12), transparent);
    border-radius: 14px;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(139,92,246,0.45), 0 4px 14px rgba(236,72,153,0.25) !important;
    background-position: right center !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ══ Inputs & Forms ══════════════════════════════════════════════ */
[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFormSubmitButton"] small {
    display: none !important;
}

[data-testid="InputInstructions"] {
    display: none !important;
}

[data-testid="InputInstructions"] span {
    display: none !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
[data-testid="stForm"] .stTextInput > div > div > input,
[data-testid="stForm"] .stTextArea > div > div > textarea {

    background: var(--ss-input) !important;
    border: 1.5px solid var(--ss-border) !important;
    border-radius: 12px !important;

    color: var(--ss-text-1) !important;
    -webkit-text-fill-color: var(--ss-text-1) !important;

    font-size: 0.9rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
[data-testid="stForm"] input::placeholder,
[data-testid="stForm"] textarea::placeholder {
    color: var(--ss-placeholder) !important;
    opacity: 1 !important;
    font-weight: 500 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
    outline: none !important;
}
.stTextInput > label, .stTextArea > label,
.stFileUploader > label, .stSelectbox > label,
[data-testid="stForm"] label {
    color: var(--ss-text-2) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: var(--ss-text-2) !important;
}

/* ══ File uploader ════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: var(--ss-input) !important;
    border: 2px dashed var(--ss-border-strong) !important;
    border-radius: 16px !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(139,92,246,0.55) !important;
    background: rgba(139,92,246,0.04) !important;
}
[data-testid="stFileUploadDropzone"] p { color: var(--ss-text-3) !important; }

/* ══ Containers (st.container(border=True)) ══════════════════════ */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--ss-card) !important;
    border: 1px solid var(--ss-border) !important;
    border-radius: 20px !important;
    animation: fadeInUp 0.35s ease both !important;
}

/* ══ Metrics ══════════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: var(--ss-card) !important;
    border: 1px solid var(--ss-border) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    transition: transform 0.2s ease !important;
}
[data-testid="stMetric"]:hover { transform: translateY(-2px) !important; }
[data-testid="stMetricLabel"] > div {
    color: var(--ss-text-3) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] > div {
    color: var(--ss-text-1) !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
}

/* ══ Expander ══════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: var(--ss-card) !important;
    border: 1px solid var(--ss-border) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    color: var(--ss-text-2) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 12px 16px !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--ss-text-1) !important;
    background: var(--ss-nav-hover) !important;
}

/* ══ Divider ══════════════════════════════════════════════════════ */
hr { border: none !important; border-top: 1px solid var(--ss-border) !important; }

/* ══ Alerts ════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid var(--ss-border) !important;
}
[data-testid="stNotification"] {
    color: var(--ss-text-1) !important;
}

/* ══ Main content block ═══════════════════════════════════════════ */
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}
[data-testid="stAppViewBlockContainer"] {
    background: transparent !important;
    color: var(--ss-text-1) !important;
}

/* ══ Avatar (always accent gradient) ════════════════════════════ */
.user-avatar-small {
    width: 42px; height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    color: #fff; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    border: 2px solid var(--ss-avatar-ring);
    box-shadow: 0 3px 12px rgba(139,92,246,0.30);
    flex-shrink: 0;
}
.user-avatar-large {
    width: 96px; height: 96px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    color: #fff; font-weight: 900;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.5rem;
    border: 3px solid var(--ss-avatar-ring);
    box-shadow: 0 8px 32px rgba(139,92,246,0.35), 0 0 0 6px var(--ss-avatar-glow);
    animation: pulseGlow 3s ease-in-out infinite;
}

/* ══ Notification item ════════════════════════════════════════════ */
.notification-item {
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    transition: background 0.18s ease, transform 0.18s ease;
    animation: slideInLeft 0.3s ease both;
}
.notification-item:hover {
    background: var(--ss-nav-hover) !important;
    transform: translateX(4px);
}

/* ══ Feed header ════════════════════════════════════════════════ */
.feed-header {
    background: var(--ss-card);
    border: 1px solid var(--ss-border);
    border-radius: 18px;
    padding: 18px 24px;
    margin-bottom: 24px;
    animation: fadeIn 0.3s ease both;
}

/* ══ Info pills & badges ════════════════════════════════════════ */
.tech-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--ss-badge-bg);
    border: 1px solid var(--ss-border);
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--ss-text-2);
    margin: 3px;
}

/* ══ Radio & sidebar typography ════════════════════════════════ */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }

/* ══ Page animation wrapper ════════════════════════════════════ */
.page-enter { animation: fadeInUp 0.4s ease both; }

/* ══ Sidebar user card ════════════════════════════════════════ */
.sidebar-user-card {
    background: var(--ss-card);
    border: 1px solid var(--ss-border);
    border-radius: 16px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 12px 0;
}
.sidebar-user-name {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--ss-text-1);
}
.sidebar-user-handle {
    font-size: 0.77rem;
    color: var(--ss-text-3);
    font-weight: 600;
}

/* ══ Sidebar brand ════════════════════════════════════════════ */
.sidebar-brand-wrap {
    padding: 22px 16px 12px;
    text-align: center;
    border-bottom: 1px solid var(--ss-border);
    margin-bottom: 8px;
}
.sidebar-tagline {
    font-size: 0.72rem;
    color: var(--ss-text-3);
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 4px;
}
.hero-sub {
    color: var(--ss-text-2) !important;
    font-weight: 500;
}
.feature-desc {
    color: var(--ss-text-3) !important;
    font-weight: 500;
}
.profile-stat-label {
    color: var(--ss-stat-label) !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em;
}
.settings-section-label {
    color: var(--ss-stat-label) !important;
    font-weight: 700 !important;
    letter-spacing: 0.07em;
}

/* ══ Architecture pipeline steps ════════════════════════════ */
.pipeline-step {
    background: var(--ss-card);
    border: 1px solid var(--ss-border);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
    animation: slideInLeft 0.35s ease both;
    transition: border-color 0.2s;
}
.pipeline-step:hover { border-color: rgba(139,92,246,0.4); }
.pipeline-num {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 800;
    flex-shrink: 0;
}
.pipeline-text { font-size: 0.87rem; color: var(--ss-text-2); font-weight: 500; }

/* ══ Post action bar ════════════════════════════════════════ */
.post-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
}

/* ══ Smooth global transitions ═════════════════════════════ */
.stApp, [data-testid="stSidebar"], .glass-card, .post-card,
[data-testid="stMetric"], [data-testid="stExpander"],
[data-testid="stVerticalBlockBorderWrapper"] {
    transition: background 0.28s ease, border-color 0.28s ease, color 0.18s ease;
}
"""

# ─────────────────────────────────────────────────────────────────────────────
# DARK PALETTE
# ─────────────────────────────────────────────────────────────────────────────
_DARK_VARS = """
:root {
    --ss-bg:            #07091A;
    --ss-sidebar:       rgba(8, 10, 22, 0.96);
    --ss-card:          rgba(14, 18, 38, 0.78);
    --ss-input:         rgba(255,255,255,0.04);
    --ss-border:        rgba(139,92,246,0.14);
    --ss-border-strong: rgba(139,92,246,0.28);
    --ss-nav-hover:     rgba(139,92,246,0.10);
    --ss-nav-active:    rgba(139,92,246,0.20);
    --ss-badge-bg:      rgba(139,92,246,0.10);
    --ss-text-2: #D1D9EC;
    --ss-text-3: #A3B4D5;
    --ss-text-3:        #8E9CB8;
    --ss-placeholder:   #7A8AAE; 
    --ss-stat-label:    #9AABC8;
    --ss-avatar-ring:   rgba(139,92,246,0.55);
    --ss-avatar-glow:   rgba(139,92,246,0.08);
    --ss-shadow-md:     0 6px 24px rgba(0,0,0,0.45);
    --ss-shadow-lg:     0 12px 40px rgba(0,0,0,0.55), 0 0 0 1px rgba(139,92,246,0.07);
    --ss-shadow-xl:     0 24px 64px rgba(0,0,0,0.65), 0 0 0 1px rgba(139,92,246,0.10);
    --ss-collapse-bg:   #5B5FD6;
    --ss-collapse-fg:   #FFFFFF;
    --ss-collapse-border: rgba(91,95,214,0.35);
    --ss-collapse-hover: #4E52C8;
    --ss-auth-title:    #F2F4FF;
    --ss-auth-subtitle: #B4BFD8;
    --ss-auth-label:    #A8B6D4;
}

/* Dark-specific Streamlit widget overrides */
[data-testid="stAppViewContainer"] .stTextInput > div > div > input,
[data-testid="stAppViewContainer"] .stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    color: #F2F4FF !important;
    -webkit-text-fill-color: #F2F4FF !important;
}
[data-testid="stAppViewContainer"] .stTextInput > div > div > input::placeholder,
[data-testid="stAppViewContainer"] .stTextArea > div > div > textarea::placeholder {
    color: var(--ss-placeholder) !important;
    opacity: 1 !important;
}
[data-testid="stMetricLabel"] > div {
    color: var(--ss-stat-label) !important;
    font-weight: 700 !important;
}
[data-testid="stMetricValue"] > div {
    color: var(--ss-text-1) !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(14, 18, 38, 0.78) !important;
}

"""

# ─────────────────────────────────────────────────────────────────────────────
# LIGHT PALETTE
# ─────────────────────────────────────────────────────────────────────────────
_LIGHT_VARS = """
:root {
    --ss-bg:            #F4F2FF;
    --ss-sidebar:       rgba(255,255,255,0.96);
    --ss-card:          rgba(255,255,255,0.88);
    --ss-input:         rgba(0,0,0,0.033);
    --ss-border:        rgba(139,92,246,0.16);
    --ss-border-strong: rgba(139,92,246,0.32);
    --ss-nav-hover:     rgba(139,92,246,0.08);
    --ss-nav-active:    rgba(139,92,246,0.15);
    --ss-badge-bg:      rgba(139,92,246,0.08);
    --ss-text-1:        #0A0C18;
    --ss-text-2:        #2C3452;
    --ss-text-3:        #464F6E;
    --ss-placeholder:   #5A6380;
    --ss-stat-label:    #3A4262;
    --ss-avatar-ring:   rgba(139,92,246,0.45);
    --ss-avatar-glow:   rgba(139,92,246,0.07);
    --ss-shadow-md:     0 4px 16px rgba(139,92,246,0.08);
    --ss-shadow-lg:     0 10px 32px rgba(139,92,246,0.10), 0 0 0 1px rgba(139,92,246,0.06);
    --ss-shadow-xl:     0 20px 56px rgba(139,92,246,0.12), 0 0 0 1px rgba(139,92,246,0.08);
    --ss-collapse-bg:   #0C0E1A;
    --ss-collapse-fg:   #FFFFFF;
    --ss-collapse-border: rgba(12,14,26,0.24);
    --ss-collapse-hover: rgba(12,14,26,0.82);
    --ss-auth-title:    #4A52D4;
    --ss-auth-subtitle: #383F5C;
    --ss-auth-label:    #383F5C;
}

/* Light-specific overrides */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: #F4F2FF !important;
    color: var(--ss-text-1) !important;
}
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: rgba(255,255,255,0.96) !important;
}
[data-testid="stSidebar"] .sidebar-brand-wrap,
[data-testid="stSidebar"] .sidebar-user-name,
[data-testid="stSidebar"] .stRadio > div > label {
    color: var(--ss-text-1) !important;
}
[data-testid="stSidebar"] .sidebar-tagline,
[data-testid="stSidebar"] .sidebar-user-handle,
[data-testid="stSidebar"] .stRadio > label {
    color: var(--ss-text-3) !important;
}
[data-testid="stHeader"] {
    background: rgba(255,255,255,0.96) !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
[data-testid="stForm"] input,
[data-testid="stForm"] textarea {
    background: #FFFFFF !important;
    color: var(--ss-text-1) !important;
    border-color: rgba(139,92,246,0.22) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
[data-testid="stForm"] input::placeholder,
[data-testid="stForm"] textarea::placeholder {
    color: var(--ss-placeholder) !important;
    opacity: 1 !important;
}
.glass-card,
.post-card,
.feature-card,
.auth-card,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMetric"],
[data-testid="stExpander"],
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.92) !important;
}
[data-testid="stMetricLabel"] > div {
    color: var(--ss-stat-label) !important;
    font-weight: 700 !important;
}
[data-testid="stMetricValue"] > div {
    color: var(--ss-text-1) !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(139,92,246,0.08) !important;
    color: var(--ss-text-1) !important;
}
[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] {
    color: #FFFFFF !important;
}
.auth-card .stMarkdown p,
.auth-card .stMarkdown span,
.auth-card .stTextInput > label,
.auth-card .stTextArea > label,
.auth-card .stFileUploader > label,
.auth-card .stSelectbox > label,
.auth-card [data-testid="stWidgetLabel"] p {
    color: var(--ss-auth-label) !important;
    font-weight: 600 !important;
}
.auth-card .auth-title {
    color: var(--ss-auth-title) !important;
}
.auth-card .auth-subtitle {
    color: var(--ss-auth-subtitle) !important;
    font-weight: 500 !important;
}
.hero-sub,
.stMarkdown p,
.stMarkdown li {
    color: var(--ss-text-2) !important;
}
[data-testid="stFileUploadDropzone"] p,
[data-testid="stFileUploadDropzone"] span {
    color: var(--ss-text-3) !important;
    font-weight: 500 !important;
}
"""


def get_theme_css(theme: str = "dark") -> str:
    """Returns the full <style> block for the chosen theme."""
    palette = _DARK_VARS if theme == "dark" else _LIGHT_VARS
    return f"<style>{palette}{_ANIMATIONS}{_SHARED_CSS}</style>"
