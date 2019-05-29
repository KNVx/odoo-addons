# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import re

from odoo import _

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (
    mapping, external_to_m2o, only_create)


class SaleOrderBatchImporter(Component):
    """ Import the Ambugest Services.

    For every sale order in the list, a delayed job is created.
    """
    _name = 'ambugest.sale.order.delayed.batch.importer'
    _inherit = 'ambugest.delayed.batch.importer'
    _apply_on = 'ambugest.sale.order'


class SaleOrderImporter(Component):
    _name = 'ambugest.sale.order.importer'
    _inherit = 'ambugest.importer'
    _apply_on = 'ambugest.sale.order'

    def _import_dependencies(self):
        external_id = (self.external_data['EMPRESA'], self.external_data['CodiUP'])

        self._import_dependency(external_id, 'ambugest.res.partner', always=True)
