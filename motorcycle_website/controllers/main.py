from odoo import http
from odoo.http import request


class MotorcycleWebsite(http.Controller):
    @http.route("/compare", type="http", methods=["GET"], auth="public", website=True)
    def compate(self, **kwargs):
        motorcycles = request.env["product.template"].search(
            [("detailed_type", "=", "motorcycle")]
        )
        return request.render(
            "motorcycle_website.motorcycle_compare_template",
            {
                "motorcycles": motorcycles,
            },
        )
