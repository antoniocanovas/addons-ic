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

    @api.onchange('fead', 'faga', 'azagra', 'zona_pastoral_id')
    def assign_zona_pastoral(self):
        for record in self:
            partner = self.env['res.partner'].search([('id','=',record.partner_id.id)])
            if partner:
                partner.write({
                    'zona_pastoral_id':record.zona_pastoral_id.id,
                    'fead_id':record.fead,
                    'faga_id':record.faga,
                    'azagra_id':record.azagra,
                })





