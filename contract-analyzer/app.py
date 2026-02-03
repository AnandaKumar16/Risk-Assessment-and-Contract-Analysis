# """
# Legal Contract Analysis Assistant - Streamlit Web Application
# GenAI-powered tool for SME contract analysis
# """

# import streamlit as st
# import sys
# from pathlib import Path
# from datetime import datetime
# import html
# import re
# from collections import Counter

# import plotly.graph_objects as go

# # Add modules to path
# sys.path.append(str(Path(__file__).parent / 'modules'))

# from modules.parser import DocumentParser
# from modules.analyzer import ContractAnalyzer
# from modules.risk_scorer import RiskScorer
# from modules.report_generator import ReportGenerator


# # Page configuration
# st.set_page_config(
#     page_title="Legal Contract Analyzer for SMEs",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     :root {
#         --navy: #0B1F3A;
#         --navy-700: #0F2E55;
#         --slate: #475467;
#         --muted: #667085;
#         --bg: #F8FAFC;
#         --card: #FFFFFF;
#         --border: #E2E8F0;
#         --shadow: 0 10px 30px rgba(16, 24, 40, 0.08);
#         --green: #16A34A;
#         --amber: #F59E0B;
#         --red: #EF4444;
#         --blue: #2563EB;
#         --soft-blue: #EAF2FF;
#     }

#     .stApp {
#         background: var(--bg);
#         color: var(--slate);
#         background-image:
#             repeating-linear-gradient(
#                 -30deg,
#                 rgba(15, 23, 42, 0.04) 0px,
#                 rgba(15, 23, 42, 0.04) 40px,
#                 rgba(15, 23, 42, 0.0) 40px,
#                 rgba(15, 23, 42, 0.0) 120px
#             ),
#             repeating-linear-gradient(
#                 0deg,
#                 rgba(15, 23, 42, 0.035) 0px,
#                 rgba(15, 23, 42, 0.035) 1px,
#                 transparent 1px,
#                 transparent 60px
#             );
#         background-attachment: fixed;
#     }

#     .confidential-watermark {
#         position: fixed;
#         inset: 0;
#         pointer-events: none;
#         z-index: 0;
#         opacity: 0.06;
#         font-weight: 800;
#         font-size: 56px;
#         letter-spacing: 6px;
#         color: #0F172A;
#         transform: rotate(-24deg);
#         display: grid;
#         place-items: center;
#         text-transform: uppercase;
#         mix-blend-mode: multiply;
#     }

#     .confidential-watermark::before {
#         content: "CONFIDENTIAL";
#         display: block;
#         width: 200%;
#         text-align: center;
#         white-space: nowrap;
#         line-height: 6;
#         letter-spacing: 12px;
#     }

#     .main-header {
#         font-size: 2.6rem;
#         font-weight: 700;
#         color: var(--navy);
#         text-align: center;
#         letter-spacing: -0.5px;
#         margin-bottom: 0.5rem;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 0.75rem;
#     }

#     .wax-seal {
#         width: 44px;
#         height: 44px;
#         border-radius: 50%;
#         background:
#             radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.05) 35%, transparent 36%),
#             radial-gradient(circle at 70% 70%, rgba(0, 0, 0, 0.25), transparent 40%),
#             radial-gradient(circle, #b91c1c 0%, #9b1c1c 60%, #7f1d1d 100%);
#         box-shadow:
#             inset 0 2px 4px rgba(255, 255, 255, 0.35),
#             inset 0 -4px 6px rgba(0, 0, 0, 0.35),
#             0 6px 14px rgba(127, 29, 29, 0.3);
#         position: relative;
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#         flex: 0 0 auto;
#     }

#     .wax-seal::after {
#         content: "SEAL";
#         font-size: 0.55rem;
#         font-weight: 800;
#         color: rgba(255, 255, 255, 0.9);
#         letter-spacing: 1px;
#         text-shadow: 0 1px 2px rgba(0, 0, 0, 0.45);
#     }

#     .sub-header {
#         font-size: 1.05rem;
#         color: var(--muted);
#         text-align: center;
#         margin-bottom: 1.5rem;
#     }

#     .section-title {
#         font-size: 1.35rem;
#         font-weight: 700;
#         color: var(--navy);
#         margin: 1rem 0 0.75rem;
#     }

#     .card {
#         background: var(--card);
#         border: 1px solid var(--border);
#         border-radius: 16px;
#         box-shadow: 0 2px 8px rgba(16, 24, 40, 0.06);
#         padding: 1.25rem;
#         display: flex;
#         flex-direction: column;
#         height: 100%;
#     }

#     .card:hover {
#         box-shadow: 0 8px 16px rgba(16, 24, 40, 0.10);
#         transition: box-shadow 0.2s ease;
#     }

#     .card-compact {
#         background: var(--card);
#         border: 1px solid var(--border);
#         border-radius: 14px;
#         padding: 1rem 1.1rem;
#         display: flex;
#         flex-direction: column;
#         height: 100%;
#         box-shadow: 0 2px 8px rgba(16, 24, 40, 0.06);
#     }

#     .upload-card {
#         background: linear-gradient(135deg, #FFFFFF 0%, #F5F8FF 100%);
#         border: 1px dashed #94A3B8;
#         border-radius: 18px;
#         padding: 2rem;
#         text-align: center;
#     }

#     .upload-zone [data-testid="stFileUploader"] {
#         width: 100%;
#     }

#     .upload-zone [data-testid="stFileUploader"] > div {
#         border: 1px dashed #94A3B8;
#         border-radius: 18px;
#         padding: 2.2rem 1.5rem;
#         min-height: 220px;
#         background: linear-gradient(135deg, #FFFFFF 0%, #F5F8FF 100%);
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         text-align: center;
#         box-shadow: var(--shadow);
#     }

#     .upload-zone [data-testid="stFileUploader"] section {
#         width: 100%;
#     }

#     .upload-zone [data-testid="stFileUploader"] button {
#         margin: 0 auto;
#         border-radius: 10px;
#     }

#     .upload-hint {
#         margin-top: 0.5rem;
#         color: var(--muted);
#         font-size: 0.9rem;
#     }

#     .badge {
#         display: inline-flex;
#         align-items: center;
#         gap: 0.4rem;
#         padding: 0.25rem 0.6rem;
#         border-radius: 999px;
#         font-size: 0.8rem;
#         font-weight: 600;
#         background: var(--soft-blue);
#         color: var(--blue);
#         border: 1px solid #C7DBFF;
#     }

#     .trust-badge {
#         background: #ECFDF3;
#         color: #027A48;
#         border: 1px solid #ABEFC6;
#     }

#     .risk-tag {
#         display: inline-flex;
#         align-items: center;
#         padding: 0.25rem 0.55rem;
#         border-radius: 999px;
#         font-size: 0.78rem;
#         font-weight: 600;
#     }

#     .risk-tag.low { background: #ECFDF3; color: #027A48; border: 1px solid #ABEFC6; }
#     .risk-tag.medium { background: #FFFAEB; color: #B54708; border: 1px solid #FEC84B; }
#     .risk-tag.high { background: #FEF3F2; color: #B42318; border: 1px solid #FECDCA; }

#     .metric-card {
#         background: var(--card);
#         border: 1px solid var(--border);
#         border-radius: 16px;
#         text-align: left;
#         padding: 1.25rem;
#         box-shadow: 0 2px 8px rgba(16, 24, 40, 0.06);
#         display: flex;
#         flex-direction: column;
#         height: 100%;
#     }

#     .metrics-card {
#         background: var(--card);
#         border: 1px solid var(--border);
#         border-radius: 18px;
#         padding: 1.25rem;
#         box-shadow: 0 2px 8px rgba(16, 24, 40, 0.06);
#     }

#     .metrics-grid {
#         display: grid;
#         grid-template-columns: repeat(4, minmax(0, 1fr));
#         gap: 1rem;
#         width: 100%;
#     }

#     .metric-item {
#         background: #F8FAFF;
#         border: 1px solid #E5E7EB;
#         border-radius: 14px;
#         padding: 1rem 1.1rem;
#         display: flex;
#         flex-direction: column;
#         gap: 0.5rem;
#     }

#     .metric-label {
#         font-size: 0.8rem;
#         color: var(--muted);
#         margin-bottom: 0.35rem;
#     }

#     .metric-value {
#         font-size: 1.15rem;
#         font-weight: 700;
#         color: var(--navy);
#     }

#     .disclaimer-box {
#         background-color: #FFFBEB;
#         padding: 0.9rem 1rem;
#         border: 1px solid #FDE68A;
#         border-radius: 12px;
#         margin: 1rem 0;
#         color: #92400E;
#     }

#     .risk-high {
#         background-color: #FEF3F2;
#         padding: 1rem;
#         border-left: 4px solid #EF4444;
#         border-radius: 12px;
#         margin: 0.6rem 0;
#     }
#     .risk-medium {
#         background-color: #FFFAEB;
#         padding: 1rem;
#         border-left: 4px solid #F59E0B;
#         border-radius: 12px;
#         margin: 0.6rem 0;
#     }
#     .risk-low {
#         background-color: #ECFDF3;
#         padding: 1rem;
#         border-left: 4px solid #16A34A;
#         border-radius: 12px;
#         margin: 0.6rem 0;
#     }

#     .legal-text {
#         color: #334155;
#         font-size: 0.92rem;
#         line-height: 1.55;
#     }

#     .explain-text {
#         color: #0F172A;
#         font-weight: 600;
#         font-size: 0.95rem;
#         line-height: 1.55;
#     }

#     .inline-highlight {
#         background: #FCD34D;
#         padding: 2px 4px;
#         border-radius: 4px;
#         color: #92400E;
#         font-weight: 600;
#     }

#     .pill-row {
#         display: flex;
#         flex-wrap: wrap;
#         gap: 0.35rem;
#         margin: 0.5rem 0;
#     }

#     .pill {
#         border: 1px solid var(--border);
#         background: #F1F5F9;
#         padding: 0.15rem 0.5rem;
#         border-radius: 999px;
#         font-size: 0.72rem;
#         color: #475467;
#     }

#     .risk-gauge {
#         width: 240px;
#         height: 130px;
#         position: relative;
#         margin: 0 auto;
#     }

#     .risk-gauge-needle {
#         transition: transform 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94);
#     }

#     .risk-gauge-labels {
#         display: flex;
#         justify-content: space-between;
#         font-size: 0.7rem;
#         color: #64748B;
#         margin-top: 0.5rem;
#         width: 100%;
#     }

#     .risk-gauge-score {
#         font-size: 1.1rem;
#         font-weight: 700;
#         color: var(--navy);
#         text-align: center;
#         margin-top: 0.35rem;
#     }

#     .risk-gauge-caption {
#         font-size: 0.85rem;
#         color: var(--muted);
#         text-align: center;
#         margin-top: 0.2rem;
#     }

#     .two-col {
#         display: grid;
#         grid-template-columns: 1fr 1fr;
#         gap: 1rem;
#         align-items: stretch;
#     }

#     .sticky-note {
#         background: #F8FAFF;
#         border: 1px solid #DDE7FF;
#         border-radius: 12px;
#         padding: 0.75rem 0.9rem;
#         color: #1D4ED8;
#         font-size: 0.85rem;
#     }

#     .cta-row {
#         display: flex;
#         gap: 0.75rem;
#         flex-wrap: wrap;
#         margin-top: 0.5rem;
#     }

