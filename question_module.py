"""
Question Module (Part F - Follow-Up Questions Generation)
Generates targeted clinical follow-up questions to clarify symptom progression, severity, and context.
"""

from typing import List, Optional
from profile_module import PatientProfile


DEFAULT_FOLLOW_UP_QUESTIONS = [
    "What is your measured temperature?",
    "When exactly did the symptoms begin?",
    "Are you experiencing difficulty breathing?",
    "Is the cough dry or producing mucus?",
    "Are the symptoms improving or worsening?"
]


def generate_follow_up_questions(
    profile: PatientProfile,
    extracted_symptoms: List[str],
    missing_info: Optional[List[str]] = None,
    client=None,
    model: str = "gpt-4"
) -> List[str]:
    """
    Part F - Q6: Generate appropriate follow-up questions.
    """
    symptoms_lower = [s.lower() for s in extracted_symptoms]
    questions: List[str] = []

    # 1. Temperature question if fever or general illness
    if any(k in s for s in symptoms_lower for k in ["fever", "chills", "throat", "cough"]):
        questions.append("What is your measured temperature?")

    # 2. Timing and onset
    questions.append("When exactly did the symptoms begin?")

    # 3. Dyspnea / breathing evaluation
    questions.append("Are you experiencing difficulty breathing?")

    # 4. Cough characteristics if cough present
    if any("cough" in s for s in symptoms_lower):
        questions.append("Is the cough dry or producing mucus?")
    elif any("throat" in s for s in symptoms_lower):
        questions.append("Is it painful to swallow fluids or saliva?")
    elif any("headache" in s for s in symptoms_lower):
        questions.append("Is the headache accompanied by visual disturbances or neck stiffness?")
    elif any("chest" in s for s in symptoms_lower):
        questions.append("Does the chest discomfort radiate to your arm, neck, or jaw?")
    else:
        questions.append("Have you experienced any other associated symptoms like nausea or body aches?")

    # 5. Progression over time
    questions.append("Are the symptoms improving or worsening?")

    # Ensure at least 5 questions
    if len(questions) < 5:
        questions.append("Are you taking any over-the-counter medications that provide relief?")

    return questions[:5]


def format_follow_up_questions(questions: List[str]) -> str:
    """Formats the follow-up questions matching Part F sample output."""
    lines = [
        "FOLLOW-UP QUESTIONS",
        "--------------------------------"
    ]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
    return "\n".join(lines)
