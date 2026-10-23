"""
Prompt Module (Part D - Prompt Generation for GPT-4)
Constructs strictly constrained, high-safety prompts instructing GPT-4 to analyze symptoms,
identify differential conditions, formulate follow-up questions, and provide non-diagnostic guidance.
"""

from typing import List, Dict
from profile_module import PatientProfile


SYSTEM_PROMPT = """You are an AI-powered Medical Symptom Assistant.
Your primary role is to provide safe, objective, and educational symptom information.

Strict Clinical and Safety Constraints:
1. INFORMATIONAL ONLY: Your output is strictly for educational and informational purposes. You are NOT a doctor, and your output is NOT a medical diagnosis.
2. AVOID DEFINITIVE DIAGNOSES: Never state that the patient has a specific condition. Always use cautious phrases such as "Possible conditions may include", "Could be associated with", or "Differential considerations include".
3. AVOID INVENTING INFORMATION: Do not assume or hallucinate patient details, lab results, or symptoms not explicitly stated in the input. If information is missing, explicitly note it.
4. EXPLAIN REASONING GENERALLY: Explain clinical reasoning at an accessible, general educational level (e.g., explaining why a group of symptoms commonly co-occurs).
5. GENERATE FOLLOW-UP QUESTIONS: Formulate targeted, clinically relevant follow-up questions to gather necessary context.
6. RISK & ESCALATION GUIDANCE: Clearly identify red-flag signs and recommend appropriate professional medical evaluation without making definitive clinical triage decisions.
7. MANDATORY DISCLAIMER: Always append the exact required medical disclaimer.
"""


def construct_gpt4_prompt(
    profile: PatientProfile,
    extracted_symptoms: List[str],
    missing_info: List[str]
) -> Dict[str, str]:
    """
    Part D - Q4: Construct a prompt for GPT-4.
    Instructs GPT-4 to:
      - Analyze symptoms
      - Identify possible conditions
      - Explain the reasoning at a general level
      - Ask follow-up questions
      - Identify when professional medical care may be appropriate
      - Avoid definitive diagnosis
      - Avoid inventing information
    """
    symptoms_str = "\n".join(f"- {s}" for s in extracted_symptoms) if extracted_symptoms else "- None specified"
    missing_str = "\n".join(f"- {m}" for m in missing_info) if missing_info else "- None noted"

    user_prompt = f"""Analyze the following patient profile and symptoms:

PATIENT INFORMATION:
- Age: {profile.age}
- Sex: {profile.sex if profile.sex else 'Not specified'}
- Duration: {profile.duration if profile.duration else 'Not specified'}
- Severity: {profile.severity}
- Medical History: {profile.medical_history}
- Current Medications: {profile.current_medications}
- Allergies: {profile.allergies}

REPORTED / EXTRACTED SYMPTOMS:
{symptoms_str}

IDENTIFIED MISSING INFORMATION:
{missing_str}

INSTRUCTIONS FOR YOUR RESPONSE:
Please generate a structured analysis following this exact schema:

1. REPORTED SYMPTOMS: List the verified reported symptoms.
2. POSSIBLE CONDITIONS: List 3 to 4 possible conditions associated with these symptoms. Include a brief note explaining that these symptoms can occur in multiple conditions and the information is not sufficient to establish a diagnosis.
3. EXPLANATION: Explain the general physiological reasoning connecting these symptoms to the possible conditions.
4. MISSING INFORMATION: List key clinical details that were not provided but would be valuable for a medical evaluation.
5. FOLLOW-UP QUESTIONS: Provide 5 targeted follow-up questions to clarify the patient's condition.
6. MEDICAL ATTENTION GUIDANCE: Provide cautious guidance specifying when professional medical evaluation is warranted.
7. DISCLAIMER: Display the standard educational disclaimer.

Do not invent symptoms or provide a definitive diagnosis.
"""

    return {
        "system_prompt": SYSTEM_PROMPT.strip(),
        "user_prompt": user_prompt.strip()
    }
