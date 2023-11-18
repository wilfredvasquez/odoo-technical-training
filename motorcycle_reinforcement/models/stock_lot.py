# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLot(models.Model):
    """Odoo Stock Lot model extented to change name field behaviour."""

    _inherit = "stock.lot"

    name = fields.Char(
        "Lot/Serial Number",
        compute="_compute_generate_serial",
        default=lambda self: self.env["ir.sequence"].next_by_code("stock.lot.serial"),
        required=True,
        store=True,
        readonly=True,
        help="Unique Lot/Serial Number",
        index="trigram",
    )

    def generate_serial_values(self, rec):
        make = rec.product_id.product_tmpl_id.make[0:2].upper()
        model = rec.product_id.product_tmpl_id.model[0:2].upper()
        year = rec.product_id.product_tmpl_id.year[2:4].upper()
        battery_cap = rec.product_id.product_tmpl_id.battery_capacity.upper()
        number = self.env["ir.sequence"].next_by_code("stock.lot.serial")[2:8]
        return f"{make}{model}{year}{battery_cap}{number}"

    @api.depends("product_id")
    def _compute_generate_serial(self):
        for rec in self:
            if rec.product_id.product_tmpl_id.detailed_type == "motorcycle":
                rec.name = self.generate_serial_values(rec)
