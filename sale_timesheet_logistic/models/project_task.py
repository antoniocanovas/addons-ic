from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    km = fields.Float()
    kg = fields.Float()
    units = fields.Float()
    origin_id = fields.Many2one(
        related='sale_line_id.origin_id',
        string='Collection Point',
        readonly=True,
    )
    delivery_id = fields.Many2one(
        related='sale_line_id.delivery_id',
        string='Delivery Point',
        readonly=True,
    )
    origin_date = fields.Datetime(
        string='Collection Date',
    )
    delivery_date = fields.Datetime(
        string='Delivery Date',
    )
    fleet_vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='License Plate',
    )
    profitability = fields.Float(
        compute='_compute_profitability',
    )
    task_route_id = fields.Many2one(
        comodel_name='project.task.route',
        string='Route',
    )
    analytic_line_id = fields.Many2one(
        comodel_name='account.analytic.line',
        string='Apunte analítico',
        readonly=True,
    )

    @api.depends('user_id')
    def _get_vehicles_for_user(self):
        for record in self:
            vehiculos=record.user_id.vehicle_ids.ids
            record['vehicle_ids'] = [(6,0,vehiculos)]

    vehicle_ids = fields.Many2many(
        comodel_name='fleet.vehicle',
        relation='fleet_vehicle_project_task_rel',
        column1='project_task_id',
        column2='fleet_vehicle_id',
        string='Vehículos para Usuario',
        readonly=True,
        store=False,
        compute=_get_vehicles_for_user,
    )

    @api.depends('sale_line_id.price_subtotal', 'km')
    def _compute_profitability(self):
        for task in self:
            cost = task.fleet_vehicle_id.cost_per_km or \
                   task.sale_line_id.product_id.standard_price
            task.profitability = task.sale_line_id.price_subtotal - (
                    cost * task.km)

    def delivered_collected(self):
        for task in self:
            if task.origin_date:
                task.delivery_date = fields.datetime.now()
            else:
                task.origin_date = fields.datetime.now()


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    is_logistic_draft = fields.Boolean(
        string='Selectable on logistic routes',
        help="If you mark this check, tasks in this stage are considered "
             "selectables on logistic routes",
    )


class ProjectTaskRoute(models.Model):
    _name = 'project.task.route'
    _description = 'Project Task Route'

    name = fields.Char(
        required=True,
        string='Route',
    )
    fleet_vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='License Plate',
    )
    profitability = fields.Float(
        compute='_compute_profitability',
    )
    is_selectable = fields.Boolean(
        compute='_compute_is_selectable',
        store=True,
    )
    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='task_route_id',
        string='Tasks',
        domain="[('is_selectable', '=', True)]",
    )
    active = fields.Boolean(
        default=True,
    )

    note = fields.Html()

    #@api.depends('create_date')
    #def _compute_task_km(self):
    #    for record in self:
    #        this_km = 0
    #        for ta in record.task_ids:
    #            this_km += ta.this_km
    #        record['km'] = this_km

    km = fields.Float(
        store=False,
        #compute=_compute_task_km,
        string='Km',
    )

    @api.depends('task_ids.stage_id.is_logistic_draft')
    def _compute_is_selectable(self):
        for route in self:
            route.is_selectable = any(route.mapped(
                'task_ids.stage_id.is_logistic_draft'))

    @api.depends('task_ids.profitability')
    def _compute_profitability(self):
        for route in self:
            route.profitability = sum(route.mapped('task_ids.profitability'))
