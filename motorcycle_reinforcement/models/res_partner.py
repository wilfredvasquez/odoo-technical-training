# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    """Odoo Partner/Contact model extented to add is_new_customer boolean field."""

    _inherit = "res.partner"

    is_new_customer = fields.Boolean(
        "Es cliente nuevo?", default=True, compute="_compute_check_is_new_customer"
    )

    def check_is_new_customer(self, customer):
        is_new = True
        for order in customer.sale_order_ids:
            if order.state == "sale" and bool(
                order.order_line.filtered(
                    lambda l: l.product_template_id.detailed_type == "motorcycle"
                )
            ):
                is_new = False

        return is_new

    @api.depends("sale_order_ids")
    def _compute_check_is_new_customer(self):
        for rec in self:
            if rec.sale_order_ids:
                rec.is_new_customer = self.check_is_new_customer(rec)
            else:
                rec.is_new_customer = True
