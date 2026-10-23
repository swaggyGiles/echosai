import streamlit as st
from utils.storage import list_patients, add_patient

from utils.ui import apply_theme, sidebar_brand, page_hero

apply_theme()
sidebar_brand()
page_hero("👥", "CLINICAL RECORDS", "Patient Management", "Create and manage patient or study codes for your EEG research workflow.", "#0D9488")

st.caption("Development register. Use fictional demo data until privacy, ethics and security requirements are agreed.")
with st.expander("➕ Add patient / study code", expanded=True):
    with st.form("patient_form", clear_on_submit=True):
        name = st.text_input("Display name or study code", placeholder="e.g. DEMO-001")
        a,b = st.columns(2)
        with a: age = st.number_input("Age (optional)", min_value=0, max_value=120, value=0)
        with b: sex = st.selectbox("Sex (optional)", ["Not specified","Female","Male","Other"])
        notes = st.text_area("Notes (optional)")
        submit = st.form_submit_button("Save patient", use_container_width=True)
    if submit:
        if not name.strip(): st.error("Enter a display name or study code.")
        else:
            pid = add_patient(name.strip(), age or None, None if sex=="Not specified" else sex, notes.strip())
            st.success(f"Patient record created: #{pid}")
            st.rerun()
patients = list_patients()
st.markdown(f"### Patient list ({len(patients)})")
if patients:
    st.dataframe([{"ID":p["patient_id"],"Display name / code":p["display_name"],
      "Age":p["age"] if p["age"] is not None else "—","Sex":p["sex"] or "—",
      "Created":p["created_at"],"Notes":p["notes"]} for p in patients],
      use_container_width=True, hide_index=True)
else: st.info("No patients have been added.")
