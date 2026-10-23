"""
Safety Module (Part G - Risk / Escalation Assessment & Part I - Disclaimer)
Evaluates escalation risk with cautious non-triage language and enforces the strict medical disclaimer.
"""

from typing import List, Dict, Any
from profile_module import PatientProfile

DISCLAIMER_TEXT = """DISCLAIMER
--------------------------------
This AI-generated response is intended for
educational and informational purposes only.
It is not a medical diagnosis and does not
replace advice from a qualified healthcare
professional.
For serious, worsening or urgent symptoms,
seek appropriate medical care."""

DEFAULT_MEDICAL_ATTENTION_GUIDANCE = """MEDICAL ATTENTION
--------------------------------
If symptoms are severe, rapidly worsening,
or concerning, seek appropriate professional
medical care."""


RED_FLAG_SYMPTOMS = [
    "chest pain",
    "chest tightness",
    "difficulty breathing",
    "shortness of breath",
    "sudden numbness",
    "facial drooping",
    "loss of consciousness",
    "coughing up blood",
    "severe sudden headache",
    "high fever over 103f",
    "blue lips",
    "inability to swallow fluids"
]


def assess_risk_and_escalation(
    profile: PatientProfile,
    extracted_symptoms: List[str]
) -> Dict[str, Any]:
    """
    Part G - Q7: Design the system to identify whether the user should be encouraged to seek
    professional medical attention using cautious language without claiming a clinical triage decision.
    """
    symptoms_lower = [s.lower() for s in extracted_symptoms]
    combined_text = f"{profile.symptoms} {profile.natural_input} {profile.severity}".lower()

    detected_red_flags = []
    for flag in RED_FLAG_SYMPTOMS:
        if flag in combined_text or any(flag in s for s in symptoms_lower):
            detected_red_flags.append(flag.capitalize())

    # Risk level estimation (Informational only)
    is_severe = profile.severity.lower() == "severe" or len(detected_red_flags) > 0

    if is_severe:
        guidance = (
            "MEDICAL ATTENTION\n"
            "--------------------------------\n"
            "If symptoms are severe, rapidly worsening, or concerning, seek appropriate professional medical care.\n"
            "Prompt emergency evaluation is advised if you experience severe shortness of breath, "
            "unrelenting chest pressure, or sudden neurological changes."
        )
        risk_level = "High / Urgent Evaluation Recommended"
    elif profile.severity.lower() == "moderate":
        guidance = (
            "MEDICAL ATTENTION\n"
            "--------------------------------\n"
            "If symptoms are severe, rapidly worsening, or concerning, seek appropriate professional medical care.\n"
            "Monitor symptoms closely and consult a primary healthcare provider if symptoms persist or do not improve within 48 to 72 hours."
        )
        risk_level = "Moderate / Primary Care Consultation Advised"
    else:
        # Standard sample guidance matching prompt exactly
        guidance = DEFAULT_MEDICAL_ATTENTION_GUIDANCE
        risk_level = "Low / Routine Monitoring"

    return {
        "risk_level": risk_level,
        "guidance": guidance,
        "red_flags": detected_red_flags,
        "disclaimer": DISCLAIMER_TEXT
    }


def format_medical_attention(guidance_text: str) -> str:
    """Formats medical attention guidance block."""
    return guidance_text.strip()


def get_disclaimer() -> str:
    """Part I - Q9: Returns the exact required medical disclaimer."""
    return DISCLAIMER_TEXT.strip()
