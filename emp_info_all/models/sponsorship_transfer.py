from odoo import api, fields, models


class SponsorshipTransfer(models.Model):
    _name = "sponsorship.transfer"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    recruiter = fields.Many2one('hr.department', string='Recruiter')
    handle_by = fields.Selection([
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
    ], tracking=True)

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_approval', 'Waiting Approval'), ('approved', 'Approved')],
        default='draft')

    def action_submit(self):
        self.state = 'waiting_approval'
