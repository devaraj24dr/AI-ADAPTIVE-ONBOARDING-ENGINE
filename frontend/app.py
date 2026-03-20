# ============================================================
#  TENSOR TITANS — AI Adaptive Onboarding Engine
#  Module      : Smart Learning Dashboard
#  Description : Interactive UI — Supports PDF & DOCX upload
#  Team        : TENSOR TITANS
# ============================================================

import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title = "TENSOR TITANS — Onboarding Engine",
    page_icon  = "🧠",
    layout     = "wide"
)

st.markdown("""
    <h1 style='text-align:center; color:#6C63FF;'>🧠 TENSOR TITANS</h1>
    <h4 style='text-align:center; color:gray;'>AI-Powered Adaptive Onboarding Engine</h4>
    <hr>
""", unsafe_allow_html=True)

st.subheader("📤 Upload Documents")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📄 Your Resume")
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="resume")
    if resume_file:
        st.success(f"✅ Uploaded: {resume_file.name}")

with col2:
    st.markdown("#### 📋 Job Description")
    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx"], key="jd")
    if jd_file:
        st.success(f"✅ Uploaded: {jd_file.name}")

st.markdown("---")

if st.button("🚀 Generate My Learning Path", use_container_width=True):
    if not resume_file or not jd_file:
        st.warning("⚠️ Please upload both Resume and Job Description!")
    else:
        with st.spinner("🔍 Analyzing your profile..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    files={
                        "resume" : (resume_file.name, resume_file, resume_file.type),
                        "jd"     : (jd_file.name,     jd_file,     jd_file.type)
                    },
                    timeout=300
                )

                if response.status_code != 200:
                    st.error(f"❌ Backend Error: {response.text}")
                else:
                    data = response.json()

                    # Readiness Score
                    st.markdown("---")
                    st.subheader("📊 Your Readiness Score")
                    score = data.get("readiness_score", 0)
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("🎯 Readiness Score", f"{score}%")
                    with col_b:
                        st.metric("✅ Skills You Have", len(data.get("matched", [])))
                    with col_c:
                        st.metric("📚 Skills to Learn", len(data.get("gaps", [])))

                    # Pie Chart
                    st.markdown("---")
                    st.subheader("🎯 Skill Gap Analysis")
                    chart_data = pd.DataFrame({
                        "Category" : ["Matched Skills", "Missing Skills"],
                        "Count"    : [len(data.get("matched", [])), len(data.get("gaps", []))]
                    })
                    fig = px.pie(
                        chart_data,
                        names  = "Category",
                        values = "Count",
                        color_discrete_sequence = ["#6C63FF", "#FF6584"]
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Skill Lists
                    col_x, col_y = st.columns(2)
                    with col_x:
                        st.markdown("### ✅ Skills You Have")
                        for s in data.get("matched", []):
                            st.success(f"✔ {s}")
                    with col_y:
                        st.markdown("### ❌ Skills to Learn")
                        for s in data.get("gaps", []):
                            st.error(f"✘ {s}")

                    # Roadmap
                    st.markdown("---")
                    st.subheader("🗺️ Your Personalized Learning Roadmap")
                    roadmap = data.get("roadmap", [])
                    if roadmap:
                        for step in roadmap:
                            with st.expander(f"Step {step['step']} — {step['skill']}"):
                                st.write(f"📚 **Skill:** {step['skill']}")
                                st.write(f"📌 **Status:** {step['status'].capitalize()}")
                                st.progress(0)
                    else:
                        st.balloons()
                        st.success("🎉 No skill gaps found — You are fully ready!")

            except requests.exceptions.Timeout:
                st.error("⏱️ Timed out — please try again!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("💡 Make sure backend is running: uvicorn main:engine --reload")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Built with ❤️ by TENSOR TITANS</p>", unsafe_allow_html=True)