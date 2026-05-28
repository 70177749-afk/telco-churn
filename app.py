"""
app.py — Main Streamlit Dashboard: Telco Customer Churn Analysis
Course  : Exploratory Data Analysis
Instructor: Ali Hassan Sherazi
"""

import streamlit as st
import pandas as pd

from filters import load_data, apply_filters, compute_kpis
import charts as ch

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .dashboard-header {
        background: linear-gradient(135deg, #1A73E8 0%, #0D47A1 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        color: white;
    }
    .dashboard-header h1 {
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        color: white !important;
    }
    .dashboard-header p { margin: 0; font-size: 1.05rem; opacity: 0.88; }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 18px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 5px solid #1A73E8;
        margin-bottom: 4px;
    }
    .kpi-label { font-size: 0.78rem; color: #7F8C8D; text-transform: uppercase; letter-spacing: 0.06em; }
    .kpi-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #1C1C2E; line-height: 1.1; }

    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #1C1C2E;
        border-bottom: 2px solid #1A73E8;
        padding-bottom: 6px;
        margin: 20px 0 16px 0;
    }
    .stPlotlyChart, .stImage { border-radius: 12px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    search_text = st.text_input("🔎 Search / Text Filter", value="",
                                placeholder="Type any keyword…")

    gender_opts = sorted(df["gender"].unique().tolist())
    gender = st.multiselect("👤 Gender", gender_opts, default=gender_opts)

    contract_opts = sorted(df["Contract"].unique().tolist())
    contract = st.multiselect("📄 Contract Type", contract_opts, default=contract_opts)

    internet_opts = sorted(df["InternetService"].unique().tolist())
    internet_service = st.multiselect("🌐 Internet Service", internet_opts, default=internet_opts)

    senior_opts = ["Non-Senior", "Senior"]
    senior = st.multiselect("🧓 Senior Citizen", senior_opts, default=senior_opts)

    tenure_min, tenure_max = int(df["tenure"].min()), int(df["tenure"].max())
    tenure_range = st.slider("📅 Tenure Range (months)",
                             tenure_min, tenure_max, (tenure_min, tenure_max))

    charge_min = float(df["MonthlyCharges"].min())
    charge_max = float(df["MonthlyCharges"].max())
    monthly_range = st.slider("💲 Monthly Charges ($)",
                              charge_min, charge_max,
                              (charge_min, charge_max), step=0.5)

    st.markdown("---")
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# ── Apply Filters ─────────────────────────────────────────────────────────────
fdf = apply_filters(
    df,
    gender=gender,
    contract=contract,
    internet_service=internet_service,
    senior=senior,
    tenure_range=tenure_range,
    monthly_range=monthly_range,
    search_text=search_text,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="dashboard-header">
        <h1>📡 Telco Customer Churn Dashboard</h1>
        <p>Interactive analysis of customer behaviour, service usage, and churn drivers
        — all charts update dynamically with sidebar filters.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if fdf.empty:
    st.warning("⚠️ No records match the current filter criteria. Please adjust the filters.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpis = compute_kpis(fdf)
icons = ["👥", "🚪", "📉", "💰", "📅", "💳"]
kpi_items = list(kpis.items())

cols = st.columns(6)
for col, icon, (label, value) in zip(cols, icons, kpi_items):
    with col:
        st.markdown(
            f"""<div class="kpi-card">
                    <div class="kpi-label">{icon} {label}</div>
                    <div class="kpi-value">{value:,}</div>
                </div>""",
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

# ── Section 1 — Distribution ──────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Distribution Analysis</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.pyplot(ch.pie_churn(fdf), use_container_width=True)
with c2:
    st.pyplot(ch.histogram_monthly(fdf), use_container_width=True)
with c3:
    st.pyplot(ch.count_internet_service(fdf), use_container_width=True)

# ── Section 2 — Trends ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Trend Analysis</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.pyplot(ch.line_tenure_charges(fdf), use_container_width=True)
with c2:
    st.pyplot(ch.area_tenure_group(fdf), use_container_width=True)

# ── Section 3 — Comparisons & Relationships ───────────────────────────────────
st.markdown('<div class="section-title">📉 Comparisons & Relationships</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.pyplot(ch.bar_contract_churn(fdf), use_container_width=True)
with c2:
    st.pyplot(ch.scatter_tenure_total(fdf), use_container_width=True)

# ── Section 4 — Statistical Distributions ─────────────────────────────────────
st.markdown('<div class="section-title">🎻 Statistical Distributions</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.pyplot(ch.box_monthly_churn(fdf), use_container_width=True)
with c2:
    st.pyplot(ch.violin_tenure_churn(fdf), use_container_width=True)
with c3:
    st.pyplot(ch.heatmap_correlation(fdf), use_container_width=True)

# ── Section 5 — Bonus Pair Plot ───────────────────────────────────────────────
with st.expander("🔬 Bonus: Pair Plot (Numerical Feature Relationships)", expanded=False):
    st.info("This chart may take a few seconds to render with large datasets.")
    sample = fdf.sample(min(500, len(fdf)), random_state=42)
    st.pyplot(ch.pair_plot(sample), use_container_width=True)

# ── Raw Data Preview ──────────────────────────────────────────────────────────
with st.expander("📋 View Filtered Raw Data", expanded=False):
    st.dataframe(fdf.reset_index(drop=True), height=300, use_container_width=True)
    st.caption(f"Showing {len(fdf):,} records after filters applied.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#7F8C8D;font-size:0.85rem;'>"
    "Telco Customer Churn Dashboard · Exploratory Data Analysis · Instructor: Ali Hassan Sherazi"
    "</p>",
    unsafe_allow_html=True,
)
