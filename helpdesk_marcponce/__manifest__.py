# Copyright 2021 Marc Ponce
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    'name': 'HelpDesk Marc Ponce',
    'summary': 'HelpDesk Marc Ponce',
    'version': '14.0.1.0.0',
    'depends': ['base','mail'],
    'author': 'Marc Ponce Plaza',
    'license': 'AGPL-3',
    'installable': True,
    'category': 'Tools',
    'data': [
        'data/delete_tag_cron.xml',
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'reports/helpdesk_ticket_report_templates.xml',
        'reports/res_partner_templates.xml',
        'views/helpdesk_menu.xml',
        'wizards/create_ticket_view.xml',
        'views/helpdesk_tag_view.xml',
        'views/helpdesk_view.xml',
        'views/report_view.xml',
    ],
}