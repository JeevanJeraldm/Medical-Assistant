"""
Profile Module (Part A - Patient Information Model)
Defines the PatientProfile data structure and validation methods.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class PatientProfile:
    """Represents a structured patient health profile and symptom record."""
    age: str = ""
    sex: str = ""
    symptoms: str = ""
    duration: str = ""
    severity: str = "Mild"
    medical_history: str = "No known relevant condition"
    current_medications: str = "None"
    allergies: str = "None"
    natural_input: str = ""
    extracted_symptoms: List[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        """Checks whether the minimum essential profile fields are present."""
        return bool(self.age and (self.symptoms or self.natural_input))

    def format_summary(self) -> str:
        """Formats the patient information cleanly for clinical presentation."""
        lines = [
            f"• Age: {self.age}",
            f"• Sex: {self.sex if self.sex else 'Not specified'}",
            f"• Reported Symptoms: {self.symptoms if self.symptoms else 'Pending extraction'}",
            f"• Duration: {self.duration if self.duration else 'Not specified'}",
            f"• Severity: {self.severity if self.severity else 'Mild'}",
            f"• Medical History: {self.medical_history if self.medical_history else 'No known relevant condition'}",
            f"• Current Medications: {self.current_medications if self.current_medications else 'None'}",
            f"• Allergies: {self.allergies if self.allergies else 'None'}"
        ]
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the patient profile to a standard dictionary."""
        return {
            "age": self.age,
            "sex": self.sex,
            "symptoms": self.symptoms,
            "duration": self.duration,
            "severity": self.severity,
            "medical_history": self.medical_history,
            "current_medications": self.current_medications,
            "allergies": self.allergies,
            "natural_input": self.natural_input,
            "extracted_symptoms": self.extracted_symptoms,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatientProfile":
        """Instantiates a PatientProfile from dictionary data."""
        return cls(
            age=str(data.get("age", "")),
            sex=str(data.get("sex", "")),
            symptoms=str(data.get("symptoms", "")),
            duration=str(data.get("duration", "")),
            severity=str(data.get("severity", "Mild")),
            medical_history=str(data.get("medical_history", "No known relevant condition")),
            current_medications=str(data.get("current_medications", "None")),
            allergies=str(data.get("allergies", "None")),
            natural_input=str(data.get("natural_input", "")),
            extracted_symptoms=list(data.get("extracted_symptoms", [])),
        )
