# Copyright NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models
from odoo.tools.float_utils import float_round as round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    # TODO: check discount on invoices
    # TODO: lotes de facturacion

    # This field is created with digits=False to force
    # de creation with type numeric, like discount.
    woocommerce_discount = fields.Float(
        digits=False,
    )
    stock_move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="sale_line_id",
    )
    discount = fields.Float(
        digits=False,
    )
    website_order_line_state = fields.Selection(
        compute="_compute_website_order_line_state",
        store=True,
        selection=[
            ("processing", "Processing"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
    )

    @api.depends("order_id.state", "order_id.picking_ids", "order_id.picking_ids.state")
    def _compute_website_order_line_state(self):
        for rec in self:
            if rec.product_id.type == "service":
                if rec.order_id.state in ("sale", "done"):
                    rec.website_order_line_state = "done"
                elif rec.order_id.state == "cancel":
                    rec.website_order_line_state = "cancel"
                else:
                    rec.website_order_line_state = "processing"
            elif rec.product_id.type == "product" or rec.product_id.type == "consu":
                if rec.stock_move_ids:
                    if len(rec.stock_move_ids) == 1:
                        if rec.stock_move_ids[0].state == "cancel":
                            rec.website_order_line_state = "cancel"
                        elif rec.stock_move_ids[0].state in (
                            "draft",
                            "waiting",
                            "confirmed",
                            "partially_available",
                            "assigned",
                        ):
                            rec.website_order_line_state = "processing"
                        elif rec.stock_move_ids[0].state == "done":
                            rec.website_order_line_state = "done"
                    # TODO: acabar este else
                    else:
                        for move_states in rec.stock_move_ids.mapped("state"):
                            if len(move_states) == 1:
                                if move_states == "cancel":
                                    rec.website_order_line_state = "cancel"
                                elif move_states == "done":
                                    rec.website_order_line_state = "done"
                                elif move_states in (
                                    "draft",
                                    "waiting",
                                    "confirmed",
                                    "partially_available",
                                    "assigned",
                                ):
                                    rec.website_order_line_state = "processing"
                            else:
                                if any(
                                    state
                                    in [
                                        "draft",
                                        "waiting",
                                        "confirmed",
                                        "partially_available",
                                        "assigned",
                                    ]
                                    for state in move_states
                                ):
                                    rec.website_order_line_state = "processing"
                                else:
                                    # TODO: states done and cancel, refactor
                                    rec.website_order_line_state = "done"

                else:
                    if rec.order_id.state in ("sale", "done"):
                        rec.website_order_line_state = "done"
                    elif rec.order_id.state == "cancel":
                        rec.website_order_line_state = "cancel"
                    else:
                        rec.website_order_line_state = "processing"

    woocommerce_bind_ids = fields.One2many(
        comodel_name="woocommerce.sale.order.line",
        inverse_name="odoo_id",
        string="WooCommerce Bindings",
    )

    # TODO: refactor write and create methods
    def write(self, vals):
        print("sale order line write -- sale", vals)
        prec = self.env.ref("product.decimal_discount").digits
        # if isinstance(vals, list):
        #     for val in vals:
        #         if 'woocommerce_discount' in val:
        #             val['discount'] = val['woocommerce_discount']
        #         elif 'discount' in vals:
        #             val['discount'] = round(val['discount'], precision_digits=prec)
        #     return super().write(vals)
        # else:
        if "woocommerce_discount" in vals:
            vals["discount"] = vals["woocommerce_discount"]
        elif "discount" in vals and not self.woocommerce_discount:
            vals["discount"] = round(vals["discount"], precision_digits=prec)
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        print("sale order line create -- sale", vals_list)
        prec = self.env.ref("product.decimal_discount").digits
        for values in vals_list:
            if "woocommerce_discount" in values:
                values["discount"] = values["woocommerce_discount"]
            elif "discount" in values:
                values["discount"] = round(values["discount"], precision_digits=prec)
        return super().create(vals_list)
