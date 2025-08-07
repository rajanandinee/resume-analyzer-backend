from fpdf import FPDF
import re

# Function to clean unsupported characters
def clean_text(text):
    # Replace or remove characters that aren't supported in standard fonts
    return text.replace("₹", "Rs.").encode("ascii", "ignore").decode("ascii")

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Arial", size=12)  # Use a reliable built-in font

def generate_pdf_report(analysis_result):
    pdf = PDF()

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, txt="Resume Analysis Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"ATS Compatibility Score: {analysis_result['ats_score']}%", ln=True)
    pdf.ln(5)

    # Suggested Skills
    suggested_skills = analysis_result.get('missing_skills', [])
    pdf.cell(0, 10, txt="Suggested Skills to Add:", ln=True)
    if suggested_skills:
        for skill in suggested_skills:
            pdf.cell(0, 10, txt=f"- {clean_text(skill)}", ln=True)
    else:
        pdf.cell(0, 10, txt="- No missing skills detected", ln=True)

    # Job Recommendations
    pdf.ln(5)
    pdf.cell(0, 10, txt="Recommended Jobs:", ln=True)
    job_recommendations = analysis_result.get("job_recommendations", [])
    if job_recommendations:
        for job in job_recommendations:
            pdf.cell(0, 10, txt=f"- {clean_text(job)}", ln=True)
    else:
        pdf.cell(0, 10, txt="- No job recommendations found", ln=True)

    # Estimated Salary
    estimated_salary = analysis_result.get('estimated_salary', '').strip()
    estimated_salary = estimated_salary.replace("–", "-").replace("—", "-")
    pdf.ln(5)
    pdf.cell(0, 10, txt="Estimated Salary Range:", ln=True)
    if estimated_salary:
        pdf.cell(0, 10, txt=f"- {estimated_salary}", ln=True)
    else:
        pdf.cell(0, 10, txt="- Not Available", ln=True)
    pdf.ln(10)

    # Resume Snippet
    snippet = analysis_result.get("resume_text_snippet", "")
    pdf.multi_cell(0, 10, txt="Resume Snippet Preview:\n" + clean_text(snippet))

    # Return PDF as byte string
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # Safer than utf-8 for PDF content
    return pdf_bytes


