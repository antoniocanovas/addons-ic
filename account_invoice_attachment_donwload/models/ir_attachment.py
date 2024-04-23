# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import float_is_zero
from datetime import date
import zipfile
from io import BytesIO
import base64

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _create_temp_zip(self):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for attachment in self:
                zip_file.writestr(
                        str(attachment.name),
                        base64.decodebytes(attachment.datas),
                    )
            zip_buffer.seek(0)
            zip_file.close()
        return zip_buffer
