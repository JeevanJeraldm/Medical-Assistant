"""
Google Colab / Headless Automated Runner for Experiment 6
Enables 1-click end-to-end execution on Google Colab or non-interactive environments.
"""

import os
import sys
from profile_module import PatientProfile
from symptom_module import extract_symptoms_with_gpt4, format_extracted_symptoms
from context_module import analyze_context, format_missing_information
from prompt_module import construct_gpt4_prompt
from analysis_module import analyze_symptoms_gpt4, format_symptom_analysis_display
from question_module import generate_follow_up_questions, format_follow_up_questions
from safety_module import assess_risk_and_escalation, get_disclaimer
from save_module import save_medical_analysis
from utils import build_structured_response


def run_experiment_6_headless():
    print("=" * 70)
    print("  EXPERIMENT 6: AI-POWERED MEDICAL SYMPTOM ASSISTANT (GPT-4)")
    print("  AUTOMATED HEADLESS / COLAB PIPELINE EXECUTION")
    print("=" * 70)

    # Part A: Sample Patient Profile (Matching Experiment Specification)
    print("\n--> [Part A] Patient Profile Ingestion:")
    profile = PatientProfile(
        age="22",
        sex="Female",
        symptoms="Fever, cough and sore throat",
        duration="2 days",
        severity="Mild",
        medical_history="No known relevant condition",
        current_medications="None",
        allergies="None",
        natural_input="I have been having fever and cough for two days. My throat is also painful."
    )
    print(profile.format_summary())

    # Part B: Symptom Extraction
    print("\n--> [Part B] Symptom Extraction from Natural Language:")
    print(f"User Input: \"{profile.natural_input}\"")
    extracted = extract_symptoms_with_gpt4(profile.natural_input)
    print("Extracted Symptoms:")
    print(format_extracted_symptoms(extracted))

    # Part C: Context Analysis
    print("\n--> [Part C] Context & Missing Information Detection:")
    missing = analyze_context(profile, extracted)
    print(format_missing_information(missing))

    # Part D: Prompt Generation
    print("\n--> [Part D] GPT-4 Prompt Generation:")
    prompts = construct_gpt4_prompt(profile, extracted, missing)
    print("Prompt payload successfully generated with strict clinical guardrails.")

    # Part E: Symptom Analysis
    print("\n--> [Part E] Symptom Analysis:")
    analysis = analyze_symptoms_gpt4(profile, extracted, missing)
    print(format_symptom_analysis_display(analysis))

    # Part F: Follow-up Questions
    print("\n--> [Part F] Follow-up Questions:")
    questions = generate_follow_up_questions(profile, extracted, missing)
    print(format_follow_up_questions(questions))

    # Part G: Risk / Escalation Assessment
    print("\n--> [Part G] Risk & Escalation Guidance:")
    safety = assess_risk_and_escalation(profile, extracted)
    print(safety.get("guidance"))

    # Part H & I: Full Structured Response & Disclaimer
    print("\n--> [Part H & I] Full Structured 8-Part Response:")
    full_report = build_structured_response(
        profile=profile,
        extracted_symptoms=extracted,
        possible_conditions=analysis.get("possible_conditions", []),
        explanation=analysis.get("explanation", ""),
        missing_info=missing,
        follow_up_questions=questions,
        medical_attention_guidance=safety.get("guidance", ""),
        note=analysis.get("note")
    )
    print(full_report)

    # Part J: Save Analysis
    print("\n--> [Part J] Saving Analysis to outputs/medical_analysis.txt:")
    out_file = save_medical_analysis(full_report)
    print(f"[+] Output saved to: {out_file}")
    print("\n" + "=" * 70)
    print("  EXPERIMENT 6 COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_experiment_6_headless()
