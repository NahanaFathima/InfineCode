import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from predict import predict_eligibility

# --- Page Configuration ---
st.set_page_config(
    page_title="NGO Eligibility Analyzer",
    page_icon="🤝",
    layout="wide"
)

# --- Custom CSS Styling ---
st.markdown("""
<style>
    :root {
        --bg-0: #07111f;
        --bg-1: #0d1728;
        --bg-2: #14233b;
        --card: rgba(10, 18, 34, 0.78);
        --card-border: rgba(148, 163, 184, 0.14);
        --text-main: #eef2ff;
        --text-muted: #a8b3cf;
        --accent: #4dd7ff;
        --accent-2: #8b5cf6;
        --success: #34d399;
        --danger: #fb7185;
        --warning: #f8c15a;
    }

    html, body, [class*="css"] {
        font-family: "Segoe UI", "Trebuchet MS", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(77, 215, 255, 0.12), transparent 32%),
            radial-gradient(circle at top right, rgba(139, 92, 246, 0.16), transparent 34%),
            linear-gradient(135deg, var(--bg-0), var(--bg-1) 45%, var(--bg-2));
        color: var(--text-main);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(12, 20, 35, 0.98), rgba(15, 26, 46, 0.96));
        border-right: 1px solid rgba(77, 215, 255, 0.16);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--text-main);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(77, 215, 255, 0.15) !important;
        margin: 1rem 0;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.55rem;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label {
        border-radius: 16px;
        padding: 0.55rem 0.85rem;
        border: 1px solid rgba(148, 163, 184, 0.12);
        background: rgba(255, 255, 255, 0.03);
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        border-color: rgba(77, 215, 255, 0.35);
        background: rgba(77, 215, 255, 0.08);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        border-color: rgba(77, 215, 255, 0.55);
        background: linear-gradient(135deg, rgba(77, 215, 255, 0.16), rgba(139, 92, 246, 0.16));
        box-shadow: 0 0 0 1px rgba(77, 215, 255, 0.08) inset;
    }

    [data-testid="stSidebar"] .sidebar-shell {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 24px;
        padding: 1.25rem 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }

    .sidebar-tag {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.35rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(77, 215, 255, 0.1);
        border: 1px solid rgba(77, 215, 255, 0.18);
        color: var(--accent);
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-top: 0.75rem;
    }

    .main-title {
        text-align: center;
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.05;
        background: linear-gradient(90deg, #9be8ff, #7dd3fc, #c084fc, #fda4af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.35rem 0 0.5rem;
        letter-spacing: 0.04em;
    }
    .subtitle {
        text-align: center;
        color: var(--text-muted);
        font-size: 1.02rem;
        margin-bottom: 1.7rem;
    }
    .metric-card {
        background: linear-gradient(180deg, rgba(20, 35, 59, 0.9), rgba(10, 18, 34, 0.95));
        border: 1px solid rgba(77, 215, 255, 0.18);
        border-radius: 20px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
        margin: 0.25rem;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--accent);
    }
    .metric-label {
        font-size: 0.82rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .result-eligible {
        background: linear-gradient(135deg, rgba(16, 60, 44, 0.92), rgba(14, 90, 63, 0.92));
        border: 1px solid rgba(52, 211, 153, 0.5);
        border-radius: 24px;
        padding: 1.8rem;
        text-align: center;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.24);
        margin: 20px 0;
    }
    .result-not-eligible {
        background: linear-gradient(135deg, rgba(61, 15, 25, 0.92), rgba(92, 26, 38, 0.92));
        border: 1px solid rgba(251, 113, 133, 0.5);
        border-radius: 24px;
        padding: 1.8rem;
        text-align: center;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.24);
        margin: 20px 0;
    }
    .result-text { font-size: 2.3rem; font-weight: 800; margin: 0; letter-spacing: 0.03em; }
    .eligible-text { color: var(--success); }
    .not-eligible-text { color: var(--danger); }
    .confidence-container {
        background: rgba(10, 18, 34, 0.84);
        border-radius: 18px;
        padding: 1.1rem;
        border: 1px solid var(--card-border);
        margin: 15px 0;
    }
    .confidence-label {
        color: var(--text-muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 8px;
    }
    .confidence-value { font-size: 2rem; font-weight: 800; color: var(--warning); }
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text-main);
        border-bottom: 1px solid rgba(77, 215, 255, 0.18);
        padding-bottom: 0.7rem;
        margin: 1.2rem 0 1rem;
    }
    .info-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-left: 4px solid var(--accent-2);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin: 0.75rem 0;
        color: #dbe4ff;
        backdrop-filter: blur(10px);
    }
    .stButton > button {
        background: linear-gradient(90deg, #6d28d9, #0ea5e9);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.9rem 1.4rem;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        width: 100%;
        box-shadow: 0 14px 30px rgba(14, 165, 233, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 34px rgba(14, 165, 233, 0.32);
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: var(--text-main) !important;
        border: 1px solid rgba(148, 163, 184, 0.16) !important;
        border-radius: 14px !important;
    }

    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: var(--text-main) !important;
        font-weight: 600 !important;
    }

    .stDataFrame, [data-testid="stDataFrame"] {
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        overflow: hidden;
    }

    .stAlert {
        border-radius: 18px;
    }

    footer, #MainMenu, header {
        visibility: hidden;
    }

    .app-shell {
        max-width: 1240px;
        margin: 0 auto;
    }

    .hero-panel {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 28px;
        padding: 1.5rem 1.3rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 20px 48px rgba(0, 0, 0, 0.22);
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(139, 92, 246, 0.14);
        border: 1px solid rgba(139, 92, 246, 0.2);
        color: #ddd6fe;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("""
<div class='sidebar-shell'>
    <div style='text-align:center;'>
        <div style='font-size:3rem; line-height:1;'>🤝</div>
        <div style='margin-top:0.4rem; font-weight:800; font-size:1.02rem; letter-spacing:0.14em; color:#eaf2ff;'>NGO ANALYZER</div>
        <div style='color:var(--text-muted); font-size:0.84rem; margin-top:0.35rem;'>AI-Powered Eligibility System</div>
        <div class='sidebar-tag'>Operational Dashboard</div>
    </div>
    <hr>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigate", [
    "🏠  Home",
    "🔍  Check Eligibility",
    "📊  Analytics Dashboard",
    "📈  Visualizations",
    "📋  View Dataset"
], label_visibility="collapsed")

