from marshmallow import Schema, fields

class PaymentSchema(Schema):
    id = fields.Integer()
    order_id = fields.Integer()
    payer_id = fields.Integer()
    payment_method_id = fields.String()
    currency_id = fields.String()
    transaction_amount = fields.Integer()
    status = fields.String()

    order = fields.Nested('OrderSchema', only=('id',))