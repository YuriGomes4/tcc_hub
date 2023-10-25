from marshmallow import Schema, fields

class HistoricoSchema(Schema):
    id = fields.Integer()
    date = fields.DateTime()
    seller = fields.String()
    type = fields.String()
    ref_id = fields.String()
    change = fields.String()
    old_value = fields.String()
    new_value = fields.String()