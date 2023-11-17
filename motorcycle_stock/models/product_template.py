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
    detailed_type = fields.Selection(
        selection_add=[
            ("motorcycle", "Motorcycle"),
        ],
        ondelete={"motorcycle": "set product"},
    )
    horsepower = fields.Float("Caballos de fuerza")
    top_speed = fields.Float("Velocidad máxima")
    torque = fields.Float("Torque")
    battery_capacity = fields.Selection(
        selection=[
            ("xs", "Small"),
            ("0m", "Medium"),
            ("0l", "Larga"),
            ("xl", "Extra Large"),
        ],
        string="Capacidad de batería",
    )
    charge_time = fields.Float("Tiempo de carga")
    range = fields.Float("Rango")
    curb_weight = fields.Float("Peso")
    make = fields.Char("Marca")
    model = fields.Char("Modelo")
    year = fields.Char("Año")
    launch_date = fields.Date("Fecha de Lanzamiento")

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping["motorcycle"] = "product"
        return type_mapping

    def get_battery_capacity_value(self):
        return dict(self._fields["battery_capacity"].selection).get(
            self.battery_capacity
        )

    @api.depends("make", "model", "year")
    def _compute_name(self):
        for rec in self:
            if rec.detailed_type == "motorcycle":
                year = rec.year if rec.year else " "
                make = rec.make if rec.make else " "
                model = rec.model if rec.model else " "
                rec.name = f"{rec.year} {rec.make} {rec.model}"
