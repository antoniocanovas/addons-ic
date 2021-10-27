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

	time_start1 = fields.Char('Start Time1')
	time_waiting_order1 = fields.Char('Waiting Order Time1')
	time_pending_payment1 = fields.Char('Pending Payment Time1')
	time_done1 = fields.Char('Done Time1')
	
	def update_table_state(self, table, status, state, date):
		table_id = self.sudo().browse(table)
		new_date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
		new_date1 = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S').strftime('%H:%M')
		if status == 'New':
			table_id.time_start = new_date
			table_id.time_start1 = str(new_date1)
		if status == 'Waiting Order':
			table_id.time_waiting_order = new_date
			table_id.time_waiting_order1 = str(new_date1)
		if status == 'Pending Payment':
			table_id.time_pending_payment = new_date
			table_id.time_pending_payment1 = str(new_date1)
		if status == 'Done':
			table_id.time_done = new_date
			table_id.time_done1 = str(new_date1)
		table_id.state_id = state
	
	def update_table_order_total(self, table, amount):
		table_id = self.sudo().browse(table)
		table_id.amount = amount
