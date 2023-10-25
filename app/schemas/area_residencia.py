from marshmallow import Schema, fields

class Area_ResidenciaSchema(Schema):
    id = fields.Integer()
    data_criacao = fields.DateTime()
    data_alteracao = fields.DateTime()
    id_residencia = fields.Integer()
    nome = fields.String()

    class Meta:
        strict = True
