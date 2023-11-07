from odoo import models, fields


class MotorcycleRegistry(models.Model):
    """Manage Registration of Motorcycles"""

    _name = "motorcycle.registry"
    _description = "Motorcycle Registry"
    _rec_name = "registry_number"

    certificate_title = fields.Binary(string="Título de Propiedad")
    current_mileage = fields.Float(string="Millaje Actual")
    first_name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellido", required=True)
    license_plate = fields.Char(string="Matrícula")
    registry_date = fields.Date()
    registry_number = fields.Char(string="Número de Registro", required=True)
    vin = fields.Char(string="VIN", required=True)
