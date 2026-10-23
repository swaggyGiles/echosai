import streamlit as st
from utils.storage import list_eeg_records, list_predictions, add_prediction

from utils.ui import apply_theme, sidebar_brand, page_hero

apply_theme()
sidebar_brand()
page_hero("🤖", "AI-ASSISTED INSIGHTS", "AI Prediction", "Review the prediction workflow and saved demo results. Real model inference is not connected yet.", "#DB2777")

st.caption("CNN-LSTM integration placeholder. No XAI module.")
records = list_eeg_records()
if not records:
    st.info("Upload an EEG record first.")
else:
    options = {f'#{r["record_id"]} — {r["original_filename"]} — {r["patient_name"] or "Unassigned"}':r for r in records}
    label = st.selectbox("Select EEG record", list(options))
    st.warning("Demo mode: this action saves a placeholder only. It does not analyse EEG data or generate a real prediction.")
    if st.button("Create demo placeholder", use_container_width=True):
        r = options[label]
        pid = add_prediction(r["record_id"], "not-connected", "Not evaluated", None,
                             {"message":"CNN-LSTM model not connected"}, "demo-placeholder")
        st.success(f"Placeholder saved (ID: {pid}). No clinical prediction was made.")

st.markdown("### 🧬 Prediction history")
preds = list_predictions()
if preds:
    st.dataframe([{"ID":p["prediction_id"],"Patient":p["patient_name"] or "Unknown",
      "EEG file":p["original_filename"] or "Unknown","Result":p["predicted_class"],
      "Confidence":f'{p["confidence"]:.1%}' if p["confidence"] is not None else "Not available",
      "Model":p["model_version"],"Status":p["status"],"Created":p["created_at"]} for p in preds],
      use_container_width=True, hide_index=True)
else: st.info("Prediction history is empty.")
