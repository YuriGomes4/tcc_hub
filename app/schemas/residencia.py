from marshmallow import Schema, fields

class ResidenciaSchema(Schema):
    id = fields.Integer()
    data_criacao = fields.DateTime()
    data_alteracao = fields.DateTime()
    id_usuario = fields.Integer()
    nome = fields.String()

    class Meta:
        strict = True
