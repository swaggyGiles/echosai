import streamlit as st
from datetime import datetime
from utils.storage import list_eeg_records, list_predictions

from utils.ui import apply_theme, sidebar_brand, page_hero

apply_theme()
sidebar_brand()
page_hero("📑", "REPORTS & EXPORTS", "Report Generation", "Prepare a downloadable summary for a selected EEG record and its saved results.", "#D97706")

st.caption("Download a basic summary of an EEG record and any saved prediction.")
records, predictions = list_eeg_records(), list_predictions()
if not records:
    st.info("Upload an EEG record first.")
else:
    options = {f'#{r["record_id"]} — {r["original_filename"]} — {r["patient_name"] or "Unassigned"}':r for r in records}
    label = st.selectbox("EEG record", list(options))
    r = options[label]
    matched = [p for p in predictions if p["record_id"] == r["record_id"]]
    latest = matched[0] if matched else None
    report = f"""# EchoesAI — EEG Record Summary

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Record ID: {r["record_id"]}
Patient / study code: {r["patient_name"] or "Unassigned"}
EEG filename: {r["original_filename"]}
File format: {r["file_type"] or "Not specified"}
Sampling rate (Hz): {r["sampling_rate"] or "Not specified"}
Channels: {r["channels"] or "Not specified"}
Duration (seconds): {r["duration_seconds"] or "Not specified"}

## AI prediction
"""
    if latest:
        report += f'Latest stored result: {latest["predicted_class"]}\nModel version: {latest["model_version"]}\nStatus: {latest["status"]}\n'
    else: report += "No prediction is recorded for this EEG file.\n"
    report += """
## Important notice
This prototype is for software development and research workflow demonstration only.
It is not a clinically validated diagnostic tool. Results must not replace assessment by a qualified healthcare professional.
"""
    st.text_area("Report preview", report, height=340)
    st.download_button("Download report (.md)", report.encode("utf-8"),
      file_name=f"echoesai_record_{r['record_id']}_report.md", mime="text/markdown", use_container_width=True)
