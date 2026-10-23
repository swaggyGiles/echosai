
import streamlit as st
from utils.storage import init_storage, list_patients, list_eeg_records, list_predictions
from utils.ui import apply_theme, sidebar_brand

st.set_page_config(page_title="EchoesAI | EEG Decision Support", page_icon="🧠", layout="wide")
apply_theme()
init_storage()
sidebar_brand()

st.markdown("""
<div class="hero">
  <div class="hero-kicker">AI-assisted EEG platform</div>
  <div class="hero-title">Better insight from<br>brainwave data.</div>
  <p class="hero-copy">A unified workspace for EEG records, model-assisted prediction workflows and clear reporting — designed for research and clinical decision support.</p>
</div>
""", unsafe_allow_html=True)

patients, records, predictions = list_patients(), list_eeg_records(), list_predictions()
st.markdown('<div class="section-label">✦ Workspace overview</div>', unsafe_allow_html=True)
a, b, c = st.columns(3)
a.metric("👥  Patient records", len(patients), help="Local development records")
b.metric("〰️  EEG recordings", len(records), help="Uploaded EEG files registered in this workspace")
c.metric("🧠  Prediction records", len(predictions), help="Stored prediction entries, including placeholders")

st.markdown('<div class="section-label">🎨 Explore your workspace</div>', unsafe_allow_html=True)
cols = st.columns(3)
cards = [
    ("📤", "EEG Upload", "Register EEG files and capture sampling details.", "pages/2_EEG_Upload.py"),
    ("🤖", "AI Prediction", "Review prediction history and prepare for model integration.", "pages/3_AI_Prediction.py"),
    ("👥", "Patient Management", "Organise patient or study-code records.", "pages/4_Patient_Management.py"),
]
for col, (icon, title, desc, path) in zip(cols, cards):
    with col:
        st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-copy">{desc}</div></div>', unsafe_allow_html=True)
        st.page_link(path, label=f"Open {title} →")

st.markdown('<div class="section-label">⚡ Recommended workflow</div>', unsafe_allow_html=True)
w1, w2, w3, w4 = st.columns(4)
for col, number, title, desc in [
    (w1, "01", "Register", "Create a patient or study code."),
    (w2, "02", "Upload", "Add EEG data and metadata."),
    (w3, "03", "Predict", "Connect the trained CNN-LSTM model."),
    (w4, "04", "Report", "Export a structured summary."),
]:
    with col:
        st.markdown(f'<div class="feature-card" style="min-height:112px"><div style="font-size:11px;font-weight:800;color:#2563EB;letter-spacing:.1em">{number}</div><div class="feature-title" style="margin-top:7px">{title}</div><div class="feature-copy">{desc}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="footer-note">EchoesAI is currently a software prototype. AI inference is not connected, and this system is not clinically validated for diagnosis.</div>', unsafe_allow_html=True)
