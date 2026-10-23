# Kaggle Dataset Reference & Integration Documentation

## 📊 Overview
This project integrates clinical disease and symptom mappings sourced and synthesized from prominent medical benchmarks available on Kaggle:
1. **Disease and Symptoms Dataset / Prediction Benchmark**:
   - **Kaggle Sources**:
     - [Disease Symptom Description & Precaution Dataset](https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset) by *itachi9604*
     - [Disease and Symptoms Dataset](https://www.kaggle.com/datasets/kaushil268/disease-symptom-dataset) by *kaushil268*
     - [Medical Symptom-Condition Correlation Benchmark](https://www.kaggle.com/datasets/dhruvildave/diseases-and-symptoms-dataset) by *dhruvildave*
   - **Domain**: Clinical symptom correlation, differential condition assessment, triage risk stratification, and patient follow-up elicitation.

---

## 📁 Dataset Files in this Project

### 1. `data/sample_cases.csv`
Contains annotated patient test profiles used for standard lab evaluation, unit tests, and validation runs:
- **`case_id`**: Unique test case identifier (`CASE-001` through `CASE-006`).
- **`age`**: Patient age (numeric years).
- **`sex`**: Biological sex (`Female` / `Male` / `Other`).
- **`symptoms`**: Structured comma-separated symptom list.
- **`duration`**: Onset duration (e.g., `2 days`, `3 weeks`).
- **`severity`**: Patient-reported severity level (`Mild`, `Moderate`, `Severe`).
- **`medical_history`**: Pre-existing conditions or comorbidities.
- **`current_medications`**: Prescribed or over-the-counter medications currently taken.
- **`allergies`**: Known drug, food, or environmental allergies.
- **`natural_input`**: Realistic natural-language narrative for testing Part B (Symptom Extraction).

### 2. `data/kaggle_disease_symptoms.csv`
Clinical reference database mapped to 12 major pathology categories covering respiratory, cardiovascular, neurological, gastrointestinal, and systemic disorders:
- **`disease`**: Standard clinical condition name.
- **`primary_symptoms`**: Pathognomonic and high-frequency presentation symptoms.
- **`secondary_symptoms`**: Associated constitutional and prodromal symptoms.
- **`typical_duration`**: Expected clinical natural course without complications.
- **`severity_levels`**: Observed severity spectrum (`Mild`, `Moderate`, `Severe`).
- **`risk_level`**: Triage urgency categorization (`Low`, `Moderate`, `High`, `Critical`).
- **`possible_causes`**: Known viral, bacterial, inflammatory, or lifestyle etiologies.
- **`red_flag_indicators`**: Emergency escalation triggers requiring emergency medical services.
- **`follow_up_questions`**: Pre-compiled differential diagnostic inquiry prompts.

---

## 🔬 Clinical Purpose in Application
1. **Part B (Symptom Extraction)**: Serves as an NLP terminology vocabulary to extract clean clinical symptoms from unstructured patient phrases.
2. **Part C (Context Analysis)**: Evaluates missing clinical variables (exact body temperature, sputum nature, onset rapidity, comorbidities).
3. **Part D & E (GPT-4 Prompt Generation & Symptom Analysis)**: Provides factual grounding to GPT-4 prompts, enforcing zero-hallucination and cautious probabilistic language.
4. **Part F & G (Follow-up Questions & Risk Assessment)**: Correlates red-flag symptoms with clinical guidelines to formulate targeted inquiries and safety escalations.
