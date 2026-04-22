import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from storage import load_candidates, load_requirements, load_outreach


st.title("📊 Recruitment Dashboard")
st.caption("Live overview of your talent acquisition pipeline.")

candidates_df = load_candidates()
reqs_df = load_requirements()
outreach_df = load_outreach()

if candidates_df.empty and reqs_df.empty:
    st.info("No data yet. Start by adding requirements and fetching candidates.")
    st.stop()

# --- Top KPIs ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Requirements", len(reqs_df))
col2.metric("Total Candidates", len(candidates_df))

scored = candidates_df[candidates_df["ai_score"].notna()]
col3.metric("Scored", len(scored))

shortlisted = candidates_df[candidates_df["status"] == "Shortlisted"]
col4.metric("Shortlisted", len(shortlisted))

avg_score = pd.to_numeric(scored["ai_score"], errors="coerce").mean() if not scored.empty else 0
col5.metric("Avg AI Score", f"{avg_score:.0f}")

st.divider()

row1_col1, row1_col2 = st.columns(2)

# --- Score distribution ---
with row1_col1:
    if not scored.empty:
        st.subheader("AI Score Distribution")
        fig = px.histogram(
            scored,
            x=pd.to_numeric(scored["ai_score"], errors="coerce"),
            nbins=10,
            color_discrete_sequence=["#7F77DD"],
            labels={"x": "AI Score"},
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=260,
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_xaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Score some candidates to see the distribution.")

# --- Status funnel ---
with row1_col2:
    if not candidates_df.empty:
        st.subheader("Pipeline Funnel")
        status_order = ["New", "Shortlisted", "Contacted", "Replied", "Interview", "Rejected"]
        status_counts = candidates_df["status"].value_counts().reindex(status_order, fill_value=0)
        fig2 = go.Figure(go.Funnel(
            y=status_order,
            x=status_counts.values,
            marker=dict(color=["#7F77DD", "#1D9E75", "#EF9F27", "#D85A30", "#378ADD", "#E24B4A"]),
            textinfo="value+percent initial",
        ))
        fig2.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=260,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="gray"),
        )
        st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

# --- Candidates by role ---
with row2_col1:
    if not candidates_df.empty and "job_title" in candidates_df.columns:
        st.subheader("Candidates by Role")
        role_counts = candidates_df["job_title"].value_counts().reset_index()
        role_counts.columns = ["Role", "Count"]
        fig3 = px.bar(
            role_counts, x="Count", y="Role", orientation="h",
            color_discrete_sequence=["#1D9E75"],
        )
        fig3.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=260,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="",
        )
        st.plotly_chart(fig3, use_container_width=True)

# --- Outreach stats ---
with row2_col2:
    st.subheader("Outreach Stats")
    if not outreach_df.empty:
        total = len(outreach_df)
        replied = len(outreach_df[outreach_df["reply_received"] == "Yes"])
        connected = len(outreach_df[outreach_df["connection_status"] == "Connected"])
        pending = total - replied

        fig4 = go.Figure(go.Bar(
            x=["Sent", "Connected", "Replied", "Pending"],
            y=[total, connected, replied, pending],
            marker_color=["#7F77DD", "#1D9E75", "#EF9F27", "#888780"],
        ))
        fig4.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=260,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No outreach data yet.")

st.divider()

# --- Top candidates table ---
st.subheader("🏆 Top Scored Candidates")
if not scored.empty:
    top = scored.copy()
    top["ai_score"] = pd.to_numeric(top["ai_score"], errors="coerce")
    top = top.sort_values("ai_score", ascending=False).head(10)
    display_cols = ["name", "job_title", "current_company", "years_experience", "location", "ai_score", "status"]
    display_cols = [c for c in display_cols if c in top.columns]
    st.dataframe(
        top[display_cols].rename(columns={
            "name": "Name", "job_title": "Role", "current_company": "Company",
            "years_experience": "Exp (yrs)", "location": "Location",
            "ai_score": "Score", "status": "Status",
        }),
        use_container_width=True,
        hide_index=True,
    )

# --- Export ---
st.divider()
st.subheader("📥 Export Data")
col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    if not candidates_df.empty:
        st.download_button("⬇️ Download Candidates CSV", candidates_df.to_csv(index=False), "candidates.csv", "text/csv", use_container_width=True)
with col_e2:
    if not outreach_df.empty:
        st.download_button("⬇️ Download Outreach CSV", outreach_df.to_csv(index=False), "outreach.csv", "text/csv", use_container_width=True)
with col_e3:
    if not reqs_df.empty:
        st.download_button("⬇️ Download Requirements CSV", reqs_df.to_csv(index=False), "requirements.csv", "text/csv", use_container_width=True)