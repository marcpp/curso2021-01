from odoo import models, fields

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
    _description = 'Tickets helpdesk action'

    name = fields.Char()
    tag_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'tag_id',
        column2 = 'ticket_id',
        string = 'Tags'
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
        readonly=True
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
