from odoo import api, fields, models


class OperationRequest(models.Model):
    _name = "operation.request"
    # _inherit = 'res.users'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_code = fields.Integer(string='Employee Code', readonly="1")
    employee_ems_code = fields.Integer(string='Employee EMS Code', readonly="1")
    department = fields.Char(string='Department', readonly="1")
    job_position = fields.Char(string='Job Position', readonly="1")

    operation = fields.Selection([
        ('changingprofession', 'Changing Profession'),
        ('familyvisarequest', 'Family Visa Request'),
        ('lossingiqama', 'Lossing Iqama'),
        ('saudizationcertification', 'Saudization Certification'),
    ], tracking=True)
    expense_needed = fields.Boolean(string='Expense Needed')
    handle_by = fields.Selection([
        ('other', 'Other')
    ], tracking=True)

    description = fields.Text(string='Description')

    reason_for_saudi_certification = fields.Selection([
        ('getatenderdocument', 'Get a Tender Document'),
        ('other', 'Other'),
    ], tracking=True)
    client_name = fields.Char(string='Client Name')
    project_name = fields.Char(string='Project Name')


    state = fields.Selection(
        [('new', 'New'), ('waiting_approval', 'Waiting For Approval')],
        default='new')

    def action_submit(self):
        self.state = 'waiting_approval'
