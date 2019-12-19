# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import xmlrpc.client
from odoo import fields, models, api
import werkzeug
import string
import random

class AccessRequest(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def setxmlrpc(self):

        if not self.db or not self.url:
            raise Warning((
                "Revise los campos 'Base de datos' y 'Servidor' en la pestaña Odoo.sh"
            ))
        else:
            asesoria = self.env['res.users'].search([('name', '=', 'asesoria')])

            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            uid = common.authenticate(self.db, asesoria.rpcu, asesoria.rpcp, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

            return {
                'uid': uid,
                'models': models,
                'rpcu': asesoria.rpcu,
                'rpcp': asesoria.rpcp,
            }

    @api.multi
    def tokengenerator(self):

        temptoken = string.ascii_letters
        return ''.join(random.choice(temptoken) for i in range(10))

    @api.multi
    def writetoken(self,conn):

        user_id = models.execute_kw(self.db, conn['uid'], conn['rpcp'], 'res.users', 'search_read',
                                    [[['login', '=', 'asesoria@ingenieriacloud.com']]],
                                    {'fields': ['id',
                                                ], 'limit': 1
                                     })
        models.execute_kw(self.db, conn['uid'], conn['rpcp'], 'res.users', 'write', [[user_id[0]['id']], {
            'token': self.token
        }])

        token = models.execute_kw(self.db,conn['uid'], conn['rpcp'], 'res.users', 'search_read',
                                  [[['login', '=', 'asesoria@ingenieriacloud.com']]],
                                  {'fields': ['token',
                                              ], 'limit': 1
                                   })

        if token[0]['token'] == self.token:
            return True
        else:
            return False


    @api.multi
    def request_f(self, values):
        url = "%s/93201967" % self.url

        redirection = werkzeug.utils.redirect('%s%s' % (url, ''))

        conn = self.setxmlrpc()

        self.token = self.tokengenerator()
        writeok = self.writetoken(conn)

        if writeok == True:
            self.token='off'
            return {'type': 'ir.actions.act_url',
                    'url': url,
                    'target': 'current',
                    }

    
