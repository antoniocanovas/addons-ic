# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import xmlrpc.client
from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import string
import random


class AccessRequest(models.Model):
    _inherit = 'partner.credentials'

    db = fields.Char('Base de Datos')
    remote_company_id = fields.Integer('Id de empresa')

    def set_remote_company(self, conn):

        try:
            asesoria_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                    'res.users', 'search_read',
                                                    [[('name', '=', 'asesoria')]],
                                                    {'fields': ['company_id'], 'limit': 1})
        except Exception as e:
            raise Warning(("Exception when calling remote server $Remote User Get company: %s\n" % e))
        if asesoria_id[0]['company_id'][0] != self.remote_company_id:
            try:
                ase_company_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                           'res.users', 'write',
                                                           [asesoria_id[0]['id'],
                                                            {'company_id': self.remote_company_id}])
            except Exception as e:
                raise Warning(("Exception when calling remote server $Remote User Company_id: %s\n" % e))

    def tokengenerator(self):

        temptoken = string.ascii_letters
        return ''.join(random.choice(temptoken) for i in range(10))

    def _setxmlrpc(self):

        if not self.db or not self.url:
            raise Warning((
                "Revise los campos 'Base de datos' y 'Servidor' en la pestaña SSO"
            ))
        else:

            remote_user = self.env['res.users'].sudo().search([('name', '=', 'asesoria'),
                                                               "|",
                                                               ("active", "=", True),
                                                               ("active", "=", False),
                                                               ], limit=1)

            remote_user.token = self.tokengenerator()

            try:
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
                uid = common.authenticate(self.db, remote_user.rpcu, remote_user.rpcp, {})
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            except Exception as e:
                raise Warning(("Exception when calling remote server $common: %s\n" % e))

            return {
                'uid': uid,
                'models': models,
                'rpcu': remote_user.rpcu,
                'rpcp': remote_user.rpcp,
                'token': remote_user.token,
            }

    def writetoken(self, conn):

        try:
            user_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'res.users', 'search_read',
                                            [[['login', '=', 'asesoria']]],
                                            {'fields': ['id',
                                                        ], 'limit': 1
                                             })
        except Exception as e:
            raise Warning(("Exception when calling remote user $token: %s\n" % e))
        try:
            conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'res.users', 'write', [[user_id[0]['id']], {
                'token': conn['token'],
            }])
        except Exception as e:
            raise Warning("Exception when sending token: %s\n" % e)
        try:
            token = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'res.users', 'search_read',
                                          [[['login', '=', 'asesoria']]],
                                          {'fields': ['token',
                                                      ], 'limit': 1
                                           })
        except Exception as e:
            raise Warning(("Exception when reading remote token: %s\n" % e))
        if token[0]['token'] == conn['token']:
            return True
        else:
            raise Warning("Exception when matching token")

    def request_f(self):
        url = "%s/93201967" % self.url
        conn = self._setxmlrpc()

        writeok = self.writetoken(conn)

        if writeok == True:
            set_company = self.set_remote_company(conn)
            return {'type': 'ir.actions.act_url',
                    'url': url,
                    'target': 'current',
                    }

