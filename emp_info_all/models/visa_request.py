from odoo import api, fields, models


class VisaRequest(models.Model):
    _name = "visa.request"
    # _inherit = 'res.users'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    emp_code = fields.Integer(string='Employee Code', readonly="1")
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Char(string='Employee Department', readonly="1")
    job_position = fields.Char(string='Job Position', readonly="1")

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', tracking=True)
    email = fields.Char(string='Email')
    passport_no = fields.Integer(string='Passport Number')
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
    approve_date_from = fields.Date(string='Approve Date From', readonly="1")
    approve_date_to = fields.Date(string='Approve Date To', readonly="1")

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('submit', 'ToSubmit'), ('waiting_approval', 'Waiting Approval')],
        default='submit')

    def action_submit(self):
        self.state = 'waiting_approval'
