import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage import load_candidates, load_requirements, load_outreach

st.set_page_config(
    page_title="TA Automation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Load data
# -----------------------------
candidates_df = load_candidates()
reqs_df = load_requirements()
outreach_df = load_outreach()

requirements_count = len(reqs_df)
candidates_count = len(candidates_df)
outreach_count = len(outreach_df)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    }

    .block-container {
        max-width: 1220px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: #f7faff;
        border-right: 1px solid #e3edf9;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }

    .sidebar-brand {
        font-size: 1.05rem;
        font-weight: 700;
        color: #243b6b;
        margin-bottom: 0.25rem;
    }

    .sidebar-sub {
        color: #6b7a90;
        font-size: 0.92rem;
        margin-bottom: 0.8rem;
    }

    .header-box {
        background: linear-gradient(135deg, #e8f1ff 0%, #f5f9ff 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 24px;
        border: 1px solid #d6e6ff;
        box-shadow: 0 14px 36px rgba(37, 99, 235, 0.10);
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }

    .header-box::before {
        content: "";
        position: absolute;
        right: -70px;
        top: -70px;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(59,130,246,0.16) 0%, transparent 72%);
    }

    .header-box::after {
        content: "";
        position: absolute;
        left: 55%;
        bottom: -40px;
        width: 380px;
        height: 120px;
        background: radial-gradient(circle, rgba(191,219,254,0.45) 0%, transparent 70%);
        transform: translateX(-50%);
    }

    .title {
        position: relative;
        z-index: 2;
        font-size: 2.65rem;
        font-weight: 800;
        color: #1e3a8a;
        letter-spacing: -0.8px;
        line-height: 1.1;
        margin-bottom: 0.7rem;
    }

    .subtitle {
        position: relative;
        z-index: 2;
        font-size: 1.18rem;
        color: #2563eb;
        font-weight: 700;
        margin-bottom: 0.85rem;
    }

    .desc {
        position: relative;
        z-index: 2;
        color: #5f728c;
        font-size: 1.02rem;
        max-width: 760px;
        line-height: 1.7;
    }

    .kpi {
        background: #ffffff;
        border-radius: 22px;
        padding: 1.45rem 1.2rem;
        border: 1px solid #e5edf7;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.07);
        text-align: center;
        transition: all 0.2s ease;
    }

    .kpi:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 28px rgba(37, 99, 235, 0.13);
    }

    .kpi-number {
        font-size: 2.15rem;
        font-weight: 800;
        color: #2563eb;
        line-height: 1.1;
        margin-bottom: 0.45rem;
    }

    .kpi-label {
        color: #66758b;
        font-size: 0.96rem;
        font-weight: 600;
    }

    .section-heading {
        font-size: 1.9rem;
        font-weight: 800;
        color: #2d3142;
        margin-top: 0.6rem;
        margin-bottom: 1rem;
        letter-spacing: -0.4px;
    }

    .card {
        background: #ffffff;
        border-radius: 22px;
        padding: 1.5rem 1.5rem;
        border: 1px solid #e5edf7;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        min-height: 260px;
        transition: all 0.2s ease;
    }

    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 28px rgba(15, 23, 42, 0.08);
    }

    .step {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1rem;
        color: #384152;
        font-size: 0.98rem;
        line-height: 1.5;
    }

    .step-badge {
        min-width: 34px;
        height: 34px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        color: #1d4ed8;
        font-weight: 800;
        font-size: 1rem;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
    }

    .quick-list {
        margin: 0;
        padding-left: 1.3rem;
        color: #384152;
        line-height: 1.9;
        font-size: 0.99rem;
    }

    .quick-list li {
        margin-bottom: 0.2rem;
    }

    .footer-note {
        text-align: center;
        margin-top: 2rem;
        color: #90a0b8;
        font-size: 0.98rem;
        font-weight: 500;
    }

    div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    hr {
        margin-top: 1.2rem !important;
        margin-bottom: 1.2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🎯 TA Automation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Recruitment Pipeline</div>', unsafe_allow_html=True)
    st.divider()

    st.metric("Requirements", requirements_count)
    st.metric("Candidates", candidates_count)
    st.metric("Outreach", outreach_count)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="header-box">
        <div class="title">🎯 Caprice - TA Automation Platform</div>
        <div class="subtitle">LinkedIn Talent Acquisition, Automated</div>
        <div class="desc">
            Manage sourcing, AI scoring, and outreach in one streamlined workflow.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# KPI row
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-number">{requirements_count}</div>
            <div class="kpi-label">Requirements</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-number">{candidates_count}</div>
            <div class="kpi-label">Candidates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-number">{outreach_count}</div>
            <div class="kpi-label">Outreach Sent</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -----------------------------
# Main content
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-heading">How it works</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
            <div class="step">
                <div class="step-badge">1</div>
                <div><b>Requirements</b> – Define job specs</div>
            </div>
            <div class="step">
                <div class="step-badge">2</div>
                <div><b>Candidates</b> – Fetch profiles</div>
            </div>
            <div class="step">
                <div class="step-badge">3</div>
                <div><b>AI Scoring</b> – Rank candidates</div>
            </div>
            <div class="step">
                <div class="step-badge">4</div>
                <div><b>Outreach</b> – Send messages</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<div class="section-heading">Quick Start</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
            <ol class="quick-list">
                <li>Add job in <b>Requirements</b></li>
                <li>Fetch candidates in <b>Candidates</b></li>
                <li>Click <b>AI Score All</b></li>
                <li>Shortlist candidates</li>
                <li>Send outreach</li>
                <li>Track responses in dashboard</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    '<div class="footer-note">Simple. Clean. Automated hiring.</div>',
    unsafe_allow_html=True,
)