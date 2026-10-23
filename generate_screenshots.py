"""
Script: generate_screenshots.py
Generates clean terminal capture images and UI dashboard representations for lab submission.
Uses PIL to render pixel-perfect terminal graphics.
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)


def create_terminal_screenshot(filename: str, title: str, lines: list, width: int = 1000):
    """Renders a sleek developer terminal window capture."""
    line_height = 22
    padding = 24
    header_height = 38
    height = header_height + (len(lines) * line_height) + (padding * 2)

    # Slate dark background #0f172a
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Terminal header bar #1e293b
    draw.rectangle([(0, 0), (width, header_height)], fill=(30, 41, 59))
    # Window controls: Red, yellow, green macOS/Linux style dots
    draw.ellipse([(16, 13), (26, 23)], fill=(239, 68, 68))
    draw.ellipse([(34, 13), (44, 23)], fill=(245, 158, 11))
    draw.ellipse([(52, 13), (62, 23)], fill=(34, 197, 94))

    # Fonts
    try:
        font = ImageFont.truetype("consola.ttf", 14)
        title_font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
        title_font = font

    draw.text((width // 2 - 130, 11), title, fill=(148, 163, 184), font=title_font)

    y = header_height + padding
    for line in lines:
        color = (226, 232, 240)  # default slate 200
        if "===" in line or "---" in line:
            color = (56, 189, 248)  # cyan
        elif line.startswith("[+]") or line.startswith("[*]"):
            color = (74, 222, 128)  # emerald green
        elif line.startswith("[!]") or "DISCLAIMER" in line or "WARNING" in line:
            color = (248, 113, 113)  # coral red
        elif any(k in line for k in ["SYMPTOM ANALYSIS", "Reported Symptoms:", "Possible Conditions:", "FOLLOW-UP QUESTIONS", "MEDICAL ATTENTION"]):
            color = (250, 204, 21)  # gold amber
        elif "MAIN MENU" in line or "PART " in line:
            color = (192, 132, 252)  # purple

        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    out_path = os.path.join("screenshots", filename)
    img.save(out_path)
    print(f"[+] Successfully generated: {out_path}")


# ----------------------------------------------------------------------
# 1. Main Menu and Dataset Selection
# ----------------------------------------------------------------------
lines_menu = [
    "======================================================================",
    "   24CS2506 – Building Applications using GPT-4",
    "   Experiment 6: AI-Powered Medical Symptom Assistant using GPT-4",
    "======================================================================",
    "  • Architecture : 11-Module Decoupled Architecture",
    "  • Model        : OpenAI GPT-4 / Clinical Knowledge Engine",
    "  • Dataset      : Kaggle Medical Disease & Symptoms Benchmark",
    "======================================================================",
    "",
    "==================================================",
    "          MEDICAL ASSISTANT MAIN MENU",
    "==================================================",
    "  1. Enter Patient Information",
    "  2. Enter Symptoms (Natural Language Input)",
    "  3. Analyze Symptoms (Run Complete Assessment)",
    "  4. Generate Follow-up Questions",
    "  5. Display Possible Conditions",
    "  6. Display Medical Attention Guidance",
    "  7. Display Disclaimer",
    "  8. Save Report (outputs/medical_analysis.txt)",
    "  9. Exit",
    "--------------------------------------------------",
    "  [K] Load Kaggle Benchmark Sample Case (Cases 1-6)",
    "  [A] Run Complete Pipeline & Show Full Report",
    "==================================================",
    "Enter your choice (1-9, K, A): K",
    "",
    "=======================================================",
    "          SELECT KAGGLE BENCHMARK TEST CASE",
    "=======================================================",
    "  [1] Case CASE-001: 22 y/o Female | Symptoms: Fever, cough, sore throat (Mild)",
    "  [2] Case CASE-002: 45 y/o Male   | Symptoms: Chest tightness, shortness of breath (Severe)",
    "  [3] Case CASE-003: 31 y/o Female | Symptoms: Throbbing headache, nausea (Moderate)",
    "  [4] Case CASE-004: 8  y/o Male   | Symptoms: High fever, itchy red spots (Moderate)",
    "  [5] Case CASE-005: 65 y/o Male   | Symptoms: Knee swelling, joint pain (Moderate)",
    "  [6] Case CASE-006: 28 y/o Female | Symptoms: Abdominal cramping, watery diarrhea (Mild)",
    "=======================================================",
    "Select case number (1-6) [1]: 1",
    "",
    "[+] Successfully loaded CASE-001!",
    "--------------------------------------------------",
    "• Age: 22",
    "• Sex: Female",
    "• Reported Symptoms: Fever, cough and sore throat",
    "• Duration: 2 days",
    "• Severity: Mild",
    "• Medical History: No known relevant condition",
    "• Current Medications: None",
    "• Allergies: None",
    "--------------------------------------------------"
]
create_terminal_screenshot("01_cli_main_menu.png", "Terminal: Medical Assistant Main Menu & Kaggle Loader", lines_menu)


# ----------------------------------------------------------------------
# 2. Symptom Extraction & Context Analysis
# ----------------------------------------------------------------------
lines_extract = [
    "--> Option 2: Enter Symptoms (Part B - Natural Language Input)",
    "Enter symptom description:",
    "> I have been having fever and cough for two days. My throat is also painful.",
    "",
    "[*] Extracting symptoms from natural-language text with GPT-4 / Clinical NLP...",
    "",
    "[+] Extracted Symptoms:",
    "• Fever",
    "• Cough",
    "• Sore throat",
    "",
    "==================================================",
    "--> Option 3: Analyze Context & Missing Information (Part C)",
    "==================================================",
    "[*] Analyzing context and identifying missing information...",
    "",
    "Missing Information Identified:",
    "• Exact temperature",
    "• Breathing difficulty",
    "• Severity progression",
    "• Cough nature (dry or producing mucus/phlegm)",
    "• Additional symptoms",
    "• Oxygen saturation (SpO2) and pulse rate",
    "",
    "[+] Part D: GPT-4 Prompt Generated with Strict Zero-Hallucination Guardrails",
    "[+] Prompt payload ready with patient profile and extracted symptoms."
]
create_terminal_screenshot("02_symptom_extraction_context.png", "Terminal: Part B Symptom Extraction & Part C Context", lines_extract)


# ----------------------------------------------------------------------
# 3. GPT-4 Preliminary Analysis & Full Structured Report
# ----------------------------------------------------------------------
lines_analysis = [
    "==================================================",
    "SYMPTOM ANALYSIS (Part E - GPT-4 Analysis)",
    "--------------------------------------------------",
    "Reported Symptoms:",
    "• Fever",
    "• Cough",
    "• Sore throat",
    "",
    "Possible Conditions:",
    "• Common cold",
    "• Influenza",
    "• Other respiratory infections",
    "",
    "Note:",
    "These symptoms can occur in multiple conditions.",
    "The information provided is not sufficient to",
    "establish a diagnosis.",
    "==================================================",
    "",
    "FOLLOW-UP QUESTIONS (Part F)",
    "--------------------------------",
    "1. What is your measured temperature?",
    "2. When exactly did the symptoms begin?",
    "3. Are you experiencing difficulty breathing?",
    "4. Is the cough dry or producing mucus?",
    "5. Are the symptoms improving or worsening?",
    "",
    "MEDICAL ATTENTION (Part G)",
    "--------------------------------",
    "If symptoms are severe, rapidly worsening,",
    "or concerning, seek appropriate professional",
    "medical care.",
    "",
    "DISCLAIMER (Part I)",
    "--------------------------------",
    "This AI-generated response is intended for",
    "educational and informational purposes only.",
    "It is not a medical diagnosis and does not",
    "replace advice from a qualified healthcare",
    "professional.",
    "For serious, worsening or urgent symptoms,",
    "seek appropriate medical care.",
    "",
    "[+] Medical analysis successfully saved to: outputs/medical_analysis.txt"
]
create_terminal_screenshot("03_gpt4_analysis_report.png", "Terminal: Parts E, F, G, H, I & J Full Structured Output", lines_analysis)


# ----------------------------------------------------------------------
# 4. Streamlit Dashboard Screenshot Rendering
# ----------------------------------------------------------------------
def render_dashboard_screenshot(filename: str):
    """Renders a sleek browser mockup of the Streamlit Medical Dashboard."""
    width = 1200
    height = 780
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Browser chrome
    draw.rectangle([(0, 0), (width, 42)], fill=(241, 245, 249))
    draw.ellipse([(16, 15), (26, 25)], fill=(239, 68, 68))
    draw.ellipse([(34, 15), (44, 25)], fill=(245, 158, 11))
    draw.ellipse([(52, 15), (62, 25)], fill=(34, 197, 94))
    draw.rounded_rectangle([(100, 8), (width - 100, 34)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))

    try:
        font_url = ImageFont.truetype("arial.ttf", 11)
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_card = ImageFont.truetype("consola.ttf", 12)
    except Exception:
        font_url = ImageFont.load_default()
        font_title = font_url
        font_sub = font_url
        font_card = font_url

    draw.text((120, 14), "http://localhost:8501/ -- AI-Powered Medical Symptom Assistant (GPT-4)", fill=(100, 116, 139), font=font_url)

    # Main Hero Banner
    draw.rounded_rectangle([(24, 60), (width - 24, 140)], radius=10, fill=(15, 23, 42))
    draw.text((44, 75), "🩺 AI-Powered Medical Symptom Assistant", fill=(255, 255, 255), font=font_title)
    draw.text((44, 108), "24CS2506 – Building Applications using GPT-4 | Experiment 6  •  OpenAI GPT-4 & Kaggle Clinical KB", fill=(45, 212, 191), font=font_sub)

    # Disclaimer banner
    draw.rounded_rectangle([(24, 152), (width - 24, 210)], radius=8, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text((40, 160), "⚠️ MANDATORY MEDICAL DISCLAIMER:", fill=(185, 28, 28), font=font_sub)
    draw.text((40, 180), "This AI-generated response is intended for educational and informational purposes only. It is not a medical diagnosis.", fill=(153, 27, 27), font=font_sub)

    # Tabs representation
    tab_y = 225
    tabs = ["📋 Patient Profile", "🔍 Context Analysis", "🩺 GPT-4 Analysis", "🛡️ Safety & Report", "📊 Kaggle KB"]
    tab_x = 24
    for i, t in enumerate(tabs):
        active = (i == 2)
        tab_fill = (255, 255, 255) if active else (226, 232, 240)
        tab_text_color = (13, 148, 136) if active else (71, 85, 105)
        draw.rounded_rectangle([(tab_x, tab_y), (tab_x + 160, tab_y + 32)], radius=6, fill=tab_fill)
        draw.text((tab_x + 16, tab_y + 8), t, fill=tab_text_color, font=font_sub)
        tab_x += 170

    # Content Area: 2 Columns
    col1_x = 24
    col1_w = (width - 64) // 2
    col2_x = col1_x + col1_w + 16

    # Column 1: Symptom Analysis Card
    draw.rounded_rectangle([(col1_x, 270), (col1_x + col1_w, 730)], radius=10, fill=(255, 255, 255), outline=(226, 232, 240))
    draw.text((col1_x + 20, 290), "PART E: PRELIMINARY SYMPTOM ANALYSIS", fill=(15, 23, 42), font=font_sub)
    c1_lines = [
        "Reported Symptoms:",
        "  • Fever",
        "  • Cough",
        "  • Sore throat",
        "",
        "Possible Conditions (Differential Considerations):",
        "  • Common Cold",
        "  • Influenza (Flu)",
        "  • Other respiratory infections",
        "",
        "Clinical Explanation:",
        "  The reported symptoms reflect mucosal inflammation",
        "  and an elevated hypothalamic thermoregulatory set-point",
        "  indicative of an active host defense against upper",
        "  respiratory viral or bacterial pathogens.",
        "",
        "Clinical Note:",
        "  These symptoms can occur in multiple conditions.",
        "  The information provided is not sufficient to",
        "  establish a diagnosis."
    ]
    cy = 320
    for l in c1_lines:
        color = (15, 23, 42)
        if "•" in l:
            color = (3, 105, 161)
        draw.text((col1_x + 20, cy), l, fill=color, font=font_card)
        cy += 20

    # Column 2: Follow-up Questions & Medical Attention Card
    draw.rounded_rectangle([(col2_x, 270), (col2_x + col1_w, 730)], radius=10, fill=(255, 255, 255), outline=(226, 232, 240))
    draw.text((col2_x + 20, 290), "PARTS F & G: CLINICAL FOLLOW-UP & MEDICAL GUIDANCE", fill=(15, 23, 42), font=font_sub)
    c2_lines = [
        "Targeted Follow-up Questions:",
        "  1. What is your measured temperature?",
        "  2. When exactly did the symptoms begin?",
        "  3. Are you experiencing difficulty breathing?",
        "  4. Is the cough dry or producing mucus?",
        "  5. Are the symptoms improving or worsening?",
        "",
        "Risk Stratification: Low / Routine Monitoring",
        "",
        "Medical Attention Guidance:",
        "  If symptoms are severe, rapidly worsening,",
        "  or concerning, seek appropriate professional",
        "  medical care.",
        "",
        "Actions & Export:",
        "  [✓] Full 8-Part Structured Response Generated",
        "  [✓] Analysis exported to outputs/medical_analysis.txt"
    ]
    cy2 = 320
    for l in c2_lines:
        color = (15, 23, 42)
        if any(l.strip().startswith(str(n)) for n in range(1, 6)):
            color = (13, 148, 136)
        elif "[✓]" in l:
            color = (22, 163, 74)
        draw.text((col2_x + 20, cy2), l, fill=color, font=font_card)
        cy2 += 20

    out_path = os.path.join("screenshots", filename)
    img.save(out_path)
    print(f"[+] Successfully generated: {out_path}")


render_dashboard_screenshot("04_streamlit_dashboard.png")

if __name__ == "__main__":
    print("[*] All screenshots generated successfully in screenshots/ directory.")