st.sidebar.markdown("""
    <hr>
    <div style='display:grid; gap:0.65rem;'>
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(148,163,184,0.12); border-radius:16px; padding:0.8rem 0.9rem;'>
            <div style='color:#eaf2ff; font-weight:700; font-size:0.92rem;'>Model Status</div>
            <div style='color:var(--success); margin-top:0.25rem; font-size:0.82rem;'>● Random Forest active</div>
        </div>
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(148,163,184,0.12); border-radius:16px; padding:0.8rem 0.9rem;'>
            <div style='color:#eaf2ff; font-weight:700; font-size:0.92rem;'>Quick Tip</div>
            <div style='color:var(--text-muted); margin-top:0.25rem; font-size:0.82rem;'>Use the eligibility form to score a single applicant in seconds.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PAGE 1: HOME
# ============================================================
if page == "🏠  Home":
    st.markdown('<div class="main-title">NGO Beneficiary Eligibility Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-powered system to identify and support those who need it most</div>', unsafe_allow_html=True)

    df = pd.read_csv("data/beneficiaries.csv")
    eligible = int((df["eligibility_status"] == "Eligible").sum())
    not_eligible = int((df["eligibility_status"] == "Not Eligible").sum())
    avg_income = int(df["family_income"].mean())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total Applicants</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-color:#00ff8844;"><div class="metric-value" style="color:#00ff88;">{eligible}</div><div class="metric-label">Eligible</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="border-color:#ff444444;"><div class="metric-value" style="color:#ff4444;">{not_eligible}</div><div class="metric-label">Not Eligible</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card" style="border-color:#f0c04044;"><div class="metric-value" style="color:#f0c040;">₹{avg_income:,}</div><div class="metric-label">Avg Income</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📌 Support Programs Available</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-card">🎓 <b>Educational Scholarships</b><br><span style="color:#a0a0c0;">Supporting students from low-income families</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">🏥 <b>Medical Aid</b><br><span style="color:#a0a0c0;">Healthcare support for disabled and underprivileged</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card">🍱 <b>Food Assistance</b><br><span style="color:#a0a0c0;">Nutrition support for vulnerable families</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">💼 <b>Skill Development</b><br><span style="color:#a0a0c0;">Training programs for unemployed individuals</span></div>', unsafe_allow_html=True)

# ============================================================
# PAGE 2: CHECK ELIGIBILITY
# ============================================================
elif page == "🔍  Check Eligibility":
    st.markdown('<div class="main-title">Check Eligibility</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enter applicant details to get an AI-powered prediction</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-header">👤 Personal Details</div>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        family_income = st.number_input("Family Income (₹)", min_value=0, value=120000, step=10000)
        family_members = st.number_input("Family Members", min_value=1, max_value=20, value=4)
    with col2:
        st.markdown('<div class="section-header">📋 Background Details</div>', unsafe_allow_html=True)
        employment_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Self-Employed", "Student"])
        education_level = st.selectbox("Education Level", ["No Education", "Primary", "Secondary", "Undergraduate", "Postgraduate"])
        disability_status = st.selectbox("Disability Status", ["No", "Yes"])

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔍  ANALYZE ELIGIBILITY")

    if predict_btn:
        with st.spinner("Analyzing applicant profile..."):
            prediction, confidence = predict_eligibility(
                age=age, family_income=family_income, family_members=family_members,
                employment_status=employment_status, education_level=education_level,
                disability_status=disability_status
            )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            if prediction == "Eligible":
                st.markdown(f"""
                <div class="result-eligible">
                    <div style="font-size:3em;">✅</div>
                    <div class="result-text eligible-text">ELIGIBLE</div>
                    <div style="color:#a0ffc8; margin-top:10px;">This applicant qualifies for NGO support</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-not-eligible">
                    <div style="font-size:3em;">❌</div>
                    <div class="result-text not-eligible-text">NOT ELIGIBLE</div>
                    <div style="color:#ffa0a0; margin-top:10px;">This applicant does not meet the criteria</div>
                </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="confidence-container">
                <div class="confidence-label">AI Confidence</div>
                <div class="confidence-value">{confidence*100:.1f}%</div>
                <div style="background:#ffffff22; border-radius:10px; height:10px; margin-top:10px;">
                    <div style="background:linear-gradient(90deg,#7b2ff7,#00d4ff);
                                width:{confidence*100:.1f}%; height:10px; border-radius:10px;"></div>
                </div>
            </div>
            <div class="confidence-container">
                <div class="confidence-label">Applicant Summary</div>
                <div style="color:#e0e0f0; font-size:0.9em; margin-top:10px; line-height:1.8;">
                    👤 Age: {age}<br>
                    💰 Income: ₹{family_income:,}<br>
                    👨‍👩‍👧 Members: {family_members}<br>
                    💼 {employment_status}<br>
                    🎓 {education_level}<br>
                    ♿ Disability: {disability_status}
                </div>
            </div>""", unsafe_allow_html=True)

# ============================================================
# PAGE 3: ANALYTICS DASHBOARD
# ============================================================
elif page == "📊  Analytics Dashboard":
    st.markdown('<div class="main-title">Analytics Dashboard</div>', unsafe_allow_html=True)
    df = pd.read_csv("data/beneficiaries.csv")
    eligible = int((df["eligibility_status"] == "Eligible").sum())
    not_eligible = int((df["eligibility_status"] == "Not Eligible").sum())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-color:#00ff8844;"><div class="metric-value" style="color:#00ff88;">{eligible}</div><div class="metric-label">Eligible</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="border-color:#ff444444;"><div class="metric-value" style="color:#ff4444;">{not_eligible}</div><div class="metric-label">Not Eligible</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card" style="border-color:#f0c04044;"><div class="metric-value" style="color:#f0c040;">₹{int(df["family_income"].mean()):,}</div><div class="metric-label">Avg Income</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Eligibility Split</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        counts = df["eligibility_status"].value_counts()
        wedges, texts, autotexts = ax.pie(counts, labels=counts.index, autopct="%1.1f%%",
               colors=["#00ff88", "#ff4444"], wedgeprops=dict(width=0.6), startangle=90)
        for t in texts: t.set_color('#e0e0f0')
        for a in autotexts: a.set_color('white')
        st.pyplot(fig)
    with col2:
        st.markdown('<div class="section-header">Employment Breakdown</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        emp_counts = df["employment_status"].value_counts()
        ax.bar(emp_counts.index, emp_counts.values, color=["#00d4ff", "#7b2ff7", "#00ff88", "#ff6b6b"])
        ax.tick_params(colors='#a0a0c0')
        for spine in ['top','right']: ax.spines[spine].set_visible(False)
        for spine in ['bottom','left']: ax.spines[spine].set_color('#ffffff22')
        plt.xticks(rotation=15, color='#a0a0c0')
        plt.yticks(color='#a0a0c0')
        st.pyplot(fig)

# ============================================================
# PAGE 4: VISUALIZATIONS
# ============================================================
elif page == "📈  Visualizations":
    st.markdown('<div class="main-title">Data Visualizations</div>', unsafe_allow_html=True)
    import os
    charts_dir = "data/charts"
    if os.path.exists(charts_dir):
        charts = os.listdir(charts_dir)
        for i in range(0, len(charts), 2):
            col1, col2 = st.columns(2)
            with col1:
                name = charts[i].replace("_", " ").replace(".png", "").title()
                st.markdown(f'<div class="section-header">{name}</div>', unsafe_allow_html=True)
                st.image(f"{charts_dir}/{charts[i]}", use_column_width=True)
            if i + 1 < len(charts):
                with col2:
                    name = charts[i+1].replace("_", " ").replace(".png", "").title()
                    st.markdown(f'<div class="section-header">{name}</div>', unsafe_allow_html=True)
                    st.image(f"{charts_dir}/{charts[i+1]}", use_column_width=True)
    else:
        st.warning("No charts found. Run visualize.py first!")

# ============================================================
# PAGE 5: VIEW DATASET
# ============================================================
elif page == "📋  View Dataset":
    st.markdown('<div class="main-title">Beneficiary Dataset</div>', unsafe_allow_html=True)
    df = pd.read_csv("data/beneficiaries.csv")

    col1, col2 = st.columns([1, 3])
    with col1:
        filter_eligibility = st.selectbox("Filter by Eligibility", ["All", "Eligible", "Not Eligible"])
    with col2:
        search = st.text_input("Search by Name", "")

    if filter_eligibility != "All":
        df = df[df["eligibility_status"] == filter_eligibility]
    if search:
        df = df[df["applicant_name"].str.contains(search, case=False)]

    st.markdown(f'<div style="color:#a0a0c0; margin-bottom:10px;">Showing <span style="color:#00d4ff;">{len(df)}</span> records</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=500)