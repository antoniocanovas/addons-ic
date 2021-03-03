# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class SqlExportSuasor(models.Model):
    _inherit = 'sql.file.wizard'

    sql_date_compare = fields.Date(
        'Fecha',
    )