#     .cta-card {
#         border: 1px solid var(--border);
#         border-radius: 14px;
#         padding: 1rem 1.1rem;
#         background: var(--card);
#         box-shadow: 0 2px 8px rgba(16, 24, 40, 0.06);
#         display: flex;
#         flex-direction: column;
#         height: 100%;
#     }

#     .small-muted {
#         color: var(--muted);
#         font-size: 0.82rem;
#     }

#     .warning-box {
#         background-color: #FFFAEB;
#         padding: 0.9rem 1rem;
#         border: 1px solid #FEC84B;
#         border-left: 4px solid #F59E0B;
#         border-radius: 8px;
#         margin: 0.6rem 0;
#         color: #92400E;
#         font-size: 0.92rem;
#         line-height: 1.55;
#     }

#     /* Warning tape marquee */
#     .warning-tape {
#         position: relative;
#         overflow: hidden;
#         border-radius: 0;
#         border: 1px solid #FACC15;
#         background: repeating-linear-gradient(
#             -45deg,
#             #FDE047 0px,
#             #FDE047 14px,
#             #111827 14px,
#             #111827 28px
#         );
#         box-shadow: 0 6px 16px rgba(16, 24, 40, 0.12);
#         padding: 12px 0;
#         width: 100vw;
#         margin-left: calc(50% - 50vw);
#         margin-right: calc(50% - 50vw);
#     }

#     .warning-tape-inner {
#         display: flex;
#         width: max-content;
#         animation: marquee 36s linear infinite;
#         will-change: transform;
#     }

#     .warning-tape-track {
#         display: flex;
#         white-space: nowrap;
#         gap: 2.5rem;
#         padding-right: 2.5rem;
#         font-weight: 700;
#         color: #FFFFFF;
#         text-transform: uppercase;
#         letter-spacing: 0.4px;
#         font-size: 0.9rem;
#     }

#     .warning-tape-text {
#         padding: 0.2rem 0.75rem;
#         background: rgba(17, 24, 39, 0.92);
#         border: 1px solid rgba(253, 224, 71, 0.65);
#         text-shadow: 0 1px 2px rgba(0, 0, 0, 0.45);
#         color: #FFFFFF;
#         letter-spacing: 0.6px;
#     }

#     @keyframes marquee {
#         0% { transform: translateX(0); }
#         100% { transform: translateX(-50%); }
#     }

#     /* Tabs (Navigation) */
#     [data-baseweb="tab"] {
#         color: #0B1F3A !important;
#         font-weight: 600;
#         font-size: 0.95rem;
#     }

#     [data-baseweb="tab"][aria-selected="true"] {
#         color: #0B1F3A !important;
#     }

#     [data-baseweb="tab"]:hover {
#         color: #0F2E55 !important;
#     }

#     [data-baseweb="tab-list"] {
#         border-bottom: 1px solid #E2E8F0;
#     }
# </style>
# """, unsafe_allow_html=True)


# def initialize_session_state():
#     """Initialize session state variables."""
#     if 'analysis_complete' not in st.session_state:
#         st.session_state.analysis_complete = False
#     if 'report' not in st.session_state:
#         st.session_state.report = None
#     if 'parsed_data' not in st.session_state:
#         st.session_state.parsed_data = None
#     if 'spacy_nlp' not in st.session_state:
#         # Load spaCy model for NLP preprocessing
#         st.session_state.spacy_nlp = _load_spacy_model()


# def render_badge(text: str, kind: str = "default") -> str:
#     """Render a styled badge."""
#     if kind == "trust":
#         return f"<span class='badge trust-badge'>🔒 {html.escape(text)}</span>"
#     elif kind == "warning":
#         return f"<span class='badge' style='background: #FEF3F2; color: #B42318; border: 1px solid #FECDCA;'>⚠️ {html.escape(text)}</span>"
#     return f"<span class='badge'>✨ {html.escape(text)}</span>"


# def render_risk_meter(score: float, level: str) -> str:
#     """Render a large, clean risk score display."""
#     safe_score = max(0, min(int(score), 100))
#     level_text = level if level else "Unknown"
#     level_color = "#16A34A" if level_text == "Low" else "#F59E0B" if level_text == "Medium" else "#EF4444"
    
#     return (
#         '<div style="display:flex; flex-direction:column; align-items:center; gap:0.75rem; padding:0.4rem 0;">'
#         '<div style="font-size:0.9rem; font-weight:600; color:#475467; text-transform:uppercase; letter-spacing:0.5px;">Overall Risk Score</div>'
#         '<div style="font-size:3.2rem; font-weight:800; color:#0B1F3A; line-height:1;">'
#         f'{safe_score}<span style="font-size:1.2rem; font-weight:600; color:#94A3B8;">/100</span>'
#         '</div>'
#         f'<div style="font-size:1rem; font-weight:600; color:{level_color};">{html.escape(level_text)} Risk</div>'
#         '</div>'
#     )


# def highlight_risky_phrases(text: str) -> str:
#     """Highlight risky phrases in clause text."""
#     if not text:
#         return ""
#     risky_terms = [
#         "penalty", "liquidated damages", "indemnify", "indemnification", "terminate",
#         "unilateral", "without cause", "sole discretion", "auto-renewal", "lock-in",
#         "non-compete", "non solicitation", "exclusive", "assignment", "waiver",
#         "unlimited", "in perpetuity", "irrevocable", "fine", "forfeit", "breach"
#     ]
#     safe_text = html.escape(text)
#     for term in sorted(risky_terms, key=len, reverse=True):
#         pattern = re.compile(re.escape(term), re.IGNORECASE)
#         safe_text = pattern.sub(lambda m: f"<span class='inline-highlight'>{m.group(0)}</span>", safe_text)
#     return safe_text


# def clause_icons(text: str) -> str:
#     """Return icons representing clause types."""
#     t = (text or "").lower()
#     icons = []
#     if any(k in t for k in ["penalty", "liquidated damages", "fine", "forfeit"]):
#         icons.append("💸 Penalty")
#     if any(k in t for k in ["ip", "intellectual property", "assignment", "license"]):
#         icons.append("🧠 IP")
#     if any(k in t for k in ["terminate", "termination", "cancel"]):
#         icons.append("🛑 Termination")
#     if any(k in t for k in ["indemnify", "indemnification", "hold harmless"]):
#         icons.append("🛡️ Indemnity")
#     return " ".join(icons)


# def infer_jurisdiction(report: dict) -> str:
#     """Infer jurisdiction/governing law from clause text if present."""
#     clauses = report.get('clause_analysis', [])
#     pattern = re.compile(r"(governing law|jurisdiction|courts of|seat of arbitration)[:\s]+([^\.\n]+)", re.IGNORECASE)
#     for clause in clauses:
#         text = clause.get('text', '')
#         match = pattern.search(text)
#         if match:
#             return match.group(2).strip()
#     return "Not specified"


# def _clean_list_items(items, max_items=4):
#     """Normalize list strings (dedupe, trim, and present cleanly)."""
#     if not items:
#         return []
#     seen = set()
#     cleaned = []
#     for item in items:
#         value = re.sub(r"\s+", " ", str(item)).strip()
#         if not value:
#             continue
#         key = value.lower()
#         if key in seen:
#             continue
#         seen.add(key)
#         cleaned.append(value)
#     if len(cleaned) > max_items:
#         return cleaned[:max_items] + [f"and {len(cleaned) - max_items} more"]
#     return cleaned


# def _clean_jurisdiction(text: str) -> str:
#     """Clean jurisdiction text for grammar and punctuation."""
#     if not text:
#         return "Not specified"
#     value = re.sub(r"\s+", " ", text).strip()
#     value = re.sub(r"^(and\s+)?jurisdiction\s*", "", value, flags=re.IGNORECASE)
#     value = re.sub(r"^(and\s+)", "", value, flags=re.IGNORECASE)
#     if value and value[-1] not in ".!?":
#         value += "."
#     return value


# def _clean_amounts(text: str) -> str:
#     """Clean financial amounts list for consistent formatting."""
#     if not text:
#         return "Not specified"
#     tokens = re.split(r"[,|]+", text)
#     cleaned = []
#     for token in tokens:
#         value = re.sub(r"\s+", " ", token).strip()
#         value = re.sub(r"\b(rs)\b", "INR", value, flags=re.IGNORECASE)
#         value = value.replace("INR INR", "INR").strip()
#         if value and value.lower() not in {"rs", "rs.", "inr"}:
#             cleaned.append(value)
#     cleaned = _clean_list_items(cleaned, max_items=3)
#     return ", ".join(cleaned) if cleaned else "Not specified"


# def _contains_hindi(text: str) -> bool:
#     """Detect Devanagari script (Hindi) in text."""
#     if not text:
#         return False
#     return bool(re.search(r"[\u0900-\u097F]", text))


# def _translate_to_english(text: str) -> str:
#     """Translate text to English using googletrans if available."""
#     if not text:
#         return ""
#     try:
#         from googletrans import Translator
#     except Exception:
#         return text

#     translator = Translator()
#     chunk_size = 4000
#     chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
#     translated_chunks = []
#     for chunk in chunks:
#         try:
#             translated_chunks.append(translator.translate(chunk, dest="en").text)
#         except Exception:
#             translated_chunks.append(chunk)
#     return "\n".join(translated_chunks)


# def _load_spacy_model():
#     """Load spaCy English model with fallback."""
#     try:
#         import spacy
#         try:
#             nlp = spacy.load("en_core_web_sm")
#             return nlp
#         except OSError:
#             # Model not installed, attempt to download
#             import subprocess
#             import sys
#             subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
#             nlp = spacy.load("en_core_web_sm")
#             return nlp
#     except Exception as e:
#         logger_msg = f"Warning: Could not load spaCy model: {str(e)}"
#         return None


# def display_header():
#     """Display application header."""
#     st.markdown('<div class="main-header">Legal Contract Analysis Assistant</div>', unsafe_allow_html=True)
#     st.markdown('<div class="sub-header">Trusted, plain‑language contract insights for Indian SMEs</div>', unsafe_allow_html=True)
    
#     st.markdown(
#         f"<div style='text-align:center; margin-bottom:0.6rem;'>"
#         f"{render_badge('Confidential & Local Processing', 'trust')}"
#         f"</div>",
#         unsafe_allow_html=True
#     )


# def analyze_contract(uploaded_file):
#     """
#     Main analysis pipeline following the workflow:
#     1. Upload Contract
#     2. Extract Text
#     3. Detect Language
#     4. IF English → proceed to NLP preprocessing
#     5. ELSE IF Hindi → translate to English → proceed to NLP preprocessing
#     6. NLP preprocessing (spaCy/NLTK) → analysis
#     """
#     with st.spinner("🔍 Analyzing your contract..."):
        
#         # Progress bar
#         progress_bar = st.progress(0)
#         status_text = st.empty()
        
#         # Step 1: Upload & Extract Text
#         status_text.text("Step 1/5: Extracting text from document...")
#         progress_bar.progress(20)
        
#         parser = DocumentParser()
#         file_bytes = uploaded_file.read()
#         parsed_data = parser.parse_document(
#             file_bytes=file_bytes,
#             filename=uploaded_file.name
#         )
        
#         if parsed_data.get('error'):
#             st.error(f"❌ Error parsing document: {parsed_data['error']}")
#             return None
        
#         raw_text = parsed_data.get('raw_text', '')
        
#         # Step 2: Detect Language
#         status_text.text("Step 2/5: Detecting language...")
#         progress_bar.progress(35)
        
