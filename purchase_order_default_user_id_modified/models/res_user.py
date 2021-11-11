# Copyright 2021 NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import timedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = "res.users"
    default_purchase_user = fields.Boolean()
    is_bot = fields.Boolean()

    @api.model_cr
    def write(self, values):
        if 'default_purchase_user' in values and values['default_purchase_user'] is True:
            self._cr.execute(
                """ select id from res_users ru
    where default_purchase_user =True""")


            exists_default = self._cr.fetchone()
            if exists_default:
                raise ValidationError(_(
                    "Another default user found. Id:%s",
                ) % exists_default[0]
                                      )
            else:
                super().write(values)
        else:
            super().write(values)
