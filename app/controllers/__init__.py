from app.controllers.base_crud import CRUDBase

from .. import models, schemas

crud_residencia = CRUDBase(models.Residencia, schemas.ResidenciaSchema)
crud_area_residencia = CRUDBase(models.Area_Residencia, schemas.Area_ResidenciaSchema)
crud_usuario = CRUDBase(models.Usuario, schemas.UsuarioSchema)
crud_dispositivo = CRUDBase(models.Dispositivo, schemas.Dispositivo_Schema)
crud_log_exec = CRUDBase(models.Log_Exec, schemas.Log_Exec_Schema)