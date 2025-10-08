import pandas as pd
from fpdf import FPDF

# Load datasets
patient_df = pd.read_csv("patient_demography.csv")
claims_df = pd.read_csv("insurance_claims.csv")
clinical_df = pd.read_csv("clinical_notes.csv")

class ClaimPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Insurance Claim Document", ln=True, align="C")
        self.ln(2)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(10, 20, 200, 20)  # Line below title

    def footer(self):
        self.set_y(-25)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())  # Line above footer
        self.set_y(-20)
        self.set_font("Arial", "I", 8)
        self.multi_cell(0, 10, "Disclaimer: This document is system-generated and intended for simulation purposes only. Contact your insurer for official records.", align="C")

i = 0
for _, claim in claims_df.iterrows():
    if i < 10:
        i += 1
        patient_id = claim["Patient ID"]
        
        # Get patient info
        patient = patient_df[patient_df["Patient ID"] == patient_id].iloc[0]
        name = patient["Name"]
        address = patient["Address"]
        
        # Get clinical info
        clinical = clinical_df[clinical_df["Patient ID"] == patient_id]
        doctor = clinical.iloc[0]["Physician"] if not clinical.empty else "Unknown"

        # Create PDF
        pdf = ClaimPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Top section: Left block
        left_x, left_y = 10, 25
        pdf.set_xy(left_x, left_y)
        left_lines = [
            f"Claim ID: {claim['Claim ID']}",
            f"Claim Date: {claim['Claim Date']}",
            f"Status: {claim['Status']}"
        ]
        for line in left_lines:
            pdf.set_xy(left_x, pdf.get_y())
            pdf.cell(90, 8, line, ln=True)

        # Top section: Right block
        right_x, right_y = 110, 25
        pdf.set_xy(right_x, right_y)
        right_lines = [
            f"Patient Name: {name}",
            f"Address: {address}",
            f"Physician: {doctor}"
        ]
        for line in right_lines:
            pdf.set_xy(right_x, pdf.get_y())
            pdf.multi_cell(90, 8, line)

        # Divider between top and bottom
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.5)
        pdf.line(10, 65, 200, 65)

        # Bottom section
        pdf.set_xy(10, 70)
        bottom_lines = [
            f"Description: {claim['Claim Description']}",
            f"Procedure Code: {claim['Procedure Code']}",
            f"Amount: INR {claim['Amount Claimed']}"
        ]
        for line in bottom_lines:
            pdf.set_xy(10, pdf.get_y())
            pdf.multi_cell(190, 8, line)

        # Save PDF
        filename = f"claim_{claim['Claim ID']}.pdf"
        pdf.output(filename)

print("✅ PDF generation complete with new layout and dividers.")