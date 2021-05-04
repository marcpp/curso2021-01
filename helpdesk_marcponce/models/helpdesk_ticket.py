from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Tickets helpdesk action'

    name = fields.Char()
    date = fields.Date()
    time = fields.Float(
        string='Time'
    )
    ticket_id = fields.Many2one(
        comodel_name = 'helpdesk.ticket',
        string = "Ticket"
    )


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tickets helpdesk tag'

    name = fields.Char()
    public = fields.Boolean() 
    tag_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'tag_id',
        column2 = 'ticket_id',
        string = 'Tickets'
    )

    @api.model
    def cron_delete_tag(self):
        tickets = self.search([('ticket_ids', '=', False)])
        tickets.unlink()


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Tickets helpdesk'
    _inherit = [
        'mail.thread.cc',
        'mail.thread.blacklist',
        'mail.activity.mixin'
    ]
    _primary_email = 'email_from'


    # Els defauls es posen antes de la definició dels camps
    def _date_default_today(self):
        return fields.Date.today()


    name = fields.Char(
        string='name',
        required=True
    )
    description = fields.Text(
        string='Description'
    )
    date = fields.Date(
        string='Date',
        default=_date_default_today
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
        string='Time',
        compute='_get_time',
        inverse='_set_time',
        search='_search_time'
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
    email_from = fields.Char()


    def state_to_assign(self):
        self.ensure_one()
        self.state = 'assigned'


    def state_to_inprocess(self):
        self.ensure_one()
        self.state = 'inprocess'


    def state_to_pending(self):
        self.ensure_one()
        self.state = 'pending'


    def state_to_finalize(self):
        self.ensure_one()
        self.state = 'resolved'


    def state_to_cancel(self):
        self.ensure_one()
        self.state = 'resolved'


    def state_to_cancel_multi(self):
        # com cancelar és ensure_one creo un altre mètode que crida varies vegades a cancelar
        # usat a sale_helpdesk_marcponce
        for record in self:
            record.state_to_cancel()

    
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
        # self.write({
        #     'tag_ids': [(0,0,{'name': self.tag_name})]
        # })
        #self.tag_name = False # Esborra el text després de crear el tag

        # pasa por context el valor del nuevo nombre y la relación con el ticket
        action = self.env.ref('helpdesk_marcponce.action_new_tag').read()[0]
        # Si passa per context el que volem fer no crea el tag fins que es polsa crear, si no es crea directament
        action['context'] = {
            'default_name': self.tag_name,
            'default_ticket_ids': [(6, 0, self.ids)]
        }
        self.tag_name = False # Esborra el text després de crear el tag
        return action

    
    @api.constrains( 'time')
    def _verify_time_positive(self):
        for ticket in self:
            if ticket.time and ticket.time<0:
                raise ValidationError (_("The time cannot be negative" ))


    @api.onchange('date','time')
    def _onchange_date(self):
        self.date_limit = self.date and self.date + timedelta(days=1)


    @api.depends('action_ids.time')
    def _get_time(self):
        for record in self:
            record.time = sum(record.action_ids.mapped('time'))
    
    def _set_time(self):
        for record in self:
            time_now = sum(record.action_ids.mapped('time'))
            next_time = record.time - time_now
            if next_time:
                data = {'name': '/', 'time': next_time, 'date': fields.Date.today(), 'ticket_id': record.id}
                self.env['helpdesk.ticket.action'].create(data)
    
    def _search_time(self, operator, value):
        actions = self.env['helpdesk.ticket.action'].search([('time', operator, value)])
        return [('id', 'in', actions.mapped('ticket_id').ids)]