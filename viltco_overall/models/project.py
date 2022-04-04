from odoo import models, fields, api


class AccountLineInh(models.Model):
    _inherit = 'project.task'

    billed_hours = fields.Float('Billed Hours')

    def fill_billed_hours(self):
        record = self.env['project.task'].search([])
        for rec in record:
            if rec.billed_hours == 0:
                rec.billed_hours = rec.effective_hours


class ProjectInh(models.Model):
    _inherit = 'project.project'

    distance = fields.Float('Distance')


class HrExpenseInh(models.Model):
    _inherit = 'hr.expense'

    distance = fields.Float('Distance', compute='_compute_distance')

    @api.depends('analytic_account_id')
    def _compute_distance(self):
        if self.analytic_account_id.project_ids and self.analytic_account_id:
            self.distance = self.analytic_account_id.project_ids[0].distance
        else:
            self.distance = 0