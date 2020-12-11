# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import base64
from odoo.exceptions import ValidationError

STATE = [
    ('in', 'In'),
    ('out', 'Out'),
    ('internal', 'Internal'),
]

class DocumentTypes(models.Model):
    _name = 'document.types'
    _description = 'Document types'

    name = fields.Char('Name')
    route = fields.Selection(
        selection=STATE,
        string='Route',
    )
    active = fields.Boolean('Active', default=True)


