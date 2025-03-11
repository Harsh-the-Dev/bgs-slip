import io
import os
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from .forms import SalarySlipForm
import os
from django.conf import settings
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def salary_slip_form(request):
    """Handles form submission and generates salary slip PDF"""
    if request.method == "POST":
        form = SalarySlipForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  # ✅ Get all cleaned data (including calculated values)
            return generate_salary_slip_pdf(data)  # ✅ Pass directly to PDF function
    else:
        form = SalarySlipForm()

    return render(request, "salary_slip_form.html", {"form": form})

import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_salary_slip_pdf(data):
    """Generate a professional salary slip PDF in vertical (portrait) format"""

    buffer = io.BytesIO()
    page_width, page_height = A4
    margin = 40  # Left & Right Margin
    usable_width = page_width - (2 * margin)  # 595 - 80 = 515 points

    doc = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=margin, rightMargin=margin, topMargin=50, bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()

    # ✅ Title & Header
    title = Paragraph("<b>Bridge Group Solutions</b>", styles['Title'])
    subtitle = Paragraph(f"<b>PAYSLIP FOR  {data.get('month', 'Feburary 2025')}</b>", styles['Heading2'])
    header_table = Table([[title], [subtitle]], colWidths=[usable_width])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    # ✅ Employee Pay Summary
    emp_details = [
        ["Employee Name:", data["employee_name"]],
        ["Employee Code:", data["employee_code"]],
        ["Designation:", data["designation"]],
        ["Date of Joining:", str(data["date_of_joining"])],
        ["Paid Days:", f"{data['paid_days']} / {data['total_days']}"],
        ["Non Paid Days:", data["non_paid_days"]],
    ]
    emp_table = Table(emp_details, colWidths=[160, 355])
    emp_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    # ✅ Earnings Section (Single Column Layout)
    earnings_data = [
        ["Component", "Amount"],
        ["Basic", f"{data['basic']}"],
        ["HRA", f"{data['hra']}"],
        ["Conveyance", f"{data['conveyance']}"],
        ["Other Allowance", f"{data['other_allowance']}"],
        ["Welfare", f"{data['welfare']}"],
        ["Gross Earnings", f"{data['gross_earnings']}"],
    ]
    earnings_table = Table(earnings_data, colWidths=[250, 250])
    earnings_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    # ✅ Deductions Section (Below Earnings)
    deductions_data = [
        ["Component", "Amount"],
        ["Tax", "0.00"],
        ["PF", "0.00"],
        ["Other Deductions", "0.00"],
        ["Total Deductions", f"{data['total_deductions']}"],
    ]
    deductions_table = Table(deductions_data, colWidths=[250, 250])
    deductions_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    # ✅ Reimbursements Section
    reimbursements_data = [
        ["Component", "Amount"],
        ["Internet", f"{data['internet']}"],
        ["Traveling", f"{data['traveling']}"],
        ["Total Reimbursement", f"{data['total_reimbursement']}"],
    ]
    reimbursements_table = Table(reimbursements_data, colWidths=[250, 250])
    reimbursements_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    # ✅ Total Net Payable Section
    net_salary = [
        ["Total Net Payable:", f"{data['total_net_payable']}"],
        # ["In Words:", f"{data['net_amount_words']}"],
    ]
    net_table = Table(net_salary, colWidths=[250, 250])
    net_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    # ✅ Footer
    footer_table = Table([
        [Paragraph("<i>*This salary slip is system-generated and does not require a stamp.*</i>", styles["Normal"])]
    ], colWidths=[usable_width])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    # ✅ Wrap Everything Inside a Single Vertical Layout
    elements.extend([
        header_table,
        Spacer(1, 10),
        Paragraph("<b>Employee Pay Summary</b>", styles['Heading3']),
        emp_table,
        Spacer(1, 10),
        Paragraph("<b>Earnings</b>", styles['Heading3']),
        earnings_table,
        Spacer(1, 10),
        Paragraph("<b>Deductions</b>", styles['Heading3']),
        deductions_table,
        Spacer(1, 10),
        Paragraph("<b>Reimbursements</b>", styles['Heading3']),
        reimbursements_table,
        Spacer(1, 10),
        Paragraph("<b>Total Net Payable</b>", styles['Heading3']),
        net_table,
        Spacer(1, 15),
        footer_table
    ])

    # ✅ Generate PDF
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="salary_slip.pdf")
