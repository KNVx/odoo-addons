# Copyright NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    woocommerce_bind_ids = fields.One2many(
        comodel_name="woocommerce.sale.order",
        inverse_name="odoo_id",
        string="WooCommerce Bindings",
    )
    woocommerce_status = fields.Char(
        string="WooCommerce State",
        readonly=True,
        track_visibility="onchange",
    )
    woocommerce_status_write_date = fields.Datetime(
        compute="_compute_woocommerce_status_write_date",
        store=True,
    )

    @api.depends("state", "picking_ids", "picking_ids.state")
    def _compute_woocommerce_status_write_date(self):
        for rec in self:
            if rec.woocommerce_bind_ids:
                rec.woocommerce_status_write_date = fields.Datetime.now()

    website_order_state = fields.Selection(
        compute="_compute_website_order_state",
        selection=[
            ("processing", "Processing"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
    )

    @api.depends("order_line.website_order_line_state")
    def _compute_website_order_state(self):
        for rec in self:
            for line_states in rec.order_line.mapped("website_order_line_state"):
                if any(
                    state
                    in [
                        "draft",
                        "waiting",
                        "confirmed",
                        "partially_available",
                        "assigned",
                    ]
                    for state in line_states
                ):
                    rec.website_order_state = "processing"
                    break
                elif "cancel" in line_states:
                    rec.website_order_state = "cancel"
                    break
                else:
                    rec.website_order_state = "done"
