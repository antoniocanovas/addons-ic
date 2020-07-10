from odoo import fields, models, api


class LogisticAnalysis(models.Model):
    _name = 'fsm.logistic.analysis'
    _description = 'Logistic Analysis'


    profitability = fields.Float(
         #compute='_compute_profitability',
        readonly=True,
    )



    #@api.depends('task_ids.profitability')
    #def _compute_profitability(self):
    #    for route in self:
    #        route.profitability = sum(route.mapped('task_ids.profitability'))