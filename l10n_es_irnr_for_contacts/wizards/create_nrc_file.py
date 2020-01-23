# Copyright 2020 Ingeniería Cloud - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
from odoo import api, fields, models


class CreateNrcFile(models.TransientModel):
    _name = "create.nrc.file"
    _description = "Create NRC File"

    date_irnr = fields.Date(
        string='Declaration Date',
        required=True,
    )
    fiscalyear = fields.Char(
        string='Fiscal Year',
        required=True,
    )
    period_declaration = fields.Selection(
        selection=[
            ('0a', '0A'),
            ('1t', '1T'),
            ('2t', '2T'),
            ('3t', '3T'),
            ('4t', '4T'),
            ('01', '01'),
            ('02', '02'),
            ('03', '03'),
            ('04', '04'),
            ('05', '05'),
            ('06', '06'),
            ('07', '07'),
            ('08', '08'),
            ('09', '09'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('1p', '1P'),
            ('2p', '2P'),
            ('3p', '3P'),
        ],
        string='Period',
    )

    @api.onchange('date_irnr')
    def date_irnr_change(self):
        if self.date_irnr:
            self.fiscalyear = self.date_irnr.year

    @api.multi
    def create_nrc_file(self):
        return
