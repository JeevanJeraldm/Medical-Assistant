"""
Input Module (Part A - User Input Collection)
Provides interactive and programmatically validated input collection for patient profile details.
"""

import os
import csv
from typing import Optional, List, Dict
from profile_module import PatientProfile


def get_input_with_default(prompt: str, default: str = "") -> str:
    """Helper to collect terminal input with an optional default value."""
    if default:
        user_val = input(f"{prompt} [{default}]: ").strip()
        return user_val if user_val else default
    return input(f"{prompt}: ").strip()


def collect_patient_info_cli() -> PatientProfile:
    """
    Part A - Q1: Collect the following information from the user:
      - Age
      - Sex, if relevant
      - Symptoms
      - Duration
      - Severity
      - Relevant medical history
      - Current medications, if relevant
      - Allergies, if relevant
    """
    print("\n" + "=" * 50)
    print("        PART A: PATIENT INFORMATION INPUT")
    print("=" * 50)
    print("Please enter patient details (press Enter to accept default values):")

    # 1. Age
    while True:
        age_str = get_input_with_default("  Enter Age", "22")
        if age_str.isdigit() and int(age_str) > 0:
            break
        print("  [!] Please enter a valid positive numeric age.")

    # 2. Sex
    sex = get_input_with_default("  Enter Sex (e.g., Female, Male, Other)", "Female")

    # 3. Symptoms (Natural language or list)
    print("\n  Enter Symptoms (natural language description or comma-separated list):")
    print("  e.g., 'Fever, cough and sore throat' or full sentence description.")
    symptoms = get_input_with_default("  Symptoms", "Fever, cough and sore throat")

    # 4. Duration
    duration = get_input_with_default("  Enter Duration (e.g., 2 days, 1 week)", "2 days")

    # 5. Severity
    print("\n  Select Severity:")
    print("    [1] Mild  (Default)")
    print("    [2] Moderate")
    print("    [3] Severe")
    sev_choice = get_input_with_default("  Choose severity [1-3]", "1")
    severity_map = {"1": "Mild", "2": "Moderate", "3": "Severe"}
    severity = severity_map.get(sev_choice, "Mild")

    # 6. Relevant medical history
    history = get_input_with_default("  Relevant Medical History", "No known relevant condition")

    # 7. Current medications
    medications = get_input_with_default("  Current Medications, if relevant", "None")

    # 8. Allergies
    allergies = get_input_with_default("  Allergies, if relevant", "None")

    profile = PatientProfile(
        age=age_str,
        sex=sex,
        symptoms=symptoms,
        duration=duration,
        severity=severity,
        medical_history=history,
        current_medications=medications,
        allergies=allergies,
        natural_input=symptoms
    )

    print("\n[+] Patient information captured successfully:")
    print("-" * 50)
    print(profile.format_summary())
    print("-" * 50)
    return profile


def load_sample_cases_from_csv(csv_path: str = "data/sample_cases.csv") -> List[Dict[str, str]]:
    """Loads sample patient benchmark cases from CSV."""
    if not os.path.exists(csv_path):
        return []
    cases = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(row)
    return cases


def select_sample_case_cli() -> Optional[PatientProfile]:
    """Allows user to select a pre-configured Kaggle benchmark test case."""
    cases = load_sample_cases_from_csv()
    if not cases:
        print("[!] No sample cases found in data/sample_cases.csv.")
        return None

    print("\n" + "=" * 55)
    print("          SELECT KAGGLE BENCHMARK TEST CASE")
    print("=" * 55)
    for i, c in enumerate(cases, 1):
        print(f"  [{i}] Case {c.get('case_id')}: {c.get('age')}y/o {c.get('sex')} | Symptoms: {c.get('symptoms')} ({c.get('severity')})")
    print("=" * 55)

    choice = get_input_with_default("Select case number (1-6)", "1")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(cases):
            selected = cases[idx]
            profile = PatientProfile(
                age=selected.get("age", ""),
                sex=selected.get("sex", ""),
                symptoms=selected.get("symptoms", ""),
                duration=selected.get("duration", ""),
                severity=selected.get("severity", "Mild"),
                medical_history=selected.get("medical_history", "No known relevant condition"),
                current_medications=selected.get("current_medications", "None"),
                allergies=selected.get("allergies", "None"),
                natural_input=selected.get("natural_input", selected.get("symptoms", ""))
            )
            print(f"\n[+] Successfully loaded {selected.get('case_id')}!")
            print("-" * 50)
            print(profile.format_summary())
            print("-" * 50)
            return profile
    except ValueError:
        pass
    print("[!] Invalid selection.")
    return None
