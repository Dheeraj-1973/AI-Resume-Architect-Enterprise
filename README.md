# 🚀 AI Resume Architect - Enterprise Edition

**A Smart SaaS-style Resume Analyzer powered by Google Gemini 2.5, Python, and Streamlit.**

## 🌟 Overview
As a 3rd Year CSE Student, I noticed many qualified candidates get rejected by ATS (Applicant Tracking Systems) simply due to missing keywords. 
I built **Resume Architect** to solve this using Large Language Models (LLMs). 

Unlike basic scripts, this is a full-stack data application that visualizes your "Skill Genome" and provides a gap analysis against any job description.

## 🛠️ Tech Stack
* **Core Logic:** Python 3.10+
* **AI Engine:** Google Gemini 2.5 Flash (via `google-genai` 2025 SDK)
* **Frontend:** Streamlit (with Custom CSS for Dark Mode)
* **Data Visualization:** Plotly (Sunburst Charts & Gauge Meters)
* **Data Processing:** Pandas & JSON Parsing
* **PDF Parsing:** PyPDF2

## ✨ Key Features
1.  **Enterprise Dashboard:** A sleek, dark-mode UI with "Glassmorphism" design.
2.  **Strictness Modes:** Switch between "Lenient" and "CTO Mode" (Strict) analysis.
3.  **Visual Skill Analysis:** Interactive Sunburst charts to see skill coverage.
4.  **Direct Comparison:** Pandas DataFrame showing a side-by-side view of Required vs. Present skills.

## 🚀 How to Run Locally
1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/YourUsername/AI-Resume-Architect.git](https://github.com/YourUsername/AI-Resume-Architect.git)
    cd AI-Resume-Architect
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up API Key:**
    * Create a `.env` file.
    * Add your key: `GEMINI_API_KEY=your_google_api_key_here`
4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## 📸 Screenshots
*(Add your screenshots here later)*

---
*Built by [Dheeraj](https://www.linkedin.com/in/your-profile) | KL University*