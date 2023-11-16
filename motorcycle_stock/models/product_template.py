from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

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
        ]
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
