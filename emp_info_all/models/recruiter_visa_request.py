from odoo import api, fields, models


class RecruiterVisaRequest(models.Model):
    _name = "recruiter.request"
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
    request_by = fields.Many2one('hr.department', string='Request By')

    visa_for = fields.Selection([
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
    ], tracking=True)
    type = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ], tracking=True)
    type_of_visa = fields.Selection([
        ('businessvisitvisa', 'Business Visit Visa'),
        ('workvisitvisa', 'Work Visit Visa'),
        ('newworkvisa', 'New Work Visa'),
    ], tracking=True)

    dep_date = fields.Date(string='Departure Date')
    visa_title = fields.Char(string='Visa Title')
    country = fields.Many2one(
        'res.country', 'Country', tracking=True)
    return_date = fields.Date(string='Return Date')
    visa_no = fields.Integer(string='Visa Number')
    visa_duration = fields.Integer(string='Visa Duration')
    approve_date_from = fields.Date(string='Approve Date From', readonly="1")
    approve_date_to = fields.Date(string='Approve Date To', readonly="1")

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('tosubmit', 'ToSubmit'), ('confirm', 'Confirm')],
        default='tosubmit')

    def action_submit(self):
        self.state = 'confirm'
