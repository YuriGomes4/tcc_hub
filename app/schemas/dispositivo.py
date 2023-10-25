from marshmallow import Schema, fields

class Dispositivo_Schema(Schema):
    id = fields.Integer()
    data_criacao = fields.DateTime()
    data_alteracao = fields.DateTime()
    id_residencia = fields.Integer()
    id_area_residencia = fields.Integer()
    nome = fields.String()
    codigo = fields.String()

    class Meta:
        strict = True
