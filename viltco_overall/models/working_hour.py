from odoo import api, fields, models, _


class WorkingHour(models.Model):
    _name = "working.hour"
    _description = "Working Hour"
    _rec_name = 'working_hour'

    working_hour = fields.Float(string="Working Hour")
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Month', index=True, copy=False, tracking=True)


class OverHeadCost(models.Model):
    _name = "overhead.cost"
    _rec_name = 'overhead_cost'

    overhead_cost = fields.Float(string="OverHead Cost")










