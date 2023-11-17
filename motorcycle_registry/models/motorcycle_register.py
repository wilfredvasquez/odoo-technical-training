import re
from odoo import api, models, fields
from odoo.exceptions import ValidationError

LICENCE_PLATE_PATTERN = r"^[A-Z]{1,3}\d{1,4}[A-Z]{0,2}$"
VIN_PATTERN = r"^[A-Z]{4}\d{2}[A-Z0-9]{2}\d{5}$"


class MotorcycleRegistry(models.Model):
    """Manage Registration of Motorcycles"""

    _name = "motorcycle.registry"
    _description = "Motorcycle Registry"
    _rec_name = "registry_number"
    _sql_constraints = [
        (
            "vin_unique",
            "unique(vin)",
            "Se ha encontrado otro registro con el mismo VIN. El VIN debe ser único.",
        )
    ]

    certificate_title = fields.Binary(string="Título de Propiedad")
    current_mileage = fields.Float(string="Millaje Actual")
    owner_id = fields.Many2one("res.partner", string="Propietario")
    email = fields.Char(string="Email", related="owner_id.email", store=True)
    phone = fields.Char(string="Phone", related="owner_id.phone", store=True)
    first_name = fields.Char(string="Nombre")
    last_name = fields.Char(string="Apellido")
    license_plate = fields.Char(string="Matrícula")
    registry_date = fields.Date()
    registry_number = fields.Char(
        string="Número de Registro",
        default="MRN0000",
        copy=False,
        required=True,
        readonly=True,
    )
    vin = fields.Char(string="VIN", required=True)
    make = fields.Char(string="Marca", compute="_compute_make")
    model = fields.Char(string="Modelo", compute="_compute_model")
    year = fields.Char(string="Año", compute="_compute_year")
    motorcycle_id = fields.Many2one(
        "product.template",
        string="Motocicleta",
        domain=lambda self: [("detailed_type", "=", "motorcycle")],
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("registry_number", ("MRN0000")) == ("MRN0000"):
                vals["registry_number"] = self.env["ir.sequence"].next_by_code(
                    "registry.number"
                )
        return super().create(vals_list)

    @api.constrains("license_plate")
    def _check_license_plate_format(self):
        for record in self:
            if not record.license_plate:
                continue
            if not re.match(LICENCE_PLATE_PATTERN, record.license_plate):
                raise ValidationError(
                    """Formato inválido para la Matrícula. El formato correcto es:
                    - 1 - 4 mayúsculas
                    - 1 - 3 dígitos
                    - 2 mayúsculas opcionales

                    Por ejemplo: KLV453, KLR3453L
                    """
                )

    @api.constrains("vin")
    def _check_vin_format(self):
        for record in self:
            if not re.match(VIN_PATTERN, record.vin):
                raise ValidationError(
                    """Formato inválido para el VIN. El formato correcto es:
                    - Marca: 2 mayúsculas
                    - Modelo: 2 mayúsculas
                    - Año: 2 dígitos
                    - Capacidad de Bateria: 2 mayúsculas o dígitos
                    - Número de serie: 5 dígitos

                    Por ejemplo: KAIN220M00023, KAUK21XL84732
                    """
                )

    @api.depends("vin")
    def _compute_make(self):
        for record in self:
            if record.vin:
                record.make = record.vin[0:2]
            else:
                record.make = ""

    @api.depends("vin")
    def _compute_model(self):
        for record in self:
            if record.vin:
                record.model = record.vin[2:4]
            else:
                record.model = ""

    @api.depends("vin")
    def _compute_year(self):
        for record in self:
            if record.vin:
                record.year = record.vin[4:6]
            else:
                record.year = ""
