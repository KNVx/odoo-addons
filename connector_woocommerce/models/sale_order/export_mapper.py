# Copyright NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class WooCommerceSaleOrderExportMapper(Component):
    _name = "woocommerce.sale.order.export.mapper"
    _inherit = "woocommerce.export.mapper"

    _apply_on = "woocommerce.sale.order"

    @mapping
    def status(self, record):
        a=1
        if record.website_order_state == "processing":
            status = "processing"
        elif record.website_order_state == "done":
            status = "completed"
        elif record.website_order_state == "cancel":
            status = "cancelled"
        return {"status": status}
