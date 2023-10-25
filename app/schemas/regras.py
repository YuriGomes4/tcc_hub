from marshmallow import Schema, fields

class RegraSchema(Schema):
    id = fields.String(required=True)
    ref_id_obj = fields.String()
    tabela_obj = fields.String()
    coluna_obj = fields.String()
    valor_obj = fields.String()
    operador = fields.String()
    ref_id_new = fields.String()
    tabela_new = fields.String()
    coluna_new = fields.String()
    valor_new = fields.String()
    funcao = fields.String()
    feito = fields.Boolean()

    # Defina o parâmetro strict para controlar o comportamento de validação
    class Meta:
        strict = True