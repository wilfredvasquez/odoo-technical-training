# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    """Odoo Sale Order model extented to add is_new_customer boolean field."""

    _inherit = "sale.order"

    is_new_customer = fields.Boolean(
        "Es cliente nuevo?", related="partner_id.is_new_customer"
    )

    def apply_new_customer_pricelist(self):
        self.ensure_one()
        if self.is_new_customer:
            pricelist_discount = self.env["product.pricelist"].search(
                [("name", "=", "Nuevo Cliente 2500 Descuento")], limit=1
            )
            if pricelist_discount:
                self.pricelist_id = pricelist_discount
