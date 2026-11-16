from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class usuario_loginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # permite ler objetos do SQLAlchemy

    id: int
    username: str
    email: str
    funcao: str | None = None
    ativo: bool

class usuario_loginCreate(BaseModel):
    username : str
    email : str
    funcao : str | None = None
    password : str
    

class LoginRequest(BaseModel):
    username : str
    password: str


class ApreensaoFaunaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seq_apreensao : int
    dt_apreensao: date
    cd_municipio: Optional[str] = None
    no_municipio: Optional[str] = None
    sg_uf: Optional[str] = None
    nu_latitude_tad: Optional[float] = None
    nu_longitude_tad: Optional[float] = None
    ds_wkt_local_apreensao: Optional[str] = None
    ds_localizacao: Optional[str] = None
    tp_infracao: Optional[str] = None
    ds_tad: Optional[str] = None
    no_popular_especie: Optional[str] = None
    no_cientifico_especie: Optional[str] = None
    ds_classe: Optional[str] = None
    st_especie_ameacada: Optional[str] = None
    qt_animais: Optional[int] = None
    ds_estado_animal: Optional[str] = None
    ds_destinacao: Optional[str] = None
    no_pessoa_apreensao: Optional[str] = None
    tp_pessoa: Optional[str] = None
    vl_multa: Optional[float] = None
    sg_unidade_controle: Optional[str] = None
    st_cancelado: Optional[str] = None
    ds_sit_apreensao: Optional[str] = None

class ApreensaoFaunaCreate(ApreensaoFaunaBase):
    pass


class ApreensaoFaunaResponse(ApreensaoFaunaBase):
    pass