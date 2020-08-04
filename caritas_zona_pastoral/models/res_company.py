import base64

from odoo import fields, models, api


import logging

_logger = logging.getLogger(__name__)


class CaritasResCompany(models.Model):
    _inherit = 'res.company'

    fead = fields.Boolean('Fead')
    faga = fields.Boolean('Faga')
    azagra = fields.Boolean('Azagra')
    zona_pastoral_id = fields.Many2one('caritas.zona','Zona Pastoral')

    @api.depends('fead')
    def assign_fead(self):
        for record in self:
            if record.partner_id:
                record.partner_id.fead_id = record.fead

    @api.depends('faga')
    def assign_faga(self):
        for record in self:
            if record.partner_id:
                record.partner_id.faga_id = record.faga

    @api.depends('azagra')
    def assign_azagra(self):
        for record in self:
            if record.partner_id:
                record.partner_id.azagra_id = record.azagra

    @api.depends('zona_pastoral_id')
    def assign_zona_pastoral(self):
        for record in self:
            if record.partner_id:
                record.partner_id.zona_pastoral_id = record.zona_pastoral_id


