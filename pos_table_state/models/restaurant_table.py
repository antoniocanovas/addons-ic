# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta, date
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class RestaurantTable(models.Model):
	_inherit = 'restaurant.table'
	
	state_id = fields.Many2one('restaurant.table.state', 'State')
	time_start = fields.Datetime('Start Time')
	time_waiting_order = fields.Datetime('Waiting Order Time')
	time_pending_payment = fields.Datetime('Pending Payment Time')
	time_done = fields.Datetime('Done Time')
	amount = fields.Float('Amount')
	
	def update_table_state(self, table, status, state, date):
		table_id = self.sudo().browse(table)
		new_date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
		if status == 'New':
			table_id.time_start = new_date
		if status == 'Waiting Order':
			table_id.time_waiting_order = new_date
		if status == 'Pending Payment':
			table_id.time_pending_payment = new_date
		if status == 'Done':
			table_id.time_done = new_date
		table_id.state_id = state
	
	def update_table_order_total(self, table, amount):
		table_id = self.sudo().browse(table)
		table_id.amount = amount
