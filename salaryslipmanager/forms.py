from django import forms

from django import forms

class SalarySlipForm(forms.Form):
    # Employee Information
    employee_name = forms.CharField(max_length=100, label="Employee Name", required=True)
    employee_code = forms.CharField(max_length=20, label="Employee Code", required=True)
    designation = forms.CharField(max_length=100, label="Designation", required=True)
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Joining", required=True)
    paid_days = forms.DecimalField(label="Paid Days", required=True)
    total_days = forms.DecimalField(label="Total Days", required=True)
    non_paid_days = forms.DecimalField(label="Non Paid Days", required=True)

    # Earnings
    basic = forms.DecimalField(max_digits=10, decimal_places=2, label="Basic Salary", required=True)
    basic_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Basic YTD", required=True, initial=0.00)
    
    hra = forms.DecimalField(max_digits=10, decimal_places=2, label="House Rent Allowance", required=True)
    hra_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="HRA YTD", required=True, initial=0.00)
    
    conveyance = forms.DecimalField(max_digits=10, decimal_places=2, label="Conveyance Allowance", required=True)
    conveyance_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Conveyance YTD", required=True, initial=0.00)
    
    other_allowance = forms.DecimalField(max_digits=10, decimal_places=2, label="Other Allowance", required=True)
    other_allowance_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Other Allowance YTD", required=True, initial=0.00)
    
    welfare = forms.DecimalField(max_digits=10, decimal_places=2, label="Welfare Allowance", required=True)
    welfare_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Welfare YTD", required=True, initial=0.00)

    # Auto-calculated Gross Earnings
    gross_earnings = forms.DecimalField(max_digits=10, decimal_places=2, label="Gross Earnings", required=False, initial=0.00)

    # Deductions
    total_deductions = forms.DecimalField(max_digits=10, decimal_places=2, label="Total Deductions", required=True)
    total_deductions_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Total Deductions YTD", required=True, initial=0.00)

    # Reimbursements
    internet = forms.DecimalField(max_digits=10, decimal_places=2, label="Internet Reimbursement", required=True)
    internet_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Internet YTD", required=True, initial=0.00)
    
    traveling = forms.DecimalField(max_digits=10, decimal_places=2, label="Traveling Reimbursement", required=True)
    traveling_ytd = forms.DecimalField(max_digits=10, decimal_places=2, label="Traveling YTD", required=True, initial=0.00)

    # Auto-calculated Total Reimbursements
    total_reimbursement = forms.DecimalField(max_digits=10, decimal_places=2, label="Total Reimbursement", required=False, initial=0.00)

    # Payment Mode
    payment_mode = forms.CharField(max_length=50, label="Payment Mode", required=True)

    # Auto-calculated Total Net Payable
    total_net_payable = forms.DecimalField(max_digits=10, decimal_places=2, label="Total Net Payable", required=False, initial=0.00)

    def clean(self):
        """Automatically calculates Gross Earnings, Total Reimbursements, and Total Net Payable"""
        cleaned_data = super().clean()

        # Calculate Gross Earnings
        gross_earnings = (
            cleaned_data.get("basic", 0) +
            cleaned_data.get("hra", 0) +
            cleaned_data.get("conveyance", 0) +
            cleaned_data.get("other_allowance", 0) +
            cleaned_data.get("welfare", 0)
        )

        # Calculate Total Reimbursements
        total_reimbursement = (
            cleaned_data.get("internet", 0) +
            cleaned_data.get("traveling", 0)
        )

        # Calculate Net Payable Salary
        total_deductions = cleaned_data.get("total_deductions", 0)
        total_net_payable = gross_earnings - total_deductions + total_reimbursement

        # Assign calculated values back to form fields
        cleaned_data["gross_earnings"] = gross_earnings
        cleaned_data["total_reimbursement"] = total_reimbursement
        cleaned_data["total_net_payable"] = total_net_payable

        return cleaned_data