#         if _contains_hindi(raw_text):
#             detected_language = "Hindi"
#             status_text.text("Step 2/5: Language detected - Hindi. Translating to English...")
#             st.info("🌐 Hindi contract detected. Translating to English for analysis...")
#         else:
#             detected_language = "English"
        
#         parsed_data['language_detected'] = detected_language
        
#         # Step 3: Language-specific preprocessing
#         status_text.text(f"Step 3/5: Processing {detected_language} text...")
#         progress_bar.progress(45)
        
#         clean_text = parser.preprocess_text(raw_text)
        
#         # Step 4: Translate if Hindi
#         if detected_language == "Hindi":
#             status_text.text("Step 4/5: Translating Hindi to English...")
#             progress_bar.progress(55)
            
#             translated_text = _translate_to_english(clean_text)
#             if translated_text and translated_text.strip():
#                 parsed_data['original_language_text'] = clean_text
#                 parsed_data['translated_text'] = translated_text
#                 parsed_data['translation_applied'] = True
#                 clean_text = translated_text
#             else:
#                 st.warning("⚠️ Translation failed. Proceeding with original text.")
#                 parsed_data['translation_applied'] = False
#         else:
#             parsed_data['translation_applied'] = False
        
#         if not clean_text or len(clean_text) < 100:
#             st.error("❌ Document text is too short or empty. Please upload a valid contract.")
#             return None
        
#         st.session_state.parsed_data = parsed_data
        
#         # Step 5: NLP Preprocessing & Analysis
#         status_text.text("Step 5/5: Performing NLP analysis and risk assessment...")
#         progress_bar.progress(70)
        
#         analyzer = ContractAnalyzer()
#         analysis_results = analyzer.analyze_contract(clean_text)
#         analysis_results['language_detected'] = detected_language
        
#         if analysis_results.get('error'):
#             st.error(f"❌ Error analyzing contract: {analysis_results['error']}")
#             return None
        
#         # Risk scoring
#         status_text.text("Step 5/5: Scoring risks and identifying unfavorable clauses...")
#         progress_bar.progress(85)
        
#         scorer = RiskScorer()
#         risk_assessment = scorer.score_contract(analysis_results)
        
#         # Generate report
#         status_text.text("Step 5/5: Generating comprehensive report...")
#         progress_bar.progress(95)
        
#         generator = ReportGenerator()
#         full_report = generator.generate_full_report(
#             parsed_data,
#             analysis_results,
#             risk_assessment
#         )
        
#         progress_bar.progress(100)
#         status_text.text("✅ Analysis complete!")
        
#         return full_report


# def display_sme_summary(report):
#     """Display executive summary for SME owners."""
#     st.header("📋 Executive Summary for Business Owners")
    
#     sme_summary = report.get('sme_summary', {})
    
#     overview = report.get('contract_overview', {})
#     risk = report.get('risk_assessment', {})
#     risk_score = risk.get('overall_score', 0)
#     risk_level = sme_summary.get('overall_risk', 'Unknown')
#     risk_class = 'low' if risk_level == 'Low' else 'medium' if risk_level == 'Medium' else 'high'
    
#     st.markdown(
#         f"<div style='margin-bottom:0.5rem;'>"
#         f"{render_badge(sme_summary.get('contract_type', 'Contract'))} "
#         f"<span class='risk-tag {risk_class}'>{risk_level} Risk</span>"
#         f"</div>",
#         unsafe_allow_html=True
#     )
    
#     st.markdown("<div class='section-title'>Contract Overview</div>", unsafe_allow_html=True)
#     metrics_html = f"""
#     <div class='metrics-card'>
#         <div class='metrics-grid'>
#             <div class='metric-item'>
#                 <div class='metric-label'>Contract Type</div>
#                 <div class='metric-value'>{sme_summary.get('contract_type', 'Unknown')}</div>
#             </div>
#             <div class='metric-item'>
#                 <div class='metric-label'>Overall Risk</div>
#                 <div class='metric-value'>{risk_level}</div>
#             </div>
#             <div class='metric-item'>
#                 <div class='metric-label'>Total Clauses</div>
#                 <div class='metric-value'>{overview.get('total_clauses', 0)}</div>
#             </div>
#             <div class='metric-item'>
#                 <div class='metric-label'>Risk Score</div>
#                 <div class='metric-value'>{risk_score}/100</div>
#             </div>
#         </div>
#     </div>
#     """
#     st.markdown(metrics_html, unsafe_allow_html=True)

#     st.markdown("<div class='section-title'>Overall Risk Meter</div>", unsafe_allow_html=True)
#     col_meter, col_facts = st.columns([1, 2])

#     with col_meter:
#         st.markdown(render_risk_meter(risk_score, risk_level), unsafe_allow_html=True)
#         st.markdown(
#             f"<div class='pill-row'>"
#             f"<span class='risk-tag {risk_class}'>{risk_level} Risk</span>"
#             f"</div>",
#             unsafe_allow_html=True
#         )

#     with col_facts:
#         entities = report.get('entities', {})
#         raw_parties = entities.get('Parties', []) or entities.get('parties', [])
#         raw_durations = entities.get('Durations', []) or entities.get('durations', [])
#         raw_amounts = entities.get('Amounts', []) or entities.get('amounts', [])
#         parties = ", ".join(_clean_list_items(raw_parties, max_items=2))
#         durations = ", ".join(_clean_list_items(raw_durations, max_items=4))
#         amounts = _clean_amounts(", ".join(raw_amounts))
#         jurisdiction = _clean_jurisdiction(infer_jurisdiction(report))

#         key_facts_html = f"""
#         <div class='card'>
#             <div class='section-title' style='margin-top:0;'>Key Facts</div>
#             <div class='metric-label'>Parties</div>
#             <div class='metric-value'>{parties or 'Not detected'}</div>
#             <div class='metric-label'>Duration</div>
#             <div class='metric-value'>{durations or 'Not specified'}</div>
#             <div class='metric-label'>Jurisdiction</div>
#             <div class='metric-value'>{jurisdiction}</div>
#             <div class='metric-label'>Financial Exposure</div>
#             <div class='metric-value'>{amounts}</div>
#         </div>
#         """
#         st.markdown(key_facts_html, unsafe_allow_html=True)
    
#     # Summary text
#     st.markdown("<div class='section-title'>What This Means for Your Business</div>", unsafe_allow_html=True)
#     st.info(sme_summary.get('summary', 'No summary available'))
    
#     # Key takeaways
#     st.markdown("<div class='section-title'>Key Takeaways</div>", unsafe_allow_html=True)
#     for takeaway in sme_summary.get('key_takeaways', []):
#         st.markdown(f"- {takeaway}")
    
#     # Action items
#     st.markdown("<div class='section-title'>Recommended Actions</div>", unsafe_allow_html=True)
#     for action in sme_summary.get('recommended_actions', []):
#         st.markdown(f"{action}")


# def display_risk_assessment(report):
#     """Display detailed risk assessment."""
#     st.header("⚠️ Risk Assessment")
    
#     risk = report.get('risk_assessment', {})
    
#     # Overall risk gauge
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         score = risk.get('overall_score', 0)
#         level = risk.get('overall_level', 'Unknown')
        
#         # Visual risk score display
#         st.markdown(render_risk_meter(score, level), unsafe_allow_html=True)
    
#     with col2:
#         stats = risk.get('statistics', {})
        
#         st.markdown("### Risk Distribution")

#         risk_factors = risk.get('risk_factors', [])

#         def normalize_factor_label(factor: str) -> str:
#             if not factor:
#                 return "Other"
#             label = factor.split(":")[0].strip()
#             if label.lower().startswith("contains"):
#                 return "Ambiguity"
#             if label.lower().startswith("unfavorable term"):
#                 return "Unfavorable term"
#             return label.title()

#         factor_counts = Counter(normalize_factor_label(f) for f in risk_factors if f)

#         if factor_counts:
#             labels = list(factor_counts.keys())
#             values = list(factor_counts.values())
#         else:
#             labels = ["High Risk", "Medium Risk", "Low Risk"]
#             values = [
#                 stats.get('high_risk_clauses', 0),
#                 stats.get('medium_risk_clauses', 0),
#                 stats.get('low_risk_clauses', 0)
#             ]

#         pie_colors = [
#             "#D32F2F",
#             "#F4511E",
#             "#FB8C00",
#             "#FDD835",
#             "#C0CA33",
#             "#43A047",
#             "#1D4ED8",
#             "#7C3AED",
#             "#0EA5E9"
#         ]

#         fig = go.Figure(
#             data=[
#                 go.Pie(
#                     labels=labels,
#                     values=values,
#                     hole=0,
#                     pull=[0.04] * len(labels),
#                     textinfo="label+percent",
#                     textposition="outside",
#                     textfont=dict(color="#0B1F3A", size=13),
#                     insidetextfont=dict(color="#0B1F3A", size=12),
#                     outsidetextfont=dict(color="#0B1F3A", size=13),
#                     marker=dict(colors=pie_colors, line=dict(color="#FFFFFF", width=2)),
#                     sort=False,
#                     direction="clockwise"
#                 )
#             ]
#         )

#         fig.update_layout(
#             margin=dict(t=10, b=10, l=10, r=10),
#             showlegend=False,
#             font=dict(color="#0B1F3A"),
#             paper_bgcolor="rgba(0,0,0,0)",
#             plot_bgcolor="rgba(0,0,0,0)",
#             uniformtext_minsize=10,
#             uniformtext_mode="hide"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     st.markdown("<div class='section-title'>Risk Heatmap (Clause Risk)</div>", unsafe_allow_html=True)
#     clause_risks = risk.get('clause_risks', [])
#     if clause_risks:
#         heat_cells = []
#         for cr in clause_risks:
#             score_val = cr.get('risk_score', 0)
#             label = cr.get('clause_number', 'N/A')
#             if score_val >= 60:
#                 color = '#EF4444'
#             elif score_val >= 30:
#                 color = '#F59E0B'
#             else:
#                 color = '#16A34A'
#             heat_cells.append(
#                 f"<div style='width:38px;height:38px;border-radius:8px;background:{color};"
#                 f"display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.7rem;'"
#                 f"title='Clause {label}: {score_val}/100'>{label}</div>"
#             )
#         st.markdown(
#             "<div style='display:flex;flex-wrap:wrap;gap:6px;'>" + "".join(heat_cells) + "</div>",
#             unsafe_allow_html=True
#         )
#     else:
#         st.info("Heatmap will appear after clause risks are calculated.")
    
#     # Key concerns
#     st.markdown("<div class='section-title'>Top 5 Risk Drivers</div>", unsafe_allow_html=True)
#     concerns = risk.get('key_concerns', [])
    
#     if concerns:
#         for i, concern in enumerate(concerns[:5], 1):
#             with st.expander(f"{i}. {concern}"):
#                 st.markdown("This risk driver appears in multiple clauses. Consider renegotiating or clarifying affected terms.")
#     else:
#         st.success("No major concerns identified")
    
#     # Mitigation strategies
#     st.markdown("<div class='section-title'>Risk Mitigation Strategies</div>", unsafe_allow_html=True)
#     strategies = risk.get('mitigation_strategies', [])
    
#     for strategy in strategies:
#         st.markdown(f"- {strategy}")


# def display_unfavorable_clauses(report):
#     """Display unfavorable clauses requiring attention."""
#     col1, col2 = st.columns([0.3, 1])
#     with col1:
#         st.markdown(render_badge('Requires Attention', 'warning'), unsafe_allow_html=True)
#     with col2:
#         st.header("Unfavorable Clauses")
    
