"""
Save Module (Part J - Save Analysis to File)
Saves the complete structured medical analysis report to disk.
"""

import os
import datetime
from typing import Optional


DEFAULT_OUTPUT_PATH = os.path.join("outputs", "medical_analysis.txt")


def save_medical_analysis(
    report_text: str,
    output_path: str = DEFAULT_OUTPUT_PATH,
    append_timestamp_header: bool = True
) -> str:
    """
    Part J - Q10: Save the generated analysis to: outputs/medical_analysis.txt
    """
    # Ensure parent output directory exists
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    header = ""
    if append_timestamp_header:
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = (
            f"======================================================================\n"
            f"   AI-POWERED MEDICAL SYMPTOM ASSISTANT REPORT (GPT-4)\n"
            f"   Generated: {timestamp_str}\n"
            f"======================================================================\n\n"
        )

    full_content = header + report_text.strip() + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    return os.path.abspath(output_path)
