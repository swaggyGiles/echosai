import streamlit as st
from pathlib import Path
from utils.storage import list_patients, add_eeg_record

from utils.ui import apply_theme, sidebar_brand, page_hero

apply_theme()
sidebar_brand()
page_hero("〰️", "EEG DATA WORKFLOW", "EEG Upload", "Import EEG recordings, add signal metadata, and organize each study in one place.", "#7C3AED")

st.caption("Upload an EEG file and save its metadata. Model inference is not performed on this page.")
patients = list_patients()
if not patients:
    st.warning("Create a patient/study code first in Patient Management.")
else:
    patient_options = {f'{p["patient_id"]} — {p["display_name"]}':p["patient_id"] for p in patients}
    with st.form("upload_form"):
        patient_label = st.selectbox("Patient / study code", list(patient_options))
        uploaded = st.file_uploader("Choose EEG file", type=["edf","bdf","csv","txt","npy","mat"])
        a,b = st.columns(2)
        with a:
            file_type = st.selectbox("File format", ["EDF","BDF","CSV","TXT","NPY","MAT","Other"])
            sampling_rate = st.number_input("Sampling rate (Hz)", min_value=0.0, value=0.0, step=1.0)
        with b:
            channels = st.text_input("Channels (optional)", placeholder="e.g. Fp1, Fp2, F3, F4")
            duration = st.number_input("Duration in seconds (optional)", min_value=0.0, value=0.0, step=1.0)
        notes = st.text_area("Notes (optional)")
        submit = st.form_submit_button("Save EEG record", use_container_width=True)
    if submit:
        if uploaded is None:
            st.error("Please choose an EEG file.")
        else:
            folder = Path("data") / "uploads"; folder.mkdir(parents=True, exist_ok=True)
            safe_name = Path(uploaded.name).name
            dest = folder / safe_name
            if dest.exists(): dest = folder / f"{dest.stem}_{uploaded.size}{dest.suffix}"
            dest.write_bytes(uploaded.getbuffer())
            rid = add_eeg_record(patient_options[patient_label], uploaded.name, str(dest), file_type,
              sampling_rate or None, channels, duration or None, notes)
            st.success(f"Record saved. Record ID: {rid}")
            st.info("This is metadata/file storage only. Connect your team's model later to analyse EEG data.")
