from odoo import models, api, fields, _

class CreateTicket(models.TransientModel):
    _name = 'create.ticket'

    name = fields.Char(
        required=True
    )

    def create_ticket(self):
        #Només s'executarà des dels tag
        self.ensure_one()
        active_id = self._context.get('active_id', False)
        if active_id and self._context.get('active_model') == 'helpdesk.ticket.tag':
            # Crear un nou ticket
            ticket = self.env['helpdesk.ticket'].create({
                'name': self.name,
                'tag_ids': [(6, 0, [active_id])]
            })

            # Obre l'acció creada amb mode formulari
            action = self.env.ref('helpdesk_marcponce.helpdesk_ticket_action').read()[0]
            action['res_id'] = ticket.id
            action['views'] = [(self.env.ref('helpdesk_marcponce.view_helpdesk_ticket_form').id, 'form')]
            return action
        # Tanca la finestra si arriba fins a aquí
        return {'type': 'ir.actions.act_window_close'}