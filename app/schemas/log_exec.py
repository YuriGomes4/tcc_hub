from marshmallow import Schema, fields

class Log_Exec_Schema(Schema):
    id = fields.Integer()
    data_criacao = fields.DateTime()
    data_alteracao = fields.DateTime()
    id_residencia = fields.Integer()
    id_are_residencia = fields.Integer()
    id_dispositivo = fields.Integer()
    acao = fields.String()
    status = fields.String()

    class Meta:
        strict = True
