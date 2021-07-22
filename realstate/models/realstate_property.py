# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models

# fields.Selection(selection=TYPES, required=True, string='Types')

STATES = [
    ('new', 'NEW'),
    ('publish', 'PUBLISH'),
    ('sale', 'SALE'),
    ('done', 'DONE'),
    ('cancel', 'CANCEL'),
]


class RealstateProperty(models.Model):
    _name = 'realstate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Realstate Property Model'

    name = fields.Char('Name',  required=True)
    currency_id = fields.Many2one('res.currency')
    type = fields.Many2one('realstate.type')
    realstate_area = fields.Many2one('realstate.area')
    advice_ids = fields.One2many(
        'realstate.advice',
        'property_id',
        string='Advices'
    )
    extra_ids = fields.Many2many(
        'realstate.extras',
        string='Extras'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Comercial'
    )
    to_sale = fields.Boolean(string='To Sale')
    to_rent = fields.Boolean(string='To rent')
    to_season = fields.Boolean(string='Season')
    income_date = fields.Date(string='Income Date')
    outgoing_date = fields.Date(string='Outgoing Date')
    customer_id = fields.Many2one('res.partner', string='Comercial')
    active = fields.Boolean(string='Active', default=True)
    # state = fields.Boolean(string='Phone')
    property_state = fields.Selection(string='State', selection=STATES)
    photo = fields.Binary(string='Photo')
    # Vivienda
    street = fields.Char(string='Street', related='address_id.street')
    street2 = fields.Char(string='Street2', related='address_id.street2')
    city = fields.Char(string='City', related='address_id.city')
    state_id = fields.Many2one(string='State', related='address_id.state_id')
    inhabited = fields.Boolean(string='Inhabited')
    useful_space = fields.Char(string='Useful space')
    built_space = fields.Char(string='Built space')
    # origin = fields.Boolean(string='Phone')
    property_origin = fields.Selection(selection=[('new', 'NEW'), ('2hand', 'SECOND HAND')], string="Origin", default='new')
    built_date = fields.Date(string='Built date')
    furnished = fields.Boolean(string='Furnished')
    alarm = fields.Boolean(string='Alarm')
    security = fields.Boolean(string='Security')
    note = fields.Text('Description')
    # Oferta
    sale_price = fields.Float(string='Sale', digits=(7, 2))
    rental_price = fields.Float(string='Rental', digits=(5, 2))
    advance_price = fields.Float(string='Advance', digits=(4, 2))
    community_price = fields.Float(string='Community', digits=(4, 2))
    date = fields.Date(string='Date')
    last_change = fields.Date(string='Last chance')
    exclusivity = fields.Boolean(string='Exclusivity')
    owner_id = fields.Many2one('res.partner', string='Owner')
    owner_vat_file1 = fields.Binary(related='owner_id.vat_file1', readonly=False)
    owner_vat_file2 = fields.Binary(related='owner_id.vat_file2', readonly=False)
    # HABITABILITY
    room_qty = fields.Integer(string='Rooms')
    builtin_wardroble = fields.Boolean(string='Builtin wardrobe')
    living_room_qty = fields.Integer(string='Living rooms')
    # kitchen = fields.Boolean(string='Phone')
    kitchen = fields.Selection(selection=[('kitchen', 'KITCHEN'), ('office', 'OFFICE')], string="Kitchen",
                               default='kitchen')
    bathroom_qty = fields.Integer(string='Bathrooms')
    bathroom_bedroom = fields.Boolean(string='Bathroom in bedroom')
    parking = fields.Many2one('realstate.parking', string='Parking')
    storage_room = fields.Boolean(string='Storage room')
    balcony = fields.Boolean(string='Balcony')
    solarium = fields.Boolean(string='Solarium')
    garden = fields.Boolean(string='Garden')
    patio = fields.Boolean(string='Patio')
    heating_id = fields.Many2one('realstate.heating', string='Heating')
    cooling_id = fields.Many2one('realstate.cooling', string='Air cooling')
    energy_certificate = fields.Binary(string='Energy certificate')
    energy_certificate_name = fields.Char(string='Energy certificate')
    environment_id = fields.Many2one('realstate.enviroment', string='Enviroment id')
    elevator = fields.Boolean(string='Elevator')
    phone = fields.Boolean(string='Phone')
    satellite_tv = fields.Boolean(string='Satellite TV')
    internet_id = fields.Many2one('realstate.internet', string='Internet')
    # orientation = fields.Boolean(string='Phone')
    property_orientation = fields.Selection(
        selection=[('sur', 'SUR'), ('sureste', 'SURESTE'), ('este', 'ESTE'), ('noreste', 'NORESTE'), ('norte', 'NORTE'),
                   ('noroeste', 'NOROESTE'), ('oeste', 'OESTE'), ('suroeste', 'SUROESTE')], string="Orientation",
        default='este')
    conservation = fields.Char(string='Conservation')
    # pool = fields.Boolean(string='Phone')
    swimmingpool = fields.Selection(selection=[('no', 'NO'), ('private', 'PRIVATE'), ('communitary', 'COMMUNITARY')],
                            string="Pool", default='no')
    barbecue = fields.Boolean(string='Barbecue')
    hearth = fields.Boolean(string='Chimenea')
    state = fields.Selection(selection=STATES,
                            string="State", default='new')
    address_id = fields.Many2one('res.partner', string='Address')
    service_amount = fields.Monetary('Service Amount', currency_field='currency_id')
    notary_cost = fields.Float('Notary cost')
    plusvalia_amount  = fields.Float('Capital gain')
    advice_ids = fields.One2many('realstate.advice', 'property_id' )
    opportunity_ids = fields.One2many('crm.lead', 'realstate_id')
    event_ids = fields.One2many('calendar.event', 'realstate_id')
    contribution_file  = fields.Binary(string='Contribution file' )
    name_contribution_file  = fields.Char(string='Contribution file name')
    titlet_dead = fields.Binary(string='Titlet dead')
    name_titlet_dead = fields.Char(string='Titlet dead name')
    title_dead_simple  = fields.Binary(string='Titlet dead simple')
    name_title_dead_simple  = fields.Char(string='Titlet dead simple name')
    document_url = fields.Char('Cloud folder')

    def _get_opportunity_count(self):
        self.opportunity_ids_count = len(self.opportunity_ids)

    opportunity_ids_count = fields.Integer('Opportunity', compute=_get_opportunity_count, store=False)

    def _get_event_count(self):
        self.event_ids_count = len(self.event_ids)

    event_ids_count = fields.Integer('Event', compute=_get_event_count, store=False)

