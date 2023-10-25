from marshmallow import Schema, fields

class OrderSchema(Schema):
    id = fields.Integer(dump_only=True)
    date_created = fields.DateTime()
    date_closed = fields.DateTime()
    last_updated = fields.DateTime()
    manufacturing_ending_date = fields.DateTime()
    comment = fields.String()
    pack_id = fields.Integer()
    pickup_id = fields.Integer()
    total_amount = fields.Integer()
    paid_amount = fields.Integer()
    expiration_date = fields.DateTime()
    currency_id = fields.String()
    status = fields.String()
    status_detail = fields.String()
    shipping = fields.String()
    json = fields.String()

    buyer_id = fields.Integer()
    seller_id = fields.Integer()

    buyer = fields.Nested('BuyerSchema', only=('id', 'nickname'))
    vendedor = fields.Nested('VendedorSchema', only=('id_ml', 'nome'))  # Replace 'VendedorSchema' with the actual schema name
    order_items = fields.Nested('OrderItemSchema', many=True, exclude=('order', 'order_id'))
    payments = fields.Nested('PaymentSchema', many=True, exclude=('order', 'order_id'))