#     unfavorable = report.get('unfavorable_clauses', [])
    
#     if not unfavorable:
#         st.success("✅ No significantly unfavorable clauses detected!")
#         return
    
#     st.markdown(
#         f"<div class='warning-box'>⚠️ Found {len(unfavorable)} clause(s) that may be unfavorable to your business.</div>",
#         unsafe_allow_html=True
#     )
    
#     for clause in unfavorable:
#         risk_level = clause.get('risk_level', 'Unknown')
        
#         # Choose appropriate styling
#         if risk_level == 'High':
#             container_class = 'risk-high'
#         elif risk_level == 'Medium':
#             container_class = 'risk-medium'
#         else:
#             container_class = 'risk-low'
        
#         with st.expander(
#             f"Clause {clause.get('clause_number', 'N/A')}: {clause.get('clause_heading', 'Untitled')} "
#             f"- {risk_level} Risk ({clause.get('risk_score', 0)}/100)"
#         ):
#             # Build entire content as pure HTML for proper alignment
#             risks_text = html.escape(clause.get('why_unfavorable', 'N/A'))
#             recs = clause.get('recommendations', [])
#             rec_items = "".join(f"<li>{html.escape(rec)}</li>" for rec in recs) or "<li>No recommendations available.</li>"

#             content_html = f"""
#             <div class='{container_class}'>
#                 <div class='section-title' style='margin-top:0.25rem;'>Before vs After (Renegotiation View)</div>
#                 <div class='two-col'>
#                     <div class='card-compact'>
#                         <div class='section-title' style='margin-top:0;font-size:1rem;'>Current Clause Risks</div>
#                         <div class='legal-text'>{risks_text}</div>
#                     </div>
#                     <div class='card-compact'>
#                         <div class='section-title' style='margin-top:0;font-size:1rem;'>Safer, Balanced Alternatives</div>
#                         <ul style='margin:0; padding-left:1.1rem; color:#475467; font-size:0.92rem; line-height:1.55;'>
#                             {rec_items}
#                         </ul>
#                     </div>
#                 </div>
#                 <div class='sticky-note'>Why this helps you: reduces financial exposure, adds balance, and improves clarity for execution.</div>
#             </div>
#             """
#             st.markdown(content_html, unsafe_allow_html=True)


# def display_clause_analysis(report):
#     """Display detailed clause-by-clause analysis."""
#     st.header("📄 Clause-by-Clause Analysis")
    
#     clauses = report.get('clause_analysis', [])
    
#     if not clauses:
#         st.warning("No clauses were extracted from the contract.")
#         return
    
#     st.info(f"Total of {len(clauses)} clause(s) identified and analyzed.")
    
#     # Filter options
#     col1, col2 = st.columns(2)
    
#     with col1:
#         filter_risk = st.selectbox(
#             "Filter by Risk Level",
#             ["All", "High", "Medium", "Low"]
#         )
    
#     with col2:
#         show_details = st.checkbox("Show full clause text", value=True)
    
#     # Filter clauses
#     filtered_clauses = clauses
#     if filter_risk != "All":
#         filtered_clauses = [c for c in clauses if c.get('risk_level') == filter_risk]
    
#     # Display clauses
#     for clause in filtered_clauses:
#         risk_level = clause.get('risk_level', 'Low')
#         risk_score = clause.get('risk_score', 0)
        
#         # Color code by risk
#         if risk_level == 'High':
#             expander_label = f"🔴 Clause {clause.get('number', 'N/A')}: {clause.get('heading', 'Untitled')} (Risk: {risk_score}/100)"
#         elif risk_level == 'Medium':
#             expander_label = f"🟡 Clause {clause.get('number', 'N/A')}: {clause.get('heading', 'Untitled')} (Risk: {risk_score}/100)"
#         else:
#             expander_label = f"🟢 Clause {clause.get('number', 'N/A')}: {clause.get('heading', 'Untitled')} (Risk: {risk_score}/100)"
        
#         with st.expander(expander_label):
#             icons = clause_icons(clause.get('text', ''))
#             risk_class = 'low' if risk_level == 'Low' else 'medium' if risk_level == 'Medium' else 'high'
            
#             st.markdown(
#                 f"<div class='pill-row'>"
#                 f"<span class='risk-tag {risk_class}'>{risk_level} Risk</span>"
#                 f"<span class='pill'>Score: {risk_score}/100</span>"
#                 f"<span class='pill'>{icons or '📄 General'}</span>"
#                 f"</div>",
#                 unsafe_allow_html=True
#             )

#             # Build cards as pure HTML to maintain flex alignment
#             clause_text = clause.get('text', 'No text available')
            
#             if show_details:
#                 highlighted = highlight_risky_phrases(clause_text)
#                 clause_content = f"<div class='legal-text'>{highlighted}</div>"
#             else:
#                 clause_content = "<div class='small-muted'>Hidden</div>"
            
#             plain_lang = html.escape(clause.get('plain_language_summary', 'No summary available'))
#             impact_text = html.escape(clause.get('impact_on_sme', 'Impact assessment not available'))
            
#             two_column_html = f"""
#             <div class='two-col'>
#                 <div class='card'>
#                     <div class='metric-label'>Original Clause</div>
#                     {clause_content}
#                 </div>
#                 <div class='card'>
#                     <div class='metric-label'>Plain‑Language Explanation</div>
#                     <div class='explain-text'>{plain_lang}</div>
#                     <div class='metric-label' style='margin-top:0.6rem;'>Impact on Your Business</div>
#                     <div class='legal-text'>{impact_text}</div>
#                 </div>
#             </div>
#             """
#             st.markdown(two_column_html, unsafe_allow_html=True)
            
#             st.markdown("<div class='section-title'>Obligations • Rights • Prohibitions</div>", unsafe_allow_html=True)
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 obligations = clause.get('obligations', [])
#                 if obligations:
#                     st.markdown("**Your Obligations**")
#                     for obl in obligations[:3]:
#                         st.markdown(f"- {obl}")
            
#             with col2:
#                 rights = clause.get('rights', [])
#                 if rights:
#                     st.markdown("**Your Rights**")
#                     for right in rights[:3]:
#                         st.markdown(f"- {right}")
            
#             with col3:
#                 prohibitions = clause.get('prohibitions', [])
#                 if prohibitions:
#                     st.markdown("**Prohibitions**")
#                     for proh in prohibitions[:3]:
#                         st.markdown(f"- {proh}")
            
#             risk_factors = clause.get('risk_factors', [])
#             if risk_factors:
#                 st.markdown("<div class='section-title'>Risk Factors</div>", unsafe_allow_html=True)
#                 for factor in risk_factors:
#                     st.markdown(
#                         f"<div class='warning-box'>{html.escape(factor)}</div>",
#                         unsafe_allow_html=True
#                     )
            
#             ambiguities = clause.get('ambiguities', [])
#             if ambiguities:
#                 st.markdown("<div class='section-title'>Ambiguities Detected</div>", unsafe_allow_html=True)
#                 for amb in ambiguities:
#                     st.markdown(
#                         f"<div class='warning-box'>⚠️ {html.escape(amb)}</div>",
#                         unsafe_allow_html=True
#                     )


# def display_entities(report):
#     """Display extracted entities."""
#     st.header("🔍 Key Information Extracted")
    
#     entities = report.get('entities', {})
    
#     if not entities:
#         st.info("No entities were extracted from the contract.")
#         return
    
#     cols = st.columns(2)
    
#     col_index = 0
#     for entity_type, entity_list in entities.items():
#         if entity_list:
#             with cols[col_index % 2]:
#                 # Build card content as pure HTML for proper alignment
#                 entity_items = "".join(f"<li>{html.escape(str(item))}</li>" for item in entity_list[:5])
#                 card_html = f"""
#                 <div class='card'>
#                     <div class='metric-label'>{html.escape(entity_type)}</div>
#                     <ul style='margin: 0.5rem 0 0 1.1rem; padding: 0; color: #475467; font-size: 0.92rem; line-height: 1.6;'>
#                         {entity_items}
#                     </ul>
#                 </div>
#                 """
#                 st.markdown(card_html, unsafe_allow_html=True)
#             col_index += 1


# def export_report(report):
#     """Provide export options for the report."""
#     st.header("📥 Export Report")
    
#     generator = ReportGenerator()
#     generator.report_data = report
    
#     st.markdown("<div class='section-title'>Export‑Ready Executive Summary</div>", unsafe_allow_html=True)
#     sme_summary = report.get('sme_summary', {})
    
#     # Build card content as pure HTML for proper alignment
#     contract_type = html.escape(sme_summary.get('contract_type', 'Unknown'))
#     overall_risk = html.escape(sme_summary.get('overall_risk', 'Unknown'))
#     summary = html.escape(sme_summary.get('summary', ''))
    
#     summary_html = f"""
#     <div class='card'>
#         <div class='metric-label'>Contract Type</div>
#         <div class='metric-value'>{contract_type}</div>
#         <div class='metric-label' style='margin-top:0.8rem;'>Overall Risk</div>
#         <div class='metric-value'>{overall_risk}</div>
#         <div class='legal-text' style='margin-top:0.8rem;'>{summary}</div>
#     </div>
#     """
#     st.markdown(summary_html, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Markdown export
#         st.markdown("### Export as Markdown")
#         md_content = generator.export_to_markdown()
        
#         st.download_button(
#             label="📄 Download Markdown Report",
#             data=md_content,
#             file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
#             mime="text/markdown"
#         )
    
#     with col2:
#         # JSON export
#         st.markdown("### Export as JSON")
#         json_content = generator.export_to_json()
        
#         st.download_button(
#             label="📊 Download JSON Data",
#             data=json_content,
#             file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#             mime="application/json"
#         )

#     st.markdown("<div class='disclaimer-box'>This analysis is for informational and analytical purposes only and does not constitute legal advice. All interpretations are based solely on the provided contract text.</div>", unsafe_allow_html=True)


# def main():
#     """Main application."""
#     initialize_session_state()
#     display_header()
    
#     # Sidebar
#     with st.sidebar:
#         st.markdown("### 🔒 Trust & Privacy")
#         st.markdown(render_badge("Confidential processing", "trust"), unsafe_allow_html=True)
#         st.markdown("<div class='small-muted'>Your document stays on this device. No external APIs.</div>", unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         st.markdown("### 📄 Supported Formats")
#         st.markdown("- PDF\n- DOCX\n- DOC\n- TXT")
        
#         st.markdown("---")
        
#         # How to use (short manual)
#         st.markdown("### ✅ How to Use")
#         st.markdown("""
#         1. Upload your contract (PDF/DOCX/TXT)
#         2. Click **Analyze Contract**
#         3. Review Summary, Risks, and Clauses
#         4. Export report for sharing
#         """)
        
#         st.markdown("---")
#         st.markdown("**Version:** 1.0.0")
#         st.markdown("**Last Updated:** February 2026")
    
#     # Main content area
#     if st.session_state.analysis_complete and st.session_state.report:
#         report = st.session_state.report

