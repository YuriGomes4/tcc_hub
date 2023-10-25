from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    id = fields.Integer()
    order_id = fields.Integer()
    item_id = fields.String()
    title = fields.String()
    category_id = fields.String()
    variation_id = fields.Integer()
    warranty = fields.String()
    condition = fields.String()
    unit_price = fields.Integer()
    currency_id = fields.String()
    quantity = fields.Integer()
    requested_quantity = fields.Field()
    sale_fee = fields.Integer()
    listing_type_id = fields.String()

    seller_id = fields.Integer()

    #vendedor = fields.Nested('VendedorSchema', only=('id_ml', 'nome'))  # Replace 'VendedorSchema' with the actual schema name
    order = fields.Nested('OrderSchema', only=('id',))