from marshmallow import Schema, fields

class ProdutoSchema(Schema):
    id = fields.String(required=True)
    category_id = fields.String()
    cost = fields.Float()
    price = fields.Float()
    title = fields.String()
    listing_type_id = fields.String()
    free_shipping = fields.String()
    shipping_free_cost = fields.Float()
    sale_fee = fields.Float()
    sales = fields.Integer()
    invoicing = fields.Float()
    seller = fields.String()
    json = fields.String()

    # Defina o parâmetro strict para controlar o comportamento de validação
    class Meta:
        strict = True