#         with st.expander("📁 Analyze another contract", expanded=False):
#             st.markdown("<div class='upload-zone'>", unsafe_allow_html=True)
#             new_file = st.file_uploader(
#                 "Drag & drop your contract",
#                 type=['pdf', 'docx', 'doc', 'txt'],
#                 key="new_contract_upload",
#                 label_visibility="collapsed"
#             )
#             st.markdown("<div class='upload-hint'>PDF, DOCX, DOC, or TXT • Confidential & local processing</div>", unsafe_allow_html=True)
#             st.markdown("</div>", unsafe_allow_html=True)
#             if new_file is not None:
#                 if st.button("Analyze New Contract", type="primary"):
#                     new_report = analyze_contract(new_file)
#                     if new_report:
#                         st.session_state.report = new_report
#                         st.session_state.analysis_complete = True
#                         st.rerun()
        
#         # Create tabs for different sections
#         tabs = st.tabs([
#             "📋 Summary",
#             "⚠️ Risk Assessment",
#             "🚨 Unfavorable Clauses",
#             "📄 Clause Analysis",
#             "🔍 Entities",
#             "📥 Export"
#         ])
        
#         with tabs[0]:
#             display_sme_summary(report)
        
#         with tabs[1]:
#             display_risk_assessment(report)
        
#         with tabs[2]:
#             display_unfavorable_clauses(report)
        
#         with tabs[3]:
#             display_clause_analysis(report)
        
#         with tabs[4]:
#             display_entities(report)
        
#         with tabs[5]:
#             export_report(report)
        
#     else:
#         st.markdown("<div class='confidential-watermark'></div>", unsafe_allow_html=True)
#         tape_text = (
#             "This tool provides informational analysis only and is not legal advice. "
#             "Please consult a qualified legal professional before making decisions."
#         )
#         st.markdown(
#             "<div class='warning-tape'>"
#             "  <div class='warning-tape-inner'>"
#             "    <div class='warning-tape-track'>"
#             f"      <span class='warning-tape-text'>{tape_text}</span>"
#             f"      <span class='warning-tape-text'>{tape_text}</span>"
#             f"      <span class='warning-tape-text'>{tape_text}</span>"
#             "    </div>"
#             "    <div class='warning-tape-track'>"
#             f"      <span class='warning-tape-text'>{tape_text}</span>"
#             f"      <span class='warning-tape-text'>{tape_text}</span>"
#             f"      <span class='warning-tape-text'>{tape_text}</span>"
#             "    </div>"
#             "  </div>"
#             "</div>",
#             unsafe_allow_html=True
#         )
#         st.markdown("<div class='section-title'>Start Your Contract Analysis</div>", unsafe_allow_html=True)
#         st.markdown("<div class='upload-zone'>", unsafe_allow_html=True)
#         uploaded_file = st.file_uploader(
#             "Drag & drop your contract",
#             type=['pdf', 'docx', 'doc', 'txt'],
#             help="Upload your contract in PDF, DOCX, or TXT format",
#             key="landing_upload",
#             label_visibility="collapsed"
#         )
#         st.markdown("<div class='upload-hint'>PDF, DOCX, DOC, or TXT • Confidential & local processing</div>", unsafe_allow_html=True)
#         st.markdown("<div class='upload-hint'>🔐 We do not store your documents</div>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#         if uploaded_file is not None:
#             st.success(f"✅ File uploaded: {uploaded_file.name}")
#             if st.button("🚀 Analyze Contract", type="primary"):
#                 report = analyze_contract(uploaded_file)
#                 if report:
#                     st.session_state.report = report
#                     st.session_state.analysis_complete = True
#                     st.rerun()



# if __name__ == "__main__":
#     main()





"""
Legal Contract Analysis Assistant - Streamlit Web Application
GenAI-powered tool for SME contract analysis
PROFESSIONAL REDESIGN - Sophisticated Corporate Aesthetic
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import html
import re
from collections import Counter

import plotly.graph_objects as go

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

from modules.parser import DocumentParser
from modules.analyzer import ContractAnalyzer
from modules.risk_scorer import RiskScorer
from modules.report_generator import ReportGenerator


# Page configuration
st.set_page_config(
    page_title="Legal Contract Analyzer for SMEs",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Redesign
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-navy: #1a2332;
        --primary-gold: #d4af37;
        --accent-burgundy: #6b2c3e;
        --slate-100: #f8fafc;
        --slate-200: #e2e8f0;
        --slate-300: #cbd5e1;
        --slate-600: #475569;
        --slate-700: #334155;
        --slate-800: #1e293b;
        --slate-900: #0f172a;
        --success-green: #059669;
        --warning-amber: #d97706;
        --danger-red: #dc2626;
        --info-blue: #0284c7;
        --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e8edf3 100%);
        --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 40px rgba(0, 0, 0, 0.03);
        --card-shadow-hover: 0 4px 6px rgba(0, 0, 0, 0.07), 0 15px 50px rgba(0, 0, 0, 0.05);
    }

    /* Global Styles */
    .stApp {
        background: var(--bg-gradient);
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--slate-800);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--primary-navy);
        letter-spacing: -0.02em;
    }

    /* Header Section */
    .main-header {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: var(--primary-navy);
        text-align: center;
        letter-spacing: -0.03em;
        margin: 2rem 0 1rem;
        position: relative;
        line-height: 1.1;
    }

    .main-header::after {
        content: '';
        display: block;
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-gold) 0%, var(--accent-burgundy) 100%);
        margin: 1.5rem auto;
        border-radius: 2px;
    }

    .sub-header {
        font-size: 1.15rem;
        color: var(--slate-600);
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
        letter-spacing: 0.01em;
    }

    /* Watermark */
    .confidential-watermark {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: 0.025;
        font-family: 'Playfair Display', Georgia, serif;
        font-weight: 800;
        font-size: 72px;
        letter-spacing: 8px;
        color: var(--primary-navy);
        transform: rotate(-35deg);
        display: grid;
        place-items: center;
        text-transform: uppercase;
    }

    .confidential-watermark::before {
        content: "CONFIDENTIAL";
        display: block;
        width: 200%;
        text-align: center;
        line-height: 8;
    }

    /* Section Titles */
    .section-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin: 2rem 0 1.25rem;
        position: relative;
        padding-left: 20px;
    }

    .section-title::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 28px;
        background: linear-gradient(180deg, var(--primary-gold) 0%, var(--accent-burgundy) 100%);
        border-radius: 2px;
    }

    /* Cards */
    .card {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        box-shadow: var(--card-shadow);
        padding: 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-gold) 0%, var(--accent-burgundy) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .card:hover {
        box-shadow: var(--card-shadow-hover);
        transform: translateY(-2px);
        border-color: rgba(212, 175, 55, 0.3);
    }

    .card:hover::before {
        opacity: 1;
    }

    .card-compact {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }

    /* Upload Zone */
    .upload-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px dashed var(--slate-300);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .upload-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 50% 50%, rgba(212, 175, 55, 0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .upload-card:hover {
        border-color: var(--primary-gold);
        background: linear-gradient(135deg, #ffffff 0%, #fefce8 100%);
    }

    .upload-card:hover::before {
        opacity: 1;
    }

    .upload-zone [data-testid="stFileUploader"] > div {
        border: 2px dashed var(--slate-300);
        border-radius: 16px;
        padding: 3rem 2rem;
        min-height: 240px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        transition: all 0.3s ease;
    }

    .upload-zone [data-testid="stFileUploader"] > div:hover {
        border-color: var(--primary-gold);
        background: linear-gradient(135deg, #ffffff 0%, #fefce8 100%);
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        background: linear-gradient(135deg, var(--slate-100) 0%, var(--slate-200) 100%);
        color: var(--slate-700);
        border: 1px solid var(--slate-300);
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }

    .badge:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .trust-badge {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        color: var(--success-green);
        border-color: #86efac;
    }

    .warning-badge {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: var(--warning-amber);
        border-color: #fcd34d;
    }

    /* Risk Tags */
    .risk-tag {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.85rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: all 0.2s ease;
    }

    .risk-tag:hover {
        transform: scale(1.05);
    }

    .risk-tag.low { 
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        color: var(--success-green);
        border: 1px solid #86efac;
    }
    
    .risk-tag.medium { 
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: var(--warning-amber);
        border: 1px solid #fcd34d;
    }
    
    .risk-tag.high { 
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: var(--danger-red);
        border: 1px solid #fca5a5;
    }

    /* Metrics */
    .metrics-card {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: var(--card-shadow);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }

    .metric-item {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid var(--slate-200);
        border-radius: 10px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-gold) 0%, var(--accent-burgundy) 100%);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }

    .metric-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    .metric-item:hover::before {
        transform: scaleX(1);
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--slate-600);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    .metric-value {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary-navy);
        line-height: 1.2;
    }

    /* Risk Boxes */
    .risk-high {
        background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
        padding: 1.5rem;
        border-left: 4px solid var(--danger-red);
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.08);
    }

    .risk-medium {
        background: linear-gradient(135deg, #fef3c7 0%, #fefce8 100%);
        padding: 1.5rem;
        border-left: 4px solid var(--warning-amber);
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
    }

    .risk-low {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
        padding: 1.5rem;
        border-left: 4px solid var(--success-green);
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.08);
    }

    /* Text Styles */
    .legal-text {
        color: var(--slate-700);
        font-size: 0.95rem;
        line-height: 1.7;
        font-weight: 400;
    }

    .explain-text {
        color: var(--primary-navy);
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.7;
    }

    .inline-highlight {
        background: linear-gradient(120deg, #fef3c7 0%, #fde68a 100%);
        padding: 2px 6px;
        border-radius: 4px;
        color: var(--warning-amber);
        font-weight: 700;
        border-bottom: 2px solid var(--primary-gold);
    }

    /* Pills */
    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.75rem 0;
    }

    .pill {
        border: 1px solid var(--slate-300);
        background: linear-gradient(135deg, #ffffff 0%, var(--slate-100) 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        color: var(--slate-700);
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .pill:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-color: var(--primary-gold);
    }

    /* Disclaimer & Warning Boxes */
    .disclaimer-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fefce8 100%);
        padding: 1.25rem 1.5rem;
        border: 1px solid #fde68a;
        border-left: 4px solid var(--warning-amber);
        border-radius: 10px;
        margin: 1.5rem 0;
        color: var(--slate-800);
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
    }

    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fefce8 100%);
        padding: 1.25rem 1.5rem;
        border: 1px solid #fde68a;
        border-left: 4px solid var(--warning-amber);
        border-radius: 10px;
        margin: 1rem 0;
        color: var(--slate-800);
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
    }

    /* Warning Tape */
    .warning-tape {
        position: relative;
        overflow: hidden;
        background: var(--primary-navy);
        border-top: 3px solid var(--primary-gold);
        border-bottom: 3px solid var(--primary-gold);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        padding: 16px 0;
        width: 100vw;
        margin-left: calc(50% - 50vw);
        margin-right: calc(50% - 50vw);
    }

    .warning-tape-inner {
        display: flex;
        width: max-content;
        animation: marquee 40s linear infinite;
    }

    .warning-tape-track {
        display: flex;
        white-space: nowrap;
        gap: 3rem;
        padding-right: 3rem;
        font-weight: 600;
        color: var(--slate-100);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.85rem;
    }

    .warning-tape-text {
        padding: 0.3rem 1rem;
        background: rgba(212, 175, 55, 0.15);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 4px;
        color: var(--primary-gold);
        letter-spacing: 0.08em;
    }

    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    /* Sticky Note */
    .sticky-note {
        background: linear-gradient(135deg, #fef3c7 0%, #fefce8 100%);
        border: 1px solid #fde68a;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: var(--slate-700);
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
        position: relative;
    }

    .sticky-note::before {
        content: '💡';
        position: absolute;
        top: -10px;
        left: 10px;
        font-size: 1.5rem;
    }

    /* Two Column Layout */
    .two-col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        align-items: stretch;
    }

    /* Tabs Styling */
    [data-baseweb="tab"] {
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--slate-600) !important;
        font-weight: 600;
        font-size: 1rem;
        padding: 1rem 1.5rem;
        transition: all 0.2s ease;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary-navy) !important;
        border-bottom: 3px solid var(--primary-gold);
    }

    [data-baseweb="tab"]:hover {
        color: var(--primary-navy) !important;
        background: rgba(212, 175, 55, 0.05);
    }

    [data-baseweb="tab-list"] {
        border-bottom: 2px solid var(--slate-200);
        background: #ffffff;
        border-radius: 12px 12px 0 0;
        padding: 0 1rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-navy) 0%, var(--slate-800) 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(26, 35, 50, 0.2);
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(26, 35, 50, 0.3);
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--primary-gold) 0%, #c4941f 100%);
        color: var(--primary-navy);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(212, 175, 55, 0.4);
        background: linear-gradient(135deg, #e5c158 0%, var(--primary-gold) 100%);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ffffff 0%, var(--slate-100) 100%);
        border: 1px solid var(--slate-200);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: var(--primary-navy);
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
        border-color: var(--primary-gold);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-navy) 0%, var(--slate-900) 100%);
        color: var(--slate-100);
    }

    [data-testid="stSidebar"] h3 {
        color: var(--primary-gold);
        font-family: 'Playfair Display', Georgia, serif;
        font-weight: 700;
        font-size: 1.25rem;
        margin-top: 1.5rem;
    }

    [data-testid="stSidebar"] .small-muted {
        color: var(--slate-300);
        font-size: 0.85rem;
        line-height: 1.6;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(212, 175, 55, 0.2);
    }

    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-gold) 0%, var(--accent-burgundy) 100%);
    }

    /* Seal Decoration */
    .wax-seal {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: 
            radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.05) 40%, transparent 41%),
            radial-gradient(circle at 65% 65%, rgba(0, 0, 0, 0.3), transparent 45%),
            radial-gradient(circle, var(--accent-burgundy) 0%, #5a1f30 65%, #3d1420 100%);
        box-shadow: 
            inset 0 3px 6px rgba(255, 255, 255, 0.4),
            inset 0 -5px 8px rgba(0, 0, 0, 0.4),
            0 8px 20px rgba(107, 44, 62, 0.4);
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
    }

    .wax-seal::after {
        content: "⚖";
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.95);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }

    /* Animation Classes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Small Text */
    .small-muted {
        color: var(--slate-600);
        font-size: 0.85rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'report' not in st.session_state:
        st.session_state.report = None
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = None
    if 'spacy_nlp' not in st.session_state:
        # Load spaCy model for NLP preprocessing
        st.session_state.spacy_nlp = _load_spacy_model()


def render_badge(text: str, kind: str = "default") -> str:
    """Render a styled badge."""
    if kind == "trust":
        return f"<span class='badge trust-badge'>🔒 {html.escape(text)}</span>"
    elif kind == "warning":
        return f"<span class='badge warning-badge'>⚠️ {html.escape(text)}</span>"
    return f"<span class='badge'>✨ {html.escape(text)}</span>"


def render_risk_meter(score: float, level: str) -> str:
    """Render a large, clean risk score display."""
    safe_score = max(0, min(int(score), 100))
    level_text = level if level else "Unknown"
    level_color = "#059669" if level_text == "Low" else "#d97706" if level_text == "Medium" else "#dc2626"
    
    return (
        '<div style="display:flex; flex-direction:column; align-items:center; gap:1rem; padding:1rem 0;">'
        '<div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.15em;">Overall Risk Score</div>'
        '<div style="font-family: \'Playfair Display\', Georgia, serif; font-size:4rem; font-weight:800; color:#1a2332; line-height:1;">'
        f'{safe_score}<span style="font-size:1.5rem; font-weight:400; color:#94a3b8;">/100</span>'
        '</div>'
        f'<div style="font-size:1.1rem; font-weight:700; color:{level_color}; text-transform:uppercase; letter-spacing:0.05em;">{html.escape(level_text)} Risk</div>'
        '</div>'
    )


def highlight_risky_phrases(text: str) -> str:
    """Highlight risky phrases in clause text."""
    if not text:
        return ""
    risky_terms = [
        "penalty", "liquidated damages", "indemnify", "indemnification", "terminate",
        "unilateral", "without cause", "sole discretion", "auto-renewal", "lock-in",
        "non-compete", "non solicitation", "exclusive", "assignment", "waiver",
        "unlimited", "in perpetuity", "irrevocable", "fine", "forfeit", "breach"
    ]
    safe_text = html.escape(text)
    for term in sorted(risky_terms, key=len, reverse=True):
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        safe_text = pattern.sub(lambda m: f"<span class='inline-highlight'>{m.group(0)}</span>", safe_text)
    return safe_text


def clause_icons(text: str) -> str:
    """Return icons representing clause types."""
    t = (text or "").lower()
    icons = []
    if any(k in t for k in ["penalty", "liquidated damages", "fine", "forfeit"]):
        icons.append("💸 Penalty")
    if any(k in t for k in ["ip", "intellectual property", "assignment", "license"]):
        icons.append("🧠 IP")
    if any(k in t for k in ["terminate", "termination", "cancel"]):
        icons.append("🛑 Termination")
    if any(k in t for k in ["indemnify", "indemnification", "hold harmless"]):
        icons.append("🛡️ Indemnity")
    return " ".join(icons)


def infer_jurisdiction(report: dict) -> str:
    """Infer jurisdiction/governing law from clause text if present."""
    clauses = report.get('clause_analysis', [])
    pattern = re.compile(r"(governing law|jurisdiction|courts of|seat of arbitration)[:\s]+([^\.\n]+)", re.IGNORECASE)
    for clause in clauses:
        text = clause.get('text', '')
        match = pattern.search(text)
        if match:
            return match.group(2).strip()
    return "Not specified"


def _clean_list_items(items, max_items=4):
    """Normalize list strings (dedupe, trim, and present cleanly)."""
    if not items:
        return []
    seen = set()
    cleaned = []
    for item in items:
        value = re.sub(r"\s+", " ", str(item)).strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(value)
    if len(cleaned) > max_items:
        return cleaned[:max_items] + [f"and {len(cleaned) - max_items} more"]
    return cleaned


def _clean_jurisdiction(text: str) -> str:
    """Clean jurisdiction text for grammar and punctuation."""
    if not text:
        return "Not specified"
    value = re.sub(r"\s+", " ", text).strip()
    value = re.sub(r"^(and\s+)?jurisdiction\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^(and\s+)", "", value, flags=re.IGNORECASE)
    if value and value[-1] not in ".!?":
        value += "."
    return value


def _clean_amounts(text: str) -> str:
    """Clean financial amounts list for consistent formatting."""
    if not text:
        return "Not specified"
    tokens = re.split(r"[,|]+", text)
    cleaned = []
    for token in tokens:
        value = re.sub(r"\s+", " ", token).strip()
        value = re.sub(r"\b(rs)\b", "INR", value, flags=re.IGNORECASE)
        value = value.replace("INR INR", "INR").strip()
        if value and value.lower() not in {"rs", "rs.", "inr"}:
            cleaned.append(value)
    cleaned = _clean_list_items(cleaned, max_items=3)
    return ", ".join(cleaned) if cleaned else "Not specified"


def _contains_hindi(text: str) -> bool:
    """Detect Devanagari script (Hindi) in text."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", text))


