from odoo import api, fields, models


class EmployeeGosi(models.Model):
    _name = "employee.gosi"

    employee_id = fields.Many2one('hr.employee', string='Employee')
    emp_arabic_name = fields.Char(string='Employee Arabic Name', readonly="1")
    emp_code = fields.Integer(string='Employee Code', readonly="1")
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Char(string='Employee Department', readonly="1")
    job_position = fields.Char(string='Job Position', readonly="1")

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', tracking=True, readonly="1")
    passport_no = fields.Integer(string='Passport Number')

    type = fields.Selection([
        ('saudi', 'Saudi'),
        ('other', 'Other'),
    ],  tracking=True)
    family_card_id = fields.Integer(string='Family Card ID')

    issue_date = fields.Date(string='Issue Date')
    date_birth = fields.Date(string='Date of Birth')
    date_birth_hijri = fields.Date(string='Date of Birth(Hijri)')
    gosi_no = fields.Integer(string='Gosi Number')

    gosi_lines_id = fields.One2many('gosi.lines', 'employee_gosi_id')

