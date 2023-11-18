from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    name = fields.Char(
        "Name",
        index="trigram",
        required=True,
        translate=True,
        compute="_compute_name",
        precompute=True,
        store=True,
        readonly=True,
    )

    @api.depends("make", "model", "year")
    def _compute_name(self):
        for rec in self:
            if rec.detailed_type == "motorcycle":
                year = rec.year if rec.year else " "
                make = rec.make if rec.make else " "
                model = rec.model if rec.model else " "
                rec.name = f"{rec.year} {rec.make} {rec.model}"
