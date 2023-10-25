from marshmallow import Schema, fields

class VendedorSchema(Schema):
    id = fields.Integer()
    nome = fields.String()
    client_ml = fields.String()
    secret_ml = fields.String()
    id_ml = fields.String()
    refresh_tk_ml = fields.String()
    tk_ml = fields.String()
    tk_tiny = fields.String()
    last_updated = fields.DateTime()

    class Meta:
        strict = True
