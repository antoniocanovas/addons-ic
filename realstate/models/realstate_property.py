# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models

# fields.Selection(selection=TYPES, required=True, string='Types')

STATES = [
    ('new', 'New'),
    ('auditory', 'Auditory'),
    ('publish', 'Publish'),
    ('sale', 'Available'),
    ('done', 'Done'),
    ('cancel', 'Cancel'),
]


class RealstateProperty(models.Model):
    _name = 'realstate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Realstate Property Model'

    name = fields.Char('Name',  required=True)

    def get_currency(self):
        self.currency_id = self.env.user.company_id.currency_id

    currency_id = fields.Many2one('res.currency', compute='get_currency', store=False)

    type = fields.Many2one('realstate.type')
    realstate_area = fields.Many2one('realstate.area')
    extra_ids = fields.Many2many(
        'realstate.extras',
        string='Extras'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Comercial'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )

    to_sale = fields.Boolean(string='To Sale')
    to_rent = fields.Boolean(string='To rent')
    to_season = fields.Boolean(string='Season')
    income_date = fields.Date(string='Income Date')
    outgoing_date = fields.Date(string='Outgoing Date')
    customer_id = fields.Many2one('res.partner', string='Salesman')
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
    property_origin = fields.Selection(selection=[('new', 'New construction'), ('2hand', 'Used')], string="Origin")
    built_date = fields.Date(string='Built date')
    furnished = fields.Boolean(string='Furnished')
    alarm = fields.Boolean(string='Alarm')
    security = fields.Boolean(string='Security')
    note = fields.Text('Description')
    # Oferta
    sale_price = fields.Monetary(string='Sale',  currency_field='currency_id')
    rental_price = fields.Monetary(string='Rental',  currency_field='currency_id')
    advance_price = fields.Monetary(string='Advance',  currency_field='currency_id')
    community_price = fields.Monetary(string='Community',  currency_field='currency_id')
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
    kitchen = fields.Selection(selection=[('kitchen', 'Traditional'), ('office', 'Office')], string="Kitchen")
    bathroom_qty = fields.Integer(string='Bathrooms')
    bathroom_bedroom = fields.Boolean(string='Bathroom in bedroom')
    parking = fields.Many2one('realstate.parking', string='Parking')
    storage_room = fields.Boolean(string='Storage room')
    balcony = fields.Boolean(string='Balcony')
    solarium = fields.Boolean(string='Solarium')
    garden = fields.Boolean(string='Garden')
    patio = fields.Boolean(string='courtyard')
    heating_id = fields.Many2one('realstate.heating', string='Heating')
    cooling_id = fields.Many2one('realstate.cooling', string='Air cooling')
    energy_certificate = fields.Binary(string='Energy certificate')
    energy_certificate_name = fields.Char(string='Energy certificate')
    environment_id = fields.Many2one('realstate.enviroment', string='Enviroment')
    elevator = fields.Boolean(string='Elevator')
    phone = fields.Boolean(string='Phone')
    satellite_tv = fields.Boolean(string='Satellite TV')
    internet_id = fields.Many2one('realstate.internet', string='Internet')
    # orientation = fields.Boolean(string='Phone')
    property_orientation = fields.Selection(
        selection=[('south', 'South'), ('southeast', 'Southeast'), ('east', 'East'), ('northeast', 'Northeast'), ('north', 'North'),
                   ('northwest', 'Northwest'), ('west', 'West'), ('southwest', 'Southwest')], string="Orientation")
    conservation = fields.Char(string='Conservation')
    # pool = fields.Boolean(string='Phone')
    swimmingpool = fields.Selection(selection=[('no', 'None'), ('private', 'Private'), ('communitary', 'Communitary'),('public','Public')],
                            string="Pool")
    barbecue = fields.Boolean(string='Barbecue')
    hearth = fields.Boolean(string='Fireplace')
    state = fields.Selection(selection=STATES,
                            string="Status")
    address_id = fields.Many2one('res.partner', string='Address')
    service_amount = fields.Monetary('Service Amount', currency_field='currency_id')
    notary_cost = fields.Monetary('Notary cost', currency_field='currency_id')
    plusvalia_amount = fields.Monetary('Capital gain', currency_field='currency_id')
    advice_ids = fields.One2many('realstate.advice', 'property_id',string='Advices' )
    opportunity_ids = fields.One2many('crm.lead', 'realstate_id')
    event_ids = fields.One2many('calendar.event', 'realstate_id')
    contribution_file = fields.Binary(string='Contribution file' )
    name_contribution_file = fields.Char(string='Contribution file name')
    house_deed = fields.Binary(string='House deed')
    name_house_deed = fields.Char(string='house deed name')
    house_deed_simple = fields.Binary(string='House deed simple')
    name_house_deed_simple = fields.Char(string='House simple name')
    cloud_folder = fields.Char('Cloud folder')
    private_image_ids = fields.One2many('product.image','property_id')

    def _get_product_template_image_ids(self):
        self.product_template_image_ids = self.product_id.product_template_image_ids
    product_template_image_ids = fields.Many2many('product.image', compute=_get_product_template_image_ids, readonly=True, store=False)

    def _get_opportunity_count(self):
        self.opportunity_ids_count = len(self.opportunity_ids)

    opportunity_ids_count = fields.Integer('Opportunity', compute=_get_opportunity_count, store=False)

    def _get_event_count(self):
        self.event_ids_count = len(self.event_ids)

    event_ids_count = fields.Integer('Event', compute=_get_event_count, store=False)

