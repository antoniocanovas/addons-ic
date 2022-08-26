{
    'name': 'Product Chassis',
    'version': '14.0.0.1',
    'category': 'Product',
    'description': u"""
Base module for product_vehicle, scrap_unbuild and others ...
Char field per product template chassis_pt, hidden if variants.
Char field per product product  chassis_pp, computed from pt: empty and editable if variants, else related.
It allows searching chassis in pt/pp, and create variants for new vehicles based on licenses.
""",
    'author': 'Serincloud',
    'depends': [
        'product',
    ],
    "data": [
        "views/product_views.xml",
    ],
    'installable':True,
    'application':False,
}
