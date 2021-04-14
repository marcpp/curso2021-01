from odoo import models, fields

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
        [('nuevo', 'Nuevo'),
         ('asignado', 'Asignado'),
         ('pro', 'En proceso'),
         ('pendiente', 'Pendiente'),
         ('resuelto', 'Resuelto'),
         ('cancelado', 'Cancelado')],
        string='State',
        default='nuevo'
    )
    float = fields.Float(
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

