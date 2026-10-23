"""
Streamlit Web Application: AI-Powered Medical Symptom Assistant (GPT-4)
Interactive, responsive clinical symptom assistant dashboard.
"""

import streamlit as st
import pandas as pd
import json
import os
import datetime

# Import modular components
from profile_module import PatientProfile
from symptom_module import extract_symptoms_nlp_fallback, extract_symptoms_with_gpt4, format_extracted_symptoms
from context_module import analyze_context, format_missing_information
from prompt_module import construct_gpt4_prompt
from analysis_module import analyze_symptoms_gpt4, format_symptom_analysis_display, load_kaggle_conditions
from question_module import generate_follow_up_questions, format_follow_up_questions
from safety_module import assess_risk_and_escalation, get_disclaimer, RED_FLAG_SYMPTOMS
from save_module import save_medical_analysis
from utils import build_structured_response
from input_module import load_sample_cases_from_csv

# Page configuration
st.set_page_config(
    page_title="AI Medical Symptom Assistant | GPT-4",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern clinical styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0d9488 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    
    .disclaimer-card {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        color: #991b1b;
        margin-bottom: 20px;
    }
    
    .clinical-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .stMetric {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
    }
    
    .tag-symptom {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 3px;
        border: 1px solid #bae6fd;
    }
    
    .tag-missing {
        display: inline-block;
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 3px;
        border: 1px solid #fde68a;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">🩺 AI-Powered Medical Symptom Assistant</h1>
            <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 1rem;">
                24CS2506 – Building Applications using GPT-4 | Experiment 6
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(13, 148, 136, 0.4); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; border: 1px solid #2dd4bf;">
                OpenAI GPT-4 • Kaggle Clinical KB
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Mandatory Educational Medical Disclaimer Banner
st.markdown("""
<div class="disclaimer-card">
    <strong>⚠️ MANDATORY MEDICAL DISCLAIMER:</strong><br>
    This AI-generated application is intended for <strong>educational and informational purposes only</strong>.
    It is <strong>not a medical diagnosis</strong> and does not replace professional advice, diagnosis, or treatment from a qualified healthcare professional.
    For serious, worsening, or urgent symptoms, immediately seek emergency medical care.
</div>
""", unsafe_allow_html=True)

# Sidebar: Controls, Model Configuration & Kaggle Benchmarks
st.sidebar.header("⚙️ Assistant Settings")

# Model Mode
api_key_input = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", help="If left empty, system operates in resilient Kaggle Knowledge Base mode.")
selected_model = st.sidebar.selectbox("GPT-4 Model", ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"], index=0)

client = None
if api_key_input:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key_input)
        st.sidebar.success("✓ Live OpenAI Client Connected")
    except Exception as e:
        st.sidebar.error(f"Client Init Error: {e}")
else:
    st.sidebar.info("💡 Operating in Kaggle Clinical Knowledge Base Mode (Offline Ready)")

# Kaggle Dataset Sample Case Quick-Loader
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Kaggle Benchmark Cases")
sample_cases = load_sample_cases_from_csv()
case_options = ["Custom Input"] + [f"{c.get('case_id')}: {c.get('age')}y/o {c.get('sex')} - {c.get('symptoms')[:25]}..." for c in sample_cases]
selected_case_idx = st.sidebar.selectbox("Load Sample Case", range(len(case_options)), format_func=lambda x: case_options[x])

# Pre-populate based on selection
default_age = "22"
default_sex = "Female"
default_symptoms = "Fever, cough and sore throat"
default_duration = "2 days"
default_severity = "Mild"
default_history = "No known relevant condition"
default_meds = "None"
default_allergies = "None"
default_natural = "I have been having fever and cough for two days. My throat is also painful."

if selected_case_idx > 0:
    case_data = sample_cases[selected_case_idx - 1]
    default_age = str(case_data.get("age", default_age))
    default_sex = str(case_data.get("sex", default_sex))
    default_symptoms = str(case_data.get("symptoms", default_symptoms))
    default_duration = str(case_data.get("duration", default_duration))
    default_severity = str(case_data.get("severity", default_severity))
    default_history = str(case_data.get("medical_history", default_history))
    default_meds = str(case_data.get("current_medications", default_meds))
    default_allergies = str(case_data.get("allergies", default_allergies))
    default_natural = str(case_data.get("natural_input", default_symptoms))

# Main Tabs
tabs = st.tabs([
    "📋 Part A & B: Patient Profile & Symptoms",
    "🔍 Part C & D: Context & GPT-4 Prompt",
    "🩺 Part E & F: Analysis & Follow-up",
    "🛡️ Part G & H: Guidance & Full Report",
    "📊 Kaggle Clinical Knowledge Base"
])

# ----------------- TAB 1: PATIENT PROFILE & SYMPTOMS -----------------
with tabs[0]:
    st.subheader("Part A: Patient Health Information & Symptoms Input")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Patient Demographics")
        age = st.text_input("Age", value=default_age, help="Patient age in years")
        sex = st.selectbox("Sex", ["Female", "Male", "Other", "Prefer not to say"], index=0 if default_sex == "Female" else (1 if default_sex == "Male" else 2))
        duration = st.text_input("Symptom Duration", value=default_duration, help="e.g., 2 days, 1 week, 3 hours")
        severity = st.selectbox("Reported Severity", ["Mild", "Moderate", "Severe"], index=["Mild", "Moderate", "Severe"].index(default_severity) if default_severity in ["Mild", "Moderate", "Severe"] else 0)

    with col2:
        st.markdown("#### Medical Background")
        medical_history = st.text_input("Relevant Medical History", value=default_history)
        medications = st.text_input("Current Medications", value=default_meds)
        allergies = st.text_input("Allergies", value=default_allergies)
    
    st.markdown("---")
    st.markdown("#### Part B: Natural-Language Symptom Input")
    st.caption("Enter patient narrative or verbatim statement describing current complaints.")
    natural_input = st.text_area(
        "Natural Language Patient Description",
        value=default_natural,
        height=100
    )
    
    profile = PatientProfile(
        age=age,
        sex=sex,
        symptoms=default_symptoms,
        duration=duration,
        severity=severity,
        medical_history=medical_history,
        current_medications=medications,
        allergies=allergies,
        natural_input=natural_input
    )
    
    # Symptom Extraction Button
    if st.button("🚀 Extract Symptoms & Begin Assessment", type="primary", use_container_width=True):
        st.session_state["extracted_symptoms"] = extract_symptoms_with_gpt4(natural_input, client=client, model=selected_model)
        st.session_state["profile"] = profile
        st.success("Symptoms extracted successfully!")

# Ensure extracted symptoms exist in session
if "extracted_symptoms" not in st.session_state:
    st.session_state["extracted_symptoms"] = extract_symptoms_with_gpt4(default_natural, client=client, model=selected_model)
if "profile" not in st.session_state:
    st.session_state["profile"] = profile

extracted_symptoms = st.session_state["extracted_symptoms"]
current_profile = st.session_state["profile"]

with tabs[0]:
    st.markdown("#### Extracted Clinical Symptoms (Part B Output)")
    symptom_tags_html = "".join([f'<span class="tag-symptom">✓ {s}</span>' for s in extracted_symptoms])
    st.markdown(symptom_tags_html, unsafe_allow_html=True)

# ----------------- TAB 2: CONTEXT & PROMPT GENERATION -----------------
with tabs[1]:
    st.subheader("Part C: Context Analysis (Missing Information Detection)")
    missing_info = analyze_context(current_profile, extracted_symptoms)
    st.session_state["missing_info"] = missing_info
    
    st.markdown("The system analyzes clinical completeness and flags critical diagnostic parameters:")
    missing_tags_html = "".join([f'<span class="tag-missing">⚠️ {m}</span>' for m in missing_info])
    st.markdown(missing_tags_html, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Part D: Prompt Construction for GPT-4")
    st.caption("Constructed according to strict clinical guardrails (Part D - Q4).")
    prompt_payload = construct_gpt4_prompt(current_profile, extracted_symptoms, missing_info)
    
    with st.expander("👁️ View System Prompt (Clinical Safety Guardrails)", expanded=False):
        st.code(prompt_payload["system_prompt"], language="markdown")
        
    with st.expander("👁️ View Formatted User Prompt", expanded=True):
        st.code(prompt_payload["user_prompt"], language="markdown")

# ----------------- TAB 3: SYMPTOM ANALYSIS & FOLLOW-UP -----------------
with tabs[2]:
    st.subheader("Part E: Preliminary Symptom Analysis (GPT-4)")
    
    analysis_res = analyze_symptoms_gpt4(
        current_profile,
        extracted_symptoms,
        st.session_state.get("missing_info", []),
        client=client,
        model=selected_model
    )
    st.session_state["analysis_res"] = analysis_res
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("##### 📌 Reported Symptoms")
        for s in analysis_res.get("reported_symptoms", []):
            st.markdown(f"- **{s}**")
            
        st.markdown("##### 🩺 Possible Conditions (Differential Considerations)")
        for c in analysis_res.get("possible_conditions", []):
            st.markdown(f"- 🔸 **{c}**")
            
        st.info(analysis_res.get("note", ""))
        
    with col_b:
        st.markdown("##### 💡 Clinical Explanation")
        st.write(analysis_res.get("explanation", ""))
        
    st.markdown("---")
    st.subheader("Part F: Targeted Follow-Up Questions")
    follow_up_qs = generate_follow_up_questions(
        current_profile,
        extracted_symptoms,
        st.session_state.get("missing_info", []),
        client=client,
        model=selected_model
    )
    st.session_state["follow_up_qs"] = follow_up_qs
    
    for i, q in enumerate(follow_up_qs, 1):
        st.markdown(f"**{i}.** {q}")

# ----------------- TAB 4: RISK, GUIDANCE & STRUCTURED REPORT -----------------
with tabs[3]:
    st.subheader("Part G: Risk Assessment & Medical Attention Guidance")
    safety_res = assess_risk_and_escalation(current_profile, extracted_symptoms)
    st.session_state["safety_res"] = safety_res
    
    st.markdown(f"**Urgency / Risk Stratification:** `{safety_res.get('risk_level')}`")
    
    if safety_res.get("red_flags"):
        st.error(f"🚨 Red-Flag Symptoms Detected: {', '.join(safety_res.get('red_flags'))}")
    else:
        st.success("✓ No immediate acute emergency red-flag keywords detected in initial narrative.")
        
    st.markdown("##### 🏥 Medical Attention Guidance")
    st.warning(safety_res.get("guidance"))
    
    st.markdown("---")
    st.subheader("Part H: Complete Structured Response (8 Sections)")
    
    full_report = build_structured_response(
        profile=current_profile,
        extracted_symptoms=extracted_symptoms,
        possible_conditions=analysis_res.get("possible_conditions", []),
        explanation=analysis_res.get("explanation", ""),
        missing_info=st.session_state.get("missing_info", []),
        follow_up_questions=follow_up_qs,
        medical_attention_guidance=safety_res.get("guidance", ""),
        note=analysis_res.get("note")
    )
    st.session_state["full_report"] = full_report
    
    st.text_area("Complete Formatted Analysis", value=full_report, height=350)
    
    # Part J: Save / Export Analysis
    col_save1, col_save2 = st.columns([1, 1])
    with col_save1:
        if st.button("💾 Save Analysis to outputs/medical_analysis.txt", use_container_width=True):
            saved_path = save_medical_analysis(full_report)
            st.success(f"Report saved to `{saved_path}`!")
    with col_save2:
        st.download_button(
            label="📥 Download Report File (.txt)",
            data=full_report,
            file_name="medical_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )

# ----------------- TAB 5: KAGGLE DATASET EXPLORER -----------------
with tabs[4]:
    st.subheader("📊 Kaggle Clinical Disease & Symptoms Knowledge Base")
    st.caption("Sourced and synthesized from Kaggle's Disease-Symptom Benchmark Datasets.")
    
    kaggle_records = load_kaggle_conditions()
    if kaggle_records:
        df_kaggle = pd.DataFrame(kaggle_records)
        search_query = st.text_input("Search Conditions or Symptoms in Knowledge Base", "")
        if search_query:
            df_filtered = df_kaggle[df_kaggle.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
        else:
            df_filtered = df_kaggle
            
        st.dataframe(df_filtered[["disease", "primary_symptoms", "typical_duration", "risk_level", "possible_causes"]], use_container_width=True)
        st.caption(f"Showing {len(df_filtered)} reference conditions.")
    else:
        st.warning("Kaggle dataset CSV not found at data/kaggle_disease_symptoms.csv")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px;">
    <strong>24CS2506 – Building Applications using GPT-4</strong> | Experiment 6: AI-Powered Medical Symptom Assistant<br>
    Built with Python, Streamlit, and OpenAI GPT-4 Architecture | Sourced with Kaggle Medical Benchmark Data
</div>
""", unsafe_allow_html=True)
