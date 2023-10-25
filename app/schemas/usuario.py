from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id = fields.Integer()
    data_criacao = fields.DateTime()
    data_alteracao = fields.DateTime()
    id_publico = fields.String()
    nome = fields.String()
    email = fields.Email()
    senha = fields.String(load_only=True)  # Marcado como load_only para não ser serializado
    
    class Meta:
        strict = True
