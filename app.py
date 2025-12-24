import os
import json
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
import plotly.graph_objects as go
import plotly.express as px

# --- 1. CONFIGURATION & SETUP ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"
genai.configure(api_key=api_key)

st.set_page_config(page_title="Resume Architect Enterprise", page_icon="🏢", layout="wide")

# Navigation State
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

def go_to_app():
    st.session_state['page'] = 'app'

def go_home():
    st.session_state['page'] = 'home'

# --- 2. ADVANCED STYLING (The "Enterprise Dark" Look) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0E1117; }
    
    /* Typography */
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; }
    .main-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(120deg, #3498db, #8e44ad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 20px;
    }
    
    /* Metrics Cards */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #41444C;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161a24;
    }
    
    /* Custom Button */
    .stButton>button {
        background: linear-gradient(90deg, #3498db, #2980b9);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(52, 152, 219, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def get_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_tech_sunburst(skills_data):
    # Prepare data for Sunburst Chart
    data = []
    for category, skills in skills_data.items():
        for skill in skills:
            data.append(dict(
                Category=category,
                Skill=skill['name'],
                Status="Match" if skill['present'] else "Missing",
                Value=10 if skill['present'] else 5
            ))
            
    df = pd.DataFrame(data)
    
    fig = px.sunburst(
        df, 
        path=['Category', 'Status', 'Skill'], 
        values='Value',
        color='Status',
        color_discrete_map={'Match': '#00C853', 'Missing': '#FF5252'},
        title="Skill Coverage Visualization"
    )
    fig.update_layout(
        height=400, 
        paper_bgcolor='rgba(0,0,0,0)', 
        font={'color': "white"}
    )
    return fig

# --- 4. PAGE: WELCOME SCREEN ---
if st.session_state['page'] == 'home':
    st.markdown("<h1 class='main-title'>RESUME ARCHITECT <br><span style='font-size: 2rem; color: white;'>ENTERPRISE EDITION</span></h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<p style='text-align: center; color: #b0bec5; font-size: 1.2rem;'>Powered by Gemini 2.5 • Pandas Analysis • Plotly Visualization</p>", unsafe_allow_html=True)
        if st.button("🚀 ACCESS DASHBOARD", use_container_width=True):
            go_to_app()
            st.rerun()
            
    # Mockup Stats
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AI Model", "Gemini 2.5 Flash", "Latest")
    c2.metric("Parsing Engine", "PyPDF2 + OCR", "Active")
    c3.metric("Visualization", "Plotly Charts", "Interactive")
    c4.metric("Latency", "< 2.5s", "Optimized")

# --- 5. PAGE: DASHBOARD INTERFACE ---
elif st.session_state['page'] == 'app':
    
    # Sidebar Configuration
    with st.sidebar:
        if st.button("⬅️ Exit Dashboard"):
            go_home()
            st.rerun()
        st.header("⚙️ Configuration")
        strictness = st.select_slider("Analysis Strictness", options=["Lenient", "Balanced", "Strict (CTO Mode)"])
        st.info(f"Current Mode: **{strictness}**")
        st.markdown("---")
        st.caption("Enterprise v5.0")

    st.title("📊 Candidate Analysis Dashboard")

    col_l, col_r = st.columns([1, 1])
    with col_l:
        jd = st.text_area("Job Description (Paste Here)", height=200)
    with col_r:
        uploaded_file = st.file_uploader("Candidate Resume (PDF)", type=["pdf"])

    if st.button("RUN DEEP ANALYSIS", type="primary", use_container_width=True):
        if uploaded_file is not None and jd:
            with st.spinner("🔄 Processing Neural Networks... Parsing Structured Data..."):
                try:
                    resume_text = get_pdf_text(uploaded_file)
                    
                    # COMPLEX PROMPT FOR STRUCTURED DATA
                    prompt = f"""
                    Role: You are a {strictness} Technical Recruiter.
                    Task: Analyze the RESUME against the JOB DESCRIPTION.
                    
                    RESUME: {resume_text}
                    JOB DESCRIPTION: {jd}
                    
                    OUTPUT: Provide ONLY a valid JSON object with this EXACT structure:
                    {{
                        "match_percentage": (integer),
                        "candidate_summary": (string),
                        "skills_analysis": {{
                            "Technical Skills": [
                                {{"name": "Python", "present": true}}, 
                                {{"name": "Java", "present": false}} 
                                // extract ACTUAL skills from JD
                            ],
                            "Soft Skills": [
                                {{"name": "Communication", "present": true}}
                            ],
                            "Tools & Cloud": [
                                {{"name": "AWS", "present": false}}
                            ]
                        }},
                        "key_gaps": ["gap1", "gap2"],
                        "verdict": "Strong Hire / Weak Hire / Interview"
                    }}
                    """
                    
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    # Data Cleaning
                    raw_text = response.text.strip()
                    # Sometimes Gemini wraps JSON in markdown, remove it
                    if "```json" in raw_text:
                        raw_text = raw_text.split("```json")[1].split("```")[0]
                    elif "```" in raw_text:
                        raw_text = raw_text.split("```")[1].split("```")[0]
                        
                    data = json.loads(raw_text)
                    
                    # --- DASHBOARD LAYOUT ---
                    
                    # 1. Top Level Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Match Score", f"{data['match_percentage']}%", delta=f"{data['match_percentage']-50}% vs Avg")
                    m2.metric("Verdict", data['verdict'])
                    m3.metric("Mode", strictness)
                    
                    # 2. Executive Summary
                    st.info(f"**Executive Summary:** {data['candidate_summary']}")
                    
                    # 3. Deep Dive Tabs
                    tab_viz, tab_data, tab_action = st.tabs(["🧬 Skill Genome (Viz)", "📋 Data Table", "🚀 Action Plan"])
                    
                    with tab_viz:
                        st.subheader("Skill Coverage Sunburst")
                        st.markdown("Outer ring: Specific Skills. Inner Ring: Status (Red=Missing).")
                        fig = create_tech_sunburst(data['skills_analysis'])
                        st.plotly_chart(fig, use_container_width=True)
                        
                    with tab_data:
                        st.subheader("Comparison Table")
                        # Flatten JSON for Table
                        table_data = []
                        for cat, skills in data['skills_analysis'].items():
                            for skill in skills:
                                table_data.append({
                                    "Category": cat,
                                    "Skill": skill['name'],
                                    "Status": "✅ Match" if skill['present'] else "❌ Missing"
                                })
                        st.dataframe(pd.DataFrame(table_data), use_container_width=True)
                        
                    with tab_action:
                        st.subheader("Critical Gaps to Close")
                        for gap in data['key_gaps']:
                            st.error(f"Gap: {gap}")
                
                except Exception as e:
                    st.error(f"Analysis Failed: {e}")
                    st.warning("Please try a simpler Job Description or check your API key.")