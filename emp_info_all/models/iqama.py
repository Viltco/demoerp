from odoo import api, fields, models


class IqamaRequest(models.Model):
    _name = "iqama.request"
    _rec_name = 'iqama_type'

    iqama_type = fields.Selection([
        ('employee', 'Employee'),
        ('family', 'Family'),
        ('newbornbaby', 'New Born Baby'),
    ], required=True, tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    emp_code = fields.Integer(string='Employee Code', readonly="1")
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Char(string='Employee Department', readonly="1")
    job_position = fields.Char(string='Job Position', readonly="1")
    office = fields.Char(string='Office', readonly="1")
    name_as_passport = fields.Char(string='Name(As in Passport)')
    arabic_name = fields.Char(string='Arabic Name')
    nationality = fields.Many2one(
        'res.country', 'Nationality', tracking=True)
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('non-muslim', 'Non-Muslim'),
        ('other', 'Other'),
    ], tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    profession = fields.Char(string='Profession')

    iqama_number = fields.Integer(string='Iqama Number', readonly="1")
    serial_number = fields.Integer(string='Serial Number', readonly="1")
    iqama_position = fields.Char(string='Iqama Position', readonly="1")
    place_of_issue = fields.Char(string='Place of Issue', readonly="1")
    date_of_issue = fields.Date(string='Date of Issue', readonly="1")
    date_of_expiry = fields.Date(string='Date of Expiry', readonly="1")
    date_of_expiry_hijri = fields.Date(string='Date of Expiry(Hijri)', readonly="1")

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_approval', 'Waiting Approval')],
        default='draft')


    def action_confirm(self):
        self.state = 'waiting_approval'

