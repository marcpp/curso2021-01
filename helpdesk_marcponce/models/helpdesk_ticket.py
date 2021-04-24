from odoo import models, fields, api

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Tickets helpdesk action'

    name = fields.Char()
    date = fields.Date()
    ticket_id = fields.Many2one(
        comodel_name = 'helpdesk.ticket',
        string = "Ticket"
    )


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tickets helpdesk tag'

    name = fields.Char()
    tag_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'tag_id',
        column2 = 'ticket_id',
        string = 'Tickets'
    )


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Tickets helpdesk'

    name = fields.Char(
        string='name',
        required=True
    )
    description = fields.Text(
        string='Description'
    )
    date = fields.Date(
        string='Date'
    )
    state = fields.Selection(
        [('new', 'New'),
         ('assigned', 'Assigned'),
         ('inprocess', 'In process'),
         ('pending', 'Pending'),
         ('resolved', 'Resolved'),
         ('canceled', 'Canceled')],
        string='State',
        default='new'
    )
    time = fields.Float(
        string='Time'
    )
    assigned = fields.Boolean(
        string='Assigned',
        compute='_compute_assigned'
    )
    date_limit = fields.Date(
        string='Date Limit'
    )
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions todo'
    )
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive peventive actions todo'
    )
    user_id = fields.Many2one(
        comodel_name = 'res.users',
        string = 'Assigned to'
    )
    action_ids = fields.One2many(
        comodel_name = 'helpdesk.ticket.action',
        inverse_name = 'ticket_id',
        string = 'Actions'
    )
    tag_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket.tag',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'ticket_id',
        column2 = 'tag_id',
        string = 'Tags'
    )
    ticket_qty = fields.Integer(
        string = 'Ticket QTY',
        compute = '_compute_ticket_qty'
    )
    tag_name = fields.Char(
        string = 'Tag name'
    )
    color = fields.Integer(
        string = 'Color', 
        default=10
    )


    def state_to_assign(self):
        self.state = 'assigned'


    def state_to_inprocess(self):
        self.state = 'inprocess'


    def state_to_pending(self):
        self.state = 'pending'


    def state_to_finalize(self):
        self.state = 'resolved'


    def state_to_cancel(self):
        self.state = 'resolved'

    
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False # Es pot fer amb un if però així és més limpio

    
    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)

    
    def create_tag(self):
        self.ensure_one()
        self.write({
            'tag_ids': [(0,0,{'name': self.tag_name})]
        })
        self.tag_name = False # Esborra el text després de crear el tag