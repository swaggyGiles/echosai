import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .stApp {background: linear-gradient(135deg,#F5F7FF,#F0FDFA);}
    [data-testid="stSidebar"] {background: linear-gradient(165deg,#111B3C,#243B78,#164E63);}
    [data-testid="stSidebar"] * {color:#F4F8FF;}
    .hero {padding:30px;border-radius:24px;color:white;background:linear-gradient(112deg,#172554,#4338CA,#2563EB,#0891B2);margin-bottom:22px}
    .hero-title {font-size:35px;font-weight:800;color:white}
    .hero-kicker {font-size:11px;font-weight:800;letter-spacing:.18em;color:#BDEBFF}
    .hero-copy {color:#DDEBFF}
    .section-label {font-size:12px;color:#4F46E5;font-weight:800;letter-spacing:.14em;margin:22px 0 10px}
    .feature-card {background:white;border:1px solid #DCE7F5;border-radius:17px;padding:18px;min-height:120px}
    .feature-icon {font-size:24px}.feature-title {font-weight:800;color:#17345B}.feature-copy {color:#6A7F98;font-size:12px}
    </style>
    """, unsafe_allow_html=True)

def sidebar_brand():
    with st.sidebar:
        st.markdown("## 🧠 EchoesAI")
        st.caption("Cognitive Decision Support")
        st.divider()
        st.caption("EEG workflow • Prototype")
        st.caption("AI inference not connected")

def page_hero(icon, kicker, title, description, accent="#4F46E5"):
    st.markdown(f"""
    <div class="hero">
      <div class="hero-kicker">{kicker}</div>
      <div class="hero-title">{icon} {title}</div>
      <p class="hero-copy">{description}</p>
    </div>
    """, unsafe_allow_html=True)
