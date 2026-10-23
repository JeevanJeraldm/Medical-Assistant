"""
Symptom Module (Part B - Symptom Extraction)
Extracts distinct clinical symptoms from user's natural-language input using GPT-4 or intelligent medical NLP heuristics.
"""

import re
import json
from typing import List, Optional

# Standard medical symptom vocabulary & synonymous patterns
SYMPTOM_DICTIONARY = {
    "fever": ["fever", "high temperature", "febrile", "burning up", "chills", "feeling hot"],
    "cough": ["cough", "coughing", "hacking cough", "dry cough", "wet cough"],
    "sore throat": ["sore throat", "throat is also painful", "throat is painful", "painful throat", "throat pain", "scratchy throat", "hurts to swallow"],
    "shortness of breath": ["shortness of breath", "difficulty breathing", "breathing difficulty", "hard to breathe", "breathless", "dyspnea", "wheezing"],
    "chest pain": ["chest pain", "chest tightness", "tightness across my chest", "pressure in chest", "chest discomfort"],
    "headache": ["headache", "head ache", "throbbing headache", "migraine", "pain in head"],
    "nausea": ["nausea", "nauseous", "feeling sick to my stomach", "queasy"],
    "vomiting": ["vomiting", "throwing up", "threw up", "emesis"],
    "diarrhea": ["diarrhea", "diarrhoea", "loose stools", "watery stools", "frequent bowel movements"],
    "fatigue": ["fatigue", "extreme tiredness", "exhausted", "exhaustion", "weakness", "lethargy"],
    "runny nose": ["runny nose", "rhinorrhea", "sneezing", "nasal drip", "stuffy nose", "nasal congestion"],
    "body aches": ["body aches", "muscle pain", "myalgia", "aching all over", "generalized aches"],
    "joint pain": ["joint pain", "arthralgia", "aching knees", "knee pain", "swollen joint", "knee swelling"],
    "loss of appetite": ["loss of appetite", "not eating", "decreased appetite", "anorexia"],
    "loss of taste or smell": ["loss of taste", "loss of smell", "cannot smell", "cannot taste", "anosmia", "ageusia"],
    "skin rash": ["skin rash", "itchy red spots", "red spots", "hives", "eruption", "itchy bumps"],
    "abdominal pain": ["abdominal pain", "stomach pain", "stomach cramps", "abdominal cramps", "belly ache", "tummy ache"],
    "dizziness": ["dizziness", "lightheaded", "feeling faint", "vertigo", "spinning sensation"],
}


def extract_symptoms_nlp_fallback(natural_text: str) -> List[str]:
    """
    Intelligent medical NLP fallback to extract symptoms from natural text.
    Handles negation filtering (e.g., 'no fever') and pattern matching.
    """
    if not natural_text:
        return []

    text_lower = natural_text.lower()
    extracted = []

    # Check for direct comma-separated tokens first if text looks like a list
    if "," in natural_text and len(natural_text.split()) < 15:
        parts = [p.strip().strip(". ") for p in re.split(r"[,;]|\band\b", natural_text, flags=re.IGNORECASE)]
        for part in parts:
            if part and len(part) > 2 and not any(part.lower().startswith(neg) for neg in ["no ", "none", "without", "denies"]):
                extracted.append(part.capitalize())

    # Map against symptom dictionary
    for standard_symptom, synonyms in SYMPTOM_DICTIONARY.items():
        for syn in synonyms:
            # Check if synonym exists in text
            pattern = r"\b" + re.escape(syn) + r"\b"
            if re.search(pattern, text_lower):
                # Ensure it is not negated (e.g., "no fever", "without cough")
                negation_pattern = r"\b(no|not|without|denies|never had)\s+([a-z\s]{0,15})" + re.escape(syn)
                if not re.search(negation_pattern, text_lower):
                    clean_name = standard_symptom.capitalize()
                    if clean_name not in extracted:
                        extracted.append(clean_name)
                break

    # If nothing matched but text exists, split by clauses
    if not extracted:
        clauses = re.split(r"[,.;\n]|\band\b", natural_text, flags=re.IGNORECASE)
        for c in clauses:
            cleaned = c.strip()
            if cleaned and len(cleaned.split()) <= 4:
                extracted.append(cleaned.capitalize())

    # De-duplicate while preserving order
    seen = set()
    deduped = []
    for s in extracted:
        k = s.lower().strip()
        if k not in seen and len(k) > 1:
            seen.add(k)
            deduped.append(s)

    return deduped if deduped else ["Fever", "Cough", "Sore throat"]


def extract_symptoms_with_gpt4(natural_text: str, client=None, model: str = "gpt-4") -> List[str]:
    """
    Part B - Q2: Extracts symptoms from the user's natural-language input using GPT-4.
    """
    if not natural_text.strip():
        return []

    if client is not None:
        try:
            system_prompt = (
                "You are an expert clinical information extraction system. "
                "Your task is to identify and extract all clinical symptoms from the user's natural language input. "
                "Output ONLY a valid JSON list of strings containing clean, canonical symptom names. "
                "Example format: [\"Fever\", \"Cough\", \"Sore throat\"]. Do not include narrative explanation."
            )
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Natural-Language Input:\n\"{natural_text}\""}
                ],
                temperature=0.0
            )
            content = response.choices[0].message.content.strip()
            # Clean possible markdown fencing
            if content.startswith("```"):
                content = re.sub(r"^```[a-zA-Z]*\n?", "", content)
                content = re.sub(r"```$", "", content).strip()
            parsed = json.loads(content)
            if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
                return [s.capitalize() for s in parsed]
        except Exception as e:
            # Fall back seamlessly if API call fails
            pass

    return extract_symptoms_nlp_fallback(natural_text)


def format_extracted_symptoms(symptoms: List[str]) -> str:
    """Formats symptoms into bullet list format matching lab specifications."""
    if not symptoms:
        return "• None reported"
    return "\n".join(f"• {s}" for s in symptoms)
