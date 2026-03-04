import streamlit as st
import plotly.graph_objects as go
from engine import extract_text_from_pdf, analyze_resume

# 1. Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer 2026", 
    page_icon="🎯", 
    layout="wide"
)

# 2. Custom CSS Styling (Fixed)
st.html("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """)

# 3. Header Section
st.title("🚀 Smart Resume Analyzer & Job Matcher")
st.markdown("---")

# 4. Input Section: Two Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Job Description")
    jd_input = st.text_area(
        "Paste the job posting details here...", 
        height=300, 
        placeholder="Requirements, skills, and responsibilities..."
    )

with col2:
    st.subheader("📄 Your Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")
    if uploaded_file:
        st.info(f"Loaded: {uploaded_file.name}")

# 5. Analysis Logic
if st.button("Start AI Analysis"):
    if not jd_input or not uploaded_file:
        st.warning("⚠️ Please provide both a job description and a resume to continue.")
    else:
        with st.spinner("🤖 Agentic AI is evaluating your profile..."):
            # A. Extract text using our engine
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # B. Get JSON analysis from Gemini
            result = analyze_resume(resume_text, jd_input)
            
            if "error" in result and result["error"]:
                st.error(result["error"])
            else:
                st.markdown("### 📊 Evaluation Report")
                
                # C. Top Row: Gauge Chart and Summary
                row1_col1, row1_col2 = st.columns([1, 1])
                
                with row1_col1:
                    # Plotly Gauge Chart
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = result.get('match_score', 0),
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Overall Match %", 'font': {'size': 20, 'color': '#ff4b4b'}},
                        gauge = {
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "gray"},
                            'bar': {'color': "#ff4b4b"},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "#dddddd",
                            'steps': [
                                {'range': [0, 40], 'color': '#ffe5e5'},
                                {'range': [40, 75], 'color': '#ffcccc'},
                                {'range': [75, 100], 'color': '#ff9999'}
                            ],
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
                    st.plotly_chart(fig, use_container_width=True)

                with row1_col2:
                    st.write("**AI Profile Summary**")
                    st.success(result.get('summary', "No summary provided."))
                
                st.divider()

                # D. Bottom Row: Skills & Action Items
                row2_col1, row2_col2, row2_col3 = st.columns(3)

                with row2_col1:
                    st.write("✅ **Matching Skills**")
                    for skill in result.get('matching_skills', []):
                        st.markdown(f" - {skill}")
                
                with row2_col2:
                    st.write("⚠️ **Gap Analysis (Missing)**")
                    for skill in result.get('missing_skills', []):
                        st.markdown(f" - <span style='color:#d9534f'>{skill}</span>", unsafe_allow_html=True)
                
                with row2_col3:
                    st.write("🛠️ **Optimization Tips**")
                    for rec in result.get('recommendations', []):
                        st.markdown(f"👉 {rec}")

# 6. Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Tech Stack")
st.sidebar.caption("• Google Gemini 1.5 Flash")
st.sidebar.caption("• Python & Streamlit")
st.sidebar.caption("• Plotly Visuals")
