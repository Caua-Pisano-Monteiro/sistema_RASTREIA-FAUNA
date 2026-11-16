from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from database import Base

# Criando a tabela que será usada para entrada de novos usuários e validação de login 
class usuario_login(Base):
    __tablename__ = 'usuarios_login'
    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    username = Column(
        String(250), 
        nullable=False, 
        unique=True, 
        index=True)
    email = Column(
        String(250), 
        nullable=False, 
        unique=True
    )
    funcao = Column(
        String(100)
    )
    password = Column(
        String(255), 
        nullable=False
    )
    ativo = Column(
        Boolean, 
        default=True
    )

class apreensao_fauna(Base):
    __tablename__ = "apreensoes_fauna"

    seq_apreensao = Column(
        Integer, 
        primary_key=True, 
        index=True, 
        autoincrement=False
    )
    dt_apreensao = Column(
        Date, 
        nullable=False, 
        index=True
    )
    cd_municipio = Column(
        String(7)
    )
    no_municipio = Column(
        String(100)
    )
    sg_uf = Column(
        String(2), 
        index=True
    )
    nu_latitude_tad = Column(
        Float
    )
    nu_longitude_tad = Column(
        Float
    )
    ds_wkt_local_apreensao = Column(
        String(100)
    )
    ds_localizacao = Column(
        String(255)
    )
    tp_infracao = Column(
        String(100)
    )
    ds_tad = Column(
        String(250)
    )
    no_popular_especie = Column(
        String(150)
    )
    no_cientifico_especie = Column(
        String(150)
    )
    ds_classe = Column(
        String(50)
    )
    st_especie_ameacada = Column(
        String(1)
    )
    qt_animais = Column(
        Integer
    )
    ds_estado_animal = Column(
        String(50)
    )
    ds_destinacao = Column(
        String(150)
    )
    no_pessoa_apreensao = Column(
        String(255)
    )
    tp_pessoa = Column(
        String(1)
    )
    vl_multa = Column(
        Float
    )
    sg_unidade_controle = Column(
        String(20)
    )
    st_cancelado = Column(
        String(1)
    )
    ds_sit_apreensao = Column(
        String(50)
    )