def _translate_to_english(text: str) -> str:
    """Translate text to English using googletrans if available."""
    if not text:
        return ""
    try:
        from googletrans import Translator
    except Exception:
        return text

    translator = Translator()
    chunk_size = 4000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []
    for chunk in chunks:
        try:
            translated_chunks.append(translator.translate(chunk, dest="en").text)
        except Exception:
            translated_chunks.append(chunk)
    return "\n".join(translated_chunks)


def _load_spacy_model():
    """Load spaCy English model with fallback."""
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            return nlp
        except OSError:
            # Model not installed, attempt to download
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            nlp = spacy.load("en_core_web_sm")
            return nlp
    except Exception as e:
        logger_msg = f"Warning: Could not load spaCy model: {str(e)}"
        return None


def display_header():
    """Display application header."""
    # Centered wax seal
    st.markdown('<div style="text-align: center;"><div class="wax-seal"></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">Legal Contract Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional contract insights for discerning business leaders</div>', unsafe_allow_html=True)
    
    st.markdown(
        f"<div style='text-align:center; margin-bottom:1.5rem;'>"
        f"{render_badge('Confidential & Secure Processing', 'trust')}"
        f"</div>",
        unsafe_allow_html=True
    )


def analyze_contract(uploaded_file):
    """
    Main analysis pipeline following the workflow:
    1. Upload Contract
    2. Extract Text
    3. Detect Language
    4. IF English → proceed to NLP preprocessing
    5. ELSE IF Hindi → translate to English → proceed to NLP preprocessing
    6. NLP preprocessing (spaCy/NLTK) → analysis
    """
    with st.spinner("🔍 Analyzing your contract..."):
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Upload & Extract Text
        status_text.text("Step 1/5: Extracting text from document...")
        progress_bar.progress(20)
        
        parser = DocumentParser()
        file_bytes = uploaded_file.read()
        parsed_data = parser.parse_document(
            file_bytes=file_bytes,
            filename=uploaded_file.name
        )
        
        if parsed_data.get('error'):
            st.error(f"❌ Error parsing document: {parsed_data['error']}")
            return None
        
        raw_text = parsed_data.get('raw_text', '')
        
        # Step 2: Detect Language
        status_text.text("Step 2/5: Detecting language...")
        progress_bar.progress(35)
        
        if _contains_hindi(raw_text):
            detected_language = "Hindi"
            status_text.text("Step 2/5: Language detected - Hindi. Translating to English...")
            st.info("🌐 Hindi contract detected. Translating to English for analysis...")
        else:
            detected_language = "English"
        
        parsed_data['language_detected'] = detected_language
        
        # Step 3: Language-specific preprocessing
        status_text.text(f"Step 3/5: Processing {detected_language} text...")
        progress_bar.progress(45)
        
        clean_text = parser.preprocess_text(raw_text)
        
        # Step 4: Translate if Hindi
        if detected_language == "Hindi":
            status_text.text("Step 4/5: Translating Hindi to English...")
            progress_bar.progress(55)
            
            translated_text = _translate_to_english(clean_text)
            if translated_text and translated_text.strip():
                parsed_data['original_language_text'] = clean_text
                parsed_data['translated_text'] = translated_text
                parsed_data['translation_applied'] = True
                clean_text = translated_text
            else:
                st.warning("⚠️ Translation failed. Proceeding with original text.")
                parsed_data['translation_applied'] = False
        else:
            parsed_data['translation_applied'] = False
        
        if not clean_text or len(clean_text) < 100:
            st.error("❌ Document text is too short or empty. Please upload a valid contract.")
            return None
        
        st.session_state.parsed_data = parsed_data
        
        # Step 5: NLP Preprocessing & Analysis
        status_text.text("Step 5/5: Performing NLP analysis and risk assessment...")
        progress_bar.progress(70)
        
        analyzer = ContractAnalyzer()
        analysis_results = analyzer.analyze_contract(clean_text)
        analysis_results['language_detected'] = detected_language
        
        if analysis_results.get('error'):
            st.error(f"❌ Error analyzing contract: {analysis_results['error']}")
            return None
        
        # Risk scoring
        status_text.text("Step 5/5: Scoring risks and identifying unfavorable clauses...")
        progress_bar.progress(85)
        
        scorer = RiskScorer()
        risk_assessment = scorer.score_contract(analysis_results)
        
        # Generate report
        status_text.text("Step 5/5: Generating comprehensive report...")
        progress_bar.progress(95)
        
        generator = ReportGenerator()
        full_report = generator.generate_full_report(
            parsed_data,
            analysis_results,
            risk_assessment
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        return full_report


def display_sme_summary(report):
    """Display executive summary for SME owners."""
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    st.header("📋 Executive Summary")
    
    sme_summary = report.get('sme_summary', {})
    
    overview = report.get('contract_overview', {})
    risk = report.get('risk_assessment', {})
    risk_score = risk.get('overall_score', 0)
    risk_level = sme_summary.get('overall_risk', 'Unknown')
    risk_class = 'low' if risk_level == 'Low' else 'medium' if risk_level == 'Medium' else 'high'
    
    st.markdown(
        f"<div style='margin-bottom:1rem;'>"
        f"{render_badge(sme_summary.get('contract_type', 'Contract'))} "
        f"<span class='risk-tag {risk_class}'>{risk_level} Risk</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    st.markdown("<div class='section-title'>Contract Overview</div>", unsafe_allow_html=True)
    metrics_html = f"""
    <div class='metrics-card'>
        <div class='metrics-grid'>
            <div class='metric-item'>
                <div class='metric-label'>Contract Type</div>
                <div class='metric-value'>{sme_summary.get('contract_type', 'Unknown')}</div>
            </div>
            <div class='metric-item'>
                <div class='metric-label'>Overall Risk</div>
                <div class='metric-value'>{risk_level}</div>
            </div>
            <div class='metric-item'>
                <div class='metric-label'>Total Clauses</div>
                <div class='metric-value'>{overview.get('total_clauses', 0)}</div>
            </div>
            <div class='metric-item'>
                <div class='metric-label'>Risk Score</div>
                <div class='metric-value'>{risk_score}/100</div>
            </div>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Risk Assessment</div>", unsafe_allow_html=True)
    col_meter, col_facts = st.columns([1, 2])

    with col_meter:
        st.markdown(render_risk_meter(risk_score, risk_level), unsafe_allow_html=True)
        st.markdown(
            f"<div class='pill-row' style='justify-content:center;'>"
            f"<span class='risk-tag {risk_class}'>{risk_level} Risk</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col_facts:
        entities = report.get('entities', {})
        raw_parties = entities.get('Parties', []) or entities.get('parties', [])
        raw_durations = entities.get('Durations', []) or entities.get('durations', [])
        raw_amounts = entities.get('Amounts', []) or entities.get('amounts', [])
        parties = ", ".join(_clean_list_items(raw_parties, max_items=2))
        durations = ", ".join(_clean_list_items(raw_durations, max_items=4))
        amounts = _clean_amounts(", ".join(raw_amounts))
        jurisdiction = _clean_jurisdiction(infer_jurisdiction(report))

        key_facts_html = f"""
        <div class='card'>
            <div class='section-title' style='margin-top:0; font-size:1.5rem;'>Key Information</div>
            <div class='metric-label'>Contracting Parties</div>
            <div class='metric-value' style='font-size:1.1rem; margin-bottom:1rem;'>{parties or 'Not detected'}</div>
            <div class='metric-label'>Contract Duration</div>
            <div class='metric-value' style='font-size:1.1rem; margin-bottom:1rem;'>{durations or 'Not specified'}</div>
            <div class='metric-label'>Governing Jurisdiction</div>
            <div class='metric-value' style='font-size:1.1rem; margin-bottom:1rem;'>{jurisdiction}</div>
            <div class='metric-label'>Financial Exposure</div>
            <div class='metric-value' style='font-size:1.1rem;'>{amounts}</div>
        </div>
        """
        st.markdown(key_facts_html, unsafe_allow_html=True)
    
    # Summary text
    st.markdown("<div class='section-title'>Business Impact Analysis</div>", unsafe_allow_html=True)
    st.info(sme_summary.get('summary', 'No summary available'))
    
    # Key takeaways
    st.markdown("<div class='section-title'>Key Takeaways</div>", unsafe_allow_html=True)
    for takeaway in sme_summary.get('key_takeaways', []):
        st.markdown(f"• {takeaway}")
    
    # Action items
    st.markdown("<div class='section-title'>Recommended Actions</div>", unsafe_allow_html=True)
    for action in sme_summary.get('recommended_actions', []):
        st.markdown(f"**→** {action}")
    
    st.markdown("</div>", unsafe_allow_html=True)


def display_risk_assessment(report):
    """Display detailed risk assessment."""
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    st.header("⚠️ Risk Assessment")
    
    risk = report.get('risk_assessment', {})
    
    # Overall risk gauge
    col1, col2 = st.columns([1, 2])
    
    with col1:
        score = risk.get('overall_score', 0)
        level = risk.get('overall_level', 'Unknown')
        
        # Visual risk score display
        st.markdown(render_risk_meter(score, level), unsafe_allow_html=True)
    
    with col2:
        stats = risk.get('statistics', {})
        
        st.markdown("<div class='section-title' style='margin-top:0;'>Risk Distribution</div>", unsafe_allow_html=True)

        risk_factors = risk.get('risk_factors', [])

        def normalize_factor_label(factor: str) -> str:
            if not factor:
                return "Other"
            label = factor.split(":")[0].strip()
            if label.lower().startswith("contains"):
                return "Ambiguity"
            if label.lower().startswith("unfavorable term"):
                return "Unfavorable term"
            return label.title()

        factor_counts = Counter(normalize_factor_label(f) for f in risk_factors if f)

        if factor_counts:
            labels = list(factor_counts.keys())
            values = list(factor_counts.values())
        else:
            labels = ["High Risk", "Medium Risk", "Low Risk"]
            values = [
                stats.get('high_risk_clauses', 0),
                stats.get('medium_risk_clauses', 0),
                stats.get('low_risk_clauses', 0)
            ]

        pie_colors = [
            "#dc2626",
            "#ea580c",
            "#d97706",
            "#ca8a04",
            "#84cc16",
            "#059669",
            "#0284c7",
            "#6366f1",
            "#8b5cf6"
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    pull=[0.05] * len(labels),
                    textinfo="label+percent",
                    textposition="outside",
                    textfont=dict(color="#1a2332", size=14, family="IBM Plex Sans"),
                    marker=dict(colors=pie_colors, line=dict(color="#FFFFFF", width=3)),
                    sort=False,
                    direction="clockwise"
                )
            ]
        )

        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            font=dict(color="#1a2332", family="IBM Plex Sans"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Clause Risk Heatmap</div>", unsafe_allow_html=True)
    clause_risks = risk.get('clause_risks', [])
    if clause_risks:
        heat_cells = []
        for cr in clause_risks:
            score_val = cr.get('risk_score', 0)
            label = cr.get('clause_number', 'N/A')
            if score_val >= 60:
                color = '#dc2626'
            elif score_val >= 30:
                color = '#d97706'
            else:
                color = '#059669'
            heat_cells.append(
                f"<div style='width:48px;height:48px;border-radius:10px;background:{color};"
                f"display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.8rem;font-weight:700;"
                f"box-shadow:0 2px 8px rgba(0,0,0,0.15);transition:all 0.2s ease;cursor:pointer;'"
                f"title='Clause {label}: {score_val}/100'>{label}</div>"
            )
        st.markdown(
            "<div style='display:flex;flex-wrap:wrap;gap:8px;'>" + "".join(heat_cells) + "</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Heatmap will appear after clause risks are calculated.")
    
    # Key concerns
    st.markdown("<div class='section-title'>Primary Risk Drivers</div>", unsafe_allow_html=True)
    concerns = risk.get('key_concerns', [])
    
    if concerns:
        for i, concern in enumerate(concerns[:5], 1):
            with st.expander(f"**{i}.** {concern}"):
                st.markdown("This risk driver appears in multiple clauses. Consider renegotiating or clarifying affected terms to reduce exposure.")
    else:
        st.success("✓ No major concerns identified")
    
    # Mitigation strategies
    st.markdown("<div class='section-title'>Risk Mitigation Strategies</div>", unsafe_allow_html=True)
    strategies = risk.get('mitigation_strategies', [])
    
    for strategy in strategies:
        st.markdown(f"• {strategy}")
    
    st.markdown("</div>", unsafe_allow_html=True)


def display_unfavorable_clauses(report):
    """Display unfavorable clauses requiring attention."""
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.3, 1])
    with col1:
        st.markdown(render_badge('Requires Attention', 'warning'), unsafe_allow_html=True)
    with col2:
        st.header("Unfavorable Clauses")
    
    unfavorable = report.get('unfavorable_clauses', [])
    
    if not unfavorable:
        st.success("✓ No significantly unfavorable clauses detected!")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    st.markdown(
        f"<div class='warning-box'>⚠️ Found **{len(unfavorable)}** clause(s) that may be unfavorable to your business interests.</div>",
        unsafe_allow_html=True
    )
    
    for clause in unfavorable:
        risk_level = clause.get('risk_level', 'Unknown')
        
        # Choose appropriate styling
        if risk_level == 'High':
            container_class = 'risk-high'
        elif risk_level == 'Medium':
            container_class = 'risk-medium'
        else:
            container_class = 'risk-low'
        
        with st.expander(
            f"**Clause {clause.get('clause_number', 'N/A')}:** {clause.get('clause_heading', 'Untitled')} "
            f"— {risk_level} Risk ({clause.get('risk_score', 0)}/100)"
        ):
            # Build entire content as pure HTML for proper alignment
            risks_text = html.escape(clause.get('why_unfavorable', 'N/A'))
            recs = clause.get('recommendations', [])
            rec_items = "".join(f"<li style='margin-bottom:0.5rem;'>{html.escape(rec)}</li>" for rec in recs) or "<li>No recommendations available.</li>"

            content_html = f"""
            <div class='{container_class}'>
                <div class='section-title' style='margin-top:0.5rem; font-size:1.25rem;'>Comparative Analysis</div>
                <div class='two-col'>
                    <div class='card-compact'>
                        <div style='font-size:0.75rem; color:#64748b; margin-bottom:0.75rem; text-transform:uppercase; letter-spacing:0.08em; font-weight:600;'>Current Risk Exposure</div>
                        <div class='legal-text'>{risks_text}</div>
                    </div>
                    <div class='card-compact'>
                        <div style='font-size:0.75rem; color:#64748b; margin-bottom:0.75rem; text-transform:uppercase; letter-spacing:0.08em; font-weight:600;'>Recommended Improvements</div>
                        <ul style='margin:0; padding-left:1.5rem; color:#334155; font-size:0.95rem; line-height:1.7;'>
                            {rec_items}
                        </ul>
                    </div>
                </div>
                <div class='sticky-note' style='margin-top:1rem; padding-left:3rem;'>
                    <strong>Business Value:</strong> These changes reduce financial exposure, improve contractual balance, and provide clearer execution pathways.
                </div>
            </div>
            """
            st.markdown(content_html, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def display_clause_analysis(report):
    """Display detailed clause-by-clause analysis."""
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    st.header("📄 Detailed Clause Analysis")
    
    clauses = report.get('clause_analysis', [])
    
    if not clauses:
        st.warning("No clauses were extracted from the contract.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    st.info(f"**{len(clauses)}** clauses identified and analyzed")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        filter_risk = st.selectbox(
            "Filter by Risk Level",
            ["All", "High", "Medium", "Low"]
        )
    
    with col2:
        show_details = st.checkbox("Show full clause text", value=True)
    
    # Filter clauses
    filtered_clauses = clauses
    if filter_risk != "All":
        filtered_clauses = [c for c in clauses if c.get('risk_level') == filter_risk]
    
    # Display clauses
    for clause in filtered_clauses:
        risk_level = clause.get('risk_level', 'Low')
        risk_score = clause.get('risk_score', 0)
        
        # Color code by risk
        if risk_level == 'High':
            expander_label = f"🔴 **Clause {clause.get('number', 'N/A')}:** {clause.get('heading', 'Untitled')} — Risk Score: {risk_score}/100"
        elif risk_level == 'Medium':
            expander_label = f"🟡 **Clause {clause.get('number', 'N/A')}:** {clause.get('heading', 'Untitled')} — Risk Score: {risk_score}/100"
        else:
            expander_label = f"🟢 **Clause {clause.get('number', 'N/A')}:** {clause.get('heading', 'Untitled')} — Risk Score: {risk_score}/100"
        
        with st.expander(expander_label):
            icons = clause_icons(clause.get('text', ''))
            risk_class = 'low' if risk_level == 'Low' else 'medium' if risk_level == 'Medium' else 'high'
            
            st.markdown(
                f"<div class='pill-row'>"
                f"<span class='risk-tag {risk_class}'>{risk_level} Risk</span>"
                f"<span class='pill'>Score: {risk_score}/100</span>"
                f"<span class='pill'>{icons or '📄 General Clause'}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            # Build cards as pure HTML to maintain flex alignment
            clause_text = clause.get('text', 'No text available')
            
            if show_details:
                highlighted = highlight_risky_phrases(clause_text)
                clause_content = f"<div class='legal-text'>{highlighted}</div>"
            else:
                clause_content = "<div class='small-muted'>Hidden</div>"
            
            plain_lang = html.escape(clause.get('plain_language_summary', 'No summary available'))
            impact_text = html.escape(clause.get('impact_on_sme', 'Impact assessment not available'))
            
            two_column_html = f"""
            <div class='two-col'>
                <div class='card'>
                    <div class='metric-label'>Original Clause Text</div>
                    {clause_content}
                </div>
                <div class='card'>
                    <div class='metric-label'>Plain-Language Interpretation</div>
                    <div class='explain-text'>{plain_lang}</div>
                    <div class='metric-label' style='margin-top:1rem;'>Business Impact</div>
                    <div class='legal-text'>{impact_text}</div>
                </div>
            </div>
            """
            st.markdown(two_column_html, unsafe_allow_html=True)
            
            st.markdown("<div class='section-title' style='font-size:1.25rem;'>Obligations, Rights & Prohibitions</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                obligations = clause.get('obligations', [])
                if obligations:
                    st.markdown("**Your Obligations**")
                    for obl in obligations[:3]:
                        st.markdown(f"• {obl}")
            
            with col2:
                rights = clause.get('rights', [])
                if rights:
                    st.markdown("**Your Rights**")
                    for right in rights[:3]:
                        st.markdown(f"• {right}")
            
            with col3:
                prohibitions = clause.get('prohibitions', [])
                if prohibitions:
                    st.markdown("**Prohibitions**")
                    for proh in prohibitions[:3]:
                        st.markdown(f"• {proh}")
            
            risk_factors = clause.get('risk_factors', [])
            if risk_factors:
                st.markdown("<div class='section-title' style='font-size:1.25rem;'>Identified Risk Factors</div>", unsafe_allow_html=True)
                for factor in risk_factors:
                    st.markdown(
                        f"<div class='warning-box'>{html.escape(factor)}</div>",
                        unsafe_allow_html=True
                    )
            
            ambiguities = clause.get('ambiguities', [])
            if ambiguities:
                st.markdown("<div class='section-title' style='font-size:1.25rem;'>Ambiguities Detected</div>", unsafe_allow_html=True)
                for amb in ambiguities:
                    st.markdown(
                        f"<div class='warning-box'>⚠️ {html.escape(amb)}</div>",
                        unsafe_allow_html=True
                    )
    
    st.markdown("</div>", unsafe_allow_html=True)


def display_entities(report):
    """Display extracted entities."""
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    st.header("🔍 Extracted Key Information")
    
    entities = report.get('entities', {})
    
    if not entities:
        st.info("No entities were extracted from the contract.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    cols = st.columns(2)
    
    col_index = 0
    for entity_type, entity_list in entities.items():
        if entity_list:
            with cols[col_index % 2]:
                # Build card content as pure HTML for proper alignment
                entity_items = "".join(f"<li style='margin-bottom:0.3rem;'>{html.escape(str(item))}</li>" for item in entity_list[:5])
                card_html = f"""
                <div class='card'>
                    <div class='metric-label'>{html.escape(entity_type)}</div>
                    <ul style='margin: 0.75rem 0 0 1.5rem; padding: 0; color: #334155; font-size: 0.95rem; line-height: 1.7;'>
                        {entity_items}
                    </ul>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
            col_index += 1
    
    st.markdown("</div>", unsafe_allow_html=True)


def export_report(report):
    """Provide export options for the report."""
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    st.header("📥 Export Report")
    
    generator = ReportGenerator()
    generator.report_data = report
    
    st.markdown("<div class='section-title'>Executive Summary Preview</div>", unsafe_allow_html=True)
    sme_summary = report.get('sme_summary', {})
    
    # Build card content as pure HTML for proper alignment
    contract_type = html.escape(sme_summary.get('contract_type', 'Unknown'))
    overall_risk = html.escape(sme_summary.get('overall_risk', 'Unknown'))
    summary = html.escape(sme_summary.get('summary', ''))
    
    summary_html = f"""
    <div class='card'>
        <div class='metric-label'>Contract Type</div>
        <div class='metric-value'>{contract_type}</div>
        <div class='metric-label' style='margin-top:1rem;'>Overall Risk Assessment</div>
        <div class='metric-value'>{overall_risk}</div>
        <div class='legal-text' style='margin-top:1rem;'>{summary}</div>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        # Markdown export
        st.markdown("### 📄 Markdown Format")
        st.markdown("<div class='small-muted'>Ideal for documentation and collaboration</div>", unsafe_allow_html=True)
        md_content = generator.export_to_markdown()
        
        st.download_button(
            label="Download Markdown Report",
            data=md_content,
            file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    with col2:
        # JSON export
        st.markdown("### 📊 JSON Format")
        st.markdown("<div class='small-muted'>Machine-readable data export</div>", unsafe_allow_html=True)
        json_content = generator.export_to_json()
        
        st.download_button(
            label="Download JSON Data",
            data=json_content,
            file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    st.markdown("<div class='disclaimer-box'>**Legal Disclaimer:** This analysis is provided for informational purposes only and does not constitute legal advice. All interpretations are based solely on the provided contract text. Please consult with a qualified legal professional before making any business decisions.</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Main application."""
    initialize_session_state()
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔒 Privacy & Security")
        st.markdown(render_badge("Confidential Processing", "trust"), unsafe_allow_html=True)
        st.markdown("<div class='small-muted'>Your documents remain secure on this device. No external APIs or data transmission.</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📄 Supported Formats")
        st.markdown("• PDF Documents  \n• Microsoft Word (DOCX/DOC)  \n• Plain Text (TXT)")
        
        st.markdown("---")
        
        # How to use (short manual)
        st.markdown("### ✅ Quick Start Guide")
        st.markdown("""
        **1.** Upload your contract document  
        **2.** Click **Analyze Contract**  
        **3.** Review comprehensive analysis  
        **4.** Export report for your records
        """)
        
        st.markdown("---")
        st.markdown("<div class='small-muted'><strong>Version:</strong> 1.0.0  \n<strong>Last Updated:</strong> February 2026</div>", unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.analysis_complete and st.session_state.report:
        report = st.session_state.report

        with st.expander("📁 Analyze Another Contract", expanded=False):
            st.markdown("<div class='upload-zone'>", unsafe_allow_html=True)
            new_file = st.file_uploader(
                "Upload a new contract document",
                type=['pdf', 'docx', 'doc', 'txt'],
                key="new_contract_upload",
                label_visibility="collapsed"
            )
            st.markdown("<div class='small-muted' style='text-align:center; margin-top:0.5rem;'>PDF, DOCX, DOC, or TXT • Secure & confidential processing</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if new_file is not None:
                if st.button("Analyze New Contract", type="primary"):
                    new_report = analyze_contract(new_file)
                    if new_report:
                        st.session_state.report = new_report
                        st.session_state.analysis_complete = True
                        st.rerun()
        
        # Create tabs for different sections
        tabs = st.tabs([
            "📋 Executive Summary",
            "⚠️ Risk Assessment",
            "🚨 Unfavorable Clauses",
            "📄 Clause Analysis",
            "🔍 Extracted Data",
            "📥 Export Report"
        ])
        
        with tabs[0]:
            display_sme_summary(report)
        
        with tabs[1]:
            display_risk_assessment(report)
        
        with tabs[2]:
            display_unfavorable_clauses(report)
        
        with tabs[3]:
            display_clause_analysis(report)
        
        with tabs[4]:
            display_entities(report)
        
        with tabs[5]:
            export_report(report)
        
    else:
        st.markdown("<div class='confidential-watermark'></div>", unsafe_allow_html=True)
        tape_text = (
            "This tool provides informational analysis only and does not constitute legal advice. "
            "Please consult a qualified legal professional before making business decisions."
        )
        st.markdown(
            "<div class='warning-tape'>"
            "  <div class='warning-tape-inner'>"
            "    <div class='warning-tape-track'>"
            f"      <span class='warning-tape-text'>{tape_text}</span>"
            f"      <span class='warning-tape-text'>{tape_text}</span>"
            f"      <span class='warning-tape-text'>{tape_text}</span>"
            "    </div>"
            "    <div class='warning-tape-track'>"
            f"      <span class='warning-tape-text'>{tape_text}</span>"
            f"      <span class='warning-tape-text'>{tape_text}</span>"
            f"      <span class='warning-tape-text'>{tape_text}</span>"
            "    </div>"
            "  </div>"
            "</div>",
            unsafe_allow_html=True
        )
        
        st.markdown("<div class='section-title' style='text-align:center; margin-top:2rem;'>Upload Your Contract</div>", unsafe_allow_html=True)
        st.markdown("<div class='upload-zone'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag and drop your contract document here",
            type=['pdf', 'docx', 'doc', 'txt'],
            help="Upload your contract in PDF, DOCX, or TXT format for professional analysis",
            key="landing_upload",
            label_visibility="collapsed"
        )
        st.markdown("<div class='small-muted' style='text-align:center; margin-top:1rem;'>Supported formats: PDF, DOCX, DOC, TXT</div>", unsafe_allow_html=True)
        st.markdown("<div class='small-muted' style='text-align:center;'>🔐 Your documents are processed locally and never stored</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded_file is not None:
            st.success(f"✓ File uploaded successfully: **{uploaded_file.name}**")
            if st.button("🚀 Analyze Contract", type="primary"):
                report = analyze_contract(uploaded_file)
                if report:
                    st.session_state.report = report
                    st.session_state.analysis_complete = True
                    st.rerun()



if __name__ == "__main__":
    main()