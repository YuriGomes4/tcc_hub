from marshmallow import Schema, fields

class BuyerSchema(Schema):
    id = fields.Integer()
    nickname = fields.String()
    first_name = fields.String()
    last_name = fields.String()