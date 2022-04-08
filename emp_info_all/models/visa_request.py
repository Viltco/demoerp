from odoo import api, fields, models


class VisaRequest(models.Model):
    _name = "visa.request"
    # _inherit = 'res.users'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    emp_code = fields.Char(string='Employee Code' , related='employee_id.pin')
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Many2one('hr.department', related='employee_id.department_id')
    job_position = fields.Many2one('hr.job', related='employee_id.job_id')

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', tracking=True , related='employee_id.country_id')
    email = fields.Char(string='Email' ,related='employee_id.work_email')
    passport_no = fields.Char(string='Passport Number' ,related='employee_id.passport_id')
    fiscal_year = fields.Date(string='Fiscal Year')

    visa_for = fields.Selection([
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
    ], tracking=True)
    type = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ],  tracking=True)
    type_of_visa = fields.Selection([
        ('exitre-entryvisa', 'Exit Re-Enter Visa'),
        ('finalexit', 'Final Exit'),
        ('extensionofexitre-entryvisa', 'Extension Of Exit Re-Entry Visa'),
    ], tracking=True)
    purpose_of_visa = fields.Selection([
        ('training', 'Training'),
        ('businesstrip', 'Business Trip'),
        ('annualvacation', 'Annual Vacation'),
        ('holiday', 'Holiday'),
        ('secondment', 'Secondment'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ], tracking=True)
    dep_date = fields.Date(string='Departure Date')
    country = fields.Many2one(
        'res.country', 'Country', tracking=True)
    return_date = fields.Date(string='Return Date')
    visa_no = fields.Integer(string='Visa Number')
    visa_duration = fields.Integer(string='Visa Duration')
    approve_date_from = fields.Date(string='Approve Date From')
    approve_date_to = fields.Date(string='Approve Date To')

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('submit', 'ToSubmit'), ('waiting_approval', 'Waiting Approval') ,('approved', 'Approved'),('reject', 'Rejected')],
        default='submit')

    def action_submit(self):
        self.state = 'waiting_approval'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'reject'
