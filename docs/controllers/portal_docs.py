from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class PortalDocs(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalDocs, self)._prepare_portal_layout_values()
        doc_count = request.env['docs.docs'].search_count([])
        values['doc_count'] = doc_count
        return values

    def _doc_get_page_view_values(self, doc, access_token, **kwargs):
        values = {
            'page_name': 'doc',
            'doc': doc,
        }
        return self._get_page_view_values(doc, access_token, values, 'my_docs_history', False, **kwargs)

    @http.route(['/my/docs', '/my/docs/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_docs(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        DOC = request.env['docs.docs']

        domain = []

        searchbar_sortings = {
            'name': {'label': _('Nombre'), 'order': 'name desc'},
            'task': {'label': _('Tarea'), 'order': 'task_id desc'},
            'type': {'label': _('Tipo'), 'order': 'type_id'},
            'date': {'label': _('Fecha'), 'order': 'write_date desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'task'
        order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('docs.docs', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        doc_count = DOC.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/docs",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=doc_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        docs = DOC.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_docs_history'] = docs.ids[:100]

        values.update({
            'date': date_begin,
            'docs': docs,
            'page_name': 'doc',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/docs',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("docs.portal_my_docs", values)

    @http.route(['/my/docs/<int:doc_id>'], type='http', auth="public", website=True)
    def portal_my_doc_detail(self, doc_id, access_token=None, report_type=None, download=False, **kw):
        try:
            doc_sudo = self._document_check_access('docs.docs', doc_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=doc_sudo,
                report_type=report_type,
                report_ref='docs.docs_report',
                download=download)

        values = self._doc_get_page_view_values(doc_sudo, access_token, **kw)
        return request.render("docs.portal_doc_page", values)

    @http.route(['/my/doc/pdf/<int:doc_id>'], type='http', auth="public", website=True)
    def portal_doc_report(self, doc_id, access_token=None, **kw):
        try:
            doc_sudo = self._document_check_access('docs.docs', doc_id, access_token)
        except AccessError:
            return request.redirect('/my')
        # print report as sudo, since it require access to taxes, payment term, ... and portal
        # does not have those access rights.
        report_ref = 'docs.docs_report'
        pdf = request.env.ref(report_ref).sudo().render_qweb_pdf([doc_sudo.id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
