from odoo import models, fields


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    email = fields.Char(default='adithyaka855@gmail.com')

    def action_validate(self):
        mail_template = self.env.ref('website_repair_order.email_template_repair_order_confirmed')
        mail_template.send_mail(self.id, force_send=True)
        self.state = 'confirmed'

