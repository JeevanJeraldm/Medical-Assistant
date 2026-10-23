"""
Utils Module (Part H - Structured Response Assembly & CLI Formatting)
Assembles the complete structured response in the required 8-section format,
and provides terminal styling and formatting helpers.
"""

from typing import List, Dict, Any, Optional
from profile_module import PatientProfile
from safety_module import get_disclaimer, format_medical_attention
from context_module import format_missing_information
from symptom_module import format_extracted_symptoms
from question_module import format_follow_up_questions


# ANSI Color Codes for enhanced terminal UX
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def print_banner():
    """Prints the application startup banner."""
    print(f"{Colors.CYAN}======================================================================{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}   24CS2506 – Building Applications using GPT-4{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}   Experiment 6: AI-Powered Medical Symptom Assistant using GPT-4{Colors.RESET}")
    print(f"{Colors.CYAN}======================================================================{Colors.RESET}")
    print("  • Architecture : 11-Module Decoupled Architecture")
    print("  • Model        : OpenAI GPT-4 / Clinical Knowledge Engine")
    print("  • Dataset      : Kaggle Medical Disease & Symptoms Benchmark")
    print(f"{Colors.CYAN}======================================================================{Colors.RESET}\n")


def build_structured_response(
    profile: PatientProfile,
    extracted_symptoms: List[str],
    possible_conditions: List[str],
    explanation: str,
    missing_info: List[str],
    follow_up_questions: List[str],
    medical_attention_guidance: str,
    note: Optional[str] = None
) -> str:
    """
    Part H - Q8: Generate the complete response using the following format:
      1. Reported Symptoms
      2. Patient Information
      3. Possible Conditions
      4. Explanation
      5. Missing Information
      6. Follow-up Questions
      7. Medical Attention Guidance
      8. Disclaimer
    """
    sections = []

    # 1. Reported Symptoms
    symptoms_block = format_extracted_symptoms(extracted_symptoms)
    sections.append(f"1. Reported Symptoms\n--------------------------------\n{symptoms_block}")

    # 2. Patient Information
    patient_info_block = profile.format_summary()
    sections.append(f"2. Patient Information\n--------------------------------\n{patient_info_block}")

    # 3. Possible Conditions
    conditions_list = "\n".join(f"• {c}" for c in possible_conditions) if possible_conditions else "• Common cold\n• Influenza\n• Other respiratory infections"
    note_str = f"\n\nNote:\n{note}" if note else "\n\nNote:\nThese symptoms can occur in multiple conditions.\nThe information provided is not sufficient to\nestablish a diagnosis."
    sections.append(f"3. Possible Conditions\n--------------------------------\n{conditions_list}{note_str}")

    # 4. Explanation
    sections.append(f"4. Explanation\n--------------------------------\n{explanation.strip()}")

    # 5. Missing Information
    missing_block = format_missing_information(missing_info)
    sections.append(f"5. Missing Information\n--------------------------------\n{missing_block}")

    # 6. Follow-up Questions
    questions_list = "\n".join(f"{i}. {q}" for i, q in enumerate(follow_up_questions, 1))
    sections.append(f"6. Follow-up Questions\n--------------------------------\n{questions_list}")

    # 7. Medical Attention Guidance
    sections.append(f"7. Medical Attention Guidance\n--------------------------------\n{medical_attention_guidance.strip()}")

    # 8. Disclaimer
    disclaimer_text = get_disclaimer()
    sections.append(f"8. Disclaimer\n--------------------------------\n{disclaimer_text}")

    separator = "\n\n" + "=" * 50 + "\n\n"
    return separator.join(sections)
