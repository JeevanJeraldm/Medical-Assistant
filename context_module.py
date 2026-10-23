"""
Context Module (Part C - Context Analysis)
Analyzes the available patient information and identifies missing clinical information that may be relevant.
"""

import re
from typing import List
from profile_module import PatientProfile


def analyze_context(profile: PatientProfile, extracted_symptoms: List[str]) -> List[str]:
    """
    Part C - Q3: Analyze the available information and identify missing information that may be relevant.

    Example:
    Missing Information:
    • Exact temperature
    • Breathing difficulty
    • Severity progression
    • Additional symptoms
    """
    missing_items = []
    combined_text = f"{profile.symptoms} {profile.natural_input} {profile.duration} {profile.medical_history}".lower()
    symptoms_lower = [s.lower() for s in extracted_symptoms]

    # 1. Exact temperature check
    has_fever_mention = any("fever" in s or "chill" in s or "temperature" in s for s in symptoms_lower)
    has_numeric_temp = bool(re.search(r"\b(9\d|10\d)(\.\d)?\s*(f|c|deg|°)\b|\b(3\d|40)(\.\d)?\s*(c|deg|°)\b", combined_text))
    if has_fever_mention and not has_numeric_temp:
        missing_items.append("Exact temperature")
    elif not has_fever_mention:
        # For general respiratory or systemic cases, temperature is always relevant
        if any(s in ["cough", "sore throat", "headache", "body aches"] for s in symptoms_lower):
            missing_items.append("Exact temperature")

    # 2. Breathing difficulty / Shortness of breath
    has_breathing_mention = any("breath" in s or "dyspnea" in s or "wheez" in s for s in symptoms_lower) or "breath" in combined_text
    is_respiratory = any(s in ["cough", "sore throat", "fever", "chest pain", "runny nose"] for s in symptoms_lower)
    if is_respiratory and not has_breathing_mention:
        missing_items.append("Breathing difficulty")

    # 3. Severity progression
    has_progression = any(w in combined_text for w in ["worsening", "improving", "better", "worse", "steady", "progressed", "stable"])
    if not has_progression:
        missing_items.append("Severity progression")

    # 4. Sputum / Mucus characterization (if cough present)
    has_cough = any("cough" in s for s in symptoms_lower)
    has_sputum_info = any(w in combined_text for w in ["dry", "productive", "phlegm", "mucus", "sputum", "blood"])
    if has_cough and not has_sputum_info:
        missing_items.append("Cough nature (dry or producing mucus/phlegm)")

    # 5. Additional symptoms / constitutional signs
    missing_items.append("Additional symptoms")

    # 6. Vital signs or oxygen saturation (SpO2)
    if is_respiratory and "spo2" not in combined_text and "oxygen" not in combined_text:
        missing_items.append("Oxygen saturation (SpO2) and pulse rate")

    # De-duplicate while preserving order
    seen = set()
    cleaned_missing = []
    for item in missing_items:
        if item.lower() not in seen:
            seen.add(item.lower())
            cleaned_missing.append(item)

    return cleaned_missing


def format_missing_information(missing_list: List[str]) -> str:
    """Formats missing information into a structured bullet list."""
    if not missing_list:
        return "• None noted (comprehensive details provided)"
    return "\n".join(f"• {item}" for item in missing_list)
