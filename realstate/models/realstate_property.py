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
    _description = 'Realstate Property Model'

    name = fields.Char('Name')
    type = fields.Many2one('realstate.type')
    realstate_area = fields.Many2one('realstate.area')
    advice_ids = fields.One2many(
        'realstate.advice',
        'property_id',
        string='Advices'
    )
    auditory_ids = fields.One2many(
        'realstate.auditory',
        'property_id',
        string='Auditories'
    )
    visit_ids = fields.One2many(
        'realstate.visit',
        'property_id',
        string='Visits'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Comercial'
    )
    to_sale = fields.Boolean(string='To Sale')
    to_rent = fields.Boolean(string='To rent')
    to_holiday = fields.Boolean(string='For Holidays')
    income_date = fields.Date(string='Income Date')
    outgoing_date = fields.Date(string='Outgoing Date')
    customer_id = fields.Many2one('res.partner', string='Comercial')
    active = fields.Boolean(string='Active', default=True)
    # state = fields.Boolean(string='Phone')
    property_state = fields.Selection(string='State', selection=STATES)
    photo = fields.Binary(string='Photo')
    # Vivienda
    city = fields.Char(string='City')
    street = fields.Char(string='Street')
    number = fields.Char(string='Number')
    floor = fields.Char(string='Floor')
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
    air_id = fields.Many2one('realstate.air', string='Air')
    energy_certificate = fields.Binary(string='Energy certificate')
    environment_id = fields.Many2one('realstate.enviroment', string='Enviroment id')
    elevator = fields.Boolean(string='Elevator')
    phone = fields.Boolean(string='Phone')
    satellite_tv = fields.Boolean(string='Satellite TV')
    internet_id = fields.Many2one('realstate.internet', string='Internet')
    # orientation = fields.Boolean(string='Phone')
    property_orientation = fields.Selection(
        selection=[('sur', 'SUR'), ('sureste', 'SURESTE'), ('este', 'ESTE'), ('noreste', 'NORESTE'), ('norte', 'NORTE'),
                   ('noroeste', 'NOROESTE'), ('oeste', 'OESTE'), ('suroeste', 'SUROESTE')], string="State",
        default='este')
    conservation = fields.Char(string='Conservation')
    # pool = fields.Boolean(string='Phone')
    swimmingpool = fields.Selection(selection=[('no', 'NO'), ('private', 'PRIVATE'), ('communitary', 'COMMUNITARY')],
                            string="Pool", default='no')
    barbecue = fields.Boolean(string='Barbecue')
    hearth = fields.Boolean(string='Chimenea')
