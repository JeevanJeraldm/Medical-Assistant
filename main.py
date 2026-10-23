"""
Main Application (Part K - Complete Application Integration)
Integrates all modules into an interactive menu-driven CLI application.
Menu options:
  1. Enter Patient Information
  2. Enter Symptoms
  3. Analyze Symptoms
  4. Generate Follow-up Questions
  5. Display Possible Conditions
  6. Display Medical Attention Guidance
  7. Display Disclaimer
  8. Save Report
  9. Exit
"""

import os
import sys
from typing import Optional, List, Dict, Any

# Import all sub-modules
from profile_module import PatientProfile
from input_module import collect_patient_info_cli, select_sample_case_cli
from symptom_module import extract_symptoms_with_gpt4, format_extracted_symptoms
from context_module import analyze_context, format_missing_information
from prompt_module import construct_gpt4_prompt
from analysis_module import analyze_symptoms_gpt4, format_symptom_analysis_display
from question_module import generate_follow_up_questions, format_follow_up_questions
from safety_module import assess_risk_and_escalation, get_disclaimer
from save_module import save_medical_analysis
from utils import print_banner, build_structured_response, Colors

# Optional OpenAI client initialization
openai_client = None
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=api_key)
        print(f"[+] OpenAI client initialized with model '{OPENAI_MODEL}'.")
    except Exception as e:
        print(f"[!] Note: OpenAI client not loaded ({e}). Operating in resilient knowledge engine mode.")


