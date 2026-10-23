
import streamlit as st
from utils.storage import list_patients, list_eeg_records, list_predictions

from utils.ui import apply_theme, sidebar_brand, page_hero

apply_theme()
sidebar_brand()
page_hero("📊", "LIVE OVERVIEW", "Dashboard", "A colorful overview of your patient records, EEG uploads, and AI workflow status.", "#4F46E5")

st.caption("A live overview of records saved in this development workspace.")
patients, records, predictions = list_patients(), list_eeg_records(), list_predictions()
a,b,c = st.columns(3)
a.metric("👥 Patients", len(patients))
b.metric("〰️ EEG records", len(records))
c.metric("🧠 Predictions", len(predictions))

st.markdown('<div class="section-label">🧠 Recent EEG records</div>', unsafe_allow_html=True)
if records:
    st.dataframe([{"Record ID":r["record_id"],"Patient":r["patient_name"] or "Unassigned",
      "File":r["original_filename"],"Type":r["file_type"],"Uploaded":r["uploaded_at"]} for r in records[:10]],
      use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="feature-card"><div class="feature-title">No EEG records yet</div><div class="feature-copy">Start by adding a patient or study code, then upload an EEG file.</div></div>', unsafe_allow_html=True)
    st.page_link("pages/2_EEG_Upload.py", label="Go to EEG Upload →")

st.markdown('<div class="section-label">✨ Recent predictions</div>', unsafe_allow_html=True)
if predictions:
    st.dataframe([{"ID":p["prediction_id"],"Patient":p["patient_name"] or "Unknown",
      "File":p["original_filename"] or "Unknown","Result":p["predicted_class"],
      "Confidence":f'{p["confidence"]:.1%}' if p["confidence"] is not None else "—",
      "Status":p["status"]} for p in predictions[:10]], use_container_width=True, hide_index=True)
else:
    st.info("Prediction history will appear here after records are created. Real model inference is not connected yet.")

