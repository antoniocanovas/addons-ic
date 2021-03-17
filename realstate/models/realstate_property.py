# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


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
          'res.user',
          string='Comercial'
     )
     to_sale = fields.Boolean()
     to_rent = fields.Boolean()
     to_holiday = fields.Boolean()
     income_date = fields.Date()
     outgoing_date = fields.Date()
     customer_id = fields.Many2one('res.partner')
     active = fields.Boolean()
     #state = fields.Selection([('new','NEW'),('publish','PUBLISH'),('sale','SALE'),('done','DONE'),('cancel','CANCEL')], string='State', default='new')
     state = fields.Selection(
          [('new', 'NEW'), ('publish', 'PUBLISH'), ('sale', 'SALE'), ('done', 'DONE'), ('cancel', 'CANCEL')])
     photo = fields.Binary()
     # Vivienda
     city = fields.Char()
     street = fields.Char()
     number = fields.Char()
     floor = fields.Char()
     inhabited = fields.Boolean()
     useful_space = fields.Char()
     built_space = fields.Char()
     origin = fields.Selection(selection=[('new','NEW'),('second hand','2HAND')],string="Origin",default='new')
     built_date = fields.Date()
     furnished = fields.Boolean()
     alarm = fields.Boolean()
     security = fields.Boolean()
     note = fields.Text('Description')
     # Oferta
     sale_price = fields.Float(string='Sale', digits=(7,2))
     rental_price = fields.Float(string='Rental', digits=(5,2))
     advance_price = fields.Float(string='Advance', digits=(4,2))
     community_price = fields.Float(string='Community', digits=(4,2))
     date = fields.Date()
     last_change = fields.Date()
     exclusivity = fields.Boolean()
     owner_id = fields.Many2one('res.partner')
     # HABITABILITY
     room_qty = fields.Integer()
     builtin_wardroble = fields.Boolean()
     living_room_qty = fields.Integer()
     kitchen = fields.Selection(selection=[('kitchen','KITCHEN'),('office','OFFICE')],string="Kitchen",default='kitchen')
     bathroom_qty = fields.Integer()
     bathroom_bedroom = fields.Boolean()
     parking = fields.Many2one('realstate.parking')
     storage_room = fields.Boolean()
     balcony = fields.Boolean()
     solarium = fields.Boolean()
     garden = fields.Boolean()
     patio = fields.Boolean()
     heating_id = fields.Many2one('realstate.heating')
     air_id = fields.Many2one('realstate.air')
     energy_certificate = fields.Binary()
     environment_id = fields.Many2one('realstate.enviroment')
     elevator = fields.Boolean()
     phone = fields.Boolean()
     satellite_tv = fields.Boolean()
     internet_id = fields.Many2one('realstate.internet')
     orientation = fields.Selection(selection=[('sur'),('sureste'),('este'),('noreste'),('norte'),('noroeste'),('oeste'),('suroeste')],string="State",default='este')
     conservation = fields.Char()
     pool = fields.Selection(selection=[('no','NO'),('private','PRIVATE'),('communitary','COMMUNITARY')],string="Pool",default='no')
     barbecue = fields.Boolean()
     hearth = fields.Boolean('Chimenea')

