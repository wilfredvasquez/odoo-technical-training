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
    first_name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellido", required=True)
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("registry_number", ("S0000")) == ("S0000"):
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
