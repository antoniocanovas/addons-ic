# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RestaurantTableState(models.Model):
	_name = 'restaurant.table.state'
	_description = 'Restaurant Table State'
	_rec_name = 'name'
	
	name = fields.Char('Name')
	type = fields.Selection([('new', 'New'), ('waiting_order', 'Waiting Order'),
	                         ('pending_payment', 'Pending Payment'), ('done', 'Done'), ('manual', 'Manual')],
	                        string='Type', default='new')
	color_code = fields.Char('Color Code', default="#2f4f4f")