class MedicalAssistantApp:
    def __init__(self):
        self.profile: Optional[PatientProfile] = None
        self.extracted_symptoms: List[str] = []
        self.missing_info: List[str] = []
        self.analysis_result: Dict[str, Any] = {}
        self.follow_up_questions: List[str] = []
        self.safety_assessment: Dict[str, Any] = {}
        self.full_report_text: str = ""

        # Preload standard sample case by default so user can immediately analyze
        self._load_default_sample()

    def _load_default_sample(self):
        """Loads default sample case matching the experiment problem statement."""
        self.profile = PatientProfile(
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

    def print_menu(self):
        """Displays the required 9-option interactive menu."""
        print(f"\n{Colors.CYAN}=================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}          MEDICAL ASSISTANT MAIN MENU{Colors.RESET}")
        print(f"{Colors.CYAN}=================================================={Colors.RESET}")
        print("  1. Enter Patient Information")
        print("  2. Enter Symptoms (Natural Language Input)")
        print("  3. Analyze Symptoms (Run Complete Assessment)")
        print("  4. Generate Follow-up Questions")
        print("  5. Display Possible Conditions")
        print("  6. Display Medical Attention Guidance")
        print("  7. Display Disclaimer")
        print("  8. Save Report (outputs/medical_analysis.txt)")
        print("  9. Exit")
        print(f"{Colors.CYAN}--------------------------------------------------{Colors.RESET}")
        print("  [K] Load Kaggle Benchmark Sample Case (Cases 1-6)")
        print("  [A] Run Complete Pipeline & Show Full Report")
        print(f"{Colors.CYAN}=================================================={Colors.RESET}")

    def run_enter_patient_info(self):
        """Option 1: Enter patient demographic and clinical information."""
        print(f"\n{Colors.BOLD}--> Option 1: Enter Patient Information{Colors.RESET}")
        self.profile = collect_patient_info_cli()

    def run_enter_symptoms(self):
        """Option 2: Enter symptoms in natural language and extract."""
        print(f"\n{Colors.BOLD}--> Option 2: Enter Symptoms (Part B - Natural Language Input){Colors.RESET}")
        print("Enter symptom description (e.g., 'I have been having fever and cough for two days. My throat is also painful.'):")
        user_input = input("> ").strip()
        if not user_input:
            user_input = "I have been having fever and cough for two days. My throat is also painful."
            print(f"Using default sample text: \"{user_input}\"")

        if self.profile is None:
            self.profile = PatientProfile()
        self.profile.natural_input = user_input
        self.profile.symptoms = user_input

        print("\n[*] Extracting symptoms from natural-language text...")
        self.extracted_symptoms = extract_symptoms_with_gpt4(user_input, client=openai_client, model=OPENAI_MODEL)
        self.profile.extracted_symptoms = self.extracted_symptoms

        print(f"\n{Colors.GREEN}[+] Extracted Symptoms:{Colors.RESET}")
        print(format_extracted_symptoms(self.extracted_symptoms))

    def run_analyze_symptoms(self):
        """Option 3: Perform comprehensive symptom analysis and context checking."""
        print(f"\n{Colors.BOLD}--> Option 3: Analyze Symptoms (Part C, D, E, F, G){Colors.RESET}")
        if not self.profile:
            self._load_default_sample()

        if not self.extracted_symptoms:
            raw_text = self.profile.natural_input or self.profile.symptoms
            self.extracted_symptoms = extract_symptoms_with_gpt4(raw_text, client=openai_client, model=OPENAI_MODEL)
            self.profile.extracted_symptoms = self.extracted_symptoms

        # Part C: Context Analysis
        print("[*] Analyzing context and identifying missing information...")
        self.missing_info = analyze_context(self.profile, self.extracted_symptoms)

        # Part D & E: Symptom Analysis
        print("[*] Generating preliminary symptom analysis with GPT-4...")
        self.analysis_result = analyze_symptoms_gpt4(
            self.profile,
            self.extracted_symptoms,
            self.missing_info,
            client=openai_client,
            model=OPENAI_MODEL
        )

        # Part F: Follow-up Questions
        self.follow_up_questions = generate_follow_up_questions(
            self.profile,
            self.extracted_symptoms,
            self.missing_info,
            client=openai_client,
            model=OPENAI_MODEL
        )

        # Part G: Safety Assessment
        self.safety_assessment = assess_risk_and_escalation(self.profile, self.extracted_symptoms)

        # Assemble Full Part H Structured Response
        self.full_report_text = build_structured_response(
            profile=self.profile,
            extracted_symptoms=self.extracted_symptoms,
            possible_conditions=self.analysis_result.get("possible_conditions", []),
            explanation=self.analysis_result.get("explanation", ""),
            missing_info=self.missing_info,
            follow_up_questions=self.follow_up_questions,
            medical_attention_guidance=self.safety_assessment.get("guidance", ""),
            note=self.analysis_result.get("note")
        )

        print(f"\n{Colors.GREEN}[+] Analysis completed successfully!{Colors.RESET}")
        print("-" * 50)
        print(format_symptom_analysis_display(self.analysis_result))
        print("-" * 50)

    def run_generate_follow_up_questions(self):
        """Option 4: Display generated follow-up questions."""
        print(f"\n{Colors.BOLD}--> Option 4: Follow-up Questions (Part F){Colors.RESET}")
        if not self.follow_up_questions:
            self.run_analyze_symptoms()
        print(format_follow_up_questions(self.follow_up_questions))

    def run_display_possible_conditions(self):
        """Option 5: Display possible conditions."""
        print(f"\n{Colors.BOLD}--> Option 5: Display Possible Conditions (Part E){Colors.RESET}")
        if not self.analysis_result:
            self.run_analyze_symptoms()
        print("\nPossible Conditions:")
        print("--------------------------------")
        for c in self.analysis_result.get("possible_conditions", []):
            print(f"• {c}")
        print("\nNote:")
        print(self.analysis_result.get("note", ""))

    def run_display_medical_attention(self):
        """Option 6: Display medical attention guidance."""
        print(f"\n{Colors.BOLD}--> Option 6: Medical Attention Guidance (Part G){Colors.RESET}")
        if not self.safety_assessment:
            self.safety_assessment = assess_risk_and_escalation(self.profile, self.extracted_symptoms)
        print(self.safety_assessment.get("guidance", ""))

    def run_display_disclaimer(self):
        """Option 7: Display disclaimer."""
        print(f"\n{Colors.BOLD}--> Option 7: Display Disclaimer (Part I){Colors.RESET}")
        print(get_disclaimer())

    def run_save_report(self):
        """Option 8: Save report to outputs/medical_analysis.txt."""
        print(f"\n{Colors.BOLD}--> Option 8: Save Report (Part J){Colors.RESET}")
        if not self.full_report_text:
            print("[*] Running analysis to generate full report before saving...")
            self.run_analyze_symptoms()

        saved_path = save_medical_analysis(self.full_report_text)
        print(f"{Colors.GREEN}[+] Medical analysis successfully saved to:{Colors.RESET} {saved_path}")

    def run_load_kaggle_case(self):
        """Option K: Select from Kaggle sample benchmark cases."""
        loaded = select_sample_case_cli()
        if loaded:
            self.profile = loaded
            self.extracted_symptoms = []
            self.analysis_result = {}
            self.full_report_text = ""
            print(f"{Colors.GREEN}[+] Active patient profile updated with {self.profile.age}y/o {self.profile.sex}.{Colors.RESET}")

    def run_full_pipeline(self):
        """Option A: Run complete end-to-end pipeline and print structured response."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}======================================================================{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}       RUNNING COMPLETE END-TO-END MEDICAL ASSISTANT PIPELINE{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}======================================================================{Colors.RESET}")
        self.run_analyze_symptoms()
        print("\n" + self.full_report_text)
        self.run_save_report()

    def start(self):
        """Main interaction loop."""
        print_banner()
        while True:
            self.print_menu()
            choice = input("\nEnter your choice (1-9, K, A): ").strip().upper()
            if choice == "1":
                self.run_enter_patient_info()
            elif choice == "2":
                self.run_enter_symptoms()
            elif choice == "3":
                self.run_analyze_symptoms()
            elif choice == "4":
                self.run_generate_follow_up_questions()
            elif choice == "5":
                self.run_display_possible_conditions()
            elif choice == "6":
                self.run_display_medical_attention()
            elif choice == "7":
                self.run_display_disclaimer()
            elif choice == "8":
                self.run_save_report()
            elif choice == "9":
                print(f"\n{Colors.YELLOW}[*] Exiting Medical Symptom Assistant. Stay healthy!{Colors.RESET}")
                sys.exit(0)
            elif choice == "K":
                self.run_load_kaggle_case()
            elif choice == "A":
                self.run_full_pipeline()
            else:
                print(f"{Colors.RED}[!] Invalid choice. Please enter a number between 1 and 9.{Colors.RESET}")


if __name__ == "__main__":
    app = MedicalAssistantApp()
    app.start()
