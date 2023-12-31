{
    "name": "Motorcycle Registry",
    "summary": """Manage Registration of Motorcycles""",
    "description": """
        Motorcycle Registry
        ====================
        This Module is used to keep track of the Motorcycle Registration and Ownership of each motorcycled of the brand.
    """,
    "version": "0.0.1",
    "author": "wilfredvasquez",
    "license": "OPL-1",
    "category": "Project",
    "website": "https://github.com/wilfredvasquez",
    "company": "Bitmotto",
    "maintainer": "wilfredvasquez",
    "application": True,
    "category": "Kawiil/Motorcycle",
    "depends": ["base", "motorcycle_stock"],
    "data": [
        "security/motorcycle_registry_groups.xml",
        "security/ir.model.access.csv",
        "data/registry_data.xml",
        "views/motorcycle_register_view.xml",
    ],
    "demo": [
        "demo/motorcycle_register.xml",
    ],
}
