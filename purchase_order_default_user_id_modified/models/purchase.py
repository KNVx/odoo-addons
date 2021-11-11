# Copyright 2021 NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import timedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model_cr
    def _get_default_user_id_for_bots(self):
        if self.env.user.is_bot:
            self.env.user._cr.execute(
                """ select id from res_users ru
    where default_purchase_user =True""")
            new_default=self.env.user._cr.fetchone()
            return new_default
        else:
            return self.env.user.id

    user_id = fields.Many2one('res.users', string='Purchase Representative', index=True, track_visibility='onchange',
                              default=lambda self: self.env['purchase.order']._get_default_user_id_for_bots())



# class Users(models.Model):
#     _inherit = "res.users"
#     default_purchase_user = fields.Boolean()
#     is_bot = fields.Boolean()
#
#     @api.model_cr
#     def write(self, values):
#         if 'default_purchase_user' in values and values['default_purchase_user'] is True:
#             self._cr.execute(
#                 """ select id from res_users ru
#     where default_purchase_user =True""")
#             a = 1
#
#             exists_default = self._cr.fetchone()
#             if exists_default:
#                 raise ValidationError(_(
#                     "Another default user found. Id:%s",
#                 ) % exists_default[0]
#                                       )
#             else:
#                 super().write(values)
#         else:
#             super().write(values)
