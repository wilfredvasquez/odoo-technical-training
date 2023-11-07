from odoo import models, fields


class MotorcycleRegistry(models.Model):
    """Manage Registration of Motorcycles"""

    _name = "motorcycle.registry"
    _description = "Motorcycle Registry"

    name = fields.Char(string="Número de Registro", required=True)
    certificate_title = fields.Binary(string="Título de Propiedad")
    current_mileage = fields.Float(string="Millaje Actual")
    first_name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellido", required=True)
    license_plate = fields.Char(string="Matrícula")
    registry_date = fields.Date()
    vin = fields.Char(string="VIN", required=True)
