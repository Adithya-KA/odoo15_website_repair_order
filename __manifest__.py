{
    'name': 'Website Repairs',
    'version': '15.0.0.1.0',
    'description': 'Repair Order from Website',
    'depends': [
        'base', 'website', 'mail', 'repair', 'contacts',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_repair_order/static/src/js/action_manager.js'],
    },

    'data': [
        'views/menu.xml',
        'views/template.xml',
        'views/email_template.xml',
    ],

    'installable': True,
    'application': True

}
