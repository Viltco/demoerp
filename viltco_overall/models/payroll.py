# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    travelling_allowance = fields.Float(string="Travelling Allowance")
    mobile_allowance = fields.Float(string="Mobile Allowance")
    housing_allowance = fields.Float(string="Housing Allowance")
    medical_allowance = fields.Float(string="Medical Allowance")
    utility_allowance = fields.Float(string="Utility Allowance")
    meal_allowance = fields.Float(string="Meal Allowance")
    ss_allowance = fields.Float(string="Social Security")
    other_allowance = fields.Float(string="Other Allowance")

    income_tax = fields.Float(string="Income Tax")
    advances = fields.Float(string="Advances")
    provident_fund = fields.Float(string="Provident Fund")
    absent_deduction = fields.Float(string="Absent  Deduction")
    other_deductions = fields.Float(string="Other Deductions")

    fixed_overhead_cost = fields.Float(string="Fixed Overhead Cost", compute='_compute_overhead_cost')
    per_hour_Cost = fields.Float(string="Per Hour Cost")
    total_Cost_hour = fields.Float(string="Total Cost Hour", readonly=True, compute='total_cost_hour')
    working_hour = fields.Float(string="Working Hour", readonly=True,  compute='_compute_working_hours')

    def _compute_overhead_cost(self):
        rec = self.env['overhead.cost'].search([], limit=1)
        self.fixed_overhead_cost = rec.overhead_cost

    def _compute_working_hours(self):
        record = self.env['working.hour'].search([('month', '=', datetime.today().date().month)], limit=1)
        self.working_hour = record.working_hour

    @api.depends('wage', 'working_hour', 'fixed_overhead_cost')
    def total_cost_hour(self):
        record = self.env['working.hour'].search([('month', '=', datetime.today().date().month)], limit=1)
        for rec in self:
            rec.total_Cost_hour = ((rec.wage + rec.fixed_overhead_cost) / record.working_hour)


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip.run'

    state = fields.Selection([
        ('draft', 'New'),
        ('verify', 'Confirmed'),
        ('to_review', 'Waiting For Review'),
        ('to_ceo_approve', 'Waiting For CEO Approval'),
        ('to_dir_approve', 'Waiting For Director Approval'),
        ('approved', 'Approved'),
        ('close', 'Done'),
        ('paid', 'Paid'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')

    def action_send_review(self):
        self.write(
            {'state': 'to_review'}
        )

    def action_to_review(self):
        self.write(
            {'state': 'to_ceo_approve'}
        )

    def action_ceo_approve(self):
        self.write(
            {'state': 'to_dir_approve'}
        )

    def action_dir_approve(self):
        self.write(
            {'state': 'approved'}
